import React, { useState } from 'react';
import { MapPin, Navigation, Eye, CheckCircle2, AlertTriangle, Truck } from 'lucide-react';

export default function DigitalTwinCanvas({ facility, docks, onPinClick }) {
  const [selectedPin, setSelectedPin] = useState(null);

  if (!facility) return null;

  return (
    <div className="relative w-full h-[580px] bg-gradient-to-b from-sky-50 via-slate-100 to-slate-200 rounded-2xl overflow-hidden border border-slate-200 shadow-inner my-4 flex items-center justify-center">
      {/* Zoom / Canvas Controls (Floating Right) */}
      <div className="absolute right-4 top-4 bg-white/95 backdrop-blur-md rounded-xl p-1.5 shadow-md border border-slate-200 flex flex-col gap-1 z-20">
        <button className="w-8 h-8 rounded-lg hover:bg-slate-100 text-slate-700 font-bold flex items-center justify-center text-sm">+</button>
        <button className="w-8 h-8 rounded-lg hover:bg-slate-100 text-slate-700 font-bold flex items-center justify-center text-sm">-</button>
        <div className="h-px bg-slate-200 my-0.5"></div>
        <button className="w-8 h-8 rounded-lg hover:bg-slate-100 text-slate-600 flex items-center justify-center text-xs">⟳</button>
        <button className="w-8 h-8 rounded-lg hover:bg-slate-100 text-slate-600 flex items-center justify-center text-xs">🖵</button>
      </div>

      {/* Modern SVG Isometric Canvas Rendering Facility */}
      <svg
        viewBox="0 0 1100 620"
        className="w-full h-full object-contain filter drop-shadow-sm"
      >
        <defs>
          <linearGradient id="groundGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#f1f5f9" />
            <stop offset="100%" stopColor="#e2e8f0" />
          </linearGradient>
          <linearGradient id="roofBlue" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#2563eb" />
            <stop offset="100%" stopColor="#1d4ed8" />
          </linearGradient>
          <linearGradient id="wallBlue" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#1e40af" />
            <stop offset="100%" stopColor="#1e3a8a" />
          </linearGradient>
          <linearGradient id="containerGreen" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#0d9488" />
            <stop offset="100%" stopColor="#0f766e" />
          </linearGradient>
          <linearGradient id="palletWood" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#d97706" />
            <stop offset="100%" stopColor="#b45309" />
          </linearGradient>
        </defs>

        {/* 1. Ground Surface Grid Lines */}
        <polygon points="550,20 1080,310 550,600 20,310" fill="url(#groundGrad)" stroke="#cbd5e1" strokeWidth="1" />
        <line x1="550" y1="20" x2="550" y2="600" stroke="#e2e8f0" strokeDasharray="4 4" />
        <line x1="20" y1="310" x2="1080" y2="310" stroke="#e2e8f0" strokeDasharray="4 4" />

        {/* 2. Trees in Background Yard */}
        <g transform="translate(680, 110)">
          <circle cx="0" cy="0" r="16" fill="#86efac" />
          <circle cx="-1" cy="-2" r="13" fill="#4ade80" />
          <rect x="-2" y="12" width="4" height="10" fill="#78350f" />
        </g>
        <g transform="translate(730, 140)">
          <circle cx="0" cy="0" r="15" fill="#86efac" />
          <circle cx="-1" cy="-2" r="12" fill="#4ade80" />
          <rect x="-2" y="11" width="4" height="9" fill="#78350f" />
        </g>

        {/* 3. Left Green Shipping Container Yard */}
        <g transform="translate(40, 290)">
          <polygon points="0,40 100,-15 130,2 30,57" fill="#0f766e" />
          <polygon points="0,40 30,57 30,105 0,88" fill="#115e59" />
          <polygon points="30,57 130,2 130,50 30,105" fill="url(#containerGreen)" />
          <text x="45" y="75" fill="#ffffff" fontSize="9" fontWeight="bold" opacity="0.8" transform="rotate(-15, 45, 75)">EVERGREEN LINE</text>
        </g>

        {/* 4. Yellow Forklifts in Yard */}
        <g transform="translate(100, 220)">
          {/* Forklift Body */}
          <rect x="0" y="0" width="36" height="24" rx="4" fill="#eab308" />
          <rect x="24" y="4" width="10" height="16" rx="2" fill="#3b82f6" />
          <circle cx="8" cy="24" r="6" fill="#1e293b" />
          <circle cx="28" cy="24" r="6" fill="#1e293b" />
          <rect x="36" y="-6" width="3" height="30" fill="#64748b" />
          <rect x="39" y="14" width="12" height="3" fill="#94a3b8" />
        </g>

        {/* 5. Central Primary Facility Warehouse Building */}
        <g id="warehouse-structure">
          {/* Main Hall Walls */}
          <polygon points="260,260 520,130 520,310 260,440" fill="url(#wallBlue)" stroke="#1e3a8a" strokeWidth="1.5" />
          <polygon points="520,130 740,240 740,410 520,310" fill="#1d4ed8" stroke="#1e3a8a" strokeWidth="1.5" />

          {/* Roof Structure */}
          <polygon points="250,250 515,115 745,230 480,365" fill="url(#roofBlue)" stroke="#1e40af" strokeWidth="2" />
          
          {/* Center Facility Circular Logo on Roof */}
          <ellipse cx="500" cy="235" rx="30" ry="16" fill="#ffffff" opacity="0.9" />
          <ellipse cx="500" cy="235" rx="24" ry="12" fill="#1d4ed8" />
          <text x="490" y="239" fill="#ffffff" fontSize="10" fontWeight="bold">WH-01</text>

          {/* Bay 1 Open Loading Dock Door */}
          <polygon points="360,385 410,360 410,410 360,435" fill="#0f172a" stroke="#60a5fa" strokeWidth="1.5" />
          <rect x="372" y="380" width="24" height="20" fill="#38bdf8" opacity="0.3" />

          {/* Bay 2 Open Loading Dock Door */}
          <polygon points="430,350 480,325 480,375 430,400" fill="#0f172a" stroke="#60a5fa" strokeWidth="1.5" />
        </g>

        {/* 6. High Staged Pallet Racks on Right */}
        <g transform="translate(620, 200)">
          {/* Metal Racks */}
          <line x1="0" y1="0" x2="0" y2="120" stroke="#0284c7" strokeWidth="3" />
          <line x1="60" y1="30" x2="60" y2="150" stroke="#0284c7" strokeWidth="3" />
          <line x1="0" y1="40" x2="60" y2="70" stroke="#38bdf8" strokeWidth="2" />
          <line x1="0" y1="80" x2="60" y2="110" stroke="#38bdf8" strokeWidth="2" />

          {/* Wooden Pallets on Racks */}
          <rect x="5" y="20" width="22" height="16" fill="url(#palletWood)" rx="2" />
          <rect x="30" y="32" width="22" height="16" fill="url(#palletWood)" rx="2" />
          <rect x="5" y="60" width="22" height="16" fill="url(#palletWood)" rx="2" />
          <rect x="30" y="72" width="22" height="16" fill="url(#palletWood)" rx="2" />
        </g>

        {/* 7. Pallet Stacks on Forecourt */}
        <g transform="translate(140, 310)">
          <rect x="0" y="0" width="24" height="18" fill="url(#palletWood)" rx="2" stroke="#78350f" strokeWidth="0.5" />
          <rect x="26" y="0" width="24" height="18" fill="url(#palletWood)" rx="2" stroke="#78350f" strokeWidth="0.5" />
          <rect x="13" y="-18" width="24" height="18" fill="url(#palletWood)" rx="2" stroke="#78350f" strokeWidth="0.5" />
        </g>

        {/* 8. White Delivery Trucks */}
        {/* Truck 1: WareTrack Delivery Truck at Bay 1 */}
        <g transform="translate(240, 420)">
          {/* Cab */}
          <polygon points="0,40 50,20 50,70 0,90" fill="#2563eb" />
          <polygon points="50,20 100,45 100,95 50,70" fill="#1d4ed8" />
          <polygon points="0,40 50,20 30,10 -20,30" fill="#3b82f6" />
          {/* Box Body */}
          <polygon points="55,20 200,-50 200,20 55,90" fill="#ffffff" stroke="#cbd5e1" />
          <polygon points="55,-10 200,-80 230,-65 85,5" fill="#f8fafc" stroke="#cbd5e1" />
          <polygon points="200,-50 230,-35 230,35 200,20" fill="#f1f5f9" stroke="#cbd5e1" />
          {/* Wheels */}
          <circle cx="20" cy="85" r="9" fill="#1e293b" />
          <circle cx="150" cy="40" r="9" fill="#1e293b" />
          <circle cx="175" cy="30" r="9" fill="#1e293b" />
          {/* Snowflake Brand on Truck */}
          <text x="80" y="15" fill="#0284c7" fontSize="11" fontWeight="bold" transform="rotate(-25, 80, 15)">Snowflake</text>
        </g>

        {/* Truck 2: Inbound Bluepeak Truck */}
        <g transform="translate(520, 500)">
          <rect x="0" y="0" width="130" height="48" rx="4" fill="#ffffff" stroke="#cbd5e1" />
          <rect x="130" y="10" width="35" height="38" rx="4" fill="#10b981" />
          <circle cx="30" cy="50" r="8" fill="#1e293b" />
          <circle cx="110" cy="50" r="8" fill="#1e293b" />
          <circle cx="145" cy="50" r="8" fill="#1e293b" />
          <text x="25" y="28" fill="#047857" fontSize="11" fontWeight="bold">Bluepeak</text>
        </g>

        {/* 9. Interactive Spatial Telemetry Pins (Matching Reference 📍) */}
        {/* Pin 1: Bay 1 Active Pallet Pin */}
        <g
          transform="translate(480, 390)"
          className="cursor-pointer group"
          onClick={() => onPinClick("bay1")}
        >
          <circle cx="0" cy="0" r="14" fill="#2563eb" opacity="0.3" className="animate-ping" />
          <circle cx="0" cy="0" r="12" fill="#2563eb" />
          <MapPin x="-7" y="-7" className="w-3.5 h-3.5 text-white" />
        </g>

        {/* Pin 2: Yard Pallet Staging Pin */}
        <g
          transform="translate(730, 340)"
          className="cursor-pointer group"
          onClick={() => onPinClick("pallets")}
        >
          <circle cx="0" cy="0" r="14" fill="#2563eb" opacity="0.3" className="animate-ping" />
          <circle cx="0" cy="0" r="12" fill="#2563eb" />
          <MapPin x="-7" y="-7" className="w-3.5 h-3.5 text-white" />
        </g>

        {/* Pin 3: Loading Inbound Truck Pin */}
        <g
          transform="translate(230, 380)"
          className="cursor-pointer group"
          onClick={() => onPinClick("truck")}
        >
          <circle cx="0" cy="0" r="14" fill="#059669" opacity="0.3" className="animate-ping" />
          <circle cx="0" cy="0" r="12" fill="#059669" />
          <Truck x="-7" y="-7" className="w-3.5 h-3.5 text-white" />
        </g>
      </svg>

      {/* Floating Info Badge for Active Facility */}
      <div className="absolute left-6 top-6 bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-xl p-3 shadow-md flex items-center gap-3">
        <span className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
        <div>
          <div className="text-xs font-bold text-slate-900">{facility.plant_name} Digital Twin</div>
          <div className="text-[11px] text-slate-500 font-medium">{facility.location} • Real-time telemetry</div>
        </div>
      </div>
    </div>
  );
}
