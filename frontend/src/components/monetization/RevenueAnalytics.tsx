import React, { useState, useEffect } from 'react';
import { monetizationService } from '@/src/lib/monetizationService';
import { RevenueAnalytics } from '@/src/types/monetization-types';

export default function RevenueAnalytics() {
  const [analytics, setAnalytics] = useState<RevenueAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        // Note: We'll need to add this endpoint to our backend
        // For now, we'll simulate with mock data or empty
        const mockData: RevenueAnalytics = {
          total_revenue: 12500.00,
          total_orders: 45,
          total_subscriptions: 12,
          total_affiliates: 8,
          revenue_by_product: [
            { product_name: 'DarkWeb Intelligence Course', revenue: 5000.00 },
            { product_name: 'Premium SaaS Subscription', revenue: 4500.00 },
            { product_name: 'Advanced Threat Intelligence Ebook', revenue: 2000.00 },
            { product_name: 'Enterprise Membership', revenue: 1000.00 }
          ],
          monthly_revenue: [
            { month: 'Jan', revenue: 800.00 },
            { month: 'Feb', revenue: 950.00 },
            { month: 'Mar', revenue: 1100.00 },
            { month: 'Apr', revenue: 1200.00 },
            { month: 'May', revenue: 1300.00 },
            { month: 'Jun', revenue: 1400.00 }
          ]
        };
        setAnalytics(mockData);
      } catch (err) {
        setError('Failed to load analytics');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) return <div className="text-center py-8">Loading analytics...</div>;
  if (error) return <div className="text-center text-red-500 py-8">{error}</div>;
  if (!analytics) return <div className="text-center py-8">No analytics data available.</div>;

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-blue-600">${analytics.total_revenue.toFixed(2)}</div>
          <div className="text-sm text-gray-600">Total Revenue</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-green-600">{analytics.total_orders}</div>
          <div className="text-sm text-gray-600">Total Orders</div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-yellow-600">{analytics.total_subscriptions}</div>
          <div className="text-sm text-gray-600">Active Subscriptions</div>
        </div>
        <div className="bg-purple-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-purple-600">{analytics.total_affiliates}</div>
          <div className="text-sm text-gray-600">Total Affiliates</div>
        </div>
      </div>
      
      {/* Revenue by Product */}
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Revenue by Product</h2>
        {analytics.revenue_by_product.length === 0 ? (
          <p className="text-center text-gray-500">No product revenue data.</p>
        ) : (
          <div className="space-y-3">
            {analytics.revenue_by_product.map((item) => (
              <div key={item.product_name} className="flex justify-between items-center bg-slate-700 p-4 rounded">
                <div>
                  <h3 className="font-semibold">{item.product_name}</h3>
                </div>
                <div className="text-right">
                  <span className="text-xl font-bold text-green-400">
                    ${item.revenue.toFixed(2)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Monthly Revenue Trend */}
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Monthly Revenue Trend</h2>
        {analytics.monthly_revenue.length === 0 ? (
          <p className="text-center text-gray-500">No monthly revenue data.</p>
        ) : (
          <div className="space-y-3">
            {analytics.monthly_revenue.map((item) => (
              <div key={item.month} className="flex justify-between items-center bg-slate-700 p-4 rounded">
                <div>
                  <h3 className="font-semibold">{item.month}</h3>
                </div>
                <div className="text-right">
                  <span className="text-xl font-bold text-blue-400">
                    ${item.revenue.toFixed(2)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}