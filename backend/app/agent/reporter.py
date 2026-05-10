from typing import Dict, List

class ReportGenerator:
    def generate(self, metrics: Dict, diagnostics: Dict, log_findings: List) -> str:
        report = ["# System Diagnostic Report", ""]
        report.append("## Summary")
        report.append("")
        cpu_pct = metrics.get("cpu", {}).get("percent", 0)
        mem_pct = metrics.get("memory", {}).get("percent", 0)
        overall = "critical" if cpu_pct > 90 or mem_pct > 90 else "warning" if cpu_pct > 75 or mem_pct > 75 else "healthy"
        report.append(f"Overall Status: **{overall.upper()}**")
        report.append(f"CPU Usage: {cpu_pct}%")
        report.append(f"Memory Usage: {mem_pct}%")
        report.append("")
        report.append("## CPU Analysis")
        report.append("")
        if cpu_pct > 90:
            report.extend([f"- **CRITICAL**: CPU usage is at {cpu_pct}%", "- High CPU usage may cause system slowdowns", "- Check for runaway processes with `top` command", ""])
        elif cpu_pct > 75:
            report.extend([f"- **WARNING**: CPU usage is elevated at {cpu_pct}%", "- Monitor for further increase", ""])
        else:
            report.extend([f"- CPU usage is normal at {cpu_pct}%", ""])
        report.append("## Memory Analysis")
        report.append("")
        mem_mb = metrics.get("memory", {}).get("total_mb", 0)
        mem_used = metrics.get("memory", {}).get("used_mb", 0)
        if mem_pct > 90:
            report.extend([f"- **CRITICAL**: Memory usage is at {mem_pct}% ({mem_used}/{mem_mb} MB)", "- System may start swapping", "- Consider killing unused processes or adding more RAM", ""])
        elif mem_pct > 75:
            report.extend([f"- **WARNING**: Memory usage is elevated at {mem_pct}%", "- Monitor for memory leaks", ""])
        else:
            report.extend([f"- Memory usage is normal at {mem_pct}% ({mem_used}/{mem_mb} MB)", ""])
        report.append("## Disk Analysis")
        report.append("")
        for disk in metrics.get("disk", []):
            pct = disk.get("percent", 0)
            mount = disk.get("mountpoint", "unknown")
            if pct > 85:
                report.extend([f"- **CRITICAL**: {mount} is at {pct}% capacity", "- Clean up old logs, temp files, or unused packages", ""])
            elif pct > 70:
                report.extend([f"- **WARNING**: {mount} is at {pct}% capacity", "- Consider planning for storage expansion", ""])
            else:
                report.extend([f"- {mount}: {pct}% used (OK)", ""])
        if log_findings:
            report.append("## Log Findings")
            report.append("")
            critical = len([f for f in log_findings if f["severity"] == "critical"])
            errors = len([f for f in log_findings if f["severity"] == "error"])
            warnings = len([f for f in log_findings if f["severity"] == "warning"])
            report.extend([f"- Critical: {critical}", f"- Errors: {errors}", f"- Warnings: {warnings}", ""])
        report.append("## Recommendations")
        report.append("")
        recs = []
        if cpu_pct > 90: recs.extend(["1. Investigate high CPU processes with `top` or `htop`", "2. Check for runaway or zombie processes"])
        if mem_pct > 90: recs.extend(["3. Free up memory by stopping unused services", "4. Consider adding swap space if none exists"])
        for disk in metrics.get("disk", []):
            if disk.get("percent", 0) > 85:
                recs.append(f"5. Clean up {disk['mountpoint']} - remove old logs and temp files")
        if not recs:
            recs.append("- System is running normally. No immediate action required.")
        report.extend(recs)
        return "\n".join(report)
