import React, { useState } from 'react';
import { Sparkles, Send, CheckCircle, Database, ShieldAlert, ArrowRight } from 'lucide-react';

export default function CortexChatDrawer({ facility, isOpen, onClose, onRerouteTrigger }) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  if (!isOpen) return null;

  const handleAsk = async (textToAsk) => {
    const q = textToAsk || query;
    if (!q) return;
    setLoading(true);
    try {
      const res = await fetch('/api/cortex/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q, plant_id: facility?.plant_id })
      });
      if (res.ok) {
        const data = await res.json();
        setResponse(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-lg bg-white shadow-2xl border-l border-slate-200 p-6 flex flex-col justify-between overflow-y-auto">
      <div>
        <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center font-bold">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-extrabold text-slate-900 text-base leading-tight">Cortex AI Supply Copilot</h3>
              <p className="text-[11px] text-slate-500 font-medium">Grounded in Staged YAML Semantic Model</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 text-sm font-bold p-1">
            ✕
          </button>
        </div>

        {/* Preset Prompt Chips */}
        <div className="flex flex-col gap-1.5 mb-4">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Suggested Enterprise Queries:</span>
          <button
            onClick={() => handleAsk("What is the stockout risk for Austin battery packs?")}
            className="text-left p-2 bg-slate-50 hover:bg-blue-50 hover:text-blue-700 rounded-lg text-xs font-semibold text-slate-700 border border-slate-200 transition-colors"
          >
            💬 "Why is Austin Gigafactory battery DOI at 3.8 days?"
          </button>
          <button
            onClick={() => handleAsk("What are the liquidated damages penalties under Section 8 of Apex contract?")}
            className="text-left p-2 bg-slate-50 hover:bg-blue-50 hover:text-blue-700 rounded-lg text-xs font-semibold text-slate-700 border border-slate-200 transition-colors"
          >
            🔍 "What are the Section 8 liquidated damages for Apex Battery?"
          </button>
        </div>

        {/* 3-Way Reconciliation Ledger Response */}
        {response && (
          <div className="flex flex-col gap-3 my-4">
            {/* 1. Natural Language Explanation */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
              <div className="text-[10px] font-black text-blue-600 uppercase tracking-wide mb-1 flex items-center gap-1">
                <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
                <span>1. Conversational Synthesis</span>
              </div>
              <p className="text-xs text-slate-800 leading-relaxed font-medium">{response.explanation}</p>
            </div>

            {/* 2. Deterministic SQL */}
            <div className="bg-slate-900 rounded-xl p-3 text-white font-mono text-[11px]">
              <div className="text-[10px] font-bold text-sky-400 uppercase tracking-wide mb-1 flex items-center gap-1">
                <Database className="w-3.5 h-3.5" />
                <span>2. Deterministic Cortex SQL</span>
              </div>
              <pre className="overflow-x-auto text-sky-200 text-[10.5px] leading-tight whitespace-pre-wrap">{response.generated_sql}</pre>
            </div>

            {/* 3. Action MCP Remediation Trigger */}
            {response.query.toLowerCase().includes("austin") && (
              <div className="bg-rose-50 border border-rose-200 rounded-xl p-3.5 flex flex-col gap-2">
                <div className="flex items-center gap-1.5 text-rose-700 font-extrabold text-xs">
                  <ShieldAlert className="w-4 h-4" />
                  <span>Action Recommendation Available</span>
                </div>
                <p className="text-[11px] text-rose-900">
                  Reroute 4,500 battery units to Shenzhen EnerTech via air freight to restore Austin DOI to 14.2 days.
                </p>
                <button
                  onClick={onRerouteTrigger}
                  className="px-3 py-1.5 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-lg shadow-sm flex items-center justify-center gap-1 mt-1"
                >
                  <span>Execute 1-Click PO Reroute via MCP</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Input Bar */}
      <div className="pt-4 border-t border-slate-100">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Ask Cortex about any plant, material, or contract..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleAsk()}
            className="flex-1 bg-slate-50 border border-slate-200 text-slate-800 text-xs rounded-xl px-3.5 py-2.5 focus:outline-none focus:border-blue-500"
          />
          <button
            onClick={() => handleAsk()}
            disabled={loading}
            className="w-10 h-10 bg-blue-600 hover:bg-blue-700 text-white rounded-xl flex items-center justify-center font-bold shadow-md shadow-blue-500/20"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
