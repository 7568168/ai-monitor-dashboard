from pydantic import BaseModel
from typing import List, Dict, Optional

class CPUInfo(BaseModel):
    percent: float
    cores: List[Dict[str, float]]
    count: int
    frequency_mhz: float
    load_1m: float
    load_5m: float
    load_15m: float

class MemoryInfo(BaseModel):
    total: int
    available: int
    used: int
    percent: float
    total_mb: float
    used_mb: float
    available_mb: float

class DiskInfo(BaseModel):
    mountpoint: str
    fstype: str
    total: int
    used: int
    free: int
    percent: float
    total_gb: float
    used_gb: float
    free_gb: float

class NetworkInfo(BaseModel):
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    bytes_sent_mb: float
    bytes_recv_mb: float
    connections_count: int
    tcp_states: Dict[str, int]

class ProcessInfo(BaseModel):
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    status: str

class SystemMetrics(BaseModel):
    cpu: CPUInfo
    memory: MemoryInfo
    disk: List[DiskInfo]
    network: NetworkInfo
    processes: List[ProcessInfo]
    timestamp: int

class HealthResponse(BaseModel):
    status: str

class DiagnosisRequest(BaseModel):
    type: str = "quick"
    metrics: Optional[Dict] = None
