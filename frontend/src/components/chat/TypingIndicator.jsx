export default function TypingIndicator() {
  return (
    <div style={styles.row}>
      <div style={styles.bubble}>
        <span style={styles.dot} />
        <span style={{ ...styles.dot, animationDelay: '0.15s' }} />
        <span style={{ ...styles.dot, animationDelay: '0.3s' }} />
      </div>
    </div>
  );
}

const styles = {
  row: {
    display: 'flex',
    justifyContent: 'flex-start',
    marginBottom: 10,
  },
  bubble: {
    background: '#f1f5f9',
    borderRadius: 18,
    borderBottomLeftRadius: 4,
    padding: '14px 18px',
    display: 'flex',
    gap: 5,
    alignItems: 'center',
  },
  dot: {
    width: 7,
    height: 7,
    borderRadius: '50%',
    background: '#94a3b8',
    animation: 'bounce 1.2s infinite ease-in-out',
  },
};
