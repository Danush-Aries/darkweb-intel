import { NextResponse } from 'next/server';
import type { Lead } from '@/types/lead-types';

// Mock data - in a real app this would come from a database
const mockLeads: Lead[] = [
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    full_name: "John Doe",
    email: "john.doe@techcorp.com",
    phone: "+1-555-0123",
    job_title: "CTO",
    company: "TechCorp Solutions",
    industry: "Technology",
    company_size: "51-200",
    location: "San Francisco, CA",
    linkedin_url: "https://linkedin.com/in/johndoe",
    lead_score: 92,
    status: "qualified",
    source: "linkedin",
    niche_keywords: "AI, Machine Learning, Cybersecurity",
    pain_points: "Scaling security infrastructure, talent acquisition",
    budget_indicator: "$50K+",
    decision_maker: true,
    created_at: new Date('2026-04-20'),
    updated_at: new Date('2026-04-20'),
    notes: null,
    tags: null
  },
  {
    id: 2,
    first_name: "Sarah",
    last_name: "Chen",
    full_name: "Sarah Chen",
    email: "sarah.chen@innovateinc.com",
    phone: "+1-555-0456",
    job_title: "VP of Engineering",
    company: "Innovate Inc",
    industry: "SaaS",
    company_size: "201-1000",
    location: "New York, NY",
    linkedin_url: "https://linkedin.com/in/sarahchen",
    lead_score: 87,
    status: "qualified",
    source: "niche_prospecting",
    niche_keywords: "Cloud Security, DevSecOps",
    pain_points: "Compliance automation, reducing false positives",
    budget_indicator: "$25K-$50K",
    decision_maker: true,
    created_at: new Date('2026-04-18'),
    updated_at: new Date('2026-04-18'),
    notes: null,
    tags: null
  }
];

// Proxy to backend for leads
export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    // Forward to backend
    const backendUrl = new URL('http://localhost:8000/leads');
    // Copy query parameters
    searchParams.forEach((value, key) => {
      backendUrl.searchParams.set(key, value);
    });

    const backendResponse = await fetch(backendUrl.toString());
    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching leads from backend:', error);
    return NextResponse.json(
      { error: 'Failed to fetch leads from backend' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    // Forward to backend
    const backendResponse = await fetch('http://localhost:8000/leads/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    const data = await backendResponse.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error generating leads via backend:', error);
    return NextResponse.json(
      { error: 'Failed to generate leads via backend' },
      { status: 500 }
    );
  }
}