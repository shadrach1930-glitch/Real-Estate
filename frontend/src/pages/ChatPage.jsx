import { useChat } from '../hooks/useChat';
import MessageBubble from '../components/chat/MessageBubble';
import TypingIndicator from '../components/chat/TypingIndicator';
import MessageInput from '../components/chat/MessageInput';
import QuickActions from '../components/chat/QuickActions';

export default function ChatPage() {
  const { messages, isLoading, error, send, retry, bottomRef } = useChat();

  const showQuickActions = messages.length <= 1 && !isLoading;

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        {/* Header */}
        <header style={styles.header}>
          <div>
            <div style={styles.brand}>PrimeHomes Realty</div>
            <div style={styles.subtitle}>AI Property Assistant</div>
          </div>
          <div style={styles.statusDot} title="Online" />
        </header>

        {/* Messages */}
        <main style={styles.messages}>
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {isLoading && <TypingIndicator />}

          {error && (
            <div style={styles.errorBox}>
              <p style={styles.errorText}>{error}</p>
              <div style={styles.errorActions}>
                <button style={styles.errorBtn} onClick={retry}>
                  Dismiss
                </button>
                <button
                  style={{ ...styles.errorBtn, ...styles.errorBtnPrimary }}
                  onClick={() => send('I want to speak with an agent')}
                >
                  Speak to an Agent
                </button>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </main>

        {/* Quick actions (only at start) */}
        {showQuickActions && (
          <QuickActions onSelect={send} disabled={isLoading} />
        )}

        {/* Input */}
        <MessageInput onSend={send} disabled={isLoading} />
      </div>

      {/* Keyframes for typing dots */}
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
          40% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    background: '#e2e8f0',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'stretch',
  },
  container: {
    width: '100%',
    maxWidth: 640,
    display: 'flex',
    flexDirection: 'column',
    background: '#fff',
    boxShadow: '0 0 40px rgba(0,0,0,0.08)',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '16px 20px',
    background: '#0f172a',
    color: '#fff',
  },
  brand: {
    fontWeight: 700,
    fontSize: 17,
  },
  subtitle: {
    fontSize: 13,
    opacity: 0.75,
    marginTop: 2,
  },
  statusDot: {
    width: 10,
    height: 10,
    borderRadius: '50%',
    background: '#22c55e',
  },
  messages: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px 16px',
    display: 'flex',
    flexDirection: 'column',
  },
  errorBox: {
    background: '#fef2f2',
    border: '1px solid #fecaca',
    borderRadius: 12,
    padding: 14,
    marginBottom: 10,
  },
  errorText: {
    color: '#b91c1c',
    fontSize: 14,
    marginBottom: 10,
  },
  errorActions: {
    display: 'flex',
    gap: 8,
  },
  errorBtn: {
    padding: '6px 12px',
    borderRadius: 8,
    border: '1px solid #d1d5db',
    background: '#fff',
    fontSize: 13,
    cursor: 'pointer',
  },
  errorBtnPrimary: {
    background: '#2563eb',
    color: '#fff',
    borderColor: '#2563eb',
  },
};
