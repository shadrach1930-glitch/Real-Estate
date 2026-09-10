export default function MessageBubble({ message }) {
  const isCustomer = message.sender === 'customer';

  return (
    <div
      style={{
        ...styles.row,
        justifyContent: isCustomer ? 'flex-end' : 'flex-start',
      }}
    >
      <div
        style={{
          ...styles.bubble,
          ...(isCustomer ? styles.customer : styles.bot),
        }}
      >
        {message.content}
      </div>
    </div>
  );
}

const styles = {
  row: {
    display: 'flex',
    marginBottom: 10,
  },
  bubble: {
    maxWidth: '78%',
    padding: '12px 16px',
    borderRadius: 18,
    fontSize: 15,
    lineHeight: 1.45,
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word',
  },
  customer: {
    background: '#2563eb',
    color: '#fff',
    borderBottomRightRadius: 4,
  },
  bot: {
    background: '#f1f5f9',
    color: '#1e293b',
    borderBottomLeftRadius: 4,
  },
};
