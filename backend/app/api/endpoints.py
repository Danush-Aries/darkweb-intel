from fastapi import APIRouter, HTTPException, BackgroundTasks
from ..models.models import Keyword, IntelReport
from ..models.lead_models import Lead, LeadStatus, LeadSource
from ..services.threat_scorer import calculate_threat_score
from ..services.ai_triage import triage_content
from ..services.lead_generation_service import LeadGenerationService
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

# Pydantic models for lead generation
class LeadGenerateRequest(BaseModel):
    linkedin_keywords: Optional[List[str]] = None
    email_sources: Optional[List[str]] = None
    niche_markets: Optional[List[str]] = None
    location: Optional[str] = ""
    limit_per_source: Optional[int] = 50

class LeadResponse(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    lead_score: int
    status: str
    source: str
    niche_keywords: Optional[str] = None
    pain_points: Optional[str] = None
    budget_indicator: Optional[str] = None
    decision_maker: bool
    created_at: str
    updated_at: str

class LeadGenerationResult(BaseModel):
    linkedin_leads: List[Dict[str, Any]]
    email_leads: List[Dict[str, Any]]
    niche_leads: List[Dict[str, Any]]
    total_leads: int
    qualified_leads: int
    saved_leads: List[LeadResponse]

router = APIRouter()

@router.post("/keywords")
async def add_keyword(keyword: str):
    await Keyword.create(word=keyword)
    return {"status": "success", "keyword": keyword}

@router.get("/keywords")
async def get_keywords():
    return await Keyword.all()

@router.get("/reports")
async def get_reports():
    return await IntelReport.all()

@router.post("/scan")
async def trigger_scan(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scan_process)
    return {"status": "Scan triggered"}

async def run_scan_process():
    # Integration with Scrapy would happen here
    # For demo purposes, we simulate finding a report
    keywords = await Keyword.all()
    for k in keywords:
        mock_content = f"Found leaked password for {k.word} on dark web!"
        score = calculate_threat_score(mock_content)
        ai_summary = await triage_content(mock_content)
        await IntelReport.create(
            keyword=k.word,
            url="http://mock.onion",
            content=mock_content,
             threat_score=score,
             ai_summary=ai_summary,
             status="completed"
         )

# Lead Generation Endpoints
@router.post("/leads/generate", response_model=LeadGenerationResult)
async def generate_leads(request: LeadGenerateRequest):
    """
    Generate leads using multiple sources
    """
    async with LeadGenerationService() as service:
        results = await service.generate_leads_pipeline(
            linkedin_keywords=request.linkedin_keywords,
            email_sources=request.email_sources,
            niche_markets=request.niche_markets,
            location=request.location,
            limit_per_source=request.limit_per_source
        )
        
        # Convert saved leads to response format
        saved_leads_response = []
        for lead in results["saved_leads"]:
            saved_leads_response.append({
                "id": lead.id,
                "first_name": lead.first_name,
                "last_name": lead.last_name,
                "full_name": lead.full_name,
                "email": lead.email,
                "phone": lead.phone,
                "job_title": lead.job_title,
                "company": lead.company,
                "industry": lead.industry,
                "company_size": lead.company_size,
                "location": lead.location,
                "linkedin_url": lead.linkedin_url,
                "lead_score": lead.lead_score,
                "status": lead.status,
                "source": lead.source,
                "niche_keywords": lead.niche_keywords,
                "pain_points": lead.pain_points,
                "budget_indicator": lead.budget_indicator,
                "decision_maker": lead.decision_marker,
                "created_at": lead.created_at.isoformat() if lead.created_at else None,
                "updated_at": lead.updated_at.isoformat() if lead.updated_at else None
            })
        
        return LeadGenerationResult(
            linkedin_leads=results["linkedin_leads"],
            email_leads=results["email_leads"],
            niche_leads=results["niche_leads"],
            total_leads=results["total_leads"],
            qualified_leads=results["qualified_leads"],
            saved_leads=saved_leads_response
        )

@router.get("/leads", response_model=List[LeadResponse])
async def get_leads(
    status: Optional[str] = None,
    source: Optional[str] = None,
    min_score: Optional[int] = None,
    limit: int = 100
):
    """
    Get leads with optional filtering
    """
    query = Lead.all()
    
    if status:
        query = query.filter(status=status)
    if source:
        query = query.filter(source=source)
    if min_score is not None:
        query = query.filter(lead_score__gte=min_score)
    
    leads = await query.limit(limit)
    
    return [
        LeadResponse(
            id=lead.id,
            first_name=lead.first_name,
            last_name=lead.last_name,
            full_name=lead.full_name,
            email=lead.email,
            phone=lead.phone,
            job_title=lead.job_title,
            company=lead.company,
            industry=lead.industry,
            company_size=lead.company_size,
            location=lead.location,
            linkedin_url=lead.linkedin_url,
            lead_score=lead.lead_score,
            status=lead.status,
            source=lead.source,
            niche_keywords=lead.niche_keywords,
            pain_points=lead.pain_points,
            budget_indicator=lead.budget_indicator,
            decision_maker=lead.decision_maker,
            created_at=lead.created_at.isoformat() if lead.created_at else None,
            updated_at=lead.updated_at.isoformat() if lead.updated_at else None
        )
        for lead in leads
    ]

@router.get("/leads/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: int):
    """
    Get a specific lead by ID
    """
    lead = await Lead.get_or_none(id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return LeadResponse(
        id=lead.id,
        first_name=lead.first_name,
        last_name=lead.last_name,
        full_name=lead.full_name,
        email=lead.email,
        phone=lead.phone,
        job_title=lead.job_title,
        company=lead.company,
        industry=lead.industry,
        company_size=lead.company_size,
        location=lead.location,
        linkedin_url=lead.linkedin_url,
        lead_score=lead.lead_score,
        status=lead.status,
        source=lead.source,
        niche_keywords=lead.niche_keywords,
        pain_points=lead.pain_points,
        budget_indicator=lead.budget_indicator,
        decision_maker=lead.decision_maker,
        created_at=lead.created_at.isoformat() if lead.created_at else None,
        updated_at=lead.updated_at.isoformat() if lead.updated_at else None
    )

@router.post("/leads/{lead_id}/interact")
async def create_lead_interaction(
    lead_id: int,
    interaction_type: str,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    outcome: Optional[str] = None,
    next_step: Optional[str] = None
):
    """
    Create an interaction record for a lead
    """
    from ..models.lead_models import LeadInteraction
    
    lead = await Lead.get_or_none(id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Update last contacted timestamp
    lead.last_contacted = datetime.now()
    await lead.save()
    
    # Create interaction
    interaction = await LeadInteraction.create(
        lead=lead,
        interaction_type=interaction_type,
        subject=subject,
        content=content,
        outcome=outcome,
        next_step=next_step
    )
    
    return {
        "status": "success",
        "interaction_id": interaction.id,
        "message": f"Interaction recorded for lead {lead.full_name}"
    }

# Include scanner router
# from .scanner import router as scanner_router
# router.include_router(scanner_router, prefix="/scanner", tags=["scanner"])