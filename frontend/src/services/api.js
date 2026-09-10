/**
 * Centralized API client.
 * All frontend → backend communication goes through here.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Generate a request ID for tracing
  headers['X-Request-ID'] = crypto.randomUUID?.() || String(Date.now());

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let message = 'Something went wrong. Please try again.';
    try {
      const err = await response.json();
      message = err?.error?.message || err?.detail || message;
    } catch {
      // ignore parse errors
    }
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }

  return response.json();
}

/**
 * Send a customer message to the lead bot.
 * @param {{ conversationId?: string, message: string, customer?: object }} params
 */
export async function sendMessage({ conversationId, message, customer }) {
  return request('/api/v1/chat', {
    method: 'POST',
    body: JSON.stringify({
      conversation_id: conversationId || null,
      message,
      customer: customer || null,
    }),
  });
}

/**
 * Retrieve a conversation and its messages.
 */
export async function getConversation(conversationId) {
  return request(`/api/v1/conversations/${conversationId}`);
}
