"""
Built-in SAST scanner service.

Performs lightweight static analysis using regex-based rules.
No external tools or absolute paths required — works on any machine.
"""

import re
from typing import List, Dict, Any, Optional


# ---------------------------------------------------------------------------
# Rule definitions
# Each rule has: id, description, severity, languages, pattern
# ---------------------------------------------------------------------------

SAST_RULES: List[Dict[str, Any]] = [
    # Injection
    {
        "id": "SAST-001",
        "description": "Potential SQL injection: string formatting in query",
        "severity": "high",
        "languages": [".py", ".js", ".ts", ".java", ".php", ".rb"],
        "pattern": re.compile(
            r'(execute|query|cursor\.execute)\s*\(\s*["\'].*%[sd]|'
            r'(execute|query|cursor\.execute)\s*\(\s*f["\'].*\{',
            re.IGNORECASE,
        ),
    },
    {
        "id": "SAST-002",
        "description": "Potential command injection: shell=True with user-controlled input",
        "severity": "critical",
        "languages": [".py"],
        "pattern": re.compile(r'subprocess\.(run|call|Popen|check_output).*shell\s*=\s*True', re.IGNORECASE),
    },
    {
        "id": "SAST-003",
        "description": "Potential path traversal: unsanitised join with user input",
        "severity": "high",
        "languages": [".py", ".js", ".ts"],
        "pattern": re.compile(r'os\.path\.join\s*\(.*request\.|path\.join\s*\(.*req\.', re.IGNORECASE),
    },
    # Secrets / credentials
    {
        "id": "SAST-010",
        "description": "Hard-coded password or secret",
        "severity": "critical",
        "languages": None,  # all languages
        "pattern": re.compile(
            r'(password|passwd|secret|api_key|apikey|token)\s*=\s*["\'][^"\']{6,}["\']',
            re.IGNORECASE,
        ),
    },
    {
        "id": "SAST-011",
        "description": "AWS access key pattern",
        "severity": "critical",
        "languages": None,
        "pattern": re.compile(r'AKIA[0-9A-Z]{16}'),
    },
    {
        "id": "SAST-012",
        "description": "Generic private key PEM header",
        "severity": "critical",
        "languages": None,
        "pattern": re.compile(r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'),
    },
    # Cryptography
    {
        "id": "SAST-020",
        "description": "Use of weak hash algorithm MD5",
        "severity": "medium",
        "languages": [".py", ".js", ".ts", ".java", ".php"],
        "pattern": re.compile(r'hashlib\.md5|md5\s*\(|MessageDigest\.getInstance\s*\(\s*["\']MD5', re.IGNORECASE),
    },
    {
        "id": "SAST-021",
        "description": "Use of weak hash algorithm SHA1",
        "severity": "medium",
        "languages": [".py", ".js", ".ts", ".java"],
        "pattern": re.compile(r'hashlib\.sha1|sha1\s*\(|MessageDigest\.getInstance\s*\(\s*["\']SHA-?1["\']', re.IGNORECASE),
    },
    {
        "id": "SAST-022",
        "description": "SSL/TLS certificate verification disabled",
        "severity": "high",
        "languages": [".py", ".js", ".ts"],
        "pattern": re.compile(r'verify\s*=\s*False|rejectUnauthorized\s*:\s*false', re.IGNORECASE),
    },
    # Dangerous functions
    {
        "id": "SAST-030",
        "description": "Use of eval() — remote code execution risk",
        "severity": "high",
        "languages": [".py", ".js", ".ts", ".php", ".rb"],
        "pattern": re.compile(r'\beval\s*\('),
    },
    {
        "id": "SAST-031",
        "description": "Use of exec() with dynamic content",
        "severity": "high",
        "languages": [".py"],
        "pattern": re.compile(r'\bexec\s*\(\s*(?!compile\()(?:[^)]{3,})'),
    },
    {
        "id": "SAST-032",
        "description": "Pickle deserialization of untrusted data",
        "severity": "high",
        "languages": [".py"],
        "pattern": re.compile(r'pickle\.loads?\s*\(|cPickle\.loads?\s*\('),
    },
    # Web / XSS
    {
        "id": "SAST-040",
        "description": "Potential XSS: unescaped HTML output",
        "severity": "medium",
        "languages": [".py", ".js", ".ts", ".php"],
        "pattern": re.compile(r'innerHTML\s*=|document\.write\s*\(|mark_safe\s*\(', re.IGNORECASE),
    },
    # Debug / logging
    {
        "id": "SAST-050",
        "description": "Debug mode enabled in production code",
        "severity": "low",
        "languages": None,
        "pattern": re.compile(r'DEBUG\s*=\s*True|debug\s*=\s*true', re.IGNORECASE),
    },
    {
        "id": "SAST-051",
        "description": "Logging of potentially sensitive data",
        "severity": "low",
        "languages": None,
        "pattern": re.compile(r'log\w*\s*\(.*(?:password|token|secret|key)', re.IGNORECASE),
    },
]


class ScannerService:
    """
    Portable SAST scanner that uses built-in regex rules.
    No external dependencies or machine-specific paths required.
    """

    def __init__(self) -> None:
        self.rules = SAST_RULES

    def scan_code(self, code: str, filename: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Scan source code for security vulnerabilities.

        Args:
            code: Source code to scan.
            filename: Optional filename used to restrict language-specific rules.

        Returns:
            List of finding dicts with keys: ruleId, message, severity, file, line, column.
        """
        if not code:
            return []

        if filename is None:
            filename = "scan_target.py"

        # Determine file extension for language filtering
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        findings: List[Dict[str, Any]] = []

        lines = code.splitlines()

        for rule in self.rules:
            # Skip rules that don't apply to this language
            if rule["languages"] is not None and ext not in rule["languages"]:
                continue

            pattern: re.Pattern = rule["pattern"]

            # Line-by-line scan for accurate line numbers
            for line_no, line in enumerate(lines, start=1):
                match = pattern.search(line)
                if match:
                    findings.append({
                        "ruleId": rule["id"],
                        "message": rule["description"],
                        "severity": rule["severity"],
                        "file": filename,
                        "line": line_no,
                        "column": match.start() + 1,
                        "snippet": line.strip()[:200],
                    })

        return findings
