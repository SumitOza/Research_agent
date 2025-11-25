import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    apiKey: '',
    researchTopic: '',
    targetDemographic: '',
    sampleSize: 4,
    numQuestions: 4
  })
  
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [showDetails, setShowDetails] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'sampleSize' || name === 'numQuestions' ? parseInt(value) : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResults(null)
    setShowDetails(false)

    try {
      const response = await axios.post('/api/research', {
        api_key: formData.apiKey,
        research_topic: formData.researchTopic,
        target_demographic: formData.targetDemographic,
        sample_size: formData.sampleSize,
        num_questions: formData.numQuestions
      })

      if (response.data.success) {
        setResults(response.data)
      } else {
        setError(response.data.error || 'Research failed')
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header>
          <h1>🔬 Research Agent</h1>
          <p>AI-Powered Research Interview System</p>
        </header>

        <form onSubmit={handleSubmit} className="research-form">
          <div className="form-group">
            <label htmlFor="apiKey">Cerebras API Key *</label>
            <input
              type="password"
              id="apiKey"
              name="apiKey"
              value={formData.apiKey}
              onChange={handleChange}
              required
              placeholder="Enter your Cerebras API key"
            />
          </div>

          <div className="form-group">
            <label htmlFor="researchTopic">Research Topic *</label>
            <input
              type="text"
              id="researchTopic"
              name="researchTopic"
              value={formData.researchTopic}
              onChange={handleChange}
              required
              placeholder="e.g., Impact of aging population on healthcare"
            />
          </div>

          <div className="form-group">
            <label htmlFor="targetDemographic">Target Demographic *</label>
            <input
              type="text"
              id="targetDemographic"
              name="targetDemographic"
              value={formData.targetDemographic}
              onChange={handleChange}
              required
              placeholder="e.g., Healthcare professionals aged 30-50"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="sampleSize">Sample Size (Interviews) *</label>
              <input
                type="number"
                id="sampleSize"
                name="sampleSize"
                value={formData.sampleSize}
                onChange={handleChange}
                required
                min="1"
                max="20"
              />
            </div>

            <div className="form-group">
              <label htmlFor="numQuestions">Questions per Interview *</label>
              <input
                type="number"
                id="numQuestions"
                name="numQuestions"
                value={formData.numQuestions}
                onChange={handleChange}
                required
                min="1"
                max="10"
              />
            </div>
          </div>

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? '🔄 Running Research...' : '🚀 Start Research'}
          </button>
        </form>

        {error && (
          <div className="error-box">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {results && (
          <div className="results-container">
            <div className="results-header">
              <h2>📊 Research Analysis</h2>
              <button 
                onClick={() => setShowDetails(!showDetails)}
                className="toggle-btn"
              >
                {showDetails ? 'Hide' : 'Show'} Questions & Answers
              </button>
            </div>

            <div className="synthesis-box">
              <h3>Key Insights</h3>
              <div className="synthesis-content">
                {results.synthesis ? (
                  <div className="synthesis-text">
                    {results.synthesis.split('\n').map((line, idx) => (
                      <p key={idx}>{line}</p>
                    ))}
                  </div>
                ) : (
                  <p>No synthesis available</p>
                )}
              </div>
            </div>

            {showDetails && (
              <div className="details-container">
                {results.questions && (
                  <div className="questions-box">
                    <h3>Interview Questions</h3>
                    <ol>
                      {results.questions.map((q, idx) => (
                        <li key={idx}>{q}</li>
                      ))}
                    </ol>
                  </div>
                )}

                {results.interviews && results.interviews.length > 0 && (
                  <div className="interviews-box">
                    <h3>Interview Responses</h3>
                    {results.interviews.map((interview, idx) => (
                      <div key={idx} className="interview-card">
                        <div className="persona-header">
                          <h4>
                            {interview.persona.name} ({interview.persona.age}, {interview.persona.job})
                          </h4>
                          <p className="persona-traits">
                            Traits: {Array.isArray(interview.persona.traits) 
                              ? interview.persona.traits.join(', ') 
                              : interview.persona.traits}
                          </p>
                        </div>
                        <div className="responses">
                          {interview.responses.map((qa, qIdx) => (
                            <div key={qIdx} className="qa-pair">
                              <div className="question">
                                <strong>Q{qIdx + 1}:</strong> {qa.question}
                              </div>
                              <div className="answer">
                                <strong>A{qIdx + 1}:</strong> {qa.answer}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App

