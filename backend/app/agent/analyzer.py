import os
import re
from typing import List, Dict

LOG_PATHS = ["/var/log/syslog", "/var/log/messages", "/var/log/kern.log", "/var/log/auth.log", "/var/log/dpkg.log"]

ERROR_PATTERNS = [
    (re.compile(r'error|fail|critical|emergency', re.IGNORECASE), "error"),
    (re.compile(r'warning|warn', re.IGNORECASE), "warning"),
    (re.compile(r'oom|out of memory|killed process', re.IGNORECASE), "critical"),
    (re.compile(r'segfault|bus error', re.IGNORECASE), "critical"),
    (re.compile(r'disk.*full|no space left', re.IGNORECASE), "critical"),
]

class LogAnalyzer:
    def analyze_logs(self, max_lines: int = 1000) -> List[Dict]:
        findings = []
        for log_path in LOG_PATHS:
            if not os.path.exists(log_path):
                continue
            try:
                with open(log_path, 'r', errors='replace') as f:
                    lines = f.readlines()[-max_lines:]
                    for line in lines:
                        for pattern, severity in ERROR_PATTERNS:
                            if pattern.search(line):
                                findings.append({"source": log_path, "severity": severity, "message": line.strip()[:200]})
                                break
            except (PermissionError, OSError):
                continue
        seen = set()
        unique = []
        for f in findings:
            key = (f["source"], f["message"][:100])
            if key not in seen:
                seen.add(key)
                unique.append(f)
        return unique[:50]
