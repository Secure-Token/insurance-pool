
import { useEffect, useState } from 'react';
import { ReceiptText } from 'lucide-react';
import { getLedger } from '../services/api.js';
import { Link } from 'react-router-dom';

export default function Ledger() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadLedger() {
    try {
      setLoading(true);
      setError('');
      const data = await getLedger();
      setRows(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Unable to load ledger.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadLedger();
  }, []);

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">AUDIT TRAIL</p>
          <h1>Simulated ledger</h1>
          <p className="sub">
            Demonstration entries only; no real balances are modified.
          </p>
        </div>
      </div>

      <section className="panel">
        <div className="panel-head">
          <div>
            <h2>Ledger entries</h2>
            <p>Settlement records from the backend.</p>
          </div>
          <ReceiptText />
        </div>

        {loading ? (
          <p>Loading ledger...</p>
        ) : error ? (
          <div className="error-box">
            <p>{error}</p>
            <button onClick={loadLedger}>Retry</button>
          </div>
        ) : rows.length === 0 ? (
          <div className="empty">No ledger entries recorded.</div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Transaction</th>
                  <th>Claim</th>
                  <th>Amount</th>
                  <th>Type</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((item) => (
                  <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>
                      {item.claim_id ? (
                        <Link className="text-link" to={`/claims/${item.claim_id}`}>
                          {item.claim_id}
                        </Link>
                      ) : '—'}
                    </td>
                    <td>{item.amount ?? item.credits ?? '—'}</td>
                    <td>{item.type || item.transaction_type || '—'}</td>
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
