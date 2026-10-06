import React from 'react';
import { Truck, Check, Clock, AlertTriangle, ArrowRight } from 'lucide-react';

export default function ShipmentStepper({ shipmentData }) {
  if (!shipmentData) return null;

  return (
    <div className="bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-5 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
      {/* Left: Stepper Progress Pipeline */}
      <div className="flex-1 w-full">
        <div className="flex items-center gap-2 mb-3">
          <Truck className="w-4 h-4 text-blue-600" />
          <span className="text-xs font-black text-slate-800 tracking-tight">Shipment Tracking</span>
          <span className="text-xs text-slate-400 font-medium ml-auto">{shipmentData.carrier_name}</span>
        </div>

        {/* 5-Step Continuous Timeline */}
        <div className="flex items-center justify-between relative">
          <div className="absolute left-6 right-6 top-3.5 h-0.5 bg-slate-200 -z-0"></div>

          {shipmentData.steps.map((step, idx) => {
            const isCompleted = step.completed;
            const isActive = step.active;
            const isAlert = step.alert;

            return (
              <div key={idx} className="flex flex-col items-center text-center relative z-10">
                <div
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all shadow-sm ${
                    isAlert
                      ? 'bg-rose-500 text-white ring-4 ring-rose-100'
                      : isCompleted
                      ? 'bg-blue-600 text-white'
                      : isActive
                      ? 'bg-white text-blue-600 border-2 border-blue-600 ring-4 ring-blue-50'
                      : 'bg-white text-slate-400 border border-slate-300'
                  }`}
                >
                  {isAlert ? '!' : isCompleted ? <Check className="w-3.5 h-3.5" /> : step.step_index}
                </div>
                <span className={`text-[11px] font-bold mt-1.5 leading-tight ${isActive || isAlert ? 'text-slate-900' : 'text-slate-500'}`}>
                  {step.label}
                </span>
                <span className="text-[10px] text-slate-400 font-medium leading-tight">
                  {step.timestamp}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Right: Active Shipment Mini Info Card */}
      <div className="bg-slate-50/80 border border-slate-200 rounded-xl p-3 min-w-[240px] flex items-center justify-between gap-3 shadow-inner">
        <div className="w-9 h-9 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center">
          <Truck className="w-5 h-5" />
        </div>
        <div>
          <div className="text-xs font-black text-slate-900">{shipmentData.shipment_id}</div>
          <div className="text-[11px] text-slate-500 font-medium">To: {shipmentData.destination}</div>
          <div className="text-[10px] font-bold text-blue-600 uppercase">{shipmentData.bay_info}</div>
        </div>
        <ArrowRight className="w-4 h-4 text-slate-400" />
      </div>
    </div>
  );
}
