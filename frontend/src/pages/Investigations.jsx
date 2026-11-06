
import { useEffect, useState } from 'react';
import { getInvestigations } from '../services/api.js';
import StatusBadge from '../components/StatusBadge.jsx';
import { Link } from 'react-router-dom';

export default function Investigations() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadInvestigations() {
    try {
      setLoading(true);
      setError('');
      const data = await getInvestigations();
      setRows(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Unable to load investigations.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadInvestigations();
  }, []);

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">REVIEW WORKFLOW</p>
          <h1>Investigation queue</h1>
          <p className="sub">
            Ambiguous, contradictory, or evidence-incomplete cases.
          </p>
        </div>
      </div>

      <section className="panel">
        {loading ? (
          <p>Loading investigations...</p>
        ) : error ? (
          <div className="error-box">
            <p>{error}</p>
            <button onClick={loadInvestigations}>Retry</button>
          </div>
        ) : rows.length === 0 ? (
          <div className="empty">No investigations found.</div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Investigation ID</th>
                  <th>Claim</th>
                  <th>Review notes</th>
                  <th>Status</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((item) => (
                  <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>
                      <Link className="text-link" to={`/claims/${item.claim_id}`}>
                        {item.claim_id}
                      </Link>
                    </td>
                    <td>{item.notes || '—'}</td>
                    <td><StatusBadge status={item.status} /></td>
                    <td>{item.created_at || '—'}</td>
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
