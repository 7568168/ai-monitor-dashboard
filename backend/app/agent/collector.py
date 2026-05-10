import psutil
import os
from app.models.metrics import SystemMetrics, CPUInfo, MemoryInfo, DiskInfo, NetworkInfo, ProcessInfo
import time

class SystemMetricsCollector:
    def collect_cpu(self) -> CPUInfo:
        cores = [{"core": i, "percent": pct} for i, pct in enumerate(psutil.cpu_percent(interval=0.1, percpu=True))]
        freq = psutil.cpu_freq()
        load = os.getloadavg()
        return CPUInfo(
            percent=psutil.cpu_percent(interval=0.1), cores=cores, count=psutil.cpu_count(),
            frequency_mhz=round(freq.current / 1000 if freq else 0, 1),
            load_1m=round(load[0], 2), load_5m=round(load[1], 2), load_15m=round(load[2], 2),
        )

    def collect_memory(self) -> MemoryInfo:
        mem = psutil.virtual_memory()
        return MemoryInfo(
            total=mem.total, available=mem.available, used=mem.used, percent=mem.percent,
            total_mb=round(mem.total / (1024*1024), 1), used_mb=round(mem.used / (1024*1024), 1),
            available_mb=round(mem.available / (1024*1024), 1),
        )

    def collect_disk(self) -> list:
        disks = []
        for p in psutil.disk_partitions(all=False):
            try:
                u = psutil.disk_usage(p.mountpoint)
                disks.append(DiskInfo(
                    mountpoint=p.mountpoint, fstype=p.fstype, total=u.total, used=u.used, free=u.free,
                    percent=u.percent, total_gb=round(u.total/(1024**3), 1),
                    used_gb=round(u.used/(1024**3), 1), free_gb=round(u.free/(1024**3), 1),
                ))
            except (PermissionError, OSError):
                continue
        return disks

    def collect_network(self) -> NetworkInfo:
        net_io = psutil.net_io_counters()
        conns = psutil.net_connections(kind='inet')
        tcp_states = {}
        for c in conns:
            tcp_states[c.status] = tcp_states.get(c.status, 0) + 1
        return NetworkInfo(
            bytes_sent=net_io.bytes_sent, bytes_recv=net_io.bytes_recv,
            packets_sent=net_io.packets_sent, packets_recv=net_io.packets_recv,
            bytes_sent_mb=round(net_io.bytes_sent/(1024**2), 2),
            bytes_recv_mb=round(net_io.bytes_recv/(1024**2), 2),
            connections_count=len(conns), tcp_states=tcp_states,
        )

    def collect_processes(self) -> list:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                processes.append(ProcessInfo(
                    pid=info['pid'], name=info['name'] or 'unknown',
                    cpu_percent=round(info['cpu_percent'] or 0, 1),
                    memory_percent=round(info['memory_percent'] or 0, 1),
                    status=info['status'] or 'unknown',
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        processes.sort(key=lambda p: p.memory_percent, reverse=True)
        return processes[:20]

    def collect_all(self) -> SystemMetrics:
        return SystemMetrics(
            cpu=self.collect_cpu(), memory=self.collect_memory(),
            disk=self.collect_disk(), network=self.collect_network(),
            processes=self.collect_processes(), timestamp=int(time.time()),
        )
