const COLORS = {
  HOT: { bg: '#fef2f2', color: '#b91c1c', border: '#fecaca' },
  WARM: { bg: '#fffbeb', color: '#b45309', border: '#fde68a' },
  COLD: { bg: '#f0f9ff', color: '#0369a1', border: '#bae6fd' },
  NEW: { bg: '#f5f3ff', color: '#6d28d9', border: '#ddd6fe' },
  QUALIFIED: { bg: '#f0fdf4', color: '#15803d', border: '#bbf7d0' },
  ASSIGNED: { bg: '#eff6ff', color: '#1d4ed8', border: '#bfdbfe' },
  CONTACTED: { bg: '#ecfeff', color: '#0e7490', border: '#a5f3fc' },
  FOLLOW_UP: { bg: '#fdf4ff', color: '#a21caf', border: '#f5d0fe' },
  NEGOTIATION: { bg: '#fff7ed', color: '#c2410c', border: '#fed7aa' },
  CONVERTED: { bg: '#f0fdf4', color: '#166534', border: '#86efac' },
  LOST: { bg: '#f8fafc', color: '#64748b', border: '#e2e8f0' },
  UNQUALIFIED: { bg: '#f8fafc', color: '#64748b', border: '#e2e8f0' },
};

export default function Badge({ value }) {
  if (!value) return null;
  const c = COLORS[value] || COLORS.COLD;

  return (
    <span
      style={{
        display: 'inline-block',
        padding: '2px 10px',
        borderRadius: 999,
        fontSize: 12,
        fontWeight: 600,
        background: c.bg,
        color: c.color,
        border: `1px solid ${c.border}`,
      }}
    >
      {value}
    </span>
  );
}
