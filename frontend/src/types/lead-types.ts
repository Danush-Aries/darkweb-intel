export enum LeadStatus {
  NEW = 'new',
  QUALIFIED = 'qualified',
  CONTACTED = 'contacted',
  NURTURING = 'nurturing',
  CONVERTED = 'converted',
  LOST = 'lost'
}

export enum LeadSource {
  LINKEDIN = 'linkedin',
  EMAIL_SCRAPING = 'email_scraping',
  NICHE_PROSPECTING = 'niche_prospecting',
  MANUAL = 'manual',
  REFERRAL = 'referral'
}

export interface Lead {
  id: number;
  first_name: string | null;
  last_name: string | null;
  full_name: string;
  email: string;
  phone: string | null;
  job_title: string | null;
  company: string | null;
  industry: string | null;
  company_size: string | null;
  location: string | null;
  linkedin_url: string | null;
  lead_score: number;
  status: LeadStatus;
  source: LeadSource;
  niche_keywords: string | null;
  pain_points: string | null;
  budget_indicator: string | null;
  decision_maker: boolean;
  created_at: Date;
  updated_at: Date;
  notes: string | null;
  tags: string | null;
}

export interface LeadInteraction {
  id: number;
  lead_id: number;
  interaction_type: string;
  subject: string | null;
  content: string | null;
  outcome: string | null;
  next_step: string | null;
  created_at: Date;
}

export interface LeadGenerationRequest {
  linkedin_keywords?: string[];
  email_sources?: string[];
  niche_markets?: string[];
  location?: string;
  limit_per_source?: number;
}

export interface LeadGenerationResult {
  linkedin_leads: any[];
  email_leads: any[];
  niche_leads: any[];
  total_leads: number;
  qualified_leads: number;
  saved_leads: Lead[];
}