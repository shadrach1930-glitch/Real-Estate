# Frontend — React

Customer chat interface and (future) sales dashboard for PrimeHomes Realty Lead Bot.

## Current Features (Phase 4)

- Real-time chat connected to `POST /api/v1/chat`
- Conversation state persistence (conversation_id)
- Typing indicator
- Quick action buttons
- Error handling with retry / escalate options
- Auto-scroll
- Mobile-friendly layout

## Structure

```text
frontend/
└── src/
    ├── components/
    │   └── chat/
    │       ├── MessageBubble.jsx
    │       ├── MessageInput.jsx
    │       ├── TypingIndicator.jsx
    │       └── QuickActions.jsx
    ├── pages/
    │   └── ChatPage.jsx
    ├── hooks/
    │   └── useChat.js
    ├── services/
    │   └── api.js
    ├── App.jsx
    ├── main.jsx
    └── index.css
```

## Local Development

```bash
npm install
npm run dev
```

App runs at http://localhost:5173

Make sure the FastAPI backend is running on http://localhost:8000  
(Vite proxies `/api` requests automatically via `vite.config.js`).

## Environment

Optional:

```env
VITE_API_BASE_URL=http://localhost:8000
```

If omitted, the proxy in `vite.config.js` is used.
