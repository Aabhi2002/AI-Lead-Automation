import { useState } from 'react'
import './App.css'
import LeadQualificationTool from './components/LeadQualificationTool'
import AnalyticsDashboard from './components/AnalyticsDashboard'

function App() {
  const [activeTab, setActiveTab] = useState('qualification')

  return (
    <div className="app">
      <header className="app-header">
        <h1>Lead Management System</h1>
        <nav className="nav-tabs">
          <button
            className={activeTab === 'qualification' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('qualification')}
          >
            Lead Qualification
          </button>
          <button
            className={activeTab === 'analytics' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('analytics')}
          >
            Analytics Dashboard
          </button>
        </nav>
      </header>

      <main className="app-main">
        {activeTab === 'qualification' && <LeadQualificationTool />}
        {activeTab === 'analytics' && <AnalyticsDashboard />}
      </main>
    </div>
  )
}

export default App
