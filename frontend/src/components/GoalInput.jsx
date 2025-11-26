import { motion } from 'framer-motion';

const GoalInput = ({ goal, maxSteps, onGoalChange, onStepsChange, onSubmit, disabled }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey && !disabled) {
      onSubmit();
    }
  };

  return (
    <motion.div
      className="goal-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div>
        <label htmlFor="goal">
          Research Goal <span style={{ color: '#ef4444' }}>*</span>
        </label>
        <textarea
          id="goal"
          rows={4}
          value={goal}
          onChange={(e) => onGoalChange(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="e.g., Compare the latest Groq models and summarize their strengths"
          disabled={disabled}
          style={{
            opacity: disabled ? 0.6 : 1,
            cursor: disabled ? 'not-allowed' : 'text'
          }}
        />
        <p style={{ 
          fontSize: '0.8rem', 
          color: 'rgba(255,255,255,0.5)', 
          marginTop: '0.5rem' 
        }}>
          💡 Tip: Press Ctrl+Enter to submit
        </p>
      </div>

      <div className="steps-row">
        <label htmlFor="steps">
          Max Steps: <strong style={{ color: '#60a5fa' }}>{maxSteps}</strong>
        </label>
        <input
          id="steps"
          type="range"
          min={3}
          max={10}
          value={maxSteps}
          onChange={(e) => onStepsChange(Number(e.target.value))}
          disabled={disabled}
          style={{
            opacity: disabled ? 0.6 : 1,
            cursor: disabled ? 'not-allowed' : 'pointer'
          }}
        />
      </div>

      <button 
        type="button" 
        onClick={onSubmit}
        disabled={disabled || !goal.trim()}
        style={{
          opacity: (disabled || !goal.trim()) ? 0.5 : 1,
          cursor: (disabled || !goal.trim()) ? 'not-allowed' : 'pointer'
        }}
      >
        {disabled ? '⏳ Processing...' : '🚀 Run Automation'}
      </button>
    </motion.div>
  );
};

export default GoalInput;