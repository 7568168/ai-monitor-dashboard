import { useState, useEffect } from 'react';
import ThemeSwitcher from './components/ThemeSwitcher';
import MonitoringPanel from './components/MonitoringPanel';
import AIChat from './components/AIChat';

interface Metrics {
  cpu: { percent: number; cores: Array<{ percent: number }> };
  memory: { total: number; available: number; used: number; percent: number };
  disk: Array<{ mount: string; total: number; used: number; percent: number; fstype: string }>;
  network: { bytes_sent: number; bytes_recv: number; packets_sent: number; packets_recv: number };
  processes: Array<{ pid: number; name: string; cpu_percent: number; memory_percent: number; status: string }>;
  timestamp: number;
}

interface Alert {
  type: 'critical' | 'warning';
  message: string;
  metric: string;
}

function App() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAIChat, setShowAIChat] = useState(false);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await fetch('/api/metrics');
        if (!res.ok) throw new Error('Failed to fetch metrics');
        const data = await res.json();
        setMetrics(data);
        setLastUpdate(new Date());
        setError(null);
        const newAlerts: Alert[] = [];
        if (data.cpu.percent > 90) newAlerts.push({ type: 'critical', message: `CPU usage high: ${data.cpu.percent.toFixed(1)}%`, metric: 'cpu' });
        else if (data.cpu.percent > 75) newAlerts.push({ type: 'warning', message: `CPU usage elevated: ${data.cpu.percent.toFixed(1)}%`, metric: 'cpu' });
        if (data.memory.percent > 90) newAlerts.push({ type: 'critical', message: `Memory usage high: ${data.memory.percent.toFixed(1)}%`, metric: 'memory' });
        else if (data.memory.percent > 75) newAlerts.push({ type: 'warning', message: `Memory usage elevated: ${data.memory.percent.toFixed(1)}%`, metric: 'memory' });
        data.disk.forEach((d: any) => {
          if (d.percent > 85) newAlerts.push({ type: 'critical', message: `${d.mount} disk low: ${d.percent.toFixed(1)}%`, metric: 'disk' });
          else if (d.percent > 70) newAlerts.push({ type: 'warning', message: `${d.mount} disk space limited: ${d.percent.toFixed(1)}%`, metric: 'disk' });
        });
        setAlerts(newAlerts);
      } catch (err: any) { setError(err.message); }
      finally { setLoading(false); }
    };
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleDiagnose = () => setShowAIChat(true);
  const handleCloseAIChat = () => setShowAIChat(false);

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <div className="app-logo">🚀</div>
          <h1 className="app-title">AI Monitor Dashboard</h1>
          <span className="app-subtitle">Intelligent Diagnostics · Real-time Monitoring · 3 Themes</span>
        </div>
        <div className="header-right">
          <span className="status-text">System OK</span>
          <div className="status-dot"></div>
          <button className="ai-btn" onClick={() => setShowAIChat(!showAIChat)}>
            <span className="ai-btn-icon">✨</span>
            <span>{showAIChat ? 'Back to Monitor' : 'AI Diagnose'}</span>
          </button>
          <ThemeSwitcher />
        </div>
      </header>
      {alerts.length > 0 && (
        <div className="alerts-bar">
          {alerts.map((alert, idx) => (
            <div key={idx} className={`alert-item ${alert.type === 'critical' ? 'alert-critical' : 'alert-warning'}`}>
              <span className="alert-icon">{alert.type === 'critical' ? '🔴' : '⚠️'}</span>
              <span className="alert-msg">{alert.message}</span>
              <button className="alert-action" onClick={handleDiagnose}>Diagnose</button>
            </div>
          ))}
        </div>
      )}
      <main className="app-main">
        {loading && <div className="loading">Loading metrics...</div>}
        {error && <div className="loading">Error: {error}</div>}
        {!loading && !error && metrics && (
          showAIChat ? <AIChat metrics={metrics} onClose={handleCloseAIChat} /> : <MonitoringPanel metrics={metrics} onDiagnose={handleDiagnose} />
        )}
      </main>
      <footer className="app-footer">
        <div>Last update: <span className="update-time">{lastUpdate.toLocaleTimeString()}</span></div>
        <div>Auto-refresh every 3 seconds</div>
      </footer>
    </div>
  );
}

export default App;
