import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/common/Layout';
import StatCard from '../components/common/StatCard';
import Badge from '../components/common/Badge';
import { getDashboardSummary, getLeads } from '../services/api';

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [recent, setRecent] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [s, leads] = await Promise.all([
          getDashboardSummary(),
          getLeads({ limit: 8 }),
        ]);
        setSummary(s);
        setRecent(leads.items || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <Layout title="Dashboard">
      {loading && <p style={{ color: '#64748b' }}>Loading…</p>}
      {error && <p style={{ color: '#b91c1c' }}>{error}</p>}

      {summary && (
        <div style={styles.grid}>
          <StatCard label="Total Leads" value={summary.total_leads} accent="#2563eb" />
          <StatCard label="New" value={summary.new_leads} accent="#7c3aed" />
          <StatCard label="Hot" value={summary.hot_leads} accent="#dc2626" />
          <StatCard label="Warm" value={summary.warm_leads} accent="#d97706" />
          <StatCard label="Qualified" value={summary.qualified_leads} accent="#16a34a" />
          <StatCard label="Converted" value={summary.converted_leads} accent="#059669" />
          <StatCard label="Pending Follow-ups" value={summary.pending_follow_ups} accent="#9333ea" />
        </div>
      )}

      <h2 style={styles.sectionTitle}>Recent Leads</h2>

      <div style={styles.tableWrap}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th style={styles.th}>Customer</th>
              <th style={styles.th}>Property</th>
              <th style={styles.th}>Location</th>
              <th style={styles.th}>Budget</th>
              <th style={styles.th}>Score</th>
              <th style={styles.th}>Temp</th>
              <th style={styles.th}>Status</th>
            </tr>
          </thead>
          <tbody>
            {recent.length === 0 && (
              <tr>
                <td colSpan={7} style={styles.empty}>
                  No leads yet. New enquiries will appear here.
                </td>
              </tr>
            )}
            {recent.map((lead) => (
              <tr key={lead.id} style={styles.tr}>
                <td style={styles.td}>
                  <Link to={`/leads/${lead.id}`} style={styles.link}>
                    {lead.customer_name || 'Unknown'}
                  </Link>
                </td>
                <td style={styles.td}>{lead.property_type || '—'}</td>
                <td style={styles.td}>{lead.location || '—'}</td>
                <td style={styles.td}>
                  {lead.budget ? `₦${Number(lead.budget).toLocaleString()}` : '—'}
                </td>
                <td style={styles.td}>{lead.score ?? '—'}</td>
                <td style={styles.td}>
                  <Badge value={lead.temperature} />
                </td>
                <td style={styles.td}>
                  <Badge value={lead.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
    gap: 16,
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 600,
    color: '#0f172a',
    marginBottom: 12,
  },
  tableWrap: {
    background: '#fff',
    borderRadius: 12,
    overflow: 'hidden',
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: 14,
  },
  th: {
    textAlign: 'left',
    padding: '12px 16px',
    background: '#f8fafc',
    color: '#64748b',
    fontWeight: 600,
    fontSize: 12,
    textTransform: 'uppercase',
    letterSpacing: 0.4,
    borderBottom: '1px solid #e2e8f0',
  },
  td: {
    padding: '12px 16px',
    borderBottom: '1px solid #f1f5f9',
    color: '#334155',
  },
  tr: {
    transition: 'background 0.1s',
  },
  link: {
    color: '#2563eb',
    textDecoration: 'none',
    fontWeight: 500,
  },
  empty: {
    padding: 32,
    textAlign: 'center',
    color: '#94a3b8',
  },
};
