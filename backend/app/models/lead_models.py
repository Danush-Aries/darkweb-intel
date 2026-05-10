from tortoise import fields, models
from enum import Enum


class LeadStatus(str, Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"
    NURTURING = "nurturing"
    CONVERTED = "converted"
    LOST = "lost"


class LeadSource(str, Enum):
    LINKEDIN = "linkedin"
    EMAIL_SCRAPING = "email_scraping"
    NICHE_PROSPECTING = "niche_prospecting"
    MANUAL = "manual"
    REFERRAL = "referral"


class Lead(models.Model):
    id = fields.IntField(pk=True)
    
    # Basic Information
    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=100, null=True)
    full_name = fields.CharField(max_length=255, index=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    phone = fields.CharField(max_length=50, null=True)
    
    # Professional Information
    job_title = fields.CharField(max_length=255, null=True)
    company = fields.CharField(max_length=255, index=True)
    industry = fields.CharField(max_length=255, null=True)
    company_size = fields.CharField(max_length=100, null=True)
    location = fields.CharField(max_length=255, null=True)
    linkedin_url = fields.CharField(max_length=500, null=True, unique=True)
    
    # Lead Scoring and Qualification
    lead_score = fields.IntField(default=0)  # 0-100 score
    status = fields.CharField(max_length=50, default=LeadStatus.NEW.value, index=True)
    source = fields.CharField(max_length=50, default=LeadSource.MANUAL.value, index=True)
    
    # Niche Information
    niche_keywords = fields.TextField(null=True)  # Comma-separated keywords
    pain_points = fields.TextField(null=True)
    budget_indicator = fields.CharField(max_length=100, null=True)
    decision_maker = fields.BooleanField(default=False)
    
    # Timestamps
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True)
    last_contacted = fields.DatetimeField(null=True)
    
    # Additional Data
    notes = fields.TextField(null=True)
    tags = fields.TextField(null=True)  # Comma-separated tags
    
    class Meta:
        table = "leads"
        indexes = [
            ("company", "industry"),
            ("status", "lead_score"),
            ("source", "created_at")
        ]


class LeadInteraction(models.Model):
    id = fields.IntField(pk=True)
    lead = fields.ForeignKeyField('models.Lead', related_name='interactions')
    interaction_type = fields.CharField(max_length=100)  # email, call, meeting, etc.
    subject = fields.CharField(max_length=255, null=True)
    content = fields.TextField(null=True)
    outcome = fields.CharField(max_length=100, null=True)  # positive, negative, neutral
    next_step = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "lead_interactions"