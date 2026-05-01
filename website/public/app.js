// ─── Auth ─────────────────────────────────────────────────────
const CV_USER = sessionStorage.getItem('cv_user');
const CV_DEPT = sessionStorage.getItem('cv_dept');
if (!CV_USER) { window.location.href = '/'; }

document.getElementById('userName').textContent = CV_USER;
document.getElementById('userDept').textContent = CV_DEPT || 'Officer';
document.getElementById('userAvatar').textContent = CV_USER.charAt(0).toUpperCase();

// ─── State ────────────────────────────────────────────────────
let currentCity = 'Bangalore';
let currentPriority = 'HIGH';
let currentResults = null;
let currentCaseId = null;
let cameraMarkers = [];
let matchMarkers = [];
let trajectoryLayers = [];
let activeCard = null;

// ─── Map ──────────────────────────────────────────────────────
const map = L.map('map', { zoomControl: false, attributionControl: false })
  .setView([12.9716, 77.5946], 12);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  maxZoom: 19, crossOrigin: true,
}).addTo(map);

L.control.zoom({ position: 'bottomright' }).addTo(map);
L.control.attribution({ position: 'bottomleft', prefix: '© CartoDB | OpenStreetMap' }).addTo(map);

// ─── Init ─────────────────────────────────────────────────────
(async () => {
  await loadCity('Bangalore');
  await fetchCaseId('Bangalore');
  setDefaultRange(24);
})();

// ─── Utilities ────────────────────────────────────────────────
function pad(n) { return String(n).padStart(2, '0'); }
function toLocalIso(d) {
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}
function fmtTime(iso) {
  const d = new Date(iso);
  return d.toLocaleString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit', hour12: true });
}
function fmtDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

// ─── City / Camera loading ────────────────────────────────────
async function loadCity(city) {
  clearCams();
  try {
    const res = await fetch(`/api/cameras?city=${encodeURIComponent(city)}`);
    const data = await res.json();
    map.setView([data.center.lat, data.center.lng], data.center.zoom);
    const s = data.stats;
    document.getElementById('topCams').textContent   = (s.total_cams || 0).toLocaleString();
    document.getElementById('topCases').textContent  = s.active_cases || 0;
    document.getElementById('topAlerts').textContent = s.alerts_today || 0;

    data.cameras.forEach(cam => {
      const color = cam.status === 'online' ? '#1a73ff' : (cam.status === 'maintenance' ? '#ffb800' : '#4a6280');
      const html = `<div class="cam-marker ${cam.status}" title="${cam.name}"></div>`;
      const icon = L.divIcon({ className: '', html, iconSize: [10,10], iconAnchor: [5,5] });
      const m = L.marker([cam.lat, cam.lng], { icon })
        .addTo(map)
        .bindPopup(camPopup(cam), { maxWidth: 220 });
      cameraMarkers.push(m);
    });
  } catch(e) { console.error(e); }
}

function camPopup(cam) {
  const statusColor = cam.status === 'online' ? 'var(--green)' : cam.status === 'maintenance' ? 'var(--amber)' : 'var(--text2)';
  return `<div class="map-popup">
    <h4>${cam.name}</h4>
    <div style="font-size:10px;color:var(--text2);margin-bottom:8px">${cam.address}</div>
    <div class="popup-row"><span class="lbl">Type</span><span class="val">${cam.type}</span></div>
    <div class="popup-row"><span class="lbl">Zone</span><span class="val">${cam.zone}</span></div>
    <div class="popup-row"><span class="lbl">Resolution</span><span class="val">${cam.resolution}</span></div>
    <div class="popup-row"><span class="lbl">Status</span><span class="val" style="color:${statusColor}">${cam.status.toUpperCase()}</span></div>
    <div class="popup-row"><span class="lbl">ID</span><span class="val" style="font-family:var(--mono);font-size:10px">${cam.cam_id}</span></div>
  </div>`;
}

function clearCams() { cameraMarkers.forEach(m => map.removeLayer(m)); cameraMarkers = []; }
function clearMatches() {
  matchMarkers.forEach(m => map.removeLayer(m)); matchMarkers = [];
  trajectoryLayers.forEach(l => map.removeLayer(l)); trajectoryLayers = [];
}

// ─── Case ID ──────────────────────────────────────────────────
async function fetchCaseId(city) {
  try {
    const r = await fetch(`/api/case?city=${encodeURIComponent(city)}`);
    const d = await r.json();
    currentCaseId = d.case_id;
    document.getElementById('caseId').textContent = d.case_id;
  } catch(e) { document.getElementById('caseId').textContent = 'CASE-ERR'; }
}

// ─── City change ──────────────────────────────────────────────
async function onCityChange(city) {
  currentCity = city;
  clearMatches();
  hideResults();
  await Promise.all([loadCity(city), fetchCaseId(city)]);
}

// ─── Priority ─────────────────────────────────────────────────
const priClasses = { CRITICAL: 'active-c', HIGH: 'active-h', MEDIUM: 'active-m', LOW: 'active-l' };
const priPillMap  = { CRITICAL: 'pri-critical', HIGH: 'pri-high', MEDIUM: 'pri-medium', LOW: 'pri-low' };

function setPriority(p) {
  currentPriority = p;
  document.querySelectorAll('.pri-btn').forEach(b => b.className = 'pri-btn');
  const btn = document.getElementById(`pri-${p}`);
  if (btn) btn.classList.add(priClasses[p]);
  const badge = document.getElementById('priorityBadge');
  badge.className = `priority-badge ${priPillMap[p]}`;
  badge.textContent = p;
}

// ─── Quick interval ───────────────────────────────────────────
function setQuickInterval(hours, el) {
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  setDefaultRange(hours);
}
function setDefaultRange(hours) {
  const now = new Date();
  document.getElementById('endDt').value   = toLocalIso(now);
  document.getElementById('startDt').value = toLocalIso(new Date(now - hours * 3600000));
}

// ─── Photo ────────────────────────────────────────────────────
function handlePhoto(e) {
  const file = e.target.files[0]; if (!file) return;
  const fr = new FileReader();
  fr.onload = ev => {
    document.getElementById('previewImg').src = ev.target.result;
    document.getElementById('uploadZone').style.display = 'none';
    document.getElementById('photoPreview').style.display = 'block';
  };
  fr.readAsDataURL(file);
}
function changePhoto() {
  document.getElementById('photoInput').value = '';
  document.getElementById('uploadZone').style.display = 'block';
  document.getElementById('photoPreview').style.display = 'none';
  document.getElementById('photoInput').click();
}

// Drag & drop
const zone = document.getElementById('uploadZone');
zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
zone.addEventListener('drop', e => {
  e.preventDefault(); zone.classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  if (file?.type.startsWith('image/')) {
    const dt = new DataTransfer(); dt.items.add(file);
    document.getElementById('photoInput').files = dt.files;
    handlePhoto({ target: { files: [file] } });
  }
});

// ─── Scan animation ───────────────────────────────────────────
let scanTimer = null;
function startScanAnimation(total) {
  document.getElementById('scanOverlay').classList.add('active');
  let count = 0;
  const fill = document.getElementById('scanFill');
  const countEl = document.getElementById('scanCount');
  const pctEl = document.getElementById('scanPct');
  const subEl = document.getElementById('scanSub');
  const statusEl = document.getElementById('scanStatus');

  const phases = [
    { at: 0,   sub: 'Initializing AI face recognition engine...' },
    { at: 15,  sub: 'Extracting facial feature embeddings...' },
    { at: 30,  sub: 'Connecting to vector similarity database...' },
    { at: 50,  sub: 'Scanning CCTV network — cross-referencing frames...' },
    { at: 80,  sub: 'Analyzing biometric match candidates...' },
    { at: 95,  sub: 'Compiling detection report...' },
  ];

  const statuses = [
    'BLR_001 — MG Road Junction... checking',
    'BLR_009 — Majestic Bus Stand... checking',
    'BLR_004 — Indiranagar 100ft... checking',
    'BLR_016 — Marathahalli Bridge... checking',
    'BLR_010 — Silk Board Junction... checking',
    'BLR_023 — Nagawara Flyover... checking',
    'BLR_005 — Whitefield ITPL... checking',
    'BLR_021 — Bellandur Lake... checking',
  ];

  scanTimer = setInterval(() => {
    count = Math.min(count + 1, total);
    const pct = Math.round((count / total) * 100);
    fill.style.width = pct + '%';
    countEl.textContent = `${count} / ${total} cameras`;
    pctEl.textContent = pct + '%';
    const phase = phases.filter(p => pct >= p.at).pop();
    if (phase) subEl.textContent = phase.sub;
    statusEl.textContent = statuses[count % statuses.length] || '';
    if (count >= total) clearInterval(scanTimer);
  }, 60);
}

function stopScanAnimation() {
  clearInterval(scanTimer);
  document.getElementById('scanOverlay').classList.remove('active');
}

// ─── Search ───────────────────────────────────────────────────
async function runSearch() {
  const photo = document.getElementById('photoInput').files[0];
  if (!photo) { showToast('⚠️', 'Upload suspect photo first', 'Drag & drop or click the photo area', 'warn'); return; }

  const start = document.getElementById('startDt').value;
  const end   = document.getElementById('endDt').value;
  if (!start || !end) { showToast('⚠️', 'Set date range', 'Choose start and end time', 'warn'); return; }
  if (new Date(end) <= new Date(start)) { showToast('⚠️', 'Invalid range', 'End time must be after start time', 'warn'); return; }

  setScanBtn(true);
  clearMatches();
  hideResults();

  const totalCams = cameraMarkers.length || 25;
  startScanAnimation(totalCams);

  const fd = new FormData();
  fd.append('photo', photo);
  fd.append('city', currentCity);
  fd.append('start_datetime', start);
  fd.append('end_datetime', end);
  fd.append('case_id', currentCaseId || '');
  fd.append('priority', currentPriority);

  try {
    const [res] = await Promise.all([
      fetch('/api/search', { method: 'POST', body: fd }),
      new Promise(r => setTimeout(r, 2400)),
    ]);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Search failed');
    currentResults = data;
    stopScanAnimation();
    renderResults(data);
  } catch(err) {
    stopScanAnimation();
    showToast('❌', 'Search failed', err.message, 'warn');
  } finally {
    setScanBtn(false);
  }
}

function setScanBtn(on) {
  document.getElementById('scanBtn').disabled = on;
  document.getElementById('scanSpinner').style.display = on ? 'block' : 'none';
  document.getElementById('scanBtnText').textContent = on ? 'SCANNING NETWORK...' : '⚡ INITIATE NETWORK SCAN';
}

// ─── Render results ───────────────────────────────────────────
function renderResults(data) {
  const { results, total_cameras_scanned, matches_found, top_confidence, critical_hits, first_seen, last_seen } = data;

  // Summary grid
  const conf = Math.round((top_confidence || 0) * 100);
  document.getElementById('summaryGrid').innerHTML = `
    <div class="sum-card"><div class="sum-val val-accent">${total_cameras_scanned}</div><div class="sum-lbl">Scanned</div></div>
    <div class="sum-card"><div class="sum-val val-red">${matches_found}</div><div class="sum-lbl">Matches</div></div>
    <div class="sum-card"><div class="sum-val ${conf >= 88 ? 'val-green' : conf >= 78 ? 'val-amber' : 'val-red'}">${conf}%</div><div class="sum-lbl">Top Match</div></div>
  `;

  // Meta line
  if (first_seen && last_seen) {
    document.getElementById('resultsMeta').innerHTML =
      `<strong>First:</strong> ${fmtTime(first_seen)} &nbsp;·&nbsp; <strong>Last:</strong> ${fmtTime(last_seen)}`;
  }

  document.getElementById('exportBtn').style.display = 'block';
  document.getElementById('resultsSection').style.display = 'block';

  if (!results.length) {
    document.getElementById('timeline').innerHTML =
      '<div class="empty-state"><div class="empty-icon">🔍</div>No matches in selected window</div>';
    showToast('🔍', 'No matches found', 'Try widening the date/time range', 'info');
    return;
  }

  // Timeline cards (animate one by one)
  const tl = document.getElementById('timeline');
  tl.innerHTML = '';
  results.forEach((r, i) => {
    setTimeout(() => {
      const card = document.createElement('div');
      card.className = `t-card alert-${r.alert_level}`;
      card.style.animationDelay = `${i * 60}ms`;
      const confPct = Math.round(r.confidence * 100);
      const confColor = confPct >= 88 ? 'var(--green)' : confPct >= 78 ? 'var(--amber)' : 'var(--red)';
      card.innerHTML = `
        <div class="t-top">
          <div class="t-num">${r.order}</div>
          <div class="t-snap"><img src="${r.snapshot_url}" loading="lazy" /></div>
          <div class="t-info">
            <div class="t-cam">${r.cam_name}</div>
            <div class="t-addr">${r.area} · ${r.cam_type}</div>
            <div class="t-time">${fmtTime(r.timestamp)}</div>
          </div>
          <div class="t-alert-badge badge-${r.alert_level}">${r.alert_level}</div>
        </div>
        <div class="t-meta">
          <div class="t-meta-item"><div class="t-meta-lbl">Direction</div><div class="t-meta-val">${r.direction}</div></div>
          <div class="t-meta-item"><div class="t-meta-lbl">Height</div><div class="t-meta-val">${r.height_est}</div></div>
          <div class="t-meta-item"><div class="t-meta-lbl">Vehicle</div><div class="t-meta-val">${r.vehicle || 'None'}</div></div>
        </div>
        <div class="conf-bar-wrap">
          <div style="display:flex;justify-content:space-between;margin-bottom:3px">
            <span style="font-size:9px;color:var(--text2);letter-spacing:1px">MATCH CONFIDENCE</span>
            <span style="font-size:10px;font-weight:700;color:${confColor}">${confPct}%</span>
          </div>
          <div class="conf-bar-bg"><div class="conf-bar-fill" style="width:${confPct}%;background:${confColor}"></div></div>
        </div>
      `;
      card.addEventListener('click', () => selectCard(card, r, i));
      tl.appendChild(card);
    }, i * 80);
  });

  // Map markers + trajectory
  const latlngs = [];
  results.forEach((r, i) => {
    const cls = r.alert_level === 'CRITICAL' ? '' : r.alert_level === 'HIGH' ? 'high' : 'medium';
    const html = `<div class="match-marker ${cls}">${r.order}</div>`;
    const icon = L.divIcon({ className: '', html, iconSize: [28,28], iconAnchor: [14,14] });
    const m = L.marker([r.lat, r.lng], { icon })
      .addTo(map)
      .bindPopup(matchPopup(r), { maxWidth: 280 });
    matchMarkers.push(m);
    latlngs.push([r.lat, r.lng]);
  });

  if (latlngs.length > 1) {
    const line = L.polyline(latlngs, { color: '#ff3b5c', weight: 2.5, opacity: 0.8, dashArray: '8 5' }).addTo(map);
    trajectoryLayers.push(line);
    map.fitBounds(line.getBounds(), { padding: [60, 60] });
  } else if (latlngs.length === 1) {
    map.setView(latlngs[0], 15);
  }

  const critWord = critical_hits > 0 ? `${critical_hits} CRITICAL hit${critical_hits > 1 ? 's' : ''}` : `${matches_found} location${matches_found > 1 ? 's' : ''}`;
  showToast('🚨', `Suspect detected — ${critWord}`, `${fmtDate(first_seen)} to ${fmtDate(last_seen)}`, 'alert');
}

function selectCard(card, r, idx) {
  if (activeCard) activeCard.classList.remove('active');
  card.classList.add('active'); activeCard = card;
  map.setView([r.lat, r.lng], 16);
  matchMarkers[idx]?.openPopup();
}

function matchPopup(r) {
  const conf = Math.round(r.confidence * 100);
  const confColor = conf >= 88 ? 'var(--green)' : conf >= 78 ? 'var(--amber)' : 'var(--red)';
  return `<div class="map-popup">
    <img src="${r.snapshot_url}" />
    <h4>${r.cam_name}</h4>
    <div style="font-size:10px;color:var(--text2);margin-bottom:6px">${r.address}</div>
    <div class="popup-row"><span class="lbl">Time</span><span class="val">${fmtTime(r.timestamp)}</span></div>
    <div class="popup-row"><span class="lbl">Direction</span><span class="val">${r.direction}</span></div>
    <div class="popup-row"><span class="lbl">Clothing</span><span class="val" style="max-width:140px;text-align:right">${r.clothing}</span></div>
    <div class="popup-row"><span class="lbl">Vehicle</span><span class="val">${r.vehicle || 'None observed'}</span></div>
    <div class="popup-conf badge-${r.alert_level}" style="display:inline-block;margin-top:8px;font-size:11px;font-weight:700;padding:4px 10px;border-radius:4px">
      ${conf}% Match · ${r.alert_level}
    </div>
  </div>`;
}

function hideResults() {
  document.getElementById('resultsSection').style.display = 'none';
  document.getElementById('exportBtn').style.display = 'none';
}

// ─── Export ───────────────────────────────────────────────────
function exportReport() {
  if (!currentResults) return;
  const d = currentResults;
  const lines = [
    '╔══════════════════════════════════════════════════════════╗',
    '║             CLEARVISION  —  INTELLIGENCE REPORT         ║',
    '╚══════════════════════════════════════════════════════════╝',
    '',
    `CASE NUMBER    : ${d.case_id}`,
    `PRIORITY       : ${d.priority}`,
    `CITY           : ${d.city}`,
    `OFFICER        : ${CV_USER} (${CV_DEPT})`,
    `GENERATED      : ${new Date().toLocaleString('en-IN')}`,
    '',
    '── SEARCH WINDOW ──────────────────────────────────────────',
    `FROM : ${d.search_window.start}`,
    `TO   : ${d.search_window.end}`,
    '',
    '── SUMMARY ────────────────────────────────────────────────',
    `Cameras Scanned  : ${d.total_cameras_scanned}`,
    `Matches Found    : ${d.matches_found}`,
    `Top Confidence   : ${Math.round(d.top_confidence * 100)}%`,
    `Critical Hits    : ${d.critical_hits}`,
    `First Sighting   : ${d.first_seen ? fmtTime(d.first_seen) : '—'}`,
    `Last Sighting    : ${d.last_seen ? fmtTime(d.last_seen) : '—'}`,
    '',
    '── DETECTIONS ─────────────────────────────────────────────',
  ];
  d.results.forEach(r => {
    lines.push(`\n[${r.order}] ${r.alert_level} — ${r.cam_name}`);
    lines.push(`    Address   : ${r.address}`);
    lines.push(`    Zone      : ${r.zone}  |  Type : ${r.cam_type}`);
    lines.push(`    Time      : ${fmtTime(r.timestamp)}`);
    lines.push(`    Confidence: ${Math.round(r.confidence * 100)}%`);
    lines.push(`    Direction : ${r.direction}  |  Height : ${r.height_est}`);
    lines.push(`    Clothing  : ${r.clothing}`);
    lines.push(`    Vehicle   : ${r.vehicle || 'None observed'}`);
    lines.push(`    GPS       : ${r.lat.toFixed(4)}, ${r.lng.toFixed(4)}`);
  });
  lines.push('', '────────────────────────────────────────────────────────────');
  lines.push('END OF REPORT — CONFIDENTIAL — FOR AUTHORIZED USE ONLY');

  const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `ClearVision_${d.case_id}_${Date.now()}.txt`;
  a.click();
}

// ─── Toast ────────────────────────────────────────────────────
let toastTmr = null;
function showToast(icon, text, sub, type = 'info') {
  const t = document.getElementById('toast');
  document.getElementById('toastIcon').textContent = icon;
  document.getElementById('toastText').textContent = text;
  document.getElementById('toastSub').textContent = sub || '';
  const colors = { alert: 'var(--red)', warn: 'var(--amber)', info: 'var(--accent)', success: 'var(--green)' };
  t.style.borderColor = colors[type] || colors.info;
  t.style.display = 'block';
  t.style.animation = 'none';
  requestAnimationFrame(() => t.style.animation = 'toastIn 0.3s ease');
  if (toastTmr) clearTimeout(toastTmr);
  toastTmr = setTimeout(() => { t.style.display = 'none'; }, 5000);
}

// ─── Logout ───────────────────────────────────────────────────
function logout() {
  sessionStorage.clear();
  window.location.href = '/';
}
