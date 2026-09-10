import { Link, useLocation } from 'react-router-dom';

const NAV = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/leads', label: 'Leads' },
  { to: '/', label: 'Customer Chat' },
];

export default function Layout({ children, title }) {
  const location = useLocation();

  return (
    <div style={styles.shell}>
      <aside style={styles.sidebar}>
        <div style={styles.brand}>
          <strong>PrimeHomes</strong>
          <span style={styles.brandSub}>Sales Portal</span>
        </div>
        <nav style={styles.nav}>
          {NAV.map((item) => {
            const active = location.pathname === item.to ||
              (item.to !== '/' && location.pathname.startsWith(item.to));
            return (
              <Link
                key={item.to}
                to={item.to}
                style={{
                  ...styles.navItem,
                  ...(active ? styles.navItemActive : {}),
                }}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>

      <div style={styles.main}>
        {title && (
          <header style={styles.header}>
            <h1 style={styles.title}>{title}</h1>
          </header>
        )}
        <div style={styles.content}>{children}</div>
      </div>
    </div>
  );
}

const styles = {
  shell: {
    display: 'flex',
    minHeight: '100vh',
    background: '#f1f5f9',
  },
  sidebar: {
    width: 220,
    background: '#0f172a',
    color: '#fff',
    display: 'flex',
    flexDirection: 'column',
    padding: '24px 0',
    flexShrink: 0,
  },
  brand: {
    padding: '0 20px 24px',
    borderBottom: '1px solid #1e293b',
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
  },
  brandSub: {
    fontSize: 12,
    opacity: 0.6,
  },
  nav: {
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
    padding: '16px 12px',
  },
  navItem: {
    padding: '10px 12px',
    borderRadius: 8,
    color: '#94a3b8',
    textDecoration: 'none',
    fontSize: 14,
    fontWeight: 500,
  },
  navItemActive: {
    background: '#1e293b',
    color: '#fff',
  },
  main: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  },
  header: {
    padding: '20px 28px',
    background: '#fff',
    borderBottom: '1px solid #e2e8f0',
  },
  title: {
    fontSize: 20,
    fontWeight: 700,
    color: '#0f172a',
  },
  content: {
    flex: 1,
    padding: 28,
    overflowY: 'auto',
  },
};
