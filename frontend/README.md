# Frontend — React

Customer chat interface and internal sales dashboard for PrimeHomes Realty Lead Bot.

## Structure (from UI/UX Specification)

```text
frontend/
└── src/
    ├── components/
    │   ├── chat/
    │   ├── leads/
    │   ├── dashboard/
    │   ├── followups/
    │   └── common/
    ├── pages/
    ├── services/
    ├── hooks/
    ├── utils/
    ├── App.jsx
    └── main.jsx
```

## Local Development

```bash
npm install
npm run dev
```

App runs at http://localhost:5173

The frontend communicates **only** with the FastAPI backend. No direct database or n8n access.
