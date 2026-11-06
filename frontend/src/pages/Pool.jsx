
import { useEffect, useState } from 'react';
import { Wallet, Activity, ShieldCheck } from 'lucide-react';
import StatCard from '../components/StatCard.jsx';
import { getPool } from '../services/api.js';

export default function Pool() {
  const [pool, setPool] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadPool() {
    try {
      setLoading(true);
      setError('');
      setPool(await getPool());
    } catch (err) {
      setError(err.message || 'Unable to load pool.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPool();
  }, []);

  if (loading) return <section className="panel">Loading pool...</section>;

  if (error) {
    return (
      <section className="panel">
        <p>{error}</p>
        <button onClick={loadPool}>Retry</button>
      </section>
    );
  }

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">POOL CONTROL</p>
          <h1>Pool overview</h1>
          <p className="sub">Live simulated reserve and utilization.</p>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard
          label="Total funded"
          value={pool.total_funded}
          icon={Wallet}
        />
        <StatCard
          label="Committed"
          value={pool.committed}
          icon={Activity}
        />
        <StatCard
          label="Available"
          value={pool.available}
          icon={ShieldCheck}
        />
      </div>

      <section className="panel">
        <h2>Pool configuration snapshot</h2>

        <div className="kv">
          <span>Mode</span>
          <b>{pool.mode || '—'}</b>

          <span>Pending</span>
          <b>{pool.pending}</b>

          <span>Utilization</span>
          <b>{pool.utilization}%</b>

          <span>Cash payout</span>
          <b>Not implemented</b>

          <span>Provider refund</span>
          <b>Not implemented</b>

          <span>Settlement type</span>
          <b>Internal simulated units</b>
        </div>
      </section>
    </>
  );
}
