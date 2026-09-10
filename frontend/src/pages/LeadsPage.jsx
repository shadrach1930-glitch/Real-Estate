import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/common/Layout';
import Badge from '../components/common/Badge';
import { getLeads } from '../services/api';

const STATUSES = ['', 'NEW', 'QUALIFIED', 'ASSIGNED', 'CONTACTED', 'FOLLOW_UP', 'NEGOTIATION', 'CONVERTED', 'LOST'];
const TEMPS = ['', 'HOT', 'WARM', 'COLD'];

export default function LeadsPage() {
  const [leads, setLeads] = useState([]);
  const [total, setTotal] = useState(0);
  const [status, setStatus] = useState('');
  const [temperature, setTemperature] = useState('');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await getLeads({
          status: status || undefined,
          temperature: temperature || undefined,
          page,
          limit: 20,
        });
        setLeads(data.items || []);
        setTotal(data.total || 0);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [status, temperature, page]);

  return (
    <Layout title="Leads">
      <div style={styles.filters}>
        <select
          style={styles.select}
          value={status}
          onChange={(e) => { setStatus(e.target.value); setPage(1); }}
        >
          <option value="">All statuses</option>
          {STATUSES.filter(Boolean).map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>

        <select
          style={styles.select}
          value={temperature}
          onChange={(e) => { setTemperature(e.target.value); setPage(1); }}
        >
          <option value="">All temperatures</option>
          {TEMPS.filter(Boolean).map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>

        <span style={styles.count}>{total} lead{total !== 1 ? 's' : ''}</span>
      </div>

      {loading && <p style={{ color: '#64748b' }}>Loading…</p>}
      {error && <p style={{ color: '#b91c1c' }}>{error}</p>}

      {!loading && (
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
                <th style={styles.th}>Created</th>
              </tr>
            </thead>
            <tbody>
              {leads.length === 0 && (
                <tr>
                  <td colSpan={8} style={styles.empty}>
                    No leads match your filters.
                  </td>
                </tr>
              )}
              {leads.map((lead) => (
                <tr key={lead.id}>
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
                  <td style={styles.td}><Badge value={lead.temperature} /></td>
                  <td style={styles.td}><Badge value={lead.status} /></td>
                  <td style={styles.td}>
                    {lead.created_at
                      ? new Date(lead.created_at).toLocaleDateString()
                      : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {total > 20 && (
        <div style={styles.pagination}>
          <button
            style={styles.pageBtn}
            disabled={page <= 1}
            onClick={() => setPage((p) => p - 1)}
          >
            Previous
          </button>
          <span style={{ color: '#64748b', fontSize: 14 }}>Page {page}</span>
          <button
            style={styles.pageBtn}
            disabled={page * 20 >= total}
            onClick={() => setPage((p) => p + 1)}
          >
            Next
          </button>
        </div>
      )}
    </Layout>
  );
}

const styles = {
  filters: {
    display: 'flex',
    gap: 12,
    marginBottom: 20,
    alignItems: 'center',
  },
  select: {
    padding: '8px 12px',
    borderRadius: 8,
    border: '1px solid #cbd5e1',
    fontSize: 14,
    background: '#fff',
  },
  count: {
    marginLeft: 'auto',
    color: '#64748b',
    fontSize: 13,
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
  pagination: {
    display: 'flex',
    gap: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 20,
  },
  pageBtn: {
    padding: '8px 16px',
    borderRadius: 8,
    border: '1px solid #cbd5e1',
    background: '#fff',
    cursor: 'pointer',
    fontSize: 14,
  },
};
