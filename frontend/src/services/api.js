/**
 * Centralized API client.
 */

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

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
      // ignore
    }
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }

  return response.json();
}

// ── Chat ──────────────────────────────────────────────
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

export async function getConversation(conversationId) {
  return request(`/api/v1/conversations/${conversationId}`);
}

// ── Dashboard ─────────────────────────────────────────
export async function getDashboardSummary() {
  return request('/api/v1/dashboard/summary');
}

// ── Leads ─────────────────────────────────────────────
export async function getLeads({ status, temperature, page = 1, limit = 20 } = {}) {
  const params = new URLSearchParams();
  if (status) params.set('status', status);
  if (temperature) params.set('temperature', temperature);
  params.set('page', page);
  params.set('limit', limit);
  return request(`/api/v1/leads?${params}`);
}

export async function getLead(leadId) {
  return request(`/api/v1/leads/${leadId}`);
}

export async function updateLead(leadId, data) {
  return request(`/api/v1/leads/${leadId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export async function qualifyLead(leadId) {
  return request(`/api/v1/leads/${leadId}/qualify`, { method: 'POST' });
}

export async function getLeadHistory(leadId) {
  return request(`/api/v1/leads/${leadId}/history`);
}

// ── Follow-ups ────────────────────────────────────────
export async function getLeadFollowUps(leadId) {
  return request(`/api/v1/leads/${leadId}/follow-ups`);
}

export async function createFollowUp(leadId, data) {
  return request(`/api/v1/leads/${leadId}/follow-ups`, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateFollowUp(followUpId, data) {
  return request(`/api/v1/follow-ups/${followUpId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}
