import React, { useState, useEffect } from 'react';
import { monetizationService } from '@/src/lib/monetizationService';
import { Affiliate, Referral } from '@/src/types/monetization-types';

export default function AffiliateDashboard() {
  const [affiliates, setAffiliates] = useState<Affiliate[]>([]);
  const [referrals, setReferrals] = useState<Referral[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Fetch affiliates
        const affiliatesData = await monetizationService.getAffiliates?.() || [];
        setAffiliates(affiliatesData);
        
        // Fetch referrals (we'd need to add this endpoint)
        const referralsData = await monetizationService.getReferrals?.() || [];
        setReferrals(referralsData);
      } catch (err) {
        setError('Failed to load affiliate data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="text-center py-8">Loading affiliate data...</div>;
  if (error) return <div className="text-center text-red-500 py-8">{error}</div>;

  const totalAffiliates = affiliates.length;
  const activeAffiliates = affiliates.filter(a => a.is_active).length;
  const totalReferrals = referrals.length;
  const totalCommission = referrals.reduce((sum, r) => sum + r.commission_earned, 0);

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="text-2xl font-bold">{totalAffiliates}</div>
          <div className="text-sm text-gray-600">Total Affiliates</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <div className="text-2xl font-bold">{activeAffiliates}</div>
          <div className="text-sm text-gray-600">Active Affiliates</div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-4">
          <div className="text-2xl font-bold">{totalReferrals}</div>
          <div className="text-sm text-gray-600">Total Referrals</div>
        </div>
        <div className="bg-purple-50 rounded-lg p-4">
          <div className="text-2xl font-bold">${totalCommission.toFixed(2)}</div>
          <div className="text-sm text-gray-600">Total Commission Earned</div>
        </div>
      </div>
      
      {/* Affiliate Management */}
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Affiliate Management</h2>
        <div className="space-y-4">
          {affiliates.length === 0 ? (
            <p className="text-center text-gray-500">No affiliates registered yet.</p>
          ) : (
            <div className="space-y-3">
              {affiliates.map((affiliate) => (
                <div key={affiliate.id} className="flex justify-between items-center bg-slate-700 p-4 rounded">
                  <div>
                    <h3 className="font-semibold">{affiliate.name}</h3>
                    <p className="text-sm text-gray-400">{affiliate.email}</p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      affiliate.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {affiliate.is_active ? 'Active' : 'Inactive'}
                    </span>
                    <span className="text-sm text-gray-400">{affiliate.commission_rate}% commission</span>
                  </div>
                </div>
              ))}
            </div>
          )}
          <div className="mt-4">
            <button
              onClick={() => alert('Add affiliate functionality would be implemented here')}
              className="w-full px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
            >
              Add New Affiliate
            </button>
          </div>
        </div>
      </div>
      
      {/* Recent Referrals */}
      <div className="bg-slate-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Referrals</h2>
        {referrals.length === 0 ? (
          <p className="text-center text-gray-500">No referrals tracked yet.</p>
        ) : (
          <div className="space-y-3">
            {referrals.slice(0, 5).map((referral) => (
              <div key={referral.id} className="flex justify-between items-start bg-slate-700 p-4 rounded">
                <div>
                  <h3 className="font-semibold">Referral to {referral.referred_email}</h3>
                  <p className="text-sm text-gray-400">
                    Affiliate: {referrals.find(r => r.id === referral.affiliate_id)?.name || 'Unknown'}
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-xl font-bold text-green-400">
                    ${referral.commission_earned.toFixed(2)}
                  </span>
                  <p className="text-xs text-gray-400">Commission</p>
                </div>
              </div>
            ))}
          </div>
        )}
        <div className="mt-4 text-right">
          <button
            onClick={() => alert('Track referral functionality')}
            className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
          >
            Track New Referral
          </button>
        </div>
      </div>
    </div>
  );
}