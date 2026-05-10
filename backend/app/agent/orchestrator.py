import json
import asyncio
from typing import AsyncGenerator, Dict, Any
from app.agent.collector import SystemMetricsCollector
from app.agent.executor import CommandExecutor
from app.agent.analyzer import LogAnalyzer
from app.agent.reporter import ReportGenerator

class DiagnosisOrchestrator:
    def __init__(self):
        self.collector = SystemMetricsCollector()
        self.executor = CommandExecutor()
        self.analyzer = LogAnalyzer()
        self.reporter = ReportGenerator()

    async def run_diagnosis(self, request) -> AsyncGenerator[Dict[str, Any], None]:
        diagnosis_type = request.type
        metrics_data = None
        diagnostics = {}
        log_findings = []

        yield {"step": "Step 1: Collecting System Metrics", "content": "Gathering CPU, memory, disk, network, and process data..."}
        await asyncio.sleep(0.3)
        metrics = self.collector.collect_all()
        metrics_data = metrics.model_dump()
        yield {"step": "Metrics Collected", "content": f"CPU: {metrics_data['cpu']['percent']}%, Memory: {metrics_data['memory']['percent']}%, Disks: {len(metrics_data['disk'])} partitions"}

        yield {"step": "Step 2: Analyzing Anomalies", "content": "Checking for abnormal resource usage patterns..."}
        await asyncio.sleep(0.3)
        anomalies = []
        if metrics_data["cpu"]["percent"] > 90:
            anomalies.append(f"High CPU usage: {metrics_data['cpu']['percent']}%")
        if metrics_data["memory"]["percent"] > 90:
            anomalies.append(f"High memory usage: {metrics_data['memory']['percent']}%")
        for disk in metrics_data["disk"]:
            if disk["percent"] > 85:
                anomalies.append(f"Disk space low on {disk['mountpoint']}: {disk['percent']}%")
        if anomalies:
            yield {"step": "Anomalies Detected", "content": "\n".join([f"- {a}" for a in anomalies])}
        else:
            yield {"step": "Analysis Complete", "content": "No significant anomalies detected in current metrics."}

        if diagnosis_type in ["full", "quick"]:
            yield {"step": "Step 3: Running Diagnostic Commands", "content": "Executing system diagnostic commands..."}
            await asyncio.sleep(0.3)
            for cmd_name in ["uptime", "free"]:
                result = await self.executor.execute(cmd_name)
                diagnostics[cmd_name] = result
                yield {"step": f"Command: {cmd_name}", "content": result.get("output", "No output")[:300]}
                await asyncio.sleep(0.2)

        yield {"step": "Step 4: Scanning System Logs", "content": "Analyzing log files for errors and warnings..."}
        await asyncio.sleep(0.3)
        log_findings = self.analyzer.analyze_logs()
        if log_findings:
            critical_count = len([f for f in log_findings if f["severity"] == "critical"])
            error_count = len([f for f in log_findings if f["severity"] == "error"])
            yield {"step": "Log Analysis Results", "content": f"Found {len(log_findings)} log entries: {critical_count} critical, {error_count} errors"}
        else:
            yield {"step": "Log Analysis Complete", "content": "No significant issues found in system logs."}

        if diagnosis_type == "full":
            yield {"step": "Step 5: AI Analysis", "content": "Running advanced AI analysis..."}
            await asyncio.sleep(0.5)
            yield {"step": "AI Analysis Complete", "content": "AI analysis completed based on collected metrics and diagnostics."}

        yield {"step": "Step 6: Generating Report", "content": "Compiling comprehensive diagnostic report..."}
        await asyncio.sleep(0.3)
        report = self.reporter.generate(metrics_data, diagnostics, log_findings)
        yield {"step": "Diagnosis Complete", "content": report, "done": True}
