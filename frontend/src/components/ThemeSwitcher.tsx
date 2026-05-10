import React from 'react';

const themes = [{ id: 'datadog', label: 'Datadog' }, { id: 'vercel', label: 'Vercel' }, { id: 'grafana', label: 'Grafana' }];

export default function ThemeSwitcher() {
  const [active, setActive] = React.useState('datadog');
  React.useEffect(() => { document.documentElement.setAttribute('data-theme', active); }, [active]);
  return (
    <div className="theme-switcher">
      {themes.map((t) => (<button key={t.id} className={`theme-btn ${active === t.id ? 'active' : ''}`} onClick={() => setActive(t.id)}>{t.label}</button>))}
    </div>
  );
}
