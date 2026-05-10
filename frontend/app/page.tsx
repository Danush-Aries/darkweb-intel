import React from 'react';
import LeadGenerationDashboard from '@/src/components/LeadGenerationDashboard';

export default function Home() {
  return (
    <main className="p-8 bg-slate-900 text-white min-h-screen">
      <h1 className="text-4xl font-bold mb-8">RevenueForge AI - Lead Generation Engine</h1>
      <LeadGenerationDashboard />
    </main>
  );
}
