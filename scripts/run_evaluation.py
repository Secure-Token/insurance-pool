#!/usr/bin/env python3
"""ST fixture runner. MOCK ONLY: tests plumbing/schema/metrics, not LLM quality."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLES=ROOT/"rules"/"examples"
DEFAULT_SCHEMA=ROOT/"rules"/"evaluation_schema.json"

def evaluate_mock(case):
    """Keyword-only mock; replace with a real evaluator adapter later."""
    blob=" ".join([str(case.get("requirement","")),str(case.get("response","")),
        str(case.get("evidence","")),json.dumps(case.get("acceptance_criteria",[]))]).lower()
    findings=[]
    code=None
    if any(x in blob for x in ("omitted","missing","not implemented","failed","failure")): code="REQ_OMITTED"
    elif any(x in blob for x in ("ambiguous","unclear","undefined","fast","production-ready")): code="REQ_AMBIGUOUS"
    if code:
        findings.append({"finding_id":"MOCK-F-001","code":code,"level":"INTERACTION","role":"PRIMARY",
          "impact":"MEDIUM","description":"Mock keyword signal; requires actual evidence review.",
          "evidence_refs":[],"affected_criteria":[],"confidence":0.5,"compensability_signal":"POSSIBLE"})
    return {
      "schema_version":"1.0.0","evaluation_id":"MOCK-"+str(case.get("case_id","case")),
      "claim_id":None,"interaction_id":None,"evaluation_status":"COMPLETED",
      "requirement_assessment":{"requirement_available":bool(case.get("requirement")),
        "summary":"Mock assessment; no semantic analysis.","criteria":[]},
      "dimensions":[],"findings":findings,"severity":"MEDIUM" if findings else "UNASSESSED",
      "confidence":0.5 if findings else None,"evidence_summary":"Keyword heuristic only.",
      "missing_evidence":[],"contradictions":[],
      "recommendation":"RECOMMEND_MANUAL_REVIEW" if findings else "RECOMMEND_REJECTION",
      "manual_review_required":bool(findings),"review_reasons":["Mock signal; verify evidence manually"] if findings else [],
      "usage_attribution":{"status":"NOT_ASSESSED","affected_call_ids":[],"input_tokens":None,
        "output_tokens":None,"source_refs":[],"notes":"No token usage is inferred by this runner."},
      "policy_refs":{"rules_version":"mock","taxonomy_version":"mock","evaluation_policy_version":"mock"},
      "limitations":["MOCK_ONLY: keyword heuristic; no model inference or financial decision."]
    }

def load(path):
    with path.open(encoding="utf-8") as f:return json.load(f)
def cases_under(path):return sorted(path.glob("*/case.json"))
def gold(case):
    if "expected_failure" in case:return bool(case["expected_failure"])
    label=str(case.get("expected_label",case.get("label",""))).upper()
    if label in {"FAILURE","FAIL","POSITIVE"}:return True
    if label in {"NO_FAILURE","PASS","NEGATIVE"}:return False
    raise ValueError("missing explicit expected_failure/expected_label")
def pred(result):return bool(result["findings"])
def div(a,b):return a/b if b else 0.0
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--examples",type=Path,default=DEFAULT_EXAMPLES)
    ap.add_argument("--schema",type=Path,default=DEFAULT_SCHEMA)
    ap.add_argument("--output",type=Path,default=ROOT/"scripts"/"evaluation_report.json")
    a=ap.parse_args()
    files=cases_under(a.examples)
    if not files:print("No */case.json fixtures found",file=sys.stderr);return 2
    schema=load(a.schema); tp=fp=fn=tn=invalid=0; rows=[]
    for f in files:
        c=load(f)
        try:y=gold(c)
        except ValueError as e:print(f"SKIP {f}: {e}",file=sys.stderr);continue
        r=evaluate_mock(c); errors=[]
        if Draft202012Validator:
            errors=[e.message for e in Draft202012Validator(schema).iter_errors(r)]
        else:errors=["jsonschema not installed; validation skipped"]
        invalid+=bool(errors); p=pred(r)
        if y and p:tp+=1
        elif not y and p:fp+=1
        elif y and not p:fn+=1
        else:tn+=1
        rows.append({"fixture":str(f.relative_to(ROOT)),"gold_failure":y,"predicted_failure":p,"schema_errors":errors,"result":r})
    precision=div(tp,tp+fp);recall=div(tp,tp+fn)
    report={"run_type":"MOCK_PIPELINE_SMOKE_TEST","warning":"Metrics reflect a keyword heuristic only—not LLM accuracy.",
      "cases_run":len(rows),"schema_invalid_results":invalid,"confusion_matrix":{"TP":tp,"FP":fp,"FN":fn,"TN":tn},
      "metrics":{"precision":precision,"recall":recall,"f1":div(2*precision*recall,precision+recall),
       "false_positive_rate":div(fp,fp+tn),"false_negative_rate":div(fn,fn+tp),"accuracy":div(tp+tn,tp+fp+fn+tn)},
      "cases":rows}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="cases"},indent=2));print("Report:",a.output)
    return 1 if invalid else 0
if __name__=="__main__":raise SystemExit(main())
