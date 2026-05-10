'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Lead, LeadStatus, LeadSource, LeadGenerationRequest, LeadGenerationResult } from '@/types/lead-types';
import { mockLeads } from '@/lib/mock-leads';

export default function LeadGenerationDashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [generating, setGenerating] = useState<boolean>(false);
  const [filters, setFilters] = useState<{
    status: LeadStatus | '';
    source: LeadSource | '';
    minScore: number;
  }>({
    status: '',
    source: '',
    minScore: 0
  });
  const [generationParams, setGenerationParams] = useState<LeadGenerationRequest>({
    linkedin_keywords: ['AI', 'Cybersecurity', 'SaaS'],
    email_sources: [],
    niche_markets: ['Cybersecurity', 'Cloud Infrastructure'],
    location: 'United States',
    limit_per_source: 20
  });

  // Fetch leads on mount and when filters change
  useEffect(() => {
    fetchLeads();
  }, [filters]);

  // Fetch leads from API (or use mock data for demo)
  const fetchLeads = async () => {
    setLoading(true);
    try {
      // In a real app, this would be an API call:
      // const response = await axios.get('/api/leads', { params: filters });
      // setLeads(response.data);
      
      // For demo, use mock data with filtering
      let filteredLeads = [...mockLeads];
      
      if (filters.status) {
        filteredLeads = filteredLeads.filter(lead => lead.status === filters.status);
      }
      if (filters.source) {
        filteredLeads = filteredLeads.filter(lead => lead.source === filters.source);
      }
      if (filters.minScore > 0) {
        filteredLeads = filteredLeads.filter(lead => lead.lead_score >= filters.minScore);
      }
      
      setLeads(filteredLeads);
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setLoading(false);
    }
  };

  // Generate new leads
  const generateLeads = async () => {
    setGenerating(true);
    try {
      // In a real app, this would be an API call:
      // const response = await axios.post('/api/leads/generate', generationParams);
      // setLeads([...response.data.saved_leads, ...leads]);
      
      // For demo, simulate adding new leads
      const newLeads = [
        {
          id: Date.now(),
          first_name: "Generated",
          last_name: "Lead",
          full_name: "Generated Lead",
          email: `generated${Date.now()}@example.com`,
          job_title: "Manager",
          company: "Generated Corp",
          industry: "Technology",
          company_size: "51-200",
          location: "Remote",
          linkedin_url: null,
          lead_score: Math.floor(Math.random() * 50) + 50,
          status: LeadStatus.NEW,
          source: LeadSource.LINKEDIN,
          niche_keywords: generationParams.linkedin_keywords?.[0] || "",
          pain_points: "Generated lead for demonstration",
          budget_indicator: "$1K-$5K",
          decision_maker: false,
          created_at: new Date(),
          updated_at: new Date(),
          notes: null,
          tags: null
        }
      ];
      
      setLeads([...newLeads, ...leads]);
    } catch (error) {
      console.error('Error generating leads:', error);
    } finally {
      setGenerating(false);
    }
  };

  // Update lead status
  const updateLeadStatus = async (leadId: number, status: LeadStatus) => {
    try {
      // In a real app, this would be an API call:
      // await axios.patch(`/api/leads/${leadId}`, { status });
      
      // For demo, update locally
      setLeads(prevLeads =>
        prevLeads.map(lead =>
          lead.id === leadId ? { ...lead, status } : lead
        )
      );
    } catch (error) {
      console.error('Error updating lead status:', error);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading leads...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Lead Generation Engine</h1>
        <button
          onClick={generateLeads}
          disabled={generating}
          className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50`}
        >
          {generating ? 'Generating...' : 'Generate New Leads'}
        </button>
      </div>

      {/* Filters */}
      <div className="bg-gray-50 rounded-lg p-4 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Status</label>
            <select
              value={filters.status}
              onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value as LeadStatus || '' }))}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">All Statuses</option>
              <option value={LeadStatus.NEW}>New</option>
              <option value={LeadStatus.QUALIFIED}>Qualified</option>
              <option value={LeadStatus.CONTACTED}>Contacted</option>
              <option value={LeadStatus.NURTURING}>Nurturing</option>
              <option value={LeadStatus.CONVERTED}>Converted</option>
              <option value={LeadStatus.LOST}>Lost</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Source</label>
            <select
              value={filters.source}
              onChange={(e) => setFilters(prev => ({ ...prev, source: e.target.value as LeadSource || '' }))}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="">All Sources</option>
              <option value={LeadSource.LINKEDIN}>LinkedIn</option>
              <option value={LeadSource.EMAIL_SCRAPING}>Email Scraping</option>
              <option value={LeadSource.NICHE_PROSPECTING}>Niche Prospecting</option>
              <option value={LeadSource.MANUAL}>Manual</option>
              <option value={LeadSource.REFERRAL}>Referral</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Minimum Score</label>
            <input
              type="number"
              value={filters.minScore}
              onChange={(e) => setFilters(prev => ({ ...prev, minScore: parseInt(e.target.value) || 0 }))}
              className="w-full px-3 py-2 border rounded"
              min="0"
              max="100"
            />
          </div>
        </div>
      </div>

      {/* Generation Parameters (Collapsible) */}
      <div className="border rounded-lg p-4">
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-lg font-semibold">Generation Parameters</h2>
          <button
            onClick={() => setShowParams(!showParams)}
            className="text-sm text-blue-600 hover:underline"
          >
            {showParams ? 'Hide' : 'Show'} Parameters
          </button>
        </div>
        
        {showParams && (
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="block text-sm font-medium mb-1">LinkedIn Keywords</label>
                <input
                  type="text"
                  value={generationParams.linkedin_keywords?.join(', ') || ''}
                  onChange={(e) => {
                    const keywords = e.target.value
                      .split(',')
                      .map(k => k.trim())
                      .filter(k => k.length > 0);
                    setGenerationParams(prev => ({ ...prev, linkedin_keywords: keywords }));
                  }}
                  className="w-full px-3 py-2 border rounded"
                  placeholder="AI, Cybersecurity, SaaS"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email Sources (URLs)</label>
                <textarea
                  value={generationParams.email_sources?.join('\n') || ''}
                  onChange={(e) => {
                    const sources = e.target.value
                      .split('\n')
                      .map(s => s.trim())
                      .filter(s => s.length > 0);
                    setGenerationParams(prev => ({ ...prev, email_sources: sources }));
                  }}
                  className="w-full px-3 py-2 border rounded"
                  rows="2"
                  placeholder="https://example.com\nhttps://another-example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Niche Markets</label>
                <input
                  type="text"
                  value={generationParams.niche_markets?.join(', ') || ''}
                  onChange={(e) => {
                    const markets = e.target.value
                      .split(',')
                      .map(m => m.trim())
                      .filter(m => m.length > 0);
                    setGenerationParams(prev => ({ ...prev, niche_markets: markets }));
                  }}
                  className="w-full px-3 py-2 border rounded"
                  placeholder="Cybersecurity, Cloud Infrastructure, Fintech"
                />
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
              <div>
                <label className="block text-sm font-medium mb-1">Location</label>
                <input
                  type="text"
                  value={generationParams.location || ''}
                  onChange={(e) => setGenerationParams(prev => ({ ...prev, location: e.target.value }))}
                  className="w-full px-3 py-2 border rounded"
                  placeholder="United States"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Limit per Source</label>
                <input
                  type="number"
                  value={generationParams.limit_per_source || 20}
                  onChange={(e) => setGenerationParams(prev => ({ ...prev, limit_per_source: parseInt(e.target.value) || 20 }))}
                  className="w-full px-3 py-2 border rounded"
                  min="5"
                  max="100"
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="text-2xl font-bold">{leads.length}</div>
          <div className="text-sm text-gray-600">Total Leads</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <div className="text-2xl font-bold">{leads.filter(l => l.lead_score >= 80).length}</div>
          <div className="text-sm text-gray-600">Hot Leads (80+)</div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-4">
          <div className="text-2xl font-bold">{leads.filter(l => l.decision_maker).length}</div>
          <div className="text-sm text-gray-600">Decision Makers</div>
        </div>
        <div className="bg-purple-50 rounded-lg p-4">
          <div className="text-2xl font-bold">{leads.filter(l => l.status === LeadStatus.QUALIFIED).length}</div>
          <div className="text-sm text-gray-600">Qualified</div>
        </div>
      </div>

      {/* Leads Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Source</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {leads.length === 0 ? (
              <tr>
                <td colspan="7" className="px-6 py-4 text-center text-gray-500">
                  No leads match the current filters
                </td>
              </tr>
            ) : (
              leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center space-x-3">
                      {lead.linkedin_url && (
                        <a href={lead.linkedin_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                          🔗
                        </a>
                      )}
                      <div>
                        <div className="text-sm font-medium text-gray-900">{lead.full_name}</div>
                        {lead.email && (
                          <div className="text-xs text-gray-500">{lead.email}</div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {lead.company || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {lead.job_title || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className={`text-sm font-medium inline-flex items-center px-2.5 py-0.5 rounded text-xs ${
                      lead.lead_score >= 80 ? 'bg-green-100 text-green-800' :
                      lead.lead_score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {lead.lead_score}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {lead.source.replace('_', ' ').title()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBgColor(lead.status)} ${getStatusTextColor(lead.status)}`}>
                      {lead.status.replace('_', ' ').title()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="space-y-2">
                      <button
                        onClick={() => updateLeadStatus(lead.id, 
                          lead.status === LeadStatus.NEW ? LeadStatus.QUALIFIED :
                          lead.status === LeadStatus.QUALIFIED ? LeadStatus.CONTACTED :
                          lead.status === LeadStatus.CONTACTED ? LeadStatus.NURTURING :
                          LeadStatus.NEW
                        )}
                        className="px-3 py-1 text-xs bg-blue-500 hover:bg-blue-600 text-white rounded"
                      >
                        Update Status
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Helper functions for status styling
function getStatusBgColor(status: LeadStatus): string {
  switch (status) {
    case LeadStatus.NEW: return 'bg-blue-100';
    case LeadStatus.QUALIFIED: return 'bg-green-100';
    case LeadStatus.CONTACTED: return 'bg-yellow-100';
    case LeadStatus.NURTURING: return 'bg-purple-100';
    case LeadStatus.CONVERTED: return 'bg-indigo-100';
    case LeadStatus.LOST: return 'bg-gray-100';
    default: return 'bg-gray-100';
  }
}

function getStatusTextColor(status: LeadStatus): string {
  switch (status) {
    case LeadStatus.NEW: return 'text-blue-800';
    case LeadStatus.QUALIFIED: return 'text-green-800';
    case LeadStatus.CONTACTED: return 'text-yellow-800';
    case LeadStatus.NURTURING: return 'text-purple-800';
    case LeadStatus.CONVERTED: return 'text-indigo-800';
    case LeadStatus.LOST: return 'text-gray-800';
    default: return 'text-gray-800';
  }
}

// State for showing/hiding generation parameters
const [showParams, setShowParams] = useState(false);