
import { useEffect, useState } from 'react';
import {
  FileText,
  Clock,
  ShieldCheck,
  AlertTriangle
} from 'lucide-react';

import StatCard from '../components/StatCard.jsx';
import StatusBadge from '../components/StatusBadge.jsx';
import { getDashboard, getClaims } from '../services/api.js';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError('');

        const [dashboard, claimData] = await Promise.all([
          getDashboard(),
          getClaims()
        ]);

        setStats(dashboard);
        setClaims(claimData.slice(0, 5));
      } catch (err) {
        setError(
          err.message || 'Failed to load dashboard data.'
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return <div className="panel">Loading dashboard...</div>;
  }

  if (error) {
    return (
      <div className="panel">
        <h2>Dashboard unavailable</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">OVERVIEW</p>
          <h1>Pool dashboard</h1>
          <p className="sub">
            Claims, evaluation activity, and pool health at a glance.
          </p>
        </div>

        <Link className="primary" to="/claim/new">
          ＋ Submit claim
        </Link>
      </div>

      <div className="stats-grid">
        <StatCard
          label="Total claims"
          value={stats.total_claims}
          icon={FileText}
        />

        <StatCard
          label="Open claims"
          value={stats.open_claims}
          icon={Clock}
        />

        <StatCard
          label="Settled claims"
          value={stats.settled_claims}
          icon={ShieldCheck}
        />

        <StatCard
          label="Open investigations"
          value={stats.open_investigations}
          icon={AlertTriangle}
        />
      </div>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h2>Recent claims</h2>
            <p>Latest activity in the claim register</p>
          </div>

          <Link to="/claims" className="text-link">
            View all →
          </Link>
        </div>

        {claims.length > 0 ? (
          <ClaimTable rows={claims} />
        ) : (
          <p>No claims have been submitted yet.</p>
        )}
      </section>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h2>Evaluation pipeline</h2>
            <p>
              Model recommendation is advisory;
              policy validation remains deterministic.
            </p>
          </div>
        </div>

        <div className="pipeline">
          {[
            'Claim intake',
            'LLM analysis',
            'Policy validation',
            'Human review',
            'Simulated settlement'
          ].map((step, index) => (
            <div className="pipeline-step" key={step}>
              <span>{index + 1}</span>
              <b>{step}</b>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}

function ClaimTable({ rows }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Claim ID</th>
            <th>Claimant</th>
            <th>Reason</th>
            <th>Status</th>
            <th>Created</th>
          </tr>
        </thead>

        <tbody>
          {rows.map((claim) => (
            <tr key={claim.id}>
              <td>
                <Link
                  to={`/claims/${claim.id}`}
                  className="text-link"
                >
                  {claim.id}
                </Link>
              </td>

              <td>{claim.claimant_id || '—'}</td>
              <td>{claim.reason || '—'}</td>
              <td>
                <StatusBadge status={claim.status} />
              </td>
              <td>{claim.created_at || '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
