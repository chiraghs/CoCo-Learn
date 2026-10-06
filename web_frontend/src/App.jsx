import React, { useState, useEffect } from 'react';
import TopNavHeader from './components/TopNavHeader';
import KpiRibbon from './components/KpiRibbon';
import DigitalTwinCanvas from './components/DigitalTwinCanvas';
import DepotDetailsCard from './components/DepotDetailsCard';
import ShipmentStepper from './components/ShipmentStepper';
import DockStatusPanel from './components/DockStatusPanel';
import PlantOnboardingModal from './components/PlantOnboardingModal';
import RulesConfigModal from './components/RulesConfigModal';
import CortexChatDrawer from './components/CortexChatDrawer';
import { Sparkles } from 'lucide-react';

export default function App() {
  const [facilities, setFacilities] = useState([]);
  const [activeFacilityId, setActiveFacilityId] = useState("WH_RIVERSIDE_01");
  const [inventory, setInventory] = useState([]);
  const [docks, setDocks] = useState([]);
  const [shipmentData, setShipmentData] = useState(null);
  const [rules, setRules] = useState([]);

  // Modals state
  const [isOnboardOpen, setIsOnboardOpen] = useState(false);
  const [isRulesOpen, setIsRulesOpen] = useState(false);
  const [isCortexOpen, setIsCortexOpen] = useState(false);

  // Fetch initial facilities
  useEffect(() => {
    fetch('/api/facilities')
      .then(res => res.json())
      .then(data => {
        setFacilities(data);
        if (data.length > 0) setActiveFacilityId(data[0].plant_id);
      })
      .catch(err => {
        console.error("Using offline mock fallback for facilities", err);
      });

    fetch('/api/rules')
      .then(res => res.json())
      .then(data => setRules(data))
      .catch(e => console.error(e));
  }, []);

  // Fetch telemetry when active facility changes
  useEffect(() => {
    if (!activeFacilityId) return;

    fetch(`/api/facilities/${activeFacilityId}/inventory`)
      .then(res => res.json())
      .then(data => setInventory(data))
      .catch(e => console.error(e));

    fetch(`/api/facilities/${activeFacilityId}/docks`)
      .then(res => res.json())
      .then(data => setDocks(data))
      .catch(e => console.error(e));

    fetch(`/api/facilities/${activeFacilityId}/shipment-tracker`)
      .then(res => res.json())
      .then(data => setShipmentData(data))
      .catch(e => console.error(e));
  }, [activeFacilityId]);

  const activeFacility = facilities.find(f => f.plant_id === activeFacilityId) || facilities[0];

  const handleFacilityCreated = (newFacility) => {
    setFacilities(prev => [...prev, newFacility]);
    setActiveFacilityId(newFacility.plant_id);
  };

  const handleUpdateRule = async (ruleId, params) => {
    try {
      const res = await fetch(`/api/rules/${ruleId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parameters: params })
      });
      if (res.ok) {
        // Refresh inventory
        const invRes = await fetch(`/api/facilities/${activeFacilityId}/inventory`);
        if (invRes.ok) setInventory(await invRes.json());
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleRerouteExecuted = async () => {
    try {
      await fetch('/api/cortex/action/reroute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plant_id: "PLANT_02",
          part_id: "PART_BAT_402",
          po_id: "PO_APEX_9011",
          target_supplier_id: "SUPP-003"
        })
      });
      // Refresh inventory & facility state
      const invRes = await fetch(`/api/facilities/${activeFacilityId}/inventory`);
      if (invRes.ok) setInventory(await invRes.json());
      const facRes = await fetch(`/api/facilities/${activeFacilityId}`);
      if (facRes.ok) {
        const updated = await facRes.json();
        setFacilities(prev => prev.map(f => f.plant_id === updated.plant_id ? updated : f));
      }
      alert("🎉 Emergency PO Dispatched to Shenzhen EnerTech via MCP! Austin DOI restored to 14.2 Days.");
      setIsCortexOpen(false);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans text-slate-800">
      {/* Top Bar Header */}
      <TopNavHeader
        facilities={facilities}
        activeFacilityId={activeFacilityId}
        onSelectFacility={setActiveFacilityId}
        onOpenOnboard={() => setIsOnboardOpen(true)}
        onOpenRules={() => setIsRulesOpen(true)}
      />

      {/* Main Container */}
      <main className="flex-1 flex flex-col max-w-[1600px] w-full mx-auto px-4 pb-6">
        {/* Top 3 KPI Ribbon */}
        <KpiRibbon facility={activeFacility} />

        {/* Center Grid: Digital Twin (Left 70%) & Depot Details (Right 30%) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 px-6 items-start">
          <div className="lg:col-span-8 flex flex-col">
            <DigitalTwinCanvas
              facility={activeFacility}
              docks={docks}
              onPinClick={(pinType) => {
                if (pinType === 'truck') setIsCortexOpen(true);
                else alert(`Clicked Spatial Pin: ${pinType.toUpperCase()}`);
              }}
            />
            {/* Shipment Stepper (Bottom Left of Canvas) */}
            <ShipmentStepper shipmentData={shipmentData} />
          </div>

          <div className="lg:col-span-4 flex flex-col gap-5 pt-4">
            {/* Depot Details Card (Top Right) */}
            <DepotDetailsCard
              facility={activeFacility}
              inventory={inventory}
              onReorderSku={() => setIsCortexOpen(true)}
            />
            {/* Dock Status Panel (Bottom Right) */}
            <DockStatusPanel
              docks={docks}
              plantName={activeFacility?.plant_name}
            />
          </div>
        </div>
      </main>

      {/* Floating Action Button for Cortex AI Copilot */}
      <button
        onClick={() => setIsCortexOpen(true)}
        className="fixed bottom-6 right-6 px-4 py-3 bg-gradient-to-tr from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-extrabold text-xs rounded-full shadow-2xl flex items-center gap-2 z-40 transition-transform hover:scale-105"
      >
        <Sparkles className="w-4 h-4" />
        <span>Ask Cortex Copilot</span>
      </button>

      {/* Modals & Drawers */}
      <PlantOnboardingModal
        isOpen={isOnboardOpen}
        onClose={() => setIsOnboardOpen(false)}
        onCreated={handleFacilityCreated}
      />

      <RulesConfigModal
        isOpen={isRulesOpen}
        onClose={() => setIsRulesOpen(false)}
        rules={rules}
        onUpdateRule={handleUpdateRule}
      />

      <CortexChatDrawer
        facility={activeFacility}
        isOpen={isCortexOpen}
        onClose={() => setIsCortexOpen(false)}
        onRerouteTrigger={handleRerouteExecuted}
      />
    </div>
  );
}
