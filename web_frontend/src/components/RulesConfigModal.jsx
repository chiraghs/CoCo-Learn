import React, { useState } from 'react';
import { X, Sliders, ShieldAlert, CheckCircle, RefreshCw } from 'lucide-react';

export default function RulesConfigModal({ isOpen, onClose, rules, onUpdateRule }) {
  const [criticalDoi, setCriticalDoi] = useState(5.0);
  const [warningDoi, setWarningDoi] = useState(10.0);
  const [minOtif, setMinOtif] = useState(85.0);
  const [isSimulating, setIsSimulating] = useState(false);
  const [simResult, setSimResult] = useState(null);

  if (!isOpen) return null;

  const handleSimulate = async () => {
    setIsSimulating(true);
    try {
      const res = await fetch('/api/rules/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ critical_doi: criticalDoi, warning_doi: warningDoi })
      });
      if (res.ok) {
        const data = await res.json();
        setSimResult(data);
      }
    } catch (e) {
      setSimResult({ critical_skus: 1, warning_skus: 2, affected_facilities_count: 2 });
    } finally {
      setIsSimulating(false);
    }
  };

  const handleApply = async () => {
    await onUpdateRule("RULE_DOI_GLOBAL", {
      critical_doi: criticalDoi,
      warning_doi: warningDoi
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-5">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
              <Sliders className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-extrabold text-slate-900 text-base">Configurable Rules Engine</h3>
              <p className="text-xs text-slate-500">Live Declarative Threshold Tuning</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 p-1 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex flex-col gap-5 text-xs">
          {/* Slider 1: Critical DOI */}
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            <div className="flex items-center justify-between mb-2">
              <label className="font-bold text-slate-800">Critical Stockout DOI Threshold</label>
              <span className="font-black text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                {criticalDoi} Days
              </span>
            </div>
            <input
              type="range"
              min="1"
              max="15"
              step="0.5"
              value={criticalDoi}
              onChange={e => setCriticalDoi(parseFloat(e.target.value))}
              className="w-full accent-rose-600 cursor-pointer"
            />
            <span className="text-[10px] text-slate-400 block mt-1">Triggers emergency assembly halt alerts when inventory runway falls below this buffer.</span>
          </div>

          {/* Slider 2: Warning DOI */}
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            <div className="flex items-center justify-between mb-2">
              <label className="font-bold text-slate-800">Warning Stockout DOI Threshold</label>
              <span className="font-black text-amber-600 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                {warningDoi} Days
              </span>
            </div>
            <input
              type="range"
              min="5"
              max="30"
              step="1"
              value={warningDoi}
              onChange={e => setWarningDoi(parseFloat(e.target.value))}
              className="w-full accent-amber-600 cursor-pointer"
            />
            <span className="text-[10px] text-slate-400 block mt-1">Classifies SKU inventory as 'Low Stock' in facility drawers.</span>
          </div>

          {/* Simulation Preview Card */}
          {simResult && (
            <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl text-blue-900">
              <span className="font-bold block mb-1">Impact Simulation Preview:</span>
              <div className="grid grid-cols-3 gap-2 text-center pt-1 font-mono text-[11px]">
                <div><span className="font-bold text-rose-600">{simResult.critical_skus}</span> Critical</div>
                <div><span className="font-bold text-amber-600">{simResult.warning_skus}</span> Low Stock</div>
                <div><span className="font-bold text-slate-800">{simResult.affected_facilities_count}</span> Facilities</div>
              </div>
            </div>
          )}

          <div className="flex items-center justify-between pt-2">
            <button
              onClick={handleSimulate}
              disabled={isSimulating}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg border border-slate-300 transition-colors"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSimulating ? 'animate-spin' : ''}`} />
              <span>Simulate Impact</span>
            </button>

            <div className="flex gap-2">
              <button onClick={onClose} className="px-4 py-2 border border-slate-200 rounded-lg font-semibold text-slate-600">
                Cancel
              </button>
              <button onClick={handleApply} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold shadow-md shadow-blue-500/20">
                Apply Thresholds
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
