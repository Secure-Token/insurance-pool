
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getClaims } from '../services/api.js';
import StatusBadge from '../components/StatusBadge.jsx';

export default function Claims() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadClaims() {
    try {
      setLoading(true);
      setError('');
      const data = await getClaims();
      setRows(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Unable to load claims.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadClaims();
  }, []);

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">REGISTER</p>
          <h1>Claims & logs</h1>
          <p className="sub">
            Browse submitted claims and their current lifecycle status.
          </p>
        </div>
        <Link className="primary" to="/claim/new">
          ＋ New claim
        </Link>
      </div>

      <section className="panel">
        {loading ? (
          <p>Loading claims...</p>
        ) : error ? (
          <div className="error-box">
            <p>{error}</p>
            <button onClick={loadClaims}>Retry</button>
          </div>
        ) : rows.length === 0 ? (
          <div className="empty">No claims have been submitted.</div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Claim ID</th>
                  <th>Claimant</th>
                  <th>Reason</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((claim) => (
                  <tr key={claim.id}>
                    <td>
                      <Link className="text-link" to={`/claims/${claim.id}`}>
                        {claim.id}
                      </Link>
                    </td>
                    <td>{claim.claimant_id || '—'}</td>
                    <td>{claim.reason || '—'}</td>
                    <td><StatusBadge status={claim.status} /></td>
                    <td>{claim.created_at || '—'}</td>
                    <td>
                      <Link className="text-link" to={`/claims/${claim.id}`}>
                        Details →
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </>
  );
}
