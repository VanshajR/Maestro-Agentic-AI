import { motion } from 'framer-motion';
import StepCard from './StepCard.jsx';
import ReactMarkdown from 'react-markdown';

const Results = ({ response }) => {
  const { plan, intermediate, final_summary: finalSummary, timeline } = response;

  return (
    <section className="results-panel">
      {/* Summary Section */}
      <motion.div
        className="summary-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <p className="eyebrow">Executive Summary</p>
        <div className="markdown-content">
          <ReactMarkdown>{finalSummary}</ReactMarkdown>
        </div>
      </motion.div>

      <div className="grid-two">
        {/* Plan Section */}
        <div className="card-panel">
          <h2>Execution Plan</h2>
          <ol className="steps-list">
            {plan.map((step) => (
              <li key={step.id}>
                <span className="step-number">{step.id}</span>
                <span className="step-desc">{step.description}</span>
              </li>
            ))}
          </ol>
        </div>

        {/* Timeline Section */}
        <div className="card-panel">
          <h2>Execution Timeline</h2>
          <div className="timeline-container">
            {timeline.map((entry, index) => (
              <div key={`${entry.step_id}-${index}`} className="timeline-item">
                <div className="timeline-marker"></div>
                <div className="timeline-content">
                  <span className="tool-badge">{entry.tool}</span>
                  <span className="duration">{entry.duration.toFixed(2)}s</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Intermediate Results */}
      <h2>Detailed Findings</h2>
      <ul className="step-grid">
        {intermediate.map((item, index) => (
          <StepCard key={index} step={item.step} result={item.result} />
        ))}
      </ul>
    </section>
  );
};

export default Results;