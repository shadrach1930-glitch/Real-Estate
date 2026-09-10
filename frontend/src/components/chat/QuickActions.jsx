const ACTIONS = [
  { label: 'Buy a property', message: 'I want to buy a property' },
  { label: 'Rent a property', message: 'I want to rent a property' },
  { label: 'Find land', message: 'I need land' },
  { label: 'Speak to an agent', message: 'I want to speak with an agent' },
];

export default function QuickActions({ onSelect, disabled }) {
  return (
    <div style={styles.container}>
      {ACTIONS.map((action) => (
        <button
          key={action.label}
          style={styles.button}
          onClick={() => onSelect(action.message)}
          disabled={disabled}
        >
          {action.label}
        </button>
      ))}
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: 8,
    padding: '0 16px 12px',
  },
  button: {
    padding: '8px 14px',
    borderRadius: 20,
    border: '1px solid #cbd5e1',
    background: '#fff',
    color: '#334155',
    fontSize: 13,
    cursor: 'pointer',
    transition: 'background 0.15s',
  },
};
