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
  // Poll every 15 seconds for live telemetry
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

/* Initialize Trend Chart */
function initChart() {
  const ctx = document.getElementById('trendChart').getContext('2d');
  trendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
      datasets: [
        {
          label: 'Lluvia Acumulada (mm)',
          data: [0, 0.2, 0.5, 0.8, 1.2, 1.5, 1.5],
          borderColor: '#00D2FF',
          backgroundColor: 'rgba(0, 210, 255, 0.1)',
          fill: true,
          tension: 0.4
        },
        {
          label: 'Isoterma Cero (x100m)',
          data: [35, 36, 37, 38, 40, 40.6, 40.6],
          borderColor: '#F1C40F',
          borderDash: [5, 5],
          tension: 0.2
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: '#94A3B8' } }
      },
      scales: {
        x: { ticks: { color: '#64748B' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: '#64748B' }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });
}

/* Fetch Spatial Scan Data from Backend */
async function fetchScanData() {
  try {
    const url = isSimulationMode ? '/api/simulate-storm?severity=extreme' : '/api/scan';
    const response = await fetch(url);
    const data = await response.json();
    renderDashboard(data);
  } catch (err) {
    console.error('Error fetching NRT scan data:', err);
  }
}

/* Render Dashboard Components */
function renderDashboard(data) {
  // 1. Render Status Banner
  const bannerBox = document.getElementById('status-banner-box');
  const statusText = document.getElementById('commune-status-text');
  const summarySubtext = document.getElementById('status-summary-subtext');
  const timeTag = document.getElementById('timestamp-tag-text');

  statusText.innerText = data.commune_status;
  timeTag.innerText = `Última Actualización: ${data.timestamp}`;

  bannerBox.className = 'status-banner';
  if (data.commune_status.includes('ROJA')) {
    bannerBox.classList.add('banner-rojo');
    summarySubtext.innerText = '⚠️ ALERTA MÁXIMA DE DESBORDE Y ALUVIÓN: Activar evacuación preventiva en sectores críticos.';
  } else if (data.commune_status.includes('AMARILLA')) {
    bannerBox.classList.add('banner-amarillo');
    summarySubtext.innerText = '⚠️ PRE-ALERTA Y MONITOREO ACTIVO: Puestos de mando en preparación en La Serena.';
  } else {
    bannerBox.classList.add('banner-verde');
    summarySubtext.innerText = 'Monitoreo satelital activo NRT sin riesgo inminente de desborde hidrológico.';
  }

  // 2. Render KPIs
  const t = data.telemetry_summary;
  document.getElementById('kpi-rain-24h').innerHTML = `${t.precip_accum_24h_mm} <span class="kpi-unit">mm</span>`;
  document.getElementById('kpi-rain-6h-sub').innerText = `Últimas 6 horas: ${t.precip_accum_6h_mm} mm`;
  document.getElementById('kpi-api-soil').innerHTML = `${t.api_soil_saturation} <span class="kpi-unit">/ 100</span>`;
  document.getElementById('kpi-freezing').innerHTML = `${t.freezing_level_m.toLocaleString('es-CL')} <span class="kpi-unit">m.n.m.</span>`;
  
  const maxRisk = data.sectors.length > 0 ? data.sectors[0].score_pct : 0;
  document.getElementById('kpi-ml-risk').innerHTML = `${maxRisk}%`;

  // 3. Render Sector Matrix
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

    // Update Map Marker
    updateMapMarker(s);
  });

  // 4. Render Tactical Actions
  renderTacticalActions(data);

  // 5. Update Trend Chart Data if in Simulation Mode
  if (isSimulationMode) {
    trendChart.data.datasets[0].data = [0, 15, 35, 60, 85, 85, 85];
    trendChart.data.datasets[1].data = [28, 30, 33, 35, 35, 35, 35];
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
    radius: 12,
    fillColor: color,
    color: '#FFFFFF',
    weight: 2,
    opacity: 1,
    fillOpacity: 0.8
  }).addTo(map);

  circle.bindPopup(`
    <div style="color: #070C18; font-family: sans-serif;">
      <strong style="font-size: 1rem;">${sector.name}</strong><br>
      <b>Estado:</b> ${sector.semaforo}<br>
      <b>Riesgo ML:</b> ${sector.score_pct}%<br>
      <b>Vulnerabilidad:</b> ${sector.vulnerability}<br>
      <b>Elevación:</b> ${sector.elevation_m} m.n.m.
    </div>
  `);

  sectorMarkers[sector.key] = circle;
}

/* Render Tactical Actions based on Risks */
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
        <div class="action-desc">No se requieren acciones tácticas de emergencia. Próximo escaneo automático en 15 segundos.</div>
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
    liveText.innerText = 'MODO SIMULACIÓN (TEMPORAL JULIO 2026)';
    document.getElementById('live-indicator').style.borderColor = '#F1C40F';
    document.getElementById('live-indicator').style.color = '#F1C40F';
  } else {
    simBtn.innerText = '⚡ Simular Tormenta Extrema';
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
