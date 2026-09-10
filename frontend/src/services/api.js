/**
 * Centralized API client.
 * All frontend → backend communication goes through here.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

export async function sendMessage({ conversationId, message, customer }) {
  const response = await fetch(`${API_BASE}/api/v1/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      message,
      customer,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error?.error?.message || 'Failed to send message')
  }

  return response.json()
}

// Additional API helpers will be added as endpoints are implemented
