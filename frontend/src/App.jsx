import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    age: '35',
    sex: '0',
    cp: 'Asymptomatic',
    trestbps: '110',
    chol: '150',
    fbs: '0',
    restecg: '0',
    thalach: '180',
    exang: '0',
    oldpeak: '0.0',
    slope: 'Upsloping',
    ca: '0',
    thal: 'Normal'
  })

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [chatMessage, setChatMessage] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [chatLoading, setChatLoading] = useState(false)
  const chatEndRef = useRef(null)

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chatHistory, chatLoading])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handlePredict = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      const result = await response.json()
      setPrediction(result)
    } catch (error) {
      console.error('Prediction error:', error)
      setPrediction({ result: '❌ Error connecting to server', probability: 0 })
    } finally {
      setLoading(false)
    }
  }

  const handleChat = async (e) => {
    e.preventDefault()
    if (!chatMessage.trim()) return

    const userMessage = chatMessage
    setChatMessage('')
    setChatLoading(true)

    // Add user message to history
    setChatHistory(prev => [...prev, { 
      type: 'user', 
      message: userMessage,
      timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    }])

    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage })
      })

      const result = await response.json()

      // Add AI response to history
      setChatHistory(prev => [...prev, { 
        type: 'ai', 
        message: result.reply,
        timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      }])
    } catch (error) {
      console.error('Chat error:', error)
      setChatHistory(prev => [...prev, { 
        type: 'ai', 
        message: '⚠️ Connection error. Please try again!',
        timestamp: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
      }])
    } finally {
      setChatLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <div className="header-content">
          <h1>🫀 Heart Disease Prediction System</h1>
          <p>AI-powered heart disease risk assessment with intelligent medical chatbot</p>
        </div>
      </header>

      <div className="container">
        <div className="prediction-section">
          <div className="section-header">
            <h2>📋 Patient Assessment</h2>
            <span className="section-badge">ML Prediction</span>
          </div>
          <form onSubmit={handlePredict} className="prediction-form">
            <div className="form-grid">
              <div className="form-group">
                <label>Age:</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleInputChange}
                  required
                  min="29"
                  max="77"
                  placeholder="29 - 77"
                />
              </div>

              <div className="form-group">
                <label>Sex:</label>
                <select name="sex" value={formData.sex} onChange={handleInputChange} required>
                  <option value="">Select</option>
                  <option value="0">Female</option>
                  <option value="1">Male</option>
                </select>
              </div>

              <div className="form-group">
                <label>Chest Pain Type:</label>
                <select name="cp" value={formData.cp} onChange={handleInputChange} required>
                  <option value="">Select</option>
                  <option value="Typical Angina">Typical Angina</option>
                  <option value="Atypical Angina">Atypical Angina</option>
                  <option value="Non-anginal Pain">Non-anginal Pain</option>
                  <option value="Asymptomatic">Asymptomatic</option>
                </select>
              </div>

              <div className="form-group">
                <label>Resting Blood Pressure:</label>
                <input
                  type="number"
                  name="trestbps"
                  value={formData.trestbps}
                  onChange={handleInputChange}
                  required
                  min="94"
                  max="200"
                  placeholder="94 - 200"
                />
              </div>

              <div className="form-group">
                <label>Cholesterol:</label>
                <input
                  type="number"
                  name="chol"
                  value={formData.chol}
                  onChange={handleInputChange}
                  required
                  min="126"
                  max="564"
                  placeholder="126 - 564"
                />
              </div>

              <div className="form-group">
                <label>Fasting Blood Sugar &gt; 120 mg/dl:</label>
                <select name="fbs" value={formData.fbs} onChange={handleInputChange} required>
                  <option value="">Select</option>
                  <option value="0">No</option>
                  <option value="1">Yes</option>
                </select>
              </div>

              <div className="form-group">
                <label>Resting ECG:</label>
                <select name="restecg" value={formData.restecg} onChange={handleInputChange} required>
                  <option value="">Select</option>
                  <option value="0">Normal</option>
                  <option value="1">ST-T wave abnormality</option>
                  <option value="2">Left ventricular hypertrophy</option>
                </select>
              </div>

              <div className="form-group">
                <label>Max Heart Rate:</label>
                <input
                  type="number"
                  name="thalach"
                  value={formData.thalach}
                  onChange={handleInputChange}
                  required
                  min="71"
                  max="202"
                  placeholder="71 - 202"
                />
              </div>

              <div className="form-group">
                <label>Exercise Induced Angina:</label>
                <select name="exang" value={formData.exang} onChange={handleInputChange} required>
                  <option value="">Select</option>
                  <option value="0">No</option>
                  <option value="1">Yes</option>
                </select>
              </div>

              <div className="form-group">
                <label>ST Depression:</label>
                <input
                  type="number"
                  name="oldpeak"
                  value={formData.oldpeak}
                  onChange={handleInputChange}
                  required
                  min="0"
                  max="6.2"
                  step="0.1"
                  placeholder="0.0 - 6.2"
                />
              </div>

              <div className="form-group">
                <label>ST Slope:</label>
                <select name="slope" value={formData.slope} onChange={handleInputChange} required>
                  <option value="">Select</option>
                  <option value="Upsloping">Upsloping</option>
                  <option value="Flat">Flat</option>
                  <option value="Downsloping">Downsloping</option>
                </select>
              </div>

              <div className="form-group">
                <label>Major Vessels (0-3):</label>
                <input
                  type="number"
                  name="ca"
                  value={formData.ca}
                  onChange={handleInputChange}
                  required
                  min="0"
                  max="3"
                />
              </div>

              <div className="form-group">
                <label>Thalassemia:</label>
                <select name="thal" value={formData.thal} onChange={handleInputChange} required>
                  <option value="">Select</option>
                  <option value="Normal">Normal</option>
                  <option value="Fixed Defect">Fixed Defect</option>
                  <option value="Reversible Defect">Reversible Defect</option>
                </select>
              </div>
            </div>

            <button type="submit" disabled={loading} className="predict-btn">
              <span className="btn-icon">{loading ? '🔄' : '🔍'}</span>
              {loading ? 'Analyzing Patient Data...' : 'Predict Heart Disease Risk'}
            </button>
          </form>

          {prediction && (
            <div className={`result animate-in ${prediction.result === 'Invalid input values' ? 'invalid-input' : prediction.result.includes('High') ? 'high-risk' : prediction.result.includes('Moderate') ? 'moderate-risk' : 'low-risk'}`}>
              <div className="result-header">
                <h3>Prediction Result</h3>
                {prediction.result !== 'Invalid input values' && (
                  <span className="risk-badge">{(prediction.probability * 100).toFixed(1)}% Risk</span>
                )}
              </div>
              <div className="result-content">
                <p className="result-text">{prediction.result}</p>
                {prediction.result !== 'Invalid input values' ? (
                  <div className="risk-meter">
                    <div className="risk-bar">
                      <div 
                        className="risk-fill" 
                        style={{width: `${prediction.probability * 100}%`}}
                      ></div>
                    </div>
                    <p className="probability">Risk Probability: {(prediction.probability * 100).toFixed(1)}%</p>
                  </div>
                ) : (
                  prediction.message && <p className="error-message">⚠️ {prediction.message}</p>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="chat-section">
          <div className="section-header">
            <h2>🤖 AI Medical Assistant</h2>
            <span className="section-badge">Always Available</span>
          </div>
          <div className="chat-container">
            <div className="chat-messages">
              {chatHistory.length === 0 && (
                <div className="chat-welcome">
                  <div className="welcome-icon">🏥</div>
                  <h3>Welcome to AI Medical Assistant</h3>
                  <p>Ask me anything about heart health, symptoms, prevention, diet, exercise, and more!</p>
                </div>
              )}
              {chatHistory.map((msg, index) => (
                <div key={index} className={`message ${msg.type} animate-slideIn`}>
                  <div className="message-avatar">
                    {msg.type === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    <div className="message-header">
                      <strong>{msg.type === 'user' ? 'You' : 'Assistant'}</strong>
                      <span className="timestamp">{msg.timestamp}</span>
                    </div>
                    <p className="message-text">{msg.message}</p>
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div className="message ai animate-slideIn">
                  <div className="message-avatar">🤖</div>
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            <form onSubmit={handleChat} className="chat-form">
              <input
                type="text"
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                placeholder="Ask about heart health, symptoms, diet..."
                disabled={chatLoading}
                className="chat-input"
              />
              <button 
                type="submit" 
                disabled={chatLoading || !chatMessage.trim()}
                className="chat-submit"
              >
                <span>{chatLoading ? '⏳' : '➤'}</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
                