import React from 'react';
import { Plus, CheckCircle, AlertCircle, BatteryCharging } from 'lucide-react';

export default function DepotDetailsCard({ facility, inventory, onReorderSku }) {
  if (!facility) return null;

  return (
    <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-5 shadow-sm flex flex-col gap-5 w-full">
      {/* Header & Depot ID */}
      <div className="flex items-start justify-between">
        <div>
          <div className="text-[10px] font-bold text-slate-400 tracking-wider uppercase">DEPOT • {facility.plant_id.slice(-5)}</div>
          <h3 className="text-xl font-black text-slate-900 tracking-tight">{facility.plant_name}</h3>
          <p className="text-xs text-slate-500 font-medium">{facility.location}</p>
        </div>
        <button className="w-8 h-8 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center transition-colors">
          <Plus className="w-4 h-4" />
        </button>
      </div>

      {/* Operational Badge and Summary Stats */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className={`px-2.5 py-1 rounded-md text-xs font-bold ${
          facility.overall_status === 'Critical' ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
        }`}>
          {facility.overall_status}
        </span>
        <span className="text-xs text-slate-500 font-medium">
          1 docked • 1 arriving • 3 staged
        </span>
      </div>

      {/* Capacity Utilization Progress Bars */}
      <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-100">
        <div>
          <div className="text-[11px] font-bold text-slate-500 mb-1">Stock on hand</div>
          <div className="text-base font-extrabold text-slate-900 mb-1.5">
            {facility.stock_on_hand.toLocaleString()} <span className="text-xs font-medium text-slate-400">/ {facility.total_capacity_units.toLocaleString()}</span>
          </div>
          <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full ${facility.capacity_full_pct > 80 ? 'bg-amber-500' : 'bg-blue-600'}`}
              style={{ width: `${Math.min(100, facility.capacity_full_pct)}%` }}
            ></div>
          </div>
        </div>

        <div>
          <div className="text-[11px] font-bold text-slate-500 mb-1">Truck bays</div>
          <div className="text-base font-extrabold text-slate-900 mb-1.5">
            {facility.busy_dock_bays} / {facility.total_dock_bays} <span className="text-xs font-medium text-slate-400">busy</span>
          </div>
          <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-emerald-500 rounded-full"
              style={{ width: `${(facility.busy_dock_bays / facility.total_dock_bays) * 100}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Daily Metrics */}
      <div className="grid grid-cols-2 gap-4 text-xs pt-1">
        <div>
          <span className="text-slate-400 block text-[10px] uppercase font-bold">Outbound today</span>
          <span className="font-extrabold text-slate-800 text-sm">23 <span className="text-xs font-normal text-slate-500">trucks</span></span>
        </div>
        <div>
          <span className="text-slate-400 block text-[10px] uppercase font-bold">Put-aways today</span>
          <span className="font-extrabold text-slate-800 text-sm">15 <span className="text-xs font-normal text-slate-500">pallets</span></span>
        </div>
      </div>

      {/* Inventory SKU List */}
      <div className="pt-2 border-t border-slate-100">
        <div className="flex items-center justify-between text-xs font-bold text-slate-500 uppercase tracking-wide mb-2.5">
          <span>Inventory</span>
          <span>Units</span>
        </div>

        <div className="flex flex-col gap-2.5 max-h-48 overflow-y-auto pr-1">
          {inventory.map((item) => (
            <div key={item.part_id} className="flex items-center justify-between text-xs py-1 hover:bg-slate-50 rounded px-1.5 transition-colors">
              <div className="flex items-center gap-2">
                <span className="text-base">
                  {item.category === 'Packaging' ? '📦' : item.category === 'Powertrain' ? '🔋' : item.category === 'Safety Gear' ? '🪖' : '🧰'}
                </span>
                <span className="font-semibold text-slate-800">{item.part_name}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-slate-700">{item.on_hand_qty.toLocaleString()}</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold ${
                  item.status === 'Critical Stockout' ? 'bg-rose-100 text-rose-700' :
                  item.status === 'Low Stock' ? 'bg-amber-100 text-amber-800' :
                  'bg-emerald-100 text-emerald-800'
                }`}>
                  {item.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Forklift Fleet Status */}
      <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
        <div>
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Forklift fleet</div>
          <div className="font-semibold text-slate-800">{facility.forklift_status || "FL-01 Loading TRK-2051 at Bay 1"}</div>
        </div>
        <div className="text-right">
          <span className="text-[10px] text-slate-400 block font-bold">{facility.forklift_fleet_active || "1/2 working"}</span>
          <span className="text-xs font-extrabold text-emerald-600">75% battery</span>
        </div>
      </div>
    </div>
  );
}
