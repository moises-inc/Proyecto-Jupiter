/* ==========================================================================
   Proyecto Centinela — Consola de Demostración & Simulación (demo.js)
   ========================================================================== */

let map;
let sectorMarkers = {};
let trendChart;
let currentScenario = 'normal';

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  initChart();
  loadDemoScenario('normal');
});

function initMap() {
  map = L.map('map').setView([-29.900, -71.230], 11);

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map);
}

function initChart() {
  const ctx = document.getElementById('trendChart').getContext('2d');
  trendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
      datasets: [
        {
          label: 'Lluvia Acumulada (mm)',
          yAxisID: 'yRain',
          data: [0, 0, 0, 0, 0, 0, 0],
          borderColor: '#00D2FF',
          backgroundColor: 'rgba(0, 210, 255, 0.15)',
          borderWidth: 3,
          fill: true,
          tension: 0.3
        },
        {
          label: 'Isoterma Cero (m.n.m.)',
          yAxisID: 'yFreezing',
          data: [2200, 2200, 2200, 2200, 2200, 2200, 2200],
          borderColor: '#F1C40F',
          borderDash: [6, 4],
          borderWidth: 2.5,
          pointRadius: 4,
          tension: 0.2
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { color: '#F0F4F8', font: { family: 'Inter', size: 12, weight: 'bold' } } },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) label += ': ';
              if (context.datasetIndex === 0) label += context.parsed.y + ' mm';
              else label += context.parsed.y.toLocaleString('es-CL') + ' m.n.m.';
              return label;
            }
          }
        }
      },
      scales: {
        x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
        yRain: {
          type: 'linear', position: 'left', min: 0, max: 100,
          title: { display: true, text: 'Lluvia Acumulada (mm)', color: '#00D2FF', font: { weight: 'bold' } },
          ticks: { color: '#00D2FF' }, grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        yFreezing: {
          type: 'linear', position: 'right', min: 1000, max: 5000,
          title: { display: true, text: 'Isoterma Cero (m.n.m.)', color: '#F1C40F', font: { weight: 'bold' } },
          ticks: { color: '#F1C40F', callback: v => v.toLocaleString('es-CL') + ' m' },
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}

async function loadDemoScenario(severity) {
  currentScenario = severity;
  try {
    const response = await fetch(`/api/simulate-storm?severity=${severity}`);
    const data = await response.json();
    renderDemoDashboard(data);
  } catch (err) {
    console.error('Error loading scenario:', err);
  }
}

function renderDemoDashboard(data) {
  const bannerBox = document.getElementById('status-banner-box');
  const statusText = document.getElementById('commune-status-text');
  const summarySubtext = document.getElementById('status-summary-subtext');
  const timeTag = document.getElementById('timestamp-tag-text');

  statusText.innerText = data.commune_status;
  timeTag.innerText = `Escenario: ${data.severity.toUpperCase()}`;

  bannerBox.className = 'status-banner';
  if (data.commune_status.includes('ROJA')) {
    bannerBox.classList.add('banner-rojo');
    summarySubtext.innerText = 'SIMULACIÓN: ALERTA ROJA POR ALUVIÓN Y DESBORDE (Temporal 19 de Julio 2026).';
  } else if (data.commune_status.includes('AMARILLA')) {
    bannerBox.classList.add('banner-amarillo');
    summarySubtext.innerText = 'SIMULACIÓN: PRE-ALERTA Y LLUVIAS MODERADAS (Preparación de Recursos).';
  } else {
    bannerBox.classList.add('banner-verde');
    summarySubtext.innerText = 'SIMULACIÓN: Día normal sin precipitaciones ni riesgo hidrológico.';
  }

  const t = data.telemetry_summary;
  document.getElementById('kpi-rain-24h').innerHTML = `${t.precip_accum_24h_mm} <span class="kpi-unit">mm</span>`;
  document.getElementById('kpi-rain-6h-sub').innerText = `Últimas 6 horas: ${t.precip_accum_6h_mm} mm`;
  document.getElementById('kpi-api-soil').innerHTML = `${t.api_soil_saturation} <span class="kpi-unit">/ 100</span>`;
  document.getElementById('kpi-freezing').innerHTML = `${t.freezing_level_m.toLocaleString('es-CL')} <span class="kpi-unit">m.n.m.</span>`;
  
  const maxRisk = data.sectors.length > 0 ? data.sectors[0].score_pct : 0;
  document.getElementById('kpi-ml-risk').innerHTML = `${maxRisk}%`;

  const sectorContainer = document.getElementById('sector-grid-list');
  sectorContainer.innerHTML = '';

  data.sectors.forEach(s => {
    const card = document.createElement('div');
    card.className = 'sector-card';

    let badgeClass = 'badge-verde';
    if (s.semaforo.includes('ROJA')) badgeClass = 'badge-rojo';
    else if (s.semaforo.includes('AMARILLA')) badgeClass = 'badge-amarillo';

    card.innerHTML = `
      <div>
        <div class="sector-name">${s.name}</div>
        <div class="sector-vulnerability"><strong>Peligro:</strong> ${s.disaster_type}</div>
        <div class="sector-vulnerability" style="color: var(--brand-blue); margin-top: 2px;">
          <strong>ETA Impacto:</strong> ${s.eta_impact} (Tc: ${s.concentration_time_hours}h) • Cota ${s.elevation_m}m
        </div>
      </div>
      <span class="sector-badge ${badgeClass}">${s.semaforo} (${s.score_pct}%)</span>
    `;
    sectorContainer.appendChild(card);

    updateMapMarker(s);
  });

  renderTacticalActions(data);

  if (data.trend_series && trendChart) {
    trendChart.data.labels = data.trend_series.labels;
    trendChart.data.datasets[0].data = data.trend_series.rain_accum_mm;
    trendChart.data.datasets[1].data = data.trend_series.freezing_level_m;
    trendChart.update();
  }
}

function updateMapMarker(sector) {
  const coords = [sector.coordinates.lat, sector.coordinates.lon];
  let color = '#2ECC71';
  let fillColor = 'rgba(46, 204, 113, 0.18)';
  if (sector.semaforo.includes('ROJA')) {
    color = '#E74C3C';
    fillColor = 'rgba(231, 76, 60, 0.30)';
  } else if (sector.semaforo.includes('AMARILLA')) {
    color = '#F1C40F';
    fillColor = 'rgba(241, 196, 15, 0.25)';
  }

  if (sectorMarkers[sector.key]) {
    map.removeLayer(sectorMarkers[sector.key].circle);
    map.removeLayer(sectorMarkers[sector.key].marker);
  }

  // 1. Draw Continuous Spatial Coverage Zone Circle
  const coverageZone = L.circle(coords, {
    radius: sector.radius_m || 1000,
    color: color,
    weight: 1.5,
    fillColor: fillColor,
    fillOpacity: 0.35,
    dashArray: '4, 4'
  }).addTo(map);

  // 2. Draw Center Tactical Marker
  const centerMarker = L.circleMarker(coords, {
    radius: 7,
    fillColor: color,
    color: '#FFFFFF',
    weight: 2,
    opacity: 1,
    fillOpacity: 0.95
  }).addTo(map);

  const popupContent = `
    <div style="color: #070C18; font-family: sans-serif; min-width: 230px;">
      <strong style="font-size: 0.95rem; color: #00205B;">${sector.name}</strong><br>
      <hr style="margin: 4px 0; border: 0; border-top: 1px solid #ccc;">
      <b>Estado:</b> ${sector.semaforo}<br>
      <b>Riesgo ML:</b> ${sector.score_pct}%<br>
      <b>Peligro Específico:</b> ${sector.disaster_type}<br>
      <b>ETA Impacto:</b> ${sector.eta_impact} (Tc: ${sector.concentration_time_hours}h)<br>
      <b>Radio Cobertura:</b> ${sector.radius_m}m • <b>Cota:</b> ${sector.elevation_m} m.n.m.
    </div>
  `;

  coverageZone.bindPopup(popupContent);
  centerMarker.bindPopup(popupContent);

  sectorMarkers[sector.key] = { circle: coverageZone, marker: centerMarker };
}

function renderTacticalActions(data) {
  const container = document.getElementById('tactical-actions-list');
  container.innerHTML = '';

  const redSectors = data.sectors.filter(s => s.semaforo.includes('ROJA'));
  const yellowSectors = data.sectors.filter(s => s.semaforo.includes('AMARILLA'));

  if (redSectors.length > 0) {
    redSectors.forEach(s => {
      const item = document.createElement('div');
      item.className = 'action-item danger';
      item.innerHTML = `
        <div class="action-title">SIMULACIÓN: ORDEN DE EVACUACIÓN (${s.name})</div>
        <div class="action-desc">Riesgo ML al ${s.score_pct}%. Peligro: ${s.disaster_type}. ETA Impacto: ${s.eta_impact}. Proyectado aluvión y anegamiento crítico.</div>
      `;
      container.appendChild(item);
    });
  }

  if (yellowSectors.length > 0) {
    yellowSectors.forEach(s => {
      const item = document.createElement('div');
      item.className = 'action-item warning';
      item.innerHTML = `
        <div class="action-title">SIMULACIÓN: PRE-POSICIONAR RECURSOS (${s.name})</div>
        <div class="action-desc">Riesgo en incremento (${s.score_pct}%). Peligro: ${s.disaster_type}. ETA Impacto: ${s.eta_impact}. Monitorear cauces.</div>
      `;
      container.appendChild(item);
    });
  }

  if (redSectors.length === 0 && yellowSectors.length === 0) {
    container.innerHTML = `
      <div class="action-item">
        <div class="action-title">CONDICIONES NORMALES EN SIMULACIÓN</div>
        <div class="action-desc">No hay alertas de desborde hidrológico en este escenario.</div>
      </div>
    `;
  }
}

function generatePdfSci201() {
  window.print();
}
