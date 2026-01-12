import { useState } from 'react'

const LeadQualificationTool = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        company: '',
        message: ''
    })
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    const handleInputChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await fetch('http://localhost:8000/submit-lead', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const data = await response.json()
            setResult(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const getCategoryColor = (category) => {
        switch (category?.toLowerCase()) {
            case 'hot': return '#e74c3c'
            case 'warm': return '#f39c12'
            case 'cold': return '#3498db'
            default: return '#95a5a6'
        }
    }

    return (
        <div className="qualification-tool">
            <h2>Lead Qualification Tool</h2>

            <form onSubmit={handleSubmit} className="lead-form">
                <div className="form-group">
                    <label htmlFor="name">Name *</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="email">Email *</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="company">Company *</label>
                    <input
                        type="text"
                        id="company"
                        name="company"
                        value={formData.company}
                        onChange={handleInputChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="message">Message *</label>
                    <textarea
                        id="message"
                        name="message"
                        value={formData.message}
                        onChange={handleInputChange}
                        rows="4"
                        required
                    />
                </div>

                <button type="submit" disabled={loading} className="submit-btn">
                    {loading ? 'Running AI Qualification...' : 'Run AI Qualification'}
                </button>
            </form>

            {error && (
                <div className="error-message">
                    <h3>Error</h3>
                    <p>{error}</p>
                </div>
            )}

            {result && (
                <div className="results">
                    <h3>AI Qualification Results</h3>

                    <div className="result-cards">
                        <div className="result-card">
                            <h4>Score</h4>
                            <div className="score">{result.score}/100</div>
                        </div>

                        <div className="result-card">
                            <h4>Category</h4>
                            <div
                                className="category"
                                style={{ color: getCategoryColor(result.category) }}
                            >
                                {result.category}
                            </div>
                        </div>

                        <div className="result-card">
                            <h4>Recommended Action</h4>
                            <div className="action">{result.action}</div>
                        </div>
                    </div>

                    <div className="result-details">
                        <div className="detail-section">
                            <h4>AI Reasoning</h4>
                            <p>{result.reason}</p>
                        </div>

                        {result.enrichment_summary && (
                            <div className="detail-section">
                                <h4>Enrichment Summary</h4>
                                <p>{result.enrichment_summary}</p>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    )
}

export default LeadQualificationTool