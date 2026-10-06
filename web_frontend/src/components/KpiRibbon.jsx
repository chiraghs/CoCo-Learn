import React from 'react';
import { Package, Truck, Clock, ArrowUpRight } from 'lucide-react';

export default function KpiRibbon({ facility }) {
  if (!facility) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 px-6 pt-4">
      {/* Card 1: Stock on hand */}
      <div className="bg-white/90 backdrop-blur-md border border-slate-200/80 rounded-xl p-3.5 shadow-sm hover:shadow-md transition-shadow flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-lg">
            <Package className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">Stock on hand</div>
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-black text-slate-900 leading-tight">
                {facility.stock_on_hand.toLocaleString()}
              </span>
              <span className="text-xs font-bold text-emerald-600 flex items-center">
                +15
              </span>
            </div>
            <div className="text-[10px] text-slate-400 font-medium">pallets • {facility.plant_id.slice(-5)}</div>
          </div>
        </div>
      </div>

      {/* Card 2: Trucks on site */}
      <div className="bg-white/90 backdrop-blur-md border border-slate-200/80 rounded-xl p-3.5 shadow-sm hover:shadow-md transition-shadow flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center font-bold text-lg">
            <Truck className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">Trucks on site</div>
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-black text-slate-900 leading-tight">
                {facility.busy_dock_bays}
              </span>
              <span className="text-xs font-bold text-emerald-600 flex items-center">
                +{facility.active_inbound_trucks}
              </span>
            </div>
            <div className="text-[10px] text-slate-400 font-medium">
              {facility.active_inbound_trucks} inbound • {facility.plant_id.slice(-5)}
            </div>
          </div>
        </div>
      </div>

      {/* Card 3: On-time delivery */}
      <div className="bg-white/90 backdrop-blur-md border border-slate-200/80 rounded-xl p-3.5 shadow-sm hover:shadow-md transition-shadow flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-lg">
            <Clock className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">On-time delivery</div>
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-black text-slate-900 leading-tight">
                {facility.on_time_delivery_pct || 96.6}%
              </span>
              <span className="text-xs font-bold text-emerald-600 flex items-center">
                +0.4%
              </span>
            </div>
            <div className="text-[10px] text-slate-400 font-medium">last 30 days • {facility.plant_id.slice(-5)}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
