import React from 'react';
import ProductList from '@/src/components/monetization/ProductList';
import SubscriptionManagement from '@/src/components/monetization/SubscriptionManagement';
import AffiliateDashboard from '@/src/components/monetization/AffiliateDashboard';
import RevenueAnalytics from '@/src/components/monetization/RevenueAnalytics';

export default function MonetizationDashboard() {
  return (
    <main className="p-8 bg-slate-900 text-white min-h-screen">
      <h1 className="text-4xl font-bold mb-8">RevenueForge AI - Monetization Dashboard</h1>
      <div className="grid gap-6 md:grid-cols-2">
        <section>
          <h2 className="text-2xl font-semibold mb-4">Products for Sale</h2>
          <ProductList />
        </section>
        <section>
          <h2 className="text-2xl font-semibold mb-4">Subscription Management</h2>
          <SubscriptionManagement />
        </section>
      </div>
      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <section>
          <h2 className="text-2xl font-semibold mb-4">Affiliate & Referral Program</h2>
          <AffiliateDashboard />
        </section>
        <section>
          <h2 className="text-2xl font-semibold mb-4">Revenue Analytics</h2>
          <RevenueAnalytics />
        </section>
      </div>
    </main>
  );
}