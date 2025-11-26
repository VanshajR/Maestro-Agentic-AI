import { motion } from 'framer-motion';

const Loader = ({ label }) => {
  return (
    <div className="loader-card">
      <motion.div
        className="pulse"
        animate={{ scale: [1, 1.2, 1] }}
        transition={{ repeat: Infinity, duration: 1.4 }}
      />
      <p>{label}</p>
    </div>
  );
};

export default Loader;
