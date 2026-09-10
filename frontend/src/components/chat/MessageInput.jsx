import { useState } from 'react';

export default function MessageInput({ onSend, disabled }) {
  const [value, setValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!value.trim() || disabled) return;
    onSend(value);
    setValue('');
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <input
        style={styles.input}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Type your message…"
        disabled={disabled}
        autoComplete="off"
      />
      <button
        type="submit"
        style={{
          ...styles.button,
          opacity: disabled || !value.trim() ? 0.5 : 1,
        }}
        disabled={disabled || !value.trim()}
      >
        Send
      </button>
    </form>
  );
}

const styles = {
  form: {
    display: 'flex',
    gap: 8,
    padding: '12px 16px',
    borderTop: '1px solid #e2e8f0',
    background: '#fff',
  },
  input: {
    flex: 1,
    padding: '12px 16px',
    borderRadius: 24,
    border: '1px solid #cbd5e1',
    fontSize: 15,
    outline: 'none',
  },
  button: {
    padding: '12px 22px',
    borderRadius: 24,
    border: 'none',
    background: '#2563eb',
    color: '#fff',
    fontWeight: 600,
    fontSize: 15,
    cursor: 'pointer',
  },
};
