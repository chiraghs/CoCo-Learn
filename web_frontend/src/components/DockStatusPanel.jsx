import React from 'react';
import { Anchor, ArrowRight } from 'lucide-react';

export default function DockStatusPanel({ docks, plantName }) {
  if (!docks) return null;

  return (
    <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-4 shadow-sm flex flex-col gap-3">
      {/* Tab Switcher in Panel Header */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <button className="px-2.5 py-1 bg-blue-50 text-blue-700 font-bold text-xs rounded-md border border-blue-200">
            Docks {docks.length}/{docks.length}
          </button>
          <button className="px-2.5 py-1 text-slate-500 hover:text-slate-800 font-semibold text-xs rounded-md">
            Forklifts 1/2
          </button>
          <button className="px-2.5 py-1 text-slate-500 hover:text-slate-800 font-semibold text-xs rounded-md">
            Trucks 2
          </button>
        </div>
        <span className="text-[11px] font-bold text-slate-400 uppercase">{plantName || "Riverside Hub"}</span>
      </div>

      {/* Dock Bay Rows */}
      <div className="flex flex-col gap-2">
        {docks.map((dock) => {
          const isLoading = dock.status === 'Loading';
          const isDelayed = dock.status === 'Delayed';
          const isEnroute = dock.status === 'En route';

          return (
            <div key={dock.dock_id} className="flex items-center justify-between py-1.5 px-2 hover:bg-slate-50 rounded-lg text-xs transition-colors">
              <div className="flex items-center gap-2">
                <span className="font-bold text-slate-900 w-12">Bay {dock.bay_number}</span>
                <span className="text-slate-400">•</span>
                <span className="font-medium text-slate-700">
                  {dock.assigned_truck_id ? `${dock.assigned_truck_id} • ${dock.assigned_carrier}` : 'No truck assigned'}
                </span>
              </div>

              <div className="flex items-center gap-2.5">
                <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold ${
                  isLoading ? 'bg-emerald-100 text-emerald-800' :
                  isDelayed ? 'bg-rose-100 text-rose-800' :
                  isEnroute ? 'bg-sky-100 text-sky-800' :
                  'bg-slate-100 text-slate-600'
                }`}>
                  {dock.status}
                </span>

                <span className="text-slate-500 font-mono text-[11px]">
                  {dock.progress || (dock.eta_minutes ? `${dock.eta_minutes} min` : 'Available')}
                </span>

                <ArrowRight className="w-3.5 h-3.5 text-slate-300" />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
