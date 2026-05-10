import React, { useState, useEffect } from 'react';
import { monetizationService } from '@/src/lib/monetizationService';
import { Subscription } from '@/src/types/monetization-types';

export default function SubscriptionManagement() {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        setLoading(true);
        // Note: We'll need to add this endpoint to our backend
        // For now, we'll simulate with empty array or mock data
        setSubscriptions([]); // Placeholder
      } catch (err) {
        setError('Failed to load subscriptions');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchSubscriptions();
  }, []);

  if (loading) return <div className="text-center py-8">Loading subscriptions...</div>;
  if (error) return <div className="text-center text-red-500 py-8">{error}</div>;

  return (
    <div className="space-y-6">
      {subscriptions.length === 0 ? (
        <>
          <p className="text-center text-gray-500">No active subscriptions.</p>
          <div className="text-center mt-6">
            <button
              onClick={() => alert('Subscription creation functionality would be implemented here')}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
            >
              Create Subscription Plan
            </button>
          </div>
        </>
      ) : (
        <div className="space-y-4">
          {subscriptions.map((sub) => (
            <div key={sub.id} className="bg-slate-800 rounded-lg p-6">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="text-xl font-semibold mb-2">{sub.product_id} /* Product name would come from relation */</h3>
                  <p className="text-gray-400 mb-2">Customer: {sub.customer_email}</p>
                  <p className="text-gray-400">Amount: {sub.amount} {sub.currency}/{sub.billing_interval || 'month'}</p>
                </div>
                <div className="text-right">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    sub.status === 1 ? 'bg-green-100 text-green-800' : // Active
                    sub.status === 2 ? 'bg-red-100 text-red-800' : // Canceled
                    sub.status === 3 ? 'bg-yellow-100 text-yellow-800' : // Past Due
                    sub.status === 4 ? 'bg-red-100 text-red-800' : // Unpaid
                    'bg-blue-100 text-blue-800' // Trialing or other
                  }`}>
                    {sub.status === 1 ? 'Active' : 
                     sub.status === 2 ? 'Canceled' : 
                     sub.status === 3 ? 'Past Due' : 
                     sub.status === 4 ? 'Unpaid' : 
                     'Trialing'}
                  </span>
                </div>
              </div>
              <div className="mt-4">
                <button
                  onClick={() => alert('Manage subscription functionality')}
                  className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
                >
                  Manage
                </button>
                <button
                  onClick={() => alert('Cancel subscription')}
                  className="ml-2 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
                >
                  Cancel
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}