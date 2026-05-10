import os
import tempfile
import subprocess
import json
from typing import List, Dict, Any, Optional

# Path to the sast-scanner project
SAST_SCANNER_BASE = "/Users/dhanush/Desktop/github projects/sast-scanner"

class ScannerService:
    def __init__(self):
        self.sast_scanner_script = os.path.join(SAST_SCANNER_BASE, "sast_scanner.py")
        self.rules_dir = os.path.join(SAST_SCANNER_BASE, "rules")
        # Use the virtual environment's python if available
        self.venv_python = os.path.join(SAST_SCANNER_BASE, "venv", "bin", "python")
        if not os.path.exists(self.venv_python):
            self.venv_python = "python3"  # fallback to system python3
    
    def scan_code(self, code: str, filename: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scan code content for security vulnerabilities using sast-scanner.
        
        Args:
            code: The source code to scan
            filename: Optional filename to use for the temporary file
            
        Returns:
            List of findings from the scan
        """
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            if filename is None:
                filename = "scan_target.py"
            
            # Ensure the file has a proper extension for language detection
            if not any(filename.endswith(ext) for ext in ['.py', '.js', '.java', '.cs', '.cpp', '.c', '.php', '.rb', '.go']):
                filename = filename + ".py"
            
            # Write the code to a file in the temporary directory
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, 'w') as f:
                f.write(code)
            
            # Define the output SARIF file path
            output_sarif = os.path.join(temp_dir, "results.sarif")
            
            try:
                # Prepare environment with a dummy API key for Anthropic
                env = os.environ.copy()
                env["ANTHROPIC_API_KEY"] = "dummy-key-for-scanner-service"
                
                # Run the sast-scanner on the temporary directory
                cmd = [
                    self.venv_python, self.sast_scanner_script,
                    "scan", temp_dir,  # action and target
                    "--rules", self.rules_dir,
                    "--output", output_sarif
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,  # 30 second timeout
                    env=env
                )
                
                # The scanner might return non-zero if it finds vulnerabilities, but that's okay.
                # We'll check if the output file was created.
                if not os.path.exists(output_sarif):
                    # If the scanner fails to produce output, return an error finding
                    error_message = result.stderr if result.stderr else "Unknown error"
                    return [{
                        "ruleId": "SCANNER_ERROR",
                        "message": f"Scanner failed with error: {error_message}",
                        "severity": "error",
                        "file": filename
                    }]
                
                # Parse the SARIF output file
                with open(output_sarif, 'r') as f:
                    sarif_output = f.read()
                
                findings = self._parse_sarif_output(sarif_output, filename)
                return findings
                
            except subprocess.TimeoutExpired:
                return [{
                    "ruleId": "SCANNER_TIMEOUT",
                    "message": "Scanner timed out after 30 seconds",
                    "severity": "error",
                    "file": filename
                }]
            except Exception as e:
                return [{
                    "ruleId": "SCANNER_EXCEPTION",
                    "message": f"Scanner encountered an exception: {str(e)}",
                    "severity": "error",
                    "file": filename
                }]
    
    def _parse_sarif_output(self, sarif_output: str, filename: str) -> List[Dict[str, Any]]:
        """
        Parse SARIF output and convert to a list of findings.
        
        Args:
            sarif_output: The SARIF JSON output from the scanner
            filename: The filename that was scanned (for context)
            
        Returns:
            List of findings in a standardized format
        """
        findings = []
        
        try:
            sarif_data = json.loads(sarif_output)
            
            # Extract runs from SARIF
            runs = sarif_data.get("runs", [])
            
            for run in runs:
                # Extract tool information
                tool = run.get("tool", {})
                driver = tool.get("driver", {})
                
                # Extract results
                results = run.get("results", [])
                
                for result in results:
                    rule_id = result.get("ruleId", "UNKNOWN")
                    message = result.get("message", {}).get("text", "No message")
                    
                    # Extract severity from properties or default to medium
                    properties = result.get("properties", {})
                    severity = properties.get("severity", "medium").lower()
                    
                    # Extract location information
                    locations = result.get("locations", [])
                    location_info = {}
                    
                    if locations:
                        physical_location = locations[0].get("physicalLocation", {})
                        artifact_location = physical_location.get("artifactLocation", {})
                        region = physical_location.get("region", {})
                        
                        location_info = {
                            "file": artifact_location.get("uri", filename),
                            "line": region.get("startLine", 1),
                            "column": region.get("startColumn", 1)
                        }
                    else:
                        location_info = {
                            "file": filename,
                            "line": 1,
                            "column": 1
                        }
                    
                    finding = {
                        "ruleId": rule_id,
                        "message": message,
                        "severity": severity,
                        "file": location_info["file"],
                        "line": location_info["line"],
                        "column": location_info["column"],
                        "properties": properties
                    }
                    
                    findings.append(finding)
                    
        except json.JSONDecodeError as e:
            # If we can't parse the SARIF output, return an error finding
            findings.append({
                "ruleId": "SARIF_PARSE_ERROR",
                "message": f"Failed to parse SARIF output: {str(e)}",
                "severity": "error",
                "file": filename,
                "line": 1,
                "column": 1
            })
        except Exception as e:
            findings.append({
                "ruleId": "PARSE_ERROR",
                "message": f"Error parsing scanner output: {str(e)}",
                "severity": "error",
                "file": filename,
                "line": 1,
                "column": 1
            })
        
        return findings