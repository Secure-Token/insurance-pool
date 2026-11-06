
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createClaim } from '../services/api.js';

const initialForm = {
  claimant_id: '',
  task_id: '',
  reason: 'REQUIREMENT_MISSED',
  requirement: '',
  response_text: '',
  evidence: '',
  input_tokens: 0,
  output_tokens: 0,
  input_rate_per_million: 0,
  output_rate_per_million: 0
};

export default function ClaimSubmission() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  function change(event) {
    const { name, value } = event.target;
    setForm((previous) => ({ ...previous, [name]: value }));
  }

  async function submit(event) {
    event.preventDefault();

    try {
      setBusy(true);
      setError('');

      const payload = {
        ...form,
        input_tokens: Number(form.input_tokens),
        output_tokens: Number(form.output_tokens),
        input_rate_per_million: Number(form.input_rate_per_million),
        output_rate_per_million: Number(form.output_rate_per_million),
        evidence: form.evidence.trim() || null
      };

      const result = await createClaim(payload);

      if (!result?.id) {
        throw new Error('Backend did not return a claim ID.');
      }

      navigate(`/claims/${result.id}`);
    } catch (err) {
      setError(err.message || 'Claim submission failed.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">CLAIM INTAKE</p>
          <h1>Submit a claim</h1>
          <p className="sub">
            Provide the requirement, output, and verifiable evidence.
          </p>
        </div>
      </div>

      <form className="panel form-panel" onSubmit={submit}>
        <div className="form-grid">
          <label>
            Claimant ID
            <input
              name="claimant_id"
              value={form.claimant_id}
              onChange={change}
              required
              placeholder="USER-001"
            />
          </label>

          <label>
            Task ID
            <input
              name="task_id"
              value={form.task_id}
              onChange={change}
              required
              placeholder="TASK-2026-001"
            />
          </label>

          <label>
            Claim reason
            <select name="reason" value={form.reason} onChange={change}>
              <option value="REQUIREMENT_MISSED">Requirement missed</option>
              <option value="INCORRECT_OUTPUT">Incorrect output</option>
              <option value="INCOMPLETE_OUTPUT">Incomplete output</option>
              <option value="REGRESSION">Regression</option>
              <option value="OTHER">Other</option>
            </select>
          </label>

          <label className="wide">
            Original requirement
            <textarea
              name="requirement"
              value={form.requirement}
              onChange={change}
              rows="3"
              required
              placeholder="What was explicitly required?"
            />
          </label>

          <label className="wide">
            Model response / output
            <textarea
              name="response_text"
              value={form.response_text}
              onChange={change}
              rows="5"
              required
              placeholder="Paste the actual response under assessment."
            />
          </label>

          <label className="wide">
            Evidence
            <textarea
              name="evidence"
              value={form.evidence}
              onChange={change}
              rows="3"
              placeholder="Evidence, logs, or references"
            />
          </label>

          <label>
            Input tokens
            <input
              type="number"
              min="0"
              name="input_tokens"
              value={form.input_tokens}
              onChange={change}
              required
            />
          </label>

          <label>
            Output tokens
            <input
              type="number"
              min="0"
              name="output_tokens"
              value={form.output_tokens}
              onChange={change}
              required
            />
          </label>

          <label>
            Input rate / million
            <input
              type="number"
              min="0"
              step="any"
              name="input_rate_per_million"
              value={form.input_rate_per_million}
              onChange={change}
              required
            />
          </label>

          <label>
            Output rate / million
            <input
              type="number"
              min="0"
              step="any"
              name="output_rate_per_million"
              value={form.output_rate_per_million}
              onChange={change}
              required
            />
          </label>
        </div>

        {error && <div className="error-box">{error}</div>}

        <div className="form-actions">
          <span className="muted">Creates a simulated claim record.</span>
          <button className="primary" disabled={busy}>
            {busy ? 'Submitting…' : 'Submit claim →'}
          </button>
        </div>
      </form>
    </>
  );
}
