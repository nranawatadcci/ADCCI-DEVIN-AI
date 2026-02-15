# ADCCI ESG Workflow Development Pack (Add to Solution)

This folder contains implementation-ready artifacts to **develop and add the workflow process** into the Dynamics CRM unmanaged solution:

1. `workflow-stage-transition-matrix.csv` — authoritative transition matrix.
2. `power-automate-flows.md` — cloud flow definitions and trigger logic.
3. `plugin-design.md` — custom action/plugin behavior for scoring, report generation, and certificate issuance.

## How to apply in Dynamics unmanaged solution
1. Open your unmanaged solution.
2. Create/update application status choices and stage fields to match the matrix.
3. Build or update BPF stages according to the transition matrix.
4. Implement 6 Power Automate flows exactly as mapped.
5. Register the listed custom action/plugins.
6. Validate all branches (auto-approve, flagged manual review, rejection, partial validation, final approval).
