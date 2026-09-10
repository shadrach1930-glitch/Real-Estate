export default function StatCard({ label, value, accent }) {
  return (
    <div style={{ ...styles.card, borderTop: `3px solid ${accent || '#2563eb'}` }}>
      <div style={styles.value}>{value}</div>
      <div style={styles.label}>{label}</div>
    </div>
  );
}

const styles = {
  card: {
    background: '#fff',
    borderRadius: 12,
    padding: '20px 24px',
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
    minWidth: 140,
  },
  value: {
    fontSize: 28,
    fontWeight: 700,
    color: '#0f172a',
  },
  label: {
    fontSize: 13,
    color: '#64748b',
    marginTop: 4,
  },
};
