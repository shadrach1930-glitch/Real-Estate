import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/common/Layout';
import Badge from '../components/common/Badge';
import { getLeads, getLeadFollowUps, updateFollowUp } from '../services/api';

/**
 * Aggregates follow-ups from recent leads.
 * A dedicated /follow-ups endpoint can replace this later.
 */
export default function FollowUpsPage() {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState('PENDING');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch recent leads then their follow-ups
      const leadsData = await getLeads({ limit: 50 });
      const leads = leadsData.items || [];

      const all = [];
      await Promise.all(
        leads.map(async (lead) => {
          try {
            const fus = await getLeadFollowUps(lead.id);
            (fus || []).forEach((fu) => {
              all.push({
                ...fu,
                customer_name: lead.customer_name,
                lead_status: lead.status,
                lead_temperature: lead.temperature,
              });
            });
          } catch {
            // skip individual failures
          }
        })
      );

      // Sort by follow_up_date ascending
      all.sort((a, b) => new Date(a.follow_up_date) - new Date(b.follow_up_date));
      setItems(all);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleComplete = async (id) => {
    try {
      await updateFollowUp(id, { status: 'COMPLETED' });
      setItems((prev) =>
        prev.map((fu) =>
          fu.id === id ? { ...fu, status: 'COMPLETED', completed_at: new Date().toISOString() } : fu
        )
      );
    } catch (err) {
      alert(err.message);
    }
  };

  const handleCancel = async (id) => {
    try {
      await updateFollowUp(id, { status: 'CANCELLED' });
      setItems((prev) =>
        prev.map((fu) => (fu.id === id ? { ...fu, status: 'CANCELLED' } : fu))
      );
    } catch (err) {
      alert(err.message);
    }
  };

  const now = new Date();
  const filtered = items.filter((fu) => {
    if (filter === 'ALL') return true;
    if (filter === 'OVERDUE') {
      return fu.status === 'PENDING' && new Date(fu.follow_up_date) < now;
    }
    return fu.status === filter;
  });

  const isOverdue = (fu) => fu.status === 'PENDING' && new Date(fu.follow_up_date) < now;

  return (
    <Layout title="Follow-ups">
      <div style={styles.filters}>
        {['PENDING', 'OVERDUE', 'COMPLETED', 'CANCELLED', 'ALL'].map((f) => (
          <button
            key={f}
            style={{
              ...styles.filterBtn,
              ...(filter === f ? styles.filterBtnActive : {}),
            }}
            onClick={() => setFilter(f)}
          >
            {f}
          </button>
        ))}
        <span style={styles.count}>{filtered.length} item{filtered.length !== 1 ? 's' : ''}</span>
      </div>

      {loading && <p style={{ color: '#64748b' }}>Loading…</p>}
      {error && <p style={{ color: '#b91c1c' }}>{error}</p>}

      {!loading && (
        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Customer</th>
                <th style={styles.th}>Due</th>
                <th style={styles.th}>Notes</th>
                <th style={styles.th}>Status</th>
                <th style={styles.th}>Lead</th>
                <th style={styles.th}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={6} style={styles.empty}>
                    No follow-ups found.
                  </td>
                </tr>
              )}
              {filtered.map((fu) => (
                <tr key={fu.id} style={isOverdue(fu) ? styles.overdueRow : {}}>
                  <td style={styles.td}>
                    <Link to={`/leads/${fu.lead_id}`} style={styles.link}>
                      {fu.customer_name || 'Unknown'}
                    </Link>
                  </td>
                  <td style={styles.td}>
                    {new Date(fu.follow_up_date).toLocaleString()}
                    {isOverdue(fu) && (
                      <span style={styles.overdueBadge}>OVERDUE</span>
                    )}
                  </td>
                  <td style={styles.td}>{fu.notes || '—'}</td>
                  <td style={styles.td}>
                    <Badge value={fu.status} />
                  </td>
                  <td style={styles.td}>
                    <Badge value={fu.lead_temperature} />{' '}
                    <Badge value={fu.lead_status} />
                  </td>
                  <td style={styles.td}>
                    {fu.status === 'PENDING' && (
                      <div style={styles.actions}>
                        <button
                          style={styles.completeBtn}
                          onClick={() => handleComplete(fu.id)}
                        >
                          Complete
                        </button>
                        <button
                          style={styles.cancelBtn}
                          onClick={() => handleCancel(fu.id)}
                        >
                          Cancel
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  );
}

const styles = {
  filters: {
    display: 'flex',
    gap: 8,
    marginBottom: 20,
    alignItems: 'center',
    flexWrap: 'wrap',
  },
  filterBtn: {
    padding: '6px 14px',
    borderRadius: 20,
    border: '1px solid #cbd5e1',
    background: '#fff',
    fontSize: 13,
    cursor: 'pointer',
    color: '#475569',
  },
  filterBtnActive: {
    background: '#0f172a',
    color: '#fff',
    borderColor: '#0f172a',
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
    verticalAlign: 'middle',
  },
  overdueRow: {
    background: '#fef2f2',
  },
  overdueBadge: {
    marginLeft: 8,
    fontSize: 11,
    fontWeight: 700,
    color: '#b91c1c',
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
  actions: {
    display: 'flex',
    gap: 6,
  },
  completeBtn: {
    padding: '4px 10px',
    borderRadius: 6,
    border: 'none',
    background: '#16a34a',
    color: '#fff',
    fontSize: 12,
    cursor: 'pointer',
  },
  cancelBtn: {
    padding: '4px 10px',
    borderRadius: 6,
    border: '1px solid #cbd5e1',
    background: '#fff',
    fontSize: 12,
    cursor: 'pointer',
    color: '#64748b',
  },
};
