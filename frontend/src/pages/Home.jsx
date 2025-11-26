import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import GoalInput from '../components/GoalInput.jsx';
import Results from '../components/Results.jsx';
import Loader from '../components/Loader.jsx';
import { executeAgent } from '../api/agent.js';

const Home = () => {
  const [goal, setGoal] = useState('');
  const [maxSteps, setMaxSteps] = useState(5);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!goal.trim()) {
      setError('Please enter a goal to get started.');
      return;
    }
    
    setError(null);
    setLoading(true);
    setData(null);
    
    try {
      const payload = {
        plan_request: {
          goal: goal.trim(),
          max_steps: maxSteps
        }
      };
      const response = await executeAgent(payload);
      setData(response);
      
      // Scroll to results
      setTimeout(() => {
        const resultsElement = document.querySelector('.results-panel');
        if (resultsElement) {
          resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    } catch (err) {
      console.error('Execution error:', err);
      setError(
        err.response?.data?.detail || 
        err.message || 
        'An error occurred while executing the automation. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setGoal('');
    setMaxSteps(5);
    setData(null);
    setError(null);
  };

  return (
    <main className="app-shell">
      {/* Hero Section */}
      <motion.section 
        className="hero-card"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div>
          <p className="eyebrow">Agentic AI Automator</p>
          <h1>Autonomous Research Assistant</h1>
          <p className="muted">
            Transform natural language goals into actionable research workflows. 
            Our AI agent automatically selects tools, explores the web, searches GitHub, 
            and delivers comprehensive insights.
          </p>
        </div>
        
        <GoalInput
          goal={goal}
          maxSteps={maxSteps}
          onGoalChange={setGoal}
          onStepsChange={setMaxSteps}
          onSubmit={handleSubmit}
          disabled={loading}
        />

        {/* Example Goals */}
        {!data && !loading && (
          <motion.div
            style={{
              marginTop: '1rem',
              padding: '1.5rem',
              background: 'rgba(0, 0, 0, 0.2)',
              borderRadius: 'var(--radius)',
              border: '1px solid var(--border)'
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <p style={{ 
              fontSize: '0.85rem', 
              fontWeight: 600, 
              marginBottom: '0.75rem',
              color: 'rgba(255,255,255,0.7)'
            }}>
              💡 Example Goals:
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {[
                'Compare the latest Groq AI models',
                'Find popular Python web frameworks on GitHub',
                'Research recent advances in transformer architectures',
                'Search for React component libraries'
              ].map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => setGoal(example)}
                  style={{
                    padding: '0.5rem 1rem',
                    background: 'rgba(59, 130, 246, 0.1)',
                    border: '1px solid rgba(59, 130, 246, 0.3)',
                    borderRadius: '999px',
                    color: '#60a5fa',
                    fontSize: '0.85rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = 'rgba(59, 130, 246, 0.2)';
                    e.target.style.borderColor = 'rgba(59, 130, 246, 0.5)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = 'rgba(59, 130, 246, 0.1)';
                    e.target.style.borderColor = 'rgba(59, 130, 246, 0.3)';
                  }}
                >
                  {example}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </motion.section>

      {/* Loading State */}
      <AnimatePresence>
        {loading && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
          >
            <Loader label="Running autonomous agent..." />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error State */}
      <AnimatePresence>
        {error && (
          <motion.div
            className="error-banner"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
          >
            <strong>⚠️ Error:</strong> {error}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Results */}
      <AnimatePresence>
        {data && !loading && (
          <>
            <Results response={data} />
            
            {/* Action Buttons */}
            <motion.div
              style={{
                display: 'flex',
                gap: '1rem',
                justifyContent: 'center',
                marginTop: '2rem'
              }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <button
                onClick={handleReset}
                style={{
                  padding: '0.75rem 2rem',
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '1px solid var(--border)',
                  borderRadius: '999px',
                  color: 'white',
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = 'rgba(255, 255, 255, 0.15)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = 'rgba(255, 255, 255, 0.1)';
                }}
              >
                🔄 New Search
              </button>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </main>
  );
};

export default Home;