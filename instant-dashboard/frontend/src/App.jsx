import { useState } from 'react';
import './App.css';
import JsonInput from './components/JsonInput';
import PromptInput from './components/PromptInput';
import GenerateButton from './components/GenerateButton';
import DashboardPreview from './components/DashboardPreview';

// Example data for quick testing
const EXAMPLE_DATA = {
  "report_title": "Monthly Office Spending",
  "currency": "USD",
  "expenses": [
    { "item": "High-speed Internet", "amount": 250 },
    { "item": "Coffee & Snacks", "amount": 400 },
    { "item": "Software Subscriptions", "amount": 1200 },
    { "item": "Office Electricity", "amount": 350 }
  ]
};

const EXAMPLE_PROMPT = "Design a sleek analytics dashboard with a dark theme (dark blue/black background). Display key metrics as glowing cards with gradient borders. Create a vibrant bar chart for regional performance using different colors for each region. Show top products in a ranked list with progress bars. Make it look like a high-tech analytics platform.";

function App() {
  const [jsonData, setJsonData] = useState('');
  const [userPrompt, setUserPrompt] = useState(EXAMPLE_PROMPT); // Pre-filled with default prompt
  const [temperature, setTemperature] = useState(0.3);
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleGenerate = async () => {
    // Reset states
    setError('');
    setSuccess(false);
    setIsLoading(true);

    try {
      // Validate JSON
      try {
        JSON.parse(jsonData);
      } catch (e) {
        throw new Error('Invalid JSON format. Please check your JSON syntax.');
      }

      // Validate prompt
      if (!userPrompt.trim()) {
        throw new Error('Please enter a prompt describing how you want the dashboard to look.');
      }

      // Call backend API
      const response = await fetch('http://localhost:8000/generate-dashboard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          json_data: jsonData,
          user_prompt: userPrompt,
          temperature: temperature,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate dashboard');
      }

      if (data.success) {
        setGeneratedHtml(data.html_content);
        setSuccess(true);
        setTimeout(() => setSuccess(false), 3000);
      } else {
        throw new Error(data.error || 'Failed to generate dashboard');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const loadExample = () => {
    setJsonData(JSON.stringify(EXAMPLE_DATA, null, 2));
    setUserPrompt(EXAMPLE_PROMPT);
    setError('');
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">📊</div>
            <div>
              <h1>The Instant Dashboard</h1>
              <p className="subtitle">Transform JSON into beautiful dashboards with AI</p>
            </div>
          </div>
          <button className="btn btn-secondary" onClick={loadExample}>
            <span className="btn-icon">✨</span>
            Load Example
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container">
        {/* Input Section */}
        <div className="grid">
          <JsonInput value={jsonData} onChange={setJsonData} />
          <PromptInput value={userPrompt} onChange={setUserPrompt} />
        </div>

        {/* Temperature Control */}
        <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
          <div className="card-header">
            <h2 className="card-title">
              <span className="card-icon">🌡️</span>
              AI Temperature: {temperature.toFixed(1)}
            </h2>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              {temperature === 0 ? 'Deterministic' : temperature < 0.5 ? 'Consistent' : temperature < 1.0 ? 'Balanced' : temperature < 1.5 ? 'Creative' : 'Very Creative'}
            </span>
          </div>
          <div style={{ padding: '0 var(--spacing-xl) var(--spacing-lg)' }}>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '4px',
                background: `linear-gradient(to right, 
                  #3b82f6 0%, 
                  #6366f1 ${(temperature / 2) * 50}%, 
                  #8b5cf6 ${(temperature / 2) * 100}%, 
                  #d946ef ${(temperature / 2) * 100}%)`,
                outline: 'none',
                cursor: 'pointer',
              }}
            />
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: 'var(--spacing-sm)',
              fontSize: '0.75rem',
              color: 'var(--text-muted)'
            }}>
              <span>0.0 (Precise)</span>
              <span>1.0 (Balanced)</span>
              <span>2.0 (Creative)</span>
            </div>
            <div style={{
              marginTop: 'var(--spacing-sm)',
              fontSize: '0.875rem',
              color: 'var(--text-secondary)'
            }}>
              💡 Lower = more consistent results, Higher = more creative variations
            </div>
          </div>
        </div>

        {/* Generate Button */}
        <GenerateButton
          onClick={handleGenerate}
          isLoading={isLoading}
          disabled={!jsonData || !userPrompt}
        />

        {/* Error Message */}
        {error && (
          <div className="error-state">
            <div className="error-title">
              <span>⚠️</span>
              Error
            </div>
            <div className="error-message">{error}</div>
          </div>
        )}

        {/* Success Message */}
        {success && (
          <div className="success-state">
            <span>✓</span>
            Dashboard generated successfully!
          </div>
        )}

        {/* Preview Section */}
        <DashboardPreview
          htmlContent={generatedHtml}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
}

export default App;
