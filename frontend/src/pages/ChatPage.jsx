import { useState } from 'react'

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'bot',
      content: "Welcome to PrimeHomes Realty.\n\nI'm here to help you find the right property. You can tell me what you're looking for, your preferred location, budget, or whether you're buying or renting.",
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = {
      id: Date.now().toString(),
      sender: 'customer',
      content: input.trim(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Placeholder — will call POST /api/v1/chat in a later phase
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'bot',
          content: "Thanks for your message. The full chat pipeline (FastAPI → n8n → AI) will be connected in the next development phases.",
        },
      ])
      setIsLoading(false)
    }, 800)
  }

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <div>
          <strong>PrimeHomes Realty</strong>
          <div style={styles.subtitle}>AI Property Assistant</div>
        </div>
      </header>

      <main style={styles.messages}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            style={{
              ...styles.bubble,
              ...(msg.sender === 'customer' ? styles.customer : styles.bot),
            }}
          >
            {msg.content}
          </div>
        ))}
        {isLoading && (
          <div style={{ ...styles.bubble, ...styles.bot }}>
            <em>Assistant is typing…</em>
          </div>
        )}
      </main>

      <footer style={styles.inputArea}>
        <input
          style={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message…"
          disabled={isLoading}
        />
        <button style={styles.sendBtn} onClick={handleSend} disabled={isLoading || !input.trim()}>
          Send
        </button>
      </footer>
    </div>
  )
}

const styles = {
  container: {
    maxWidth: 640,
    margin: '0 auto',
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    background: '#fff',
    boxShadow: '0 0 24px rgba(0,0,0,0.08)',
  },
  header: {
    padding: '16px 20px',
    borderBottom: '1px solid #e5e7eb',
    background: '#0f172a',
    color: '#fff',
  },
  subtitle: {
    fontSize: 13,
    opacity: 0.8,
    marginTop: 2,
  },
  messages: {
    flex: 1,
    overflowY: 'auto',
    padding: 20,
    display: 'flex',
    flexDirection: 'column',
    gap: 12,
  },
  bubble: {
    maxWidth: '80%',
    padding: '12px 16px',
    borderRadius: 16,
    whiteSpace: 'pre-wrap',
    fontSize: 15,
  },
  customer: {
    alignSelf: 'flex-end',
    background: '#2563eb',
    color: '#fff',
    borderBottomRightRadius: 4,
  },
  bot: {
    alignSelf: 'flex-start',
    background: '#f1f5f9',
    color: '#1e293b',
    borderBottomLeftRadius: 4,
  },
  inputArea: {
    display: 'flex',
    gap: 8,
    padding: 16,
    borderTop: '1px solid #e5e7eb',
  },
  input: {
    flex: 1,
    padding: '12px 16px',
    borderRadius: 24,
    border: '1px solid #d1d5db',
    fontSize: 15,
    outline: 'none',
  },
  sendBtn: {
    padding: '12px 20px',
    borderRadius: 24,
    border: 'none',
    background: '#2563eb',
    color: '#fff',
    fontWeight: 600,
    cursor: 'pointer',
  },
}
