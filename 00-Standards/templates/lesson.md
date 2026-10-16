---
{
  "id": "L-<unique-id>",
  "version": "0.1",
  "status": "candidate",
  "kind": "procedural",
  "action": "<specific-reusable-action>",
  "transfer_rationale": null,
  "scope": "project",
  "project_id": "<stable-project-id>",
  "origin_project_ids": ["<stable-project-id>"],
  "production_ids": [],
  "conditions": {"tasks": [], "models": [], "interfaces": [], "formats": []},
  "evidence": [],
  "validation": {
    "result": "not_checked",
    "method": "not_checked",
    "records": [],
    "regression_checked": false,
    "unresolved_conflicts": [],
    "changes_policy": false
  },
  "activation": {"method": "none", "date": null, "authority": null}
}
---

# Bài học

Created / updated:
Summary and actionable instruction:
Observation / hypothesis / established conclusion (distinguish):
Evidence paths and exact frame/time or feedback source:
Scope, applicability and exceptions:
Why transferable beyond origin project (required for shared):
Confidence and limitations / do not infer:
Validation, regression and tradeoffs:
Applied in (attempt links) and observed outcome, without claiming causality:
Supersedes / superseded by:
Status/scope/version history, date and reason:

kind = procedural | empirical; scope = project | shared (shared uses project_id null).
Evidence/validation.records/activation.authority use workspace-relative paths, optional #anchor. User activation.authority links a saved request/decision, not merely this policy. Automatic active requires all gates in memory-policy.md. Unresolved conflicts cannot remain active. New active version retains valid evidence/activation or returns to candidate. Fill actual data before saving in memory; template is not a lesson.
