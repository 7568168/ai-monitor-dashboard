import React from 'react';
import { useState } from 'react';

interface AIChatProps { metrics: any; onClose: () => void; }

export default function AIChat({ metrics, onClose }: AIChatProps) {
  const [diagnosis, setDiagnosis] = useState('');
  const [loading, setLoading] = useState(false);

  const runDiagnosis = async (type: string) => {
    setLoading(true); setDiagnosis('');
    try {
      const res = await fetch('/api/diagnose', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ type, metrics }) });
      const reader = res.body?.getReader();
      if (!reader) return;
      const decoder = new TextDecoder();
      let fullText = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        for (const line of chunk.split('\n')) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.step) fullText += `\n### ${data.step}\n`;
              if (data.content) fullText += data.content;
              setDiagnosis(fullText);
            } catch {}
          }
        }
      }
    } catch (e: any) { setDiagnosis(`Diagnosis failed: ${e.message}`); }
    finally { setLoading(false); }
  };

  return (
    <div className="ai-chat">
      <div className="ai-chat-header"><h2>AI Intelligent Diagnosis</h2><button onClick={onClose}>Close</button></div>
      <div className="ai-chat-actions">
        <button onClick={() => runDiagnosis('quick')} disabled={loading}>Quick Diagnose</button>
        <button onClick={() => runDiagnosis('full')} disabled={loading}>Full Diagnose</button>
        <button onClick={() => runDiagnosis('logs')} disabled={loading}>Log Analysis</button>
      </div>
      <div className="ai-chat-output">
        {loading && <div className="loading-indicator">AI is analyzing...</div>}
        <pre>{diagnosis}</pre>
      </div>
    </div>
  );
}
