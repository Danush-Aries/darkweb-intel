import asyncio
import aiohttp
import re
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus, urljoin
from bs4 import BeautifulSoup
import random
from app.models.lead_models import Lead, LeadStatus, LeadSource
from tortoise.exceptions import DoesNotExist, IntegrityError

class LeadGenerationService:
    def __init__(self):
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    # LinkedIn Lead Scraping
    async def scrape_linkedin_leads(self, keywords: List[str], location: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        """
        Scrape LinkedIn for leads based on keywords and location
        """
        leads = []
        
        # Note: In production, you would use LinkedIn's official API or a licensed scraping service
        # This is a simulated implementation for demonstration purposes
        
        for keyword in keywords[:5]:  # Limit to prevent over-scraping
            # Simulate LinkedIn search results
            for i in range(min(limit // len(keywords), 10)):
                lead_data = {
                    "first_name": f"FirstName{i}",
                    "last_name": f"LastName{i}",
                    "full_name": f"FirstName{i} LastName{i}",
                    "email": f"firstname{i}.lastname{i}@{keyword.replace(' ', '').lower()}.com",
                    "job_title": f"{keyword.title()} Specialist",
                    "company": f"{keyword.title()} Corp",
                    "industry": keyword.title(),
                    "location": location or "Remote",
                    "linkedin_url": f"https://linkedin.com/in/firstname{i}-lastname{i}-{random.randint(1000, 9999)}",
                    "lead_score": random.randint(30, 90),
                    "source": LeadSource.LINKEDIN.value,
                    "status": LeadStatus.NEW.value,
                    "niche_keywords": ", ".join(keywords[:3]),
                    "decision_maker": random.choice([True, False])
                }
                leads.append(lead_data)
                
        return leads
    
    # Email Extraction from Web Sources
    async def extract_emails_from_sources(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Extract email addresses from web sources (websites, forums, etc.)
        """
        leads = []
        
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        for url in urls:
            try:
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        text = await response.text()
                        emails = re.findall(email_pattern, text)
                        
                        # Parse HTML for additional context
                        soup = BeautifulSoup(text, 'html.parser')
                        
                        for email in set(emails):  # Remove duplicates
                            # Try to extract name and company from context
                            name_parts = email.split('@')[0].split('.')
                            first_name = name_parts[0].title() if len(name_parts) > 0 else ""
                            last_name = name_parts[1].title() if len(name_parts) > 1 else ""
                            
                            lead_data = {
                                "first_name": first_name,
                                "last_name": last_name,
                                "full_name": f"{first_name} {last_name}".strip(),
                                "email": email.lower(),
                                "job_title": "Professional",  # Would be extracted from context in real implementation
                                "company": "Unknown",       # Would be extracted from context
                                "industry": "Technology",
                                "location": "Unknown",
                                "linkedin_url": None,
                                "lead_score": random.randint(20, 70),
                                "source": LeadSource.EMAIL_SCRAPING.value,
                                "status": LeadStatus.NEW.value,
                                "niche_keywords": "",
                                "decision_maker": False
                            }
                            leads.append(lead_data)
                            
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
                continue
                
        return leads
    
    # Niche Prospecting
    async def prospect_niche_markets(self, niche: str, platforms: List[str] = None) -> List[Dict[str, Any]]:
        """
        Prospect leads in specific niches/industries
        """
        if platforms is None:
            platforms = ["github", "angel_list", "crunchbase", "product_hunt"]
            
        leads = []
        
        # Simulate niche-specific prospecting
        niche_companies = [
            f"{niche.title()} Solutions",
            f"Global {niche.title()}",
            f"{niche.title()} Innovations Inc",
            f"Advanced {niche.title()} Systems",
            f"{niche.title()} Tech Labs"
        ]
        
        titles = [
            f"Senior {niche.title()} Engineer",
            f"Lead {niche.title()} Developer",
            f"{niche.title()} Product Manager",
            f"Director of {niche.title()}",
            f"VP of {niche.title()}",
            f"Founder & CEO",
            f"CTO",
            f"Head of {niche.title()}"
        ]
        
        for i, company in enumerate(niche_companies):
            for j in range(2):  # 2 leads per company
                lead_data = {
                    "first_name": f"Name{i}{j}",
                    "last_name": f"Surname{i}{j}",
                    "full_name": f"Name{i}{j} Surname{i}{j}",
                    "email": f"name{i}{j}.surname{i}{j}@{company.lower().replace(' ', '')}.com",
                    "job_title": random.choice(titles),
                    "company": company,
                    "industry": niche.title(),
                    "company_size": random.choice(["1-10", "11-50", "51-200", "201-1000", "1000+"]),
                    "location": random.choice(["San Francisco, CA", "New York, NY", "Remote", "London, UK", "Berlin, DE"]),
                    "linkedin_url": f"https://linkedin.com/in/name{i}{j}-surname{i}{j}-{random.randint(1000, 9999)}",
                    "lead_score": random.randint(50, 95),
                    "source": LeadSource.NICHE_PROSPECTING.value,
                    "status": LeadStatus.NEW.value,
                    "niche_keywords": niche,
                    "budget_indicator": random.choice(["$1K-$5K", "$5K-$10K", "$10K-$50K", "$50K+"]),
                    "decision_maker": random.choice([True, False]) if "Director" in random.choice(titles) or "VP" in random.choice(titles) or "Founder" in random.choice(titles) or "CTO" in random.choice(titles) or "Head" in random.choice(titles) else False
                }
                leads.append(lead_data)
                
        return leads
    
    # Lead Qualification and Scoring
    def calculate_lead_score(self, lead_data: Dict[str, Any]) -> int:
        """
        Calculate lead score based on various factors
        """
        score = 0
        
        # Job title seniority (0-25 points)
        senior_titles = ["CEO", "CTO", "CFO", "Founder", "President", "Vice President", "Director", "Head of"]
        mid_titles = ["Manager", "Lead", "Senior", "Principal"]
        
        title = lead_data.get("job_title", "").lower()
        if any(senior.lower() in title for senior in senior_titles):
            score += 25
        elif any(mid.lower() in title for mid in mid_titles):
            score += 15
        else:
            score += 5
            
        # Company size (0-20 points)
        company_size = lead_data.get("company_size", "")
        if company_size == "1000+":
            score += 20
        elif company_size == "201-1000":
            score += 15
        elif company_size == "51-200":
            score += 10
        elif company_size == "11-50":
            score += 5
            
        # Decision maker (0-15 points)
        if lead_data.get("decision_maker", False):
            score += 15
            
        # Email quality (0-10 points)
        email = lead_data.get("email", "")
        if email and "@" in email:
            # Professional email (company domain) vs generic
            domain = email.split("@")[1] if len(email.split("@")) > 1 else ""
            if domain and not any(generic in domain for generic in ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]):
                score += 10
            else:
                score += 5
                
        # LinkedIn presence (0-10 points)
        if lead_data.get("linkedin_url"):
            score += 10
            
        # Niche relevance (0-10 points)
        niche_keywords = lead_data.get("niche_keywords", "")
        if niche_keywords:
            score += 10
            
        # Budget indicator (0-10 points)
        budget = lead_data.get("budget_indicator", "")
        if budget:
            if "+" in budget or "50K" in budget:
                score += 10
            elif "10K" in budget:
                score += 7
            elif "5K" in budget:
                score += 4
            else:
                score += 2
                
        return min(score, 100)  # Cap at 100
    
    async def qualify_and_save_leads(self, raw_leads: List[Dict[str, Any]]) -> List[Lead]:
        """
        Qualify leads and save them to database
        """
        qualified_leads = []
        
        for lead_data in raw_leads:
            try:
                # Calculate lead score
                lead_score = self.calculate_lead_score(lead_data)
                lead_data["lead_score"] = lead_score
                
                # Determine status based on score
                if lead_score >= 80:
                    lead_data["status"] = LeadStatus.QUALIFIED.value
                elif lead_score >= 60:
                    lead_data["status"] = LeadStatus.NURTURING.value
                else:
                    lead_data["status"] = LeadStatus.NEW.value
                
                # Check if lead already exists
                existing_lead = None
                try:
                    if lead_data.get("email"):
                        existing_lead = await Lead.get(email=lead_data["email"])
                    elif lead_data.get("linkedin_url"):
                        existing_lead = await Lead.get(linkedin_url=lead_data["linkedin_url"])
                except DoesNotExist:
                    pass
                
                if existing_lead:
                    # Update existing lead
                    for key, value in lead_data.items():
                        if hasattr(existing_lead, key) and value is not None:
                            setattr(existing_lead, key, value)
                    await existing_lead.save()
                    qualified_leads.append(existing_lead)
                else:
                    # Create new lead
                    lead = await Lead.create(**lead_data)
                    qualified_leads.append(lead)
                    
            except IntegrityError as e:
                print(f"Integrity error saving lead: {str(e)}")
                continue
            except Exception as e:
                print(f"Error processing lead: {str(e)}")
                continue
                
        return qualified_leads
    
    # Main lead generation pipeline
    async def generate_leads_pipeline(self, 
                                    linkedin_keywords: List[str] = None,
                                    email_sources: List[str] = None,
                                    niche_markets: List[str] = None,
                                    location: str = "",
                                    limit_per_source: int = 50) -> Dict[str, Any]:
        """
        Complete lead generation pipeline
        """
        results = {
            "linkedin_leads": [],
            "email_leads": [],
            "niche_leads": [],
            "total_leads": 0,
            "qualified_leads": 0
        }
        
        # LinkedIn lead generation
        if linkedin_keywords:
            linkedin_raw = await self.scrape_linkedin_leads(linkedin_keywords, location, limit_per_source)
            results["linkedin_leads"] = linkedin_raw
        
        # Email extraction
        if email_sources:
            email_raw = await self.extract_emails_from_sources(email_sources)
            results["email_leads"] = email_raw
        
        # Niche prospecting
        if niche_markets:
            for niche in niche_markets:
                niche_raw = await self.prospect_niche_markets(niche, limit=limit_per_source//len(niche_markets))
                results["niche_leads"].extend(niche_raw)
        
        # Combine all leads
        all_raw_leads = results["linkedin_leads"] + results["email_leads"] + results["niche_leads"]
        
        # Qualify and save leads
        qualified_leads = await self.qualify_and_save_leads(all_raw_leads)
        
        results["total_leads"] = len(all_raw_leads)
        results["qualified_leads"] = len([l for l in qualified_leads if l.lead_score >= 60])
        results["saved_leads"] = qualified_leads
        
        return results