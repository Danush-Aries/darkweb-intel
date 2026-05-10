from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.scanner_service import ScannerService

router = APIRouter()

class ScanRequest(BaseModel):
    code: str
    filename: Optional[str] = None

class ScanResponse(BaseModel):
    findings: List[Dict[str, Any]]
    status: str = "success"

@router.post("/scan", response_model=ScanResponse)
async def scan_code(request: ScanRequest):
    """
    Scan code for security vulnerabilities.
    
    Accepts code content and optional filename, runs security scanning,
    and returns findings.
    """
    try:
        scanner_service = ScannerService()
        findings = scanner_service.scan_code(request.code, request.filename)
        
        return ScanResponse(
            findings=findings,
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scan failed: {str(e)}"
        )