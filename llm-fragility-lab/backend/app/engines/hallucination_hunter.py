class HallucinationHunter:
    def analyze(self, response: str, ground_truth: str):
        # Basic implementation - returns a simple analysis
        # In a real implementation, this would do actual hallucination detection
        
        # Simple check: if response contains ground truth, it's likely not hallucinated
        if ground_truth.lower() in response.lower():
            return {
                "is_hallucinated": False,
                "confidence": 0.9,
                "explanation": "Response contains ground truth information"
            }
        else:
            return {
                "is_hallucinated": True,
                "confidence": 0.7,
                "explanation": "Response does not contain ground truth information"
            }