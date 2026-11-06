
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getClaim, evaluateClaim } from '../services/api.js';
import StatusBadge from '../components/StatusBadge.jsx';

export default function ClaimDetail() {
  const { id } = useParams();

  const [data, setData] = useState(null);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [evaluationError, setEvaluationError] = useState('');

  async function loadClaim() {
    try {
      setLoading(true);
      setError('');
      setData(await getClaim(id));
    } catch (err) {
      setError(err.message || 'Unable to load claim.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadClaim();
  }, [id]);

  async function runEvaluation() {
    try {
      setBusy(true);
      setEvaluationError('');
      const result = await evaluateClaim(id);
      setData(result);
    } catch (err) {
      setEvaluationError(err.message || 'Evaluation failed.');
    } finally {
      setBusy(false);
    }
  }

  if (loading) {
    return <section className="panel">Loading claim...</section>;
  }

  if (error || !data) {
    return (
      <section className="panel">
        <h2>Claim unavailable</h2>
        <p>{error || 'Claim not found.'}</p>
        <Link to="/claims" className="text-link">Back to claims</Link>
      </section>
    );
  }

  const ev = data.evaluation || data.evaluation_report;

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">CLAIM DETAIL · {id}</p>
          <h1>{data.id}</h1>
          <p className="sub">Claim record, model findings, and policy decision.</p>
        </div>

        <button className="primary" onClick={runEvaluation} disabled={busy}>
          {busy ? 'Evaluating…' : 'Run evaluation'}
        </button>
      </div>

      {evaluationError && (
        <div className="error-box">
          Evaluation failed: {evaluationError}
        </div>
      )}

      <div className="detail-grid">
        <section className="panel">
          <h2>Claim information</h2>
          <dl className="details">
            <dt>Claimant</dt>
            <dd>{data.claimant_id || '—'}</dd>

            <dt>Task ID</dt>
            <dd>{data.task_id || '—'}</dd>

            <dt>Reason</dt>
            <dd>{data.reason || '—'}</dd>

            <dt>Status</dt>
            <dd><StatusBadge status={data.status} /></dd>

            <dt>Created</dt>
            <dd>{data.created_at || '—'}</dd>

            <dt>Requirement</dt>
            <dd>{data.requirement || '—'}</dd>

            <dt>Response</dt>
            <dd><pre>{data.response_text || '—'}</pre></dd>

            <dt>Evidence</dt>
            <dd>{data.evidence || '—'}</dd>

            <dt>Input tokens</dt>
            <dd>{data.input_tokens ?? '—'}</dd>

            <dt>Output tokens</dt>
            <dd>{data.output_tokens ?? '—'}</dd>
          </dl>
        </section>

        <section className="panel">
          <div className="panel-head">
            <div>
              <h2>Evaluation report</h2>
              <p>Model output is advisory only.</p>
            </div>
            <span className="demo-pill">LLM</span>
          </div>

          {ev ? (
            <>
              <div className="recommendation">
                <small>RECOMMENDATION</small>
                <strong>
                  {ev.recommendation || ev.decision || 'MANUAL_REVIEW'}
                </strong>
              </div>

              <div className="report-grid">
                <div>
                  <small>Failure category</small>
                  <b>{ev.category || ev.failure_category || '—'}</b>
                </div>
                <div>
                  <small>Severity</small>
                  <b>{ev.severity || '—'}</b>
                </div>
                <div>
                  <small>Model confidence</small>
                  <b>{ev.confidence ?? '—'}</b>
                </div>
              </div>

              <h3>Findings</h3>
              <ul>
                {(ev.findings || ev.reasons || []).map((item, index) => (
                  <li key={index}>
                    {typeof item === 'string' ? item : JSON.stringify(item)}
                  </li>
                ))}
              </ul>

              <h3>Evidence references</h3>
              <p>
                {(ev.evidence || ev.evidence_ids || []).join(', ') ||
                  'No evidence references supplied.'}
              </p>

              <p className="muted">
                Model confidence is not a calibrated probability.
              </p>
            </>
          ) : (
            <div className="empty">No evaluation record returned.</div>
          )}
        </section>
      </div>

      <Link className="text-link back" to="/claims">
        ← Back to claims
      </Link>
    </>
  );
}
