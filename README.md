<<<<<<< HEAD
ST Insurance Pool — Demo v0.1
Simulation only. This project uses simulated internal credits. It does not provide provider refunds, real funds, underwriting, or production insurance/settlement.

1. Overview
ST Insurance Pool is a demonstration workflow for submitting AI-output claims, retrieving claim records, requesting an advisory LLM evaluation, managing investigations, and viewing simulated pool/ledger information.

The LLM evaluation is advisory only. It does not approve claims or authorize settlement.
2. Prerequisites
Install the following on Windows:
- Python 3.10+ (ensure the Python launcher py is available)
- Node.js LTS and npm
- Git (if cloning the repository)
- Ollama (required only for claim evaluation)

3. Clone the repository
git clone <https://github.com/Secure-Token/insurance-pool>

4. Configure and run the backend
Open PowerShell:
cd backend

# Create the virtual environment (once)
py -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create local configuration
Copy-Item .env.example .env

# Start FastAPI
uvicorn app.main:app --reload
If PowerShell blocks virtual-environment activation, run this in the current PowerShell session and activate again:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
Backend URLs:
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health
The SQLite database is created locally using the configured DATABASE_URL. The default is sqlite:///./st_pool.db (relative to the backend working directory).
5. Install and configure Ollama 

Claim creation and retrieval do not require Ollama. The evaluation endpoint does.
1. Install Ollama from: https://ollama.com/download
2. Open a new PowerShell terminal and verify:
ollama --version
3. Download the configured model:
ollama pull qwen2.5:0.5b
4. Confirm the model is available:
ollama list
5. Confirm Ollama's local API responds:
Invoke-RestMethod http://localhost:11434/api/tags
Ollama normally runs as a local service after installation. If it is not running, start it:
ollama serve
Keep that terminal open if you started the service manually.
Backend Ollama configuration
The backend .env.example currently defines:
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:0.5b
OLLAMA_TIMEOUT=90
> These values are copied to .env in Step 4. If you change the model, pull it first and set OLLAMA_MODEL to the exact model tag returned by ollama list. Restart FastAPI after changing .env.
6. Install and run the frontend
Open a second PowerShell terminal:
cd frontend

# Install frontend dependencies
npm install

# Configure the API base URL
Create frontend/.env (or update it) with:
VITE_API_BASE_URL=http://localhost:8000
Then start Vite:
npm run dev
Open the local URL printed by Vite (normally http://localhost:5173).

> Important: Vite environment variables are loaded at startup. Stop and restart npm run dev after creating or changing frontend/.env.
7. Start-up order and terminal layout
Run these services in separate terminals:
Terminal	Directory	Command	Purpose
1	backend	.\.venv\Scripts\Activate.ps1 then uvicorn app.main:app --reload	FastAPI
2	Any	ollama serve (only if Ollama is not already running)	Local model API
3	frontend	npm run dev	React/Vite


Ollama must be reachable before you run claim evaluation. The backend and frontend can run without it for non-evaluation workflows.
8. Verify the system
Check each layer:
1. Backend health: http://localhost:8000/health
2. API docs: http://localhost:8000/docs
3. Ollama models: ollama list
4. Ollama API: http://localhost:11434/api/tags
5. Frontend: open the Vite URL and confirm dashboard data loads from port 8000.

9. Demo workflow
1. Open the frontend.
2. Submit a claim with claimant ID, task ID, requirement, model response, reason, evidence, token counts, and rates.
3. Open the created claim from the Claims page.
4. Select Run evaluation. This calls the backend evaluation endpoint and requires Ollama/model availability.
5. Review the advisory evaluation result.
6. Create or inspect investigations and view pool/ledger data as supported by the demo.
Example claim request:
{
  "claimant_id": "test_user1",
  "task_id": "task_id_1234",
  "requirement": "Provide a summary of the tasks performed.",
  "response_text": "No response was generated.",
  "reason": "INCOMPLETE_OUTPUT",
  "input_tokens": 10,
  "output_tokens": 0,
  "input_rate_per_million": 2,
  "output_rate_per_million": 3,
  "evidence": "The requested task summary was not provided; the output is empty."
}
Use evidence that reflects the actual task context and output. Do not invent task history or label a valid NOT_FOUND response as a model failure without verifying that the relevant task data was available to the model.
10. API endpoints
- GET /api/dashboard
- POST /api/claims
- GET /api/claims?status=SUBMITTED
- GET /api/claims/{id}
- POST /api/claims/{id}/evaluate — Ollama required
- GET /api/investigations
- POST /api/claims/{id}/investigations
- GET /api/pool
- GET /api/settlements/ledger
- POST /api/claims/{id}/settle — only manually approved statuses
Use /docs for request schemas and interactive API testing.
11. Known limitations
- Simulation only; no provider refunds, real funds, underwriting, or production settlement.
- Evaluation is advisory and cannot approve a claim.
- The demo does not expose an authenticated approval/adjudication endpoint.
- Evaluation may transition claims to ELIGIBILITY_REVIEW or UNDER_INVESTIGATION; ordinary evaluation does not produce APPROVED.
- Settlement therefore cannot be completed through the ordinary demo workflow until a separately designed, authenticated adjudication action exists.
- Ollama must be installed, running, and have the configured model downloaded for evaluation.
- Do not treat this demo as production-ready insurance or financial infrastructure.
12. Troubleshooting
Symptom	Likely cause	Action
HTTP 502 / All connection attempts failed on evaluation	Backend cannot reach Ollama	Check Ollama is running and OLLAMA_BASE_URL is correct
Model not found	Model tag is not downloaded or does not match configuration	Run ollama pull qwen2.5:0.5b; verify with ollama list
Unexpected token '<' / HTML received instead of JSON	Frontend called Vite or an HTML error route	Set VITE_API_BASE_URL=http://localhost:8000; restart Vite
Dashboard/API request returns 404	Wrong API path or backend route	Check Request URL and /docs
Frontend cannot connect	Backend is stopped or wrong base URL	Start FastAPI and verify http://localhost:8000/health
PowerShell activation blocked	Execution policy blocks script	Use the process-scoped bypass shown in Step 4

=======
