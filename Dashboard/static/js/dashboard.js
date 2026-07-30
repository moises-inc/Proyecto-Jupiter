/* ==========================================================================
   Proyecto Centinela — Dashboard Táctico Puesto de Mando (JavaScript)
   ========================================================================== */

let map;
let sectorMarkers = {};
let isSimulationMode = false;
let trendChart;

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  initChart();
  fetchScanData();
  
  // Poll every 15 seconds ONLY when in Live NRT Mode
  setInterval(() => {
    if (!isSimulationMode) {
      fetchScanData();
    }
  }, 15000);
});

/* Initialize Leaflet Map Centered at La Serena */
function initMap() {
  map = L.map('map').setView([-29.897, -71.220], 11);

  // Dark Map Tiles (CartoDB Dark Matter)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map);
}

/* Initialize Dual Y-Axis Trend Chart for Clear Interpretation */
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
          data: [0, 0, 0, 0.2, 0.5, 0.9, 0.9],
          borderColor: '#00D2FF',
          backgroundColor: 'rgba(0, 210, 255, 0.15)',
          borderWidth: 3,
          fill: true,
          tension: 0.3
        },
        {
          label: 'Isoterma Cero (m.n.m.)',
          yAxisID: 'yFreezing',
          data: [3800, 3900, 4000, 4050, 4060, 4070, 4070],
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
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          labels: { color: '#F0F4F8', font: { family: 'Inter', size: 12, weight: 'bold' } }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (context.datasetIndex === 0) {
                label += context.parsed.y + ' mm';
              } else {
                label += context.parsed.y.toLocaleString('es-CL') + ' m.n.m.';
              }
              return label;
            }
          }
        }
      },
      scales: {
        x: {
          ticks: { color: '#94A3B8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        yRain: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Lluvia Acumulada (mm)',
            color: '#00D2FF',
            font: { weight: 'bold' }
          },
          min: 0,
          max: 100,
          ticks: { color: '#00D2FF' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        yFreezing: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Isoterma Cero (m.n.m.)',
            color: '#F1C40F',
            font: { weight: 'bold' }
          },
          min: 1000,
          max: 5000,
          ticks: {
            color: '#F1C40F',
            callback: function(value) {
              return value.toLocaleString('es-CL') + ' m';
            }
          },
          grid: { drawOnChartArea: false }
        }
      }
    }
  });
}

/* Fetch Data from API */
async function fetchScanData() {
  try {
    const url = isSimulationMode ? '/api/simulate-storm?severity=extreme' : '/api/scan';
    const response = await fetch(url);
    const data = await response.json();
    renderDashboard(data);
  } catch (err) {
    console.error('Error fetching dashboard payload:', err);
  }
}

/* Render Full Dashboard */
function renderDashboard(data) {
  // 1. Status Banner
  const bannerBox = document.getElementById('status-banner-box');
  const statusText = document.getElementById('commune-status-text');
  const summarySubtext = document.getElementById('status-summary-subtext');
  const timeTag = document.getElementById('timestamp-tag-text');

  statusText.innerText = data.commune_status;
  timeTag.innerText = `Timestamp: ${data.timestamp}`;

  bannerBox.className = 'status-banner';
  if (data.commune_status.includes('ROJA')) {
    bannerBox.classList.add('banner-rojo');
    summarySubtext.innerText = '🚨 ALERTA MÁXIMA DE DESBORDE Y ALUVIÓN: Activar evacuación preventiva inmediata.';
  } else if (data.commune_status.includes('AMARILLA')) {
    bannerBox.classList.add('banner-amarillo');
    summarySubtext.innerText = '⚠️ PRE-ALERTA Y MONITOREO ACTIVO: Preparar Puestos de Mando en La Serena.';
  } else {
    bannerBox.classList.add('banner-verde');
    summarySubtext.innerText = 'Monitoreo satelital activo NRT sin riesgo inminente de desborde hidrológico.';
  }

  // 2. Telemetry KPIs
  const t = data.telemetry_summary;
  document.getElementById('kpi-rain-24h').innerHTML = `${t.precip_accum_24h_mm} <span class="kpi-unit">mm</span>`;
  document.getElementById('kpi-rain-6h-sub').innerText = `Últimas 6 horas: ${t.precip_accum_6h_mm} mm`;
  document.getElementById('kpi-api-soil').innerHTML = `${t.api_soil_saturation} <span class="kpi-unit">/ 100</span>`;
  document.getElementById('kpi-freezing').innerHTML = `${t.freezing_level_m.toLocaleString('es-CL')} <span class="kpi-unit">m.n.m.</span>`;
  
  const maxRisk = data.sectors.length > 0 ? data.sectors[0].score_pct : 0;
  document.getElementById('kpi-ml-risk').innerHTML = `${maxRisk}%`;

  // 3. Sector Risk Matrix List
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
        <div class="sector-vulnerability">${s.type} • Cota ${s.elevation_m}m • ${s.vulnerability}</div>
      </div>
      <span class="sector-badge ${badgeClass}">${s.semaforo.split('-')[0].trim()} (${s.score_pct}%)</span>
    `;
    sectorContainer.appendChild(card);

    updateMapMarker(s);
  });

  // 4. Tactical Actions
  renderTacticalActions(data);

  // 5. Update Trend Chart Series with Dual Axes
  if (data.trend_series && trendChart) {
    trendChart.data.labels = data.trend_series.labels;
    trendChart.data.datasets[0].data = data.trend_series.rain_accum_mm;
    trendChart.data.datasets[1].data = data.trend_series.freezing_level_m;
    trendChart.update();
  }
}

/* Update Leaflet Markers for Sectors */
function updateMapMarker(sector) {
  const coords = [sector.coordinates.lat, sector.coordinates.lon];
  
  let color = '#2ECC71';
  if (sector.semaforo.includes('ROJA')) color = '#E74C3C';
  else if (sector.semaforo.includes('AMARILLA')) color = '#F1C40F';

  if (sectorMarkers[sector.key]) {
    map.removeLayer(sectorMarkers[sector.key]);
  }

  const circle = L.circleMarker(coords, {
    radius: 14,
    fillColor: color,
    color: '#FFFFFF',
    weight: 2,
    opacity: 1,
    fillOpacity: 0.85
  }).addTo(map);

  circle.bindPopup(`
    <div style="color: #070C18; font-family: sans-serif; min-width: 200px;">
      <strong style="font-size: 1rem;">${sector.name}</strong><br>
      <hr style="margin: 4px 0;">
      <b>Estado:</b> ${sector.semaforo}<br>
      <b>Riesgo ML:</b> ${sector.score_pct}%<br>
      <b>Vulnerabilidad:</b> ${sector.vulnerability}<br>
      <b>Elevación:</b> ${sector.elevation_m} m.n.m.
    </div>
  `);

  sectorMarkers[sector.key] = circle;
}

/* Render Tactical Actions */
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
        <div class="action-title">🚨 ORDEN DE EVACUACIÓN Y ALERTA PREVENTIVA: ${s.name}</div>
        <div class="action-desc">Riesgo ML al ${s.score_pct}%. Despachar cuadrillas de Bomberos y avisar a comunidad por PWA/SAE antes del pico de escorrentía.</div>
      `;
      container.appendChild(item);
    });
  }

  if (yellowSectors.length > 0) {
    yellowSectors.forEach(s => {
      const item = document.createElement('div');
      item.className = 'action-item warning';
      item.innerHTML = `
        <div class="action-title">⚠️ PRE-POSICIONAR RECURSOS: ${s.name}</div>
        <div class="action-desc">Riesgo en incremento (${s.score_pct}%). Monitorear pasadas de ríos y preparar equipos de rescate acuático.</div>
      `;
      container.appendChild(item);
    });
  }

  if (redSectors.length === 0 && yellowSectors.length === 0) {
    container.innerHTML = `
      <div class="action-item">
        <div class="action-title">✅ CONDICIONES NORMALES DE MONITOREO</div>
        <div class="action-desc">No se requieren acciones tácticas de emergencia. Próximo escaneo automático NRT en 15 segundos.</div>
      </div>
    `;
  }
}

/* Toggle Storm Simulation Mode */
function toggleStormSimulation() {
  isSimulationMode = !isSimulationMode;

  const simBtn = document.getElementById('btn-toggle-sim');
  const liveText = document.getElementById('live-mode-text');

  if (isSimulationMode) {
    simBtn.innerText = '🔄 Volver a Modo En Vivo NRT';
    simBtn.style.background = 'rgba(231, 76, 60, 0.2)';
    simBtn.style.borderColor = '#E74C3C';
    simBtn.style.color = '#E74C3C';
    
    liveText.innerText = 'MODO SIMULACIÓN (TEMPORAL JULIO 2026)';
    document.getElementById('live-indicator').style.borderColor = '#E74C3C';
    document.getElementById('live-indicator').style.color = '#E74C3C';
  } else {
    simBtn.innerText = '⚡ Simular Tormenta Extrema';
    simBtn.style.background = 'rgba(241, 196, 15, 0.15)';
    simBtn.style.borderColor = '#F1C40F';
    simBtn.style.color = '#F1C40F';
    
    liveText.innerText = 'SISTEMA EN VIVO (NRT)';
    document.getElementById('live-indicator').style.borderColor = '#2ECC71';
    document.getElementById('live-indicator').style.color = '#2ECC71';
  }

  fetchScanData();
}

/* Generate Printable SCI-201 Report PDF */
function generatePdfSci201() {
  window.print();
}
