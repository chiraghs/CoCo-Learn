import React from 'react';
import { Search, Bell, Settings, ShieldCheck, ChevronDown, PlusCircle } from 'lucide-react';

export default function TopNavHeader({ facilities, activeFacilityId, onSelectFacility, onOpenOnboard, onOpenRules }) {
  const current = facilities.find(f => f.plant_id === activeFacilityId) || facilities[0];

  return (
    <header className="bg-white border-b border-slate-200 px-6 py-3 flex items-center justify-between sticky top-0 z-30 shadow-sm">
      {/* Brand & Search */}
      <div className="flex items-center gap-6 flex-1">
        <div className="flex items-center gap-2 cursor-pointer">
          <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold shadow-md shadow-blue-500/20">
            📦
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-slate-900 text-lg tracking-tight leading-none">WareTrack</span>
            <span className="text-[10px] font-bold text-blue-600 uppercase tracking-wider">SupplyChainIQ • Aegis</span>
          </div>
        </div>

        <div className="relative max-w-md w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search sites, trucks, forklifts, pallets, shipments..."
            className="w-full bg-slate-50 border border-slate-200 text-slate-800 text-xs rounded-full pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
          />
        </div>
      </div>

      {/* Facility Switcher & Actions */}
      <div className="flex items-center gap-3">
        {/* Onboard Facility Button */}
        <button
          onClick={onOpenOnboard}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg text-xs font-semibold border border-blue-200 transition-colors"
        >
          <PlusCircle className="w-3.5 h-3.5" />
          <span>Onboard Plant</span>
        </button>

        {/* Rules Config Button */}
        <button
          onClick={onOpenRules}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-50 hover:bg-slate-100 text-slate-700 rounded-lg text-xs font-semibold border border-slate-200 transition-colors"
        >
          <Settings className="w-3.5 h-3.5 text-slate-500" />
          <span>Config Rules</span>
        </button>

        {/* Active Facility Dropdown */}
        <div className="relative">
          <select
            value={activeFacilityId}
            onChange={(e) => onSelectFacility(e.target.value)}
            className="appearance-none bg-slate-50 border border-slate-200 text-slate-800 font-semibold text-xs rounded-lg pl-3 pr-8 py-1.5 cursor-pointer hover:bg-slate-100 focus:outline-none"
          >
            {facilities.map(f => (
              <option key={f.plant_id} value={f.plant_id}>
                {f.plant_name} ({f.capacity_full_pct}% full)
              </option>
            ))}
          </select>
          <ChevronDown className="w-3.5 h-3.5 text-slate-500 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>

        {/* Live Badge */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 text-emerald-700 rounded-full border border-emerald-200 text-[11px] font-bold">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Live 09:40</span>
        </div>

        {/* User Profile */}
        <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 text-white font-bold text-xs flex items-center justify-center shadow-sm">
            AC
          </div>
          <div className="hidden lg:flex flex-col text-left">
            <span className="text-xs font-bold text-slate-800 leading-tight">Alex Chen</span>
            <span className="text-[10px] text-slate-500 leading-tight">Operations Manager</span>
          </div>
        </div>
      </div>
    </header>
  );
}
