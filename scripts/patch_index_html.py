import json

with open('data/blueprints_dump.json') as f:
    fixtures_json = f.read()

with open('index.html') as f:
    html = f.read()

target_marker = """    // 9. FACILITY SWITCHER
    function changeFacility(facId) {
      state.currentFacilityId = facId;
      const fac = state.facilities[facId];
      if (!fac) return;
      alert(`Switched active Snowflake Iceberg facility to: ${fac.name} (${fac.loc})`);
    }"""

replacement_code = f"""    // =========================================================================
    // 9. DYNAMIC SQLITE BLUEPRINT & MULTI-FACILITY ENGINE
    // =========================================================================
    const API_BASE = (window.location.port === '8080' || window.location.port === '5500') ? 'http://localhost:8000' : '';
    const LOCAL_BLUEPRINT_FIXTURES = {fixtures_json};

    let activeBlueprintSeq = 0;
    let defaultExpandedTopologyHtml = null;
    let defaultExpandedSvgHtml = null;
    let topologyZoom = 1.0;

    async function fetchFacilitiesFromBackend() {{
      try {{
        const res = await fetch(API_BASE + '/api/facilities');
        if (!res.ok) return;
        const data = await res.json();
        if (data && data.facilities && data.facilities.length > 0) {{
          data.facilities.forEach(fac => {{
            (fac.plants || []).forEach(p => {{
              if (!state.facilities[p.id]) {{
                state.facilities[p.id] = {{
                  id: p.id,
                  name: p.name,
                  loc: p.location || fac.city,
                  badge: p.id,
                  stock: 1500,
                  cap: p.floor_area_sqm || 2000,
                  pct: 75.0,
                  doi: 12.0,
                  doiStatus: "Nominal"
                }};
              }}
            }});
          }});
        }}
      }} catch (e) {{
        console.warn('Backend /api/facilities not reached; using local state.', e);
      }}
    }}

    async function loadPlantBlueprint(plantId) {{
      if (!plantId) plantId = 'WH_RIVERSIDE_01';
      activeBlueprintSeq++;
      const currentReqSeq = activeBlueprintSeq;

      // Handle 'ALL' plants network overview
      if (plantId === 'ALL') {{
        const nodesContainer = document.getElementById('stage-topology-nodes');
        const svgEl = document.getElementById('canvas-edges-svg');
        if (nodesContainer && defaultExpandedTopologyHtml) {{
          nodesContainer.className = "relative z-10 flex gap-10 min-w-[1300px]";
          nodesContainer.innerHTML = defaultExpandedTopologyHtml;
        }}
        if (svgEl && defaultExpandedSvgHtml) {{
          svgEl.innerHTML = defaultExpandedSvgHtml;
        }}
        return;
      }}

      // Fetch dynamic CAD blueprint from SQLite backend
      try {{
        const res = await fetch(API_BASE + '/api/factories/' + plantId + '/blueprint');
        if (res.ok) {{
          const data = await res.json();
          if (currentReqSeq !== activeBlueprintSeq) return;
          if (data.status === 'success' && data.blueprint) {{
            renderBlueprintTopology(data.blueprint);
            return;
          }}
        }}
      }} catch (err) {{
        console.warn('API blueprint fetch unavailable, falling back to local fixtures:', err);
      }}

      // Offline fallback: Use pre-seeded blueprint fixtures
      if (LOCAL_BLUEPRINT_FIXTURES[plantId]) {{
        renderBlueprintTopology(LOCAL_BLUEPRINT_FIXTURES[plantId]);
      }}
    }}

    function renderBlueprintTopology(bp) {{
      if (!bp || !bp.nodes) return;

      // 1. Render Animated SVG Flow Edges
      const svgEl = document.getElementById('canvas-edges-svg');
      if (svgEl) {{
        const defs = `
          <defs>
            <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#29B5E8" />
            </marker>
            <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#EF4444" />
            </marker>
            <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#10B981" />
            </marker>
          </defs>
        `;
        let pathsHtml = '';
        (bp.edges || []).forEach(edge => {{
          const isHot = edge.is_hot;
          const strokeClass = isHot ? 'edge-flow-hot' : 'edge-flow';
          const dashes = edge.dashes ? `stroke-dasharray="${{edge.dashes}}"` : '';
          const strokeColor = edge.color || (isHot ? '#EF4444' : '#29B5E8');
          const markerId = isHot ? 'arrow-red' : (strokeColor === '#10B981' || strokeColor.includes('10b981') ? 'arrow-green' : 'arrow-blue');
          pathsHtml += `<path d="${{edge.path}}" fill="none" stroke="${{strokeColor}}" stroke-width="${{edge.stroke || '2.2'}}" class="${{strokeClass}}" ${{dashes}} marker-end="url(#${{markerId}})" />`;
        }});
        svgEl.innerHTML = defs + pathsHtml;
      }}

      // 2. Render Blueprint Node Cards
      const nodesContainer = document.getElementById('stage-topology-nodes');
      if (nodesContainer) {{
        nodesContainer.className = 'relative z-10 min-w-[1350px] min-h-[520px]';
        let nodesHtml = '';
        (bp.nodes || []).forEach(node => {{
          const isCrit = node.status === 'CRITICAL' || (node.failure_risk && node.failure_risk >= 0.85);
          const isWarn = node.status === 'WARNING' || (node.failure_risk && node.failure_risk >= 0.50 && node.failure_risk < 0.85);
          const isBackup = node.status === 'BACKUP';
          const isUnitFacility = node.type === 'UnitFacility';
          const isDispatch = node.type === 'Dispatch';
          const isInventory = node.type === 'Inventory';

          let borderClass = 'border-snowflake/30 hover:border-snowflake';
          let statusColor = 'text-emerald-500';
          let statusBg = 'bg-emerald-500';
          let statusText = 'Healthy';
          let barBg = 'bg-emerald-500';
          let health = node.health_score !== undefined ? node.health_score : (node.failure_risk !== undefined ? Math.round((1.0 - node.failure_risk) * 100) : 100);

          if (isCrit) {{
            borderClass = 'border-red-500/80 sf-card shadow-[0_0_0_2px_rgba(239,68,68,0.2),0_0_20px_-4px_rgba(239,68,68,0.35)]';
            statusColor = 'text-red-500';
            statusBg = 'bg-red-500 animate-pulse';
            statusText = 'Critical';
            barBg = 'bg-red-500';
          }} else if (isWarn) {{
            borderClass = 'border-amber-500/80 sf-card shadow-[0_0_0_2px_rgba(245,158,11,0.2),0_0_20px_-4px_rgba(245,158,11,0.35)]';
            statusColor = 'text-amber-500';
            statusBg = 'bg-amber-500';
            statusText = 'Warning';
            barBg = 'bg-amber-500';
          }} else if (isUnitFacility) {{
            borderClass = 'border-purple-500/80 sf-card shadow-[0_0_0_2px_rgba(168,85,247,0.2),0_0_20px_-4px_rgba(168,85,247,0.35)] ring-1 ring-purple-500/40';
            statusColor = 'text-purple-400';
            statusBg = 'bg-purple-400';
            statusText = 'Converged';
            barBg = 'bg-gradient-to-r from-cyan-400 via-purple-500 to-emerald-400';
          }} else if (isDispatch) {{
            borderClass = 'border-emerald-500/60 sf-card shadow-sm';
            statusColor = 'text-emerald-500';
            statusBg = 'bg-emerald-500';
            statusText = 'Dispatch';
            barBg = 'bg-emerald-500';
          }} else if (isInventory) {{
            borderClass = 'border-cyan-500/60 sf-card shadow-sm';
            statusColor = 'text-cyan-500';
            statusBg = 'bg-cyan-500';
            statusText = 'Infeed';
            barBg = 'bg-cyan-500';
          }} else if (isBackup) {{
            borderClass = 'border-emerald-500/50 border-dashed sf-card';
            statusColor = 'text-emerald-500';
            statusBg = 'bg-emerald-500';
            statusText = 'Standby';
            barBg = 'bg-emerald-500';
          }}

          let alertBadge = '';
          if (node.alert) {{
            alertBadge = `
              <span class="absolute -top-2.5 right-2 rounded-md border ${{isCrit ? 'border-red-500/60 bg-red-500/20 text-red-500' : 'border-amber-500/60 bg-amber-500/20 text-amber-500'}} px-1.5 py-0.5 text-[9px] font-bold tracking-wide uppercase shadow-sm">
                ${{node.alert}}
              </span>
            `;
          }} else if (isUnitFacility) {{
            alertBadge = `
              <span class="absolute -top-2.5 right-2 rounded-md border border-purple-500/60 bg-purple-500/20 text-purple-400 px-1.5 py-0.5 text-[9px] font-bold tracking-wide uppercase shadow-sm">
                ⚡ Converged Unit
              </span>
            `;
          }} else if (isDispatch) {{
            alertBadge = `
              <span class="absolute -top-2.5 right-2 rounded-md border border-emerald-500/60 bg-emerald-500/20 text-emerald-500 px-1.5 py-0.5 text-[9px] font-bold tracking-wide uppercase shadow-sm">
                🚢 Dispatch Bay
              </span>
            `;
          }}

          const bayLabel = node.bay ? `<div class="text-[9px] uppercase font-bold text-slate-400 tracking-wider mb-0.5 truncate font-mono-code">${{node.bay}}</div>` : '';

          let metric1 = '〰 1.2 mm/s';
          let metric2 = '🌡 65.0°C';
          let metric3 = '⏱ 120 u/h';
          if (isUnitFacility) {{
            metric1 = '🔍 100% Optical';
            metric2 = '⚡ Converged';
            metric3 = '✨ ISO-Class';
          }} else if (isDispatch) {{
            metric1 = '📦 Outbound';
            metric2 = '🌡 Ambient';
            metric3 = '🚛 Carrier Ready';
          }} else if (isInventory) {{
            metric1 = '📦 Safe Buffer';
            metric2 = '🛡 Vault Safe';
            metric3 = '📊 Monitored';
          }}

          nodesHtml += `
            <div onclick="inspectZone('${{node.machine_id || node.id}}')"
                 style="position: absolute; left: ${{node.x}}px; top: ${{node.y}}px; width: ${{node.w || 190}}px; min-height: ${{node.h || 96}}px;"
                 class="sf-card p-2.5 rounded-xl border ${{borderClass}} transition-all duration-200 hover:scale-[1.01] cursor-pointer select-none z-10 shadow-sm">
              ${{alertBadge}}
              <div class="flex h-full flex-col justify-between">
                <div>
                  ${{bayLabel}}
                  <div class="flex items-center justify-between gap-1.5">
                    <span class="truncate font-mono-code text-[11px] font-bold text-slate-800 dark:text-white">${{node.name}}</span>
                    <span class="flex items-center gap-1 text-[10px] font-medium ${{statusColor}}">
                      <span class="h-1.5 w-1.5 rounded-full ${{statusBg}}"></span>
                      ${{statusText}}
                    </span>
                  </div>
                  <p class="mt-0.5 truncate text-[10px] text-slate-500 font-mono-code">${{node.spec || ''}}</p>
                </div>

                <div class="mt-2">
                  <div class="flex items-center justify-between gap-2 text-[10px] mb-1 font-mono-code">
                    <span class="text-slate-400">Health</span>
                    <span class="font-bold text-slate-700 dark:text-slate-300">${{health}}%</span>
                  </div>
                  <div class="h-1 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
                    <div class="h-full rounded-full ${{barBg}}" style="width: ${{health}}%"></div>
                  </div>
                  <div class="mt-1.5 flex items-center justify-between text-[9px] text-slate-400 font-mono-code">
                    <span>${{metric1}}</span>
                    <span>${{metric2}}</span>
                    <span>${{metric3}}</span>
                  </div>
                </div>
              </div>
            </div>
          `;
        }});
        nodesContainer.innerHTML = nodesHtml;
      }}
    }}

    function changeFacility(facId) {{
      state.currentFacilityId = facId;
      loadPlantBlueprint(facId);

      const fac = state.facilities[facId];
      if (fac) {{
        const topClock = document.getElementById('top-sim-clock');
        if (topClock) topClock.textContent = `Active: ${{fac.name}}`;
      }}
    }}"""

if target_marker in html:
    html = html.replace(target_marker, replacement_code)
    print('Replaced facility switcher with dynamic blueprint engine')
else:
    print('Warning: target_marker not found')

# Update zoomTwin and resetCanvasTransform to support topology zoom
old_zoom = """    function zoomTwin(scale) { 
      const cont = document.getElementById('svg-viewport-container');
      cont.style.transform = `scale(${scale})`;
    }
    function resetCanvasTransform() {
      const cont = document.getElementById('svg-viewport-container');
      if (cont) cont.style.transform = "scale(1)";
    }"""

new_zoom = """    function zoomTwin(scale) { 
      if (state.activeTwinMode === 'floor') {
        const cont = document.getElementById('svg-viewport-container');
        if (cont) cont.style.transform = `scale(${scale})`;
      } else {
        topologyZoom = Math.max(0.5, Math.min(2.0, topologyZoom * scale));
        const canvas = document.getElementById('stage-canvas-content');
        if (canvas) canvas.style.transform = `scale(${topologyZoom})`;
      }
    }
    function resetCanvasTransform() {
      topologyZoom = 1.0;
      const cont = document.getElementById('svg-viewport-container');
      if (cont) cont.style.transform = "scale(1)";
      const canvas = document.getElementById('stage-canvas-content');
      if (canvas) canvas.style.transform = "scale(1)";
    }"""

if old_zoom in html:
    html = html.replace(old_zoom, new_zoom)
    print('Updated zoomTwin and resetCanvasTransform')

# Update DOMContentLoaded listener
old_dom = """    // Initialize Default View
    window.addEventListener('DOMContentLoaded', () => {
      navigatePage('twin');
      setTwinView('topology');
    });"""

new_dom = """    // Initialize Default View
    window.addEventListener('DOMContentLoaded', () => {
      navigatePage('twin');
      setTwinView('topology');

      const nodesEl = document.getElementById('stage-topology-nodes');
      const svgEl = document.getElementById('canvas-edges-svg');
      if (nodesEl) defaultExpandedTopologyHtml = nodesEl.innerHTML;
      if (svgEl) defaultExpandedSvgHtml = svgEl.innerHTML;

      fetchFacilitiesFromBackend();
    });"""

if old_dom in html:
    html = html.replace(old_dom, new_dom)
    print('Updated DOMContentLoaded listener')

with open('index.html', 'w') as f:
    f.write(html)
print('index.html updated successfully!')
