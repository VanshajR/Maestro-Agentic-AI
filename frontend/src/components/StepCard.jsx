import { motion } from 'framer-motion';

const StepCard = ({ step, result }) => {
  const hasError = result?.error;
  
  return (
    <motion.li 
      layout 
      className="step-card"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <header>
        <span className="pill">Step {step.id}</span>
        <h3>{step.description}</h3>
      </header>
      
      {hasError ? (
        <div className="result-block error">
          <p style={{ color: '#ef4444' }}>⚠️ {result.error}</p>
        </div>
      ) : result && (
        <div className="result-block">
          {/* Summary */}
          {result.summary && (
            <div>
              <p>{result.summary}</p>
            </div>
          )}
          
          {/* Text Content */}
          {result.text && (
            <div>
              <p>{result.text.substring(0, 300)}{result.text.length > 300 ? '...' : ''}</p>
            </div>
          )}
          
          {/* GitHub Results */}
          {result.results && result.results.length > 0 && (
            <div>
              <p style={{ marginBottom: '0.75rem', fontWeight: 600, color: '#60a5fa' }}>
                Found {result.results.length} repositories
                {result.total_count && ` (${result.total_count} total)`}
              </p>
              <ul>
                {result.results.map((item, idx) => (
                  <li key={item.url || idx}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      <a href={item.url} target="_blank" rel="noreferrer">
                        {item.name || 'Repository'}
                      </a>
                      {item.desc && (
                        <p className="muted" style={{ fontSize: '0.9rem', margin: 0 }}>
                          {item.desc}
                        </p>
                      )}
                      <div style={{ display: 'flex', gap: '1rem', fontSize: '0.85rem', color: 'rgba(255,255,255,0.6)' }}>
                        {item.language && <span>🔤 {item.language}</span>}
                        {item.stars !== undefined && <span>⭐ {item.stars}</span>}
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {/* Generic Data */}
          {result.data && (
            <details style={{ marginTop: '0.5rem' }}>
              <summary style={{ cursor: 'pointer', color: '#60a5fa', fontWeight: 600 }}>
                View Raw Data
              </summary>
              <pre style={{ marginTop: '0.75rem' }}>
                {JSON.stringify(result.data, null, 2)}
              </pre>
            </details>
          )}
        </div>
      )}
    </motion.li>
  );
};

export default StepCard;