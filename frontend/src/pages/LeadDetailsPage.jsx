import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import Layout from '../components/common/Layout';
import Badge from '../components/common/Badge';
import {
  getLead,
  getLeadHistory,
  updateLead,
  getLeadFollowUps,
  createFollowUp,
  updateFollowUp,
} from '../services/api';

const STATUS_OPTIONS = [
  'NEW', 'QUALIFIED', 'ASSIGNED', 'CONTACTED',
  'FOLLOW_UP', 'NEGOTIATION', 'CONVERTED', 'LOST', 'UNQUALIFIED',
];

export default function LeadDetailsPage() {
  const { id } = useParams();
  const [lead, setLead] = useState(null);
  const [history, setHistory] = useState([]);
  const [followUps, setFollowUps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updating, setUpdating] = useState(false);

  // New follow-up form
  const [showForm, setShowForm] = useState(false);
  const [fuDate, setFuDate] = useState('');
  const [fuNotes, setFuNotes] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const [l, h, fus] = await Promise.all([
          getLead(id),
          getLeadHistory(id),
          getLeadFollowUps(id),
        ]);
        setLead(l);
        setHistory(h.events || []);
        setFollowUps(fus || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  const handleStatusChange = async (newStatus) => {
    if (!lead || newStatus === lead.status) return;
    setUpdating(true);
    try {
      const updated = await updateLead(id, { status: newStatus });
      setLead((prev) => ({ ...prev, status: updated.status }));
      const h = await getLeadHistory(id);
      setHistory(h.events || []);
    } catch (err) {
      alert(err.message);
    } finally {
      setUpdating(false);
    }
  };

  const handleCreateFollowUp = async (e) => {
    e.preventDefault();
    if (!fuDate) return;
    setSaving(true);
    try {
      const created = await createFollowUp(id, {
        follow_up_date: new Date(fuDate).toISOString(),
        notes: fuNotes || null,
      });
      setFollowUps((prev) => [...prev, created]);
      setShowForm(false);
      setFuDate('');
      setFuNotes('');
    } catch (err) {
      alert(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleCompleteFu = async (fuId) => {
    try {
      await updateFollowUp(fuId, { status: 'COMPLETED' });
      setFollowUps((prev) =>
        prev.map((f) =>
          f.id === fuId ? { ...f, status: 'COMPLETED', completed_at: new Date().toISOString() } : f
        )
      );
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) {
    return (
      <Layout title="Lead Details">
        <p style={{ color: '#64748b' }}>Loading…</p>
      </Layout>
    );
  }

  if (error || !lead) {
    return (
      <Layout title="Lead Details">
        <p style={{ color: '#b91c1c' }}>{error || 'Lead not found'}</p>
        <Link to="/leads" style={{ color: '#2563eb' }}>← Back to Leads</Link>
      </Layout>
    );
  }

  const req = lead.property_requirements;
  const customer = lead.customer;

  return (
    <Layout title="Lead Details">
      <Link to="/leads" style={styles.back}>← Back to Leads</Link>

      {/* Header */}
      <div style={styles.headerCard}>
        <div>
          <h2 style={styles.name}>{customer?.name || 'Unknown Customer'}</h2>
          <div style={styles.contact}>
            {customer?.phone && <span>{customer.phone}</span>}
            {customer?.email && <span>{customer.email}</span>}
          </div>
        </div>
        <div style={styles.badges}>
          <Badge value={lead.temperature} />
          <Badge value={lead.status} />
          {lead.score != null && (
            <span style={styles.score}>Score: {lead.score}/100</span>
          )}
        </div>
      </div>

      <div style={styles.grid}>
        {/* Requirements */}
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>Property Requirements</h3>
          <dl style={styles.dl}>
            <div style={styles.row}>
              <dt style={styles.dt}>Type</dt>
              <dd style={styles.dd}>{req?.property_type || '—'}</dd>
            </div>
            <div style={styles.row}>
              <dt style={styles.dt}>Bedrooms</dt>
              <dd style={styles.dd}>{req?.bedrooms ?? '—'}</dd>
            </div>
            <div style={styles.row}>
              <dt style={styles.dt}>Location</dt>
              <dd style={styles.dd}>{req?.location || '—'}</dd>
            </div>
            <div style={styles.row}>
              <dt style={styles.dt}>Budget</dt>
              <dd style={styles.dd}>
                {req?.budget_max
                  ? `₦${Number(req.budget_max).toLocaleString()}`
                  : req?.budget_min
                    ? `From ₦${Number(req.budget_min).toLocaleString()}`
                    : '—'}
              </dd>
            </div>
            <div style={styles.row}>
              <dt style={styles.dt}>Timeline</dt>
              <dd style={styles.dd}>{req?.timeline || '—'}</dd>
            </div>
            <div style={styles.row}>
              <dt style={styles.dt}>Intent</dt>
              <dd style={styles.dd}>{lead.intent || '—'}</dd>
            </div>
          </dl>
        </div>

        {/* Status + History */}
        <div style={styles.card}>
          <h3 style={styles.cardTitle}>Update Status</h3>
          <select
            style={styles.select}
            value={lead.status}
            disabled={updating}
            onChange={(e) => handleStatusChange(e.target.value)}
          >
            {STATUS_OPTIONS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>

          <h3 style={{ ...styles.cardTitle, marginTop: 24 }}>History</h3>
          {history.length === 0 && (
            <p style={{ color: '#94a3b8', fontSize: 13 }}>No status changes yet.</p>
          )}
          <ul style={styles.history}>
            {history.map((evt, i) => (
              <li key={i} style={styles.historyItem}>
                <span style={{ fontWeight: 500 }}>
                  {evt.old_status || '—'} → {evt.new_status}
                </span>
                <span style={{ color: '#94a3b8', fontSize: 12 }}>
                  {new Date(evt.created_at).toLocaleString()}
                </span>
                {evt.reason && (
                  <span style={{ color: '#64748b', fontSize: 12 }}>{evt.reason}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Follow-ups section */}
      <div style={{ ...styles.card, marginTop: 20 }}>
        <div style={styles.fuHeader}>
          <h3 style={styles.cardTitle}>Follow-ups</h3>
          <button style={styles.addBtn} onClick={() => setShowForm((v) => !v)}>
            {showForm ? 'Cancel' : '+ Schedule Follow-up'}
          </button>
        </div>

        {showForm && (
          <form onSubmit={handleCreateFollowUp} style={styles.form}>
            <div style={styles.formRow}>
              <label style={styles.label}>
                Date & time
                <input
                  type="datetime-local"
                  style={styles.input}
                  value={fuDate}
                  onChange={(e) => setFuDate(e.target.value)}
                  required
                />
              </label>
              <label style={{ ...styles.label, flex: 1 }}>
                Notes
                <input
                  type="text"
                  style={styles.input}
                  value={fuNotes}
                  onChange={(e) => setFuNotes(e.target.value)}
                  placeholder="Optional notes…"
                />
              </label>
              <button type="submit" style={styles.saveBtn} disabled={saving}>
                {saving ? 'Saving…' : 'Save'}
              </button>
            </div>
          </form>
        )}

        {followUps.length === 0 && !showForm && (
          <p style={{ color: '#94a3b8', fontSize: 13 }}>No follow-ups scheduled.</p>
        )}

        <ul style={styles.fuList}>
          {followUps.map((fu) => (
            <li key={fu.id} style={styles.fuItem}>
              <div>
                <strong>{new Date(fu.follow_up_date).toLocaleString()}</strong>
                {fu.notes && <span style={{ color: '#64748b', marginLeft: 12 }}>{fu.notes}</span>}
              </div>
              <div style={styles.fuRight}>
                <Badge value={fu.status} />
                {fu.status === 'PENDING' && (
                  <button
                    style={styles.completeBtn}
                    onClick={() => handleCompleteFu(fu.id)}
                  >
                    Complete
                  </button>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  );
}

const styles = {
  back: {
    color: '#2563eb',
    textDecoration: 'none',
    fontSize: 14,
    marginBottom: 16,
    display: 'inline-block',
  },
  headerCard: {
    background: '#fff',
    borderRadius: 12,
    padding: '20px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 20,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  name: {
    fontSize: 20,
    fontWeight: 700,
    color: '#0f172a',
  },
  contact: {
    display: 'flex',
    gap: 16,
    marginTop: 6,
    color: '#64748b',
    fontSize: 14,
  },
  badges: {
    display: 'flex',
    gap: 8,
    alignItems: 'center',
  },
  score: {
    fontSize: 13,
    fontWeight: 600,
    color: '#334155',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: 20,
  },
  card: {
    background: '#fff',
    borderRadius: 12,
    padding: 24,
    boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: 600,
    color: '#0f172a',
    marginBottom: 16,
  },
  dl: { margin: 0 },
  row: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '8px 0',
    borderBottom: '1px solid #f1f5f9',
  },
  dt: { color: '#64748b', fontSize: 13 },
  dd: { fontWeight: 500, color: '#0f172a', fontSize: 14 },
  select: {
    width: '100%',
    padding: '10px 12px',
    borderRadius: 8,
    border: '1px solid #cbd5e1',
    fontSize: 14,
  },
  history: { listStyle: 'none', padding: 0, margin: 0 },
  historyItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
    padding: '8px 0',
    borderBottom: '1px solid #f1f5f9',
    fontSize: 13,
  },
  fuHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  addBtn: {
    padding: '6px 14px',
    borderRadius: 8,
    border: '1px solid #2563eb',
    background: '#eff6ff',
    color: '#2563eb',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
  },
  form: { marginBottom: 16 },
  formRow: {
    display: 'flex',
    gap: 12,
    alignItems: 'flex-end',
  },
  label: {
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
    fontSize: 13,
    color: '#64748b',
  },
  input: {
    padding: '8px 12px',
    borderRadius: 8,
    border: '1px solid #cbd5e1',
    fontSize: 14,
  },
  saveBtn: {
    padding: '8px 18px',
    borderRadius: 8,
    border: 'none',
    background: '#2563eb',
    color: '#fff',
    fontWeight: 600,
    fontSize: 14,
    cursor: 'pointer',
  },
  fuList: { listStyle: 'none', padding: 0, margin: 0 },
  fuItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px 0',
    borderBottom: '1px solid #f1f5f9',
    fontSize: 14,
  },
  fuRight: {
    display: 'flex',
    gap: 10,
    alignItems: 'center',
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
};
