/* ==========================================================================
   Proyecto Centinela — Consola de Demostración & Simulación (demo.js v4.0)
   ========================================================================== */

let map;
let sectorMarkers = {};
let trendChart;
let currentScenario = 'normal';
let isInitialBoundsSet = false;

// Layer Toggles & Audio State
let evacuationGroup = null;
let isEvacuationActive = false;
let isAudioAlarmEnabled = false;
let audioCtx = null;

let sciLogEntries = [
  { timestamp: "18:00 hrs", sector: "Pueblo Islón / Quebrada Santa Gracia", user: "Demo Operador", severity: "Moderado", desc: "Simulación de escenario de temporal iniciada. Cuenca alta monitorizada." }
];

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  initChart();
  loadDemoScenario('normal');
  renderSciLogList();
});

function initMap() {
  map = L.map('map').setView([-29.900, -71.210], 11);

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map);

  initEvacuationRoutes();
}

function initEvacuationRoutes() {
  evacuationGroup = L.featureGroup();

  const safePuebloIslon = L.circleMarker([-29.865, -71.200], {
    radius: 9, fillColor: '#00D2FF', color: '#FFFFFF', weight: 2, fillOpacity: 0.9
  }).bindPopup("<b>Zona Segura N°1 (Pueblo Islón)</b><br>Cerro El Brillador Cota 180m");

  const routeIslon = L.polyline([
    [-29.878, -71.218],
    [-29.870, -71.210],
    [-29.865, -71.200]
  ], { color: '#00D2FF', weight: 3, dashArray: '6, 6' }).bindPopup("Ruta Evacuación Aluvional Pueblo Islón");

  const safeLasRojas = L.circleMarker([-29.960, -71.045], {
    radius: 9, fillColor: '#00D2FF', color: '#FFFFFF', weight: 2, fillOpacity: 0.9
  }).bindPopup("<b>Zona Segura N°2 (Las Rojas)</b><br>Ladera Norte Cota 280m");

  const routeLasRojas = L.polyline([
    [-29.970, -71.055],
    [-29.960, -71.045]
  ], { color: '#00D2FF', weight: 3, dashArray: '6, 6' }).bindPopup("Ruta Evacuación Las Rojas");

  evacuationGroup.addLayer(safePuebloIslon);
  evacuationGroup.addLayer(routeIslon);
  evacuationGroup.addLayer(safeLasRojas);
  evacuationGroup.addLayer(routeLasRojas);
}

function toggleEvacuationRoutes() {
  isEvacuationActive = !isEvacuationActive;
  if (isEvacuationActive) {
    evacuationGroup.addTo(map);
  } else {
    map.removeLayer(evacuationGroup);
  }
}



function toggleAudioAlarm() {
  isAudioAlarmEnabled = !isAudioAlarmEnabled;
  const btn = document.getElementById('btn-toggle-sound');
  if (isAudioAlarmEnabled) {
    btn.innerText = '🔔 Alarma Sonora: ON';
    btn.style.borderColor = '#2ECC71';
    btn.style.color = '#2ECC71';
    playEmergencyChime();
  } else {
    btn.innerText = '🔔 Alarma Sonora: OFF';
    btn.style.borderColor = '#F1C40F';
    btn.style.color = '#F1C40F';
  }
}

function playEmergencyChime() {
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(880, audioCtx.currentTime);
    gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.3);
  } catch (e) {
    console.error('AudioContext error:', e);
  }
}

function addSciLogEntry() {
  const sectorInput = document.getElementById('log-sector-input');
  const userInput = document.getElementById('log-user-input');
  const severityInput = document.getElementById('log-severity-input');
  const descInput = document.getElementById('log-desc-input');

  if (!descInput.value.trim()) return;

  const now = new Date();
  const timeStr = `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')} hrs`;

  sciLogEntries.unshift({
    timestamp: timeStr,
    sector: sectorInput.value.trim() || 'General La Serena',
    user: userInput.value.trim() || 'Demo Operador',
    severity: severityInput.value.trim() || 'Informativo',
    desc: descInput.value.trim()
  });

  descInput.value = '';
  renderSciLogList();
}

function clearSciLogs() {
  if (confirm('¿Deseas limpiar todos los registros de la Bitácora Táctica SCI?')) {
    sciLogEntries = [];
    renderSciLogList();
  }
}

function renderSciLogList() {
  const list = document.getElementById('sci-log-list');
  if (!list) return;
  list.innerHTML = '';

  if (sciLogEntries.length === 0) {
    list.innerHTML = `<div style="color: var(--text-muted); font-size: 0.85rem; padding: 0.5rem;">No hay observaciones registradas en la Bitácora Táctica.</div>`;
    return;
  }

  sciLogEntries.forEach(item => {
    const card = document.createElement('div');
    card.style.background = 'rgba(13, 22, 41, 0.9)';
    card.style.border = '1px solid var(--card-border)';
    card.style.borderLeft = '4px solid var(--brand-blue)';
    card.style.padding = '0.75rem 1rem';
    card.style.borderRadius = '8px';
    card.style.fontSize = '0.85rem';

    if (item.severity.toLowerCase().includes('crítico') || item.severity.toLowerCase().includes('rojo') || item.severity.toLowerCase().includes('evacuación')) {
      card.style.borderLeftColor = 'var(--status-red)';
      card.style.background = 'rgba(231, 76, 60, 0.08)';
    } else if (item.severity.toLowerCase().includes('moderado') || item.severity.toLowerCase().includes('amarillo')) {
      card.style.borderLeftColor = 'var(--status-yellow)';
    }

    card.innerHTML = `
      <div style="display:flex; justify-content: space-between; align-items:center; margin-bottom: 0.35rem; font-size: 0.8rem;">
        <span style="font-weight: 700; color: #FFFFFF;">📍 ${item.sector}</span>
        <div style="display:flex; gap: 0.75rem; align-items:center;">
          <span style="background: rgba(0, 210, 255, 0.15); color: var(--brand-blue); padding: 0.15rem 0.5rem; border-radius: 4px; font-weight: 600;">${item.severity}</span>
          <span style="font-family: var(--font-mono); color: var(--text-secondary);">${item.timestamp} • ${item.user}</span>
        </div>
      </div>
      <div style="color: var(--text-primary); line-height: 1.4; font-size: 0.88rem;">${item.desc}</div>
    `;
    list.appendChild(card);
  });
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
          label: 'Límite de Nieve (Cordillera)',
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
        legend: { labels: { color: '#F0F4F8', font: { family: 'Inter', size: 11, weight: 'bold' } } }
      },
      scales: {
        x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
        yRain: {
          type: 'linear', position: 'left', min: 0, max: 100,
          title: { display: true, text: 'Lluvia (mm)', color: '#00D2FF', font: { weight: 'bold' } },
          ticks: { color: '#00D2FF' }, grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        yFreezing: {
          type: 'linear', position: 'right', min: 1000, max: 5000,
          title: { display: true, text: 'Límite de Nieve (m)', color: '#F1C40F', font: { weight: 'bold' } },
          ticks: { color: '#F1C40F', callback: v => v + 'm' },
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
    if (isAudioAlarmEnabled) playEmergencyChime();
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

  const selectDropdown = document.getElementById('sector-focus-select');
  if (selectDropdown && selectDropdown.options.length <= 1) {
    data.sectors.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.key;
      opt.innerText = s.name;
      selectDropdown.appendChild(opt);
    });
  }

  const coverageGroup = [];

  data.sectors.forEach(s => {
    const card = document.createElement('div');
    card.className = 'sector-card';
    card.style.cursor = 'pointer';
    card.onclick = () => focusSectorFromKey(s.key);

    let badgeClass = 'badge-verde';
    if (s.semaforo.includes('ROJA')) badgeClass = 'badge-rojo';
    else if (s.semaforo.includes('AMARILLA')) badgeClass = 'badge-amarillo';

    card.innerHTML = `
      <div>
        <div class="sector-name">${s.name}</div>
        <div class="sector-vulnerability"><strong>Peligro:</strong> ${s.disaster_type}</div>
        <div class="sector-vulnerability" style="color: var(--brand-blue); margin-top: 2px;">
          <strong>Llegada del Pico:</strong> ${s.eta_impact} (Tiempo de Avance: ${s.concentration_time_hours} horas) • <strong style="color: #2ECC71;">Hora de Paso Seguro (Calma):</strong> ${s.eta_safe_return || '17:00 hrs'}
        </div>
      </div>
      <span class="sector-badge ${badgeClass}">${s.semaforo} (${s.score_pct}%)</span>
    `;
    sectorContainer.appendChild(card);

    const layerPair = updateMapMarker(s);
    if (layerPair) coverageGroup.push(layerPair.circle);
  });

  if (!isInitialBoundsSet && coverageGroup.length > 0) {
    const featureGroup = L.featureGroup(coverageGroup);
    map.fitBounds(featureGroup.getBounds().pad(0.08));
    isInitialBoundsSet = true;
  }

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

  const coverageZone = L.circle(coords, {
    radius: sector.radius_m || 1000,
    color: color,
    weight: 1.5,
    fillColor: fillColor,
    fillOpacity: 0.35,
    dashArray: '4, 4'
  }).addTo(map);

  const centerMarker = L.circleMarker(coords, {
    radius: 7,
    fillColor: color,
    color: '#FFFFFF',
    weight: 2,
    opacity: 1,
    fillOpacity: 0.95
  }).addTo(map);

  const popupContent = `
    <div style="color: #070C18; font-family: sans-serif; min-width: 240px;">
      <strong style="font-size: 0.95rem; color: #00205B;">${sector.name}</strong><br>
      <hr style="margin: 4px 0; border: 0; border-top: 1px solid #ccc;">
      <b>Estado:</b> ${sector.semaforo}<br>
      <b>Riesgo ML:</b> ${sector.score_pct}%<br>
      <b>Llegada del Pico Inundación:</b> ${sector.eta_impact} (Tiempo de Avance: ${sector.concentration_time_hours} horas)<br>
      <b style="color: #2E7D32;">Hora de Paso Seguro (Calma):</b> ${sector.eta_safe_return || '17:00 hrs'}<br>
      <b>Transitabilidad:</b> ${sector.transitability_status || 'TRANSITABLE'}<br>
      <b>Radio Cobertura:</b> ${sector.radius_m}m • <b>Cota:</b> ${sector.elevation_m} m.n.m.
    </div>
  `;

  coverageZone.bindPopup(popupContent);
  centerMarker.bindPopup(popupContent);

  sectorMarkers[sector.key] = { circle: coverageZone, marker: centerMarker, coords: coords, radius_m: sector.radius_m };
  return sectorMarkers[sector.key];
}

function focusSectorFromSelect(sectorKey) {
  if (sectorKey) focusSectorFromKey(sectorKey);
}

function focusSectorFromKey(sectorKey) {
  if (sectorMarkers[sectorKey]) {
    const s = sectorMarkers[sectorKey];
    map.flyTo(s.coords, 14, { duration: 1.2 });
    s.marker.openPopup();
  }
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
        <div class="action-desc">Riesgo ML al ${s.score_pct}%. Peligro: ${s.disaster_type}. Llegada del Pico: ${s.eta_impact}. Proyectado aluvión y anegamiento crítico.</div>
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
        <div class="action-desc">Riesgo en incremento (${s.score_pct}%). Peligro: ${s.disaster_type}. Llegada del Pico: ${s.eta_impact}. Monitorear cauces.</div>
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
