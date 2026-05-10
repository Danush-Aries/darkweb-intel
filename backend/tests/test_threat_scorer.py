import pytest
from app.services.threat_scorer import calculate_threat_score

def test_calculate_threat_score_empty_content():
    """Test that empty content returns 0.0 score"""
    assert calculate_threat_score("") == 0.0
    assert calculate_threat_score(None) == 0.0

def test_calculate_threat_score_no_matches():
    """Test that content with no threat indicators returns low score"""
    content = "This is a normal sentence with no threat indicators."
    score = calculate_threat_score(content)
    assert score == 0.0

def test_calculate_threat_score_critical_indicators():
    """Test scoring with critical threat indicators"""
    # Test credit card pattern
    content = "This contains credit card information"
    score = calculate_threat_score(content)
    # Length is 37 (< 100) so score should be halved: 40 * 0.5 = 20
    assert score == 20.0
    
    # Test password list pattern
    content = "password list leaked online"
    score = calculate_threat_score(content)
    # Length is 27 (< 100) so score should be halved: 35 * 0.5 = 17.5
    assert score == 17.5
    
    # Test zero-day exploit
    content = "0day exploit found in the wild"
    score = calculate_threat_score(content)
    # Length is 30 (< 100) so score should be halved: 35 * 0.5 = 17.5
    assert score == 17.5

def test_calculate_threat_score_warning_indicators():
    """Test scoring with warning indicators"""
    # Test admin login
    content = "admin login credentials exposed"
    score = calculate_threat_score(content)
    # Length is 31 (< 100) so score should be halved: 20 * 0.5 = 10
    assert score == 10.0
    
    # Test ransomware
    content = "ransomware attack detected"
    score = calculate_threat_score(content)
    # Length is 26 (< 100) so score should be halved: 20 * 0.5 = 10
    assert score == 10.0
    
    # Test payload
    content = "malicious payload delivered"
    score = calculate_threat_score(content)
    # Length is 27 (< 100) so score should be halved: 15 * 0.5 = 7.5
    assert score == 7.5

def test_calculate_threat_score_noise_indicators():
    """Test scoring with noise/low-confidence indicators"""
    # Test email/phone
    content = "contact us at email@example.com"
    score = calculate_threat_score(content)
    # Length is 31 (< 100) so score should be halved: 5 * 0.5 = 2.5
    assert score == 2.5
    
    # Test darkweb/torrent
    content = "darkweb marketplace onion link"
    score = calculate_threat_score(content)
    # Length is 30 (< 100) so score should be halved: 2 * 0.5 = 1.0
    assert score == 1.0

def test_calculate_threat_score_multiple_indicators():
    """Test scoring with multiple threat indicators"""
    content = "credit card password list ransomware payload"
    # Length is 45 (< 100) so score should be halved
    # Expected raw score: 40 (credit card) + 35 (password list) + 20 (ransomware) + 15 (payload) = 110
    # After halving: 55.0
    score = calculate_threat_score(content)
    assert score == 55.0

def test_calculate_threat_score_density_penalty():
    """Test that short content gets score penalty"""
    # Content with critical indicator but very short
    content = "credit card"
    score = calculate_threat_score(content)
    # Length is 11 (< 100) so score should be halved: 40 * 0.5 = 20
    assert score == 20.0
    
    # Content with critical indicator but long enough (>= 100 chars)
    content = "credit card " * 20  # Makes it longer than 100 chars
    score = calculate_threat_score(content)
    # Length is >= 100 so no penalty, score should be 40
    assert score == 40.0

def test_calculate_threat_score_case_insensitive():
    """Test that scoring is case insensitive"""
    content = "CREDIT CARD PASSWORD LIST"
    # Length is 27 (< 100) so score should be halved
    # Expected raw score: 40 (credit card) + 35 (password list) = 75
    # After halving: 37.5
    score = calculate_threat_score(content)
    assert score == 37.5

def test_calculate_threat_score_normalization():
    """Test that score is normalized to 0-100 range"""
    # Very high score content
    content = "credit card password list 0day exploit admin login ransomware payload shellcode"
    # Length is 52 (< 100) so score should be halved
    # Expected raw score: 
    #   credit card: 40
    #   password list: 35
    #   0day exploit: 35
    #   admin login: 20
    #   ransomware: 20
    #   payload: 15 (matches payload|shellcode|backdoor)
    #   shellcode: 0 (already counted above - same pattern)
    # Total: 40 + 35 + 35 + 20 + 20 + 15 = 165
    # After halving: 82.5
    score = calculate_threat_score(content)
    assert score == 82.5
    
    # Test with content that would exceed 100 even after halving
    content = "credit card password list 0day exploit admin login ransomware payload shellcode " + "extra " * 20
    # Make sure it's over 100 chars to avoid halving
    score = calculate_threat_score(content)
    # Should be capped at 100
    assert score == 100.0
    
    # Medium score
    content = "credit card admin login"
    # Length is 24 (< 100) so score should be halved
    # Expected raw score: 40 + 20 = 60
    # After halving: 30.0
    score = calculate_threat_score(content)
    assert score == 30.0
