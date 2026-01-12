import { useState, useEffect } from 'react'

const AnalyticsDashboard = () => {
    const [metrics, setMetrics] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        fetchMetrics()
    }, [])

    const fetchMetrics = async () => {
        setLoading(true)
        setError(null)

        try {
            const response = await fetch('http://localhost:8000/metrics')

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const data = await response.json()
            setMetrics(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const formatScore = (score) => {
        return score ? score.toFixed(1) : '0.0'
    }

    if (loading) {
        return (
            <div className="analytics-dashboard">
                <h2>Analytics Dashboard</h2>
                <div className="loading">Loading metrics...</div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="analytics-dashboard">
                <h2>Analytics Dashboard</h2>
                <div className="error-message">
                    <h3>Error Loading Metrics</h3>
                    <p>{error}</p>
                    <button onClick={fetchMetrics} className="retry-btn">
                        Retry
                    </button>
                </div>
            </div>
        )
    }

    return (
        <div className="analytics-dashboard">
            <div className="dashboard-header">
                <h2>Analytics Dashboard</h2>
                <button onClick={fetchMetrics} className="refresh-btn">
                    Refresh
                </button>
            </div>

            <div className="metrics-grid">
                <div className="metric-card total">
                    <h3>Total Leads</h3>
                    <div className="metric-value">{metrics?.total_leads || 0}</div>
                </div>

                <div className="metric-card hot">
                    <h3>Hot Leads</h3>
                    <div className="metric-value">{metrics?.hot_leads || 0}</div>
                </div>

                <div className="metric-card warm">
                    <h3>Warm Leads</h3>
                    <div className="metric-value">{metrics?.warm_leads || 0}</div>
                </div>

                <div className="metric-card cold">
                    <h3>Cold Leads</h3>
                    <div className="metric-value">{metrics?.cold_leads || 0}</div>
                </div>

                <div className="metric-card average">
                    <h3>Average Score</h3>
                    <div className="metric-value">{formatScore(metrics?.avg_score)}</div>
                </div>
            </div>

            {metrics && (
                <div className="metrics-summary">
                    <h3>Summary</h3>
                    <div className="summary-stats">
                        <p>
                            <strong>Conversion Rate:</strong> {' '}
                            {metrics.total_leads > 0
                                ? ((metrics.hot_leads / metrics.total_leads) * 100).toFixed(1)
                                : '0.0'
                            }% of leads are hot
                        </p>
                        <p>
                            <strong>Quality Distribution:</strong> {' '}
                            Hot: {metrics.hot_leads},
                            Warm: {metrics.warm_leads},
                            Cold: {metrics.cold_leads}
                        </p>
                    </div>
                </div>
            )}
        </div>
    )
}

export default AnalyticsDashboard