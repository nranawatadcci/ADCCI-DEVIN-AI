# Development of a Dynamics CRM Unmanaged Solution Using Workflow Process

This document translates the provided process diagrams into a practical **Dynamics 365 CRM (Dataverse) unmanaged solution design**.

## 1) Solution Scope

Build an unmanaged solution for the Sustainability Label journey:

1. EOI (Expression of Interest) submission and eligibility checks.
2. Auto-approval path for clearly eligible applicants.
3. Manual review path for flagged/ineligible EOI.
4. Self-assessment and document submission cycle.
5. Validation, scoring, report generation, and endorsements.
6. Certificate issuance and case closure.

---

## 2) Target Components in the Unmanaged Solution

Create one unmanaged solution, for example:

- **Publisher**: `adc`
- **Solution name**: `ADC Sustainability Workflow (Unmanaged)`
- **Versioning**: semantic (`1.0.0.0`, `1.1.0.0`, etc.)

### Include these component types

- Tables (entities)
- Columns (fields)
- Option sets (choices)
- Business process flow (stages)
- Real-time/background workflows (where applicable)
- Cloud flows (Power Automate) for notifications/integration
- Plugins/custom workflow activities (for complex scoring/report logic)
- Security roles
- Views/forms/charts
- Email templates and Word template for certificate/report

---

## 3) Core Data Model

## Main table: `adc_application`

Recommended key columns:

- `adc_applicationnumber` (Auto Number)
- `adc_company` (Lookup: Account/Contact)
- `adc_stage` (Choice)
- `adc_statusreason` (Choice)
- `adc_eoisubmittedon` (DateTime)
- `adc_eligibilityscore` (Whole Number)
- `adc_isflagged` (Yes/No)
- `adc_selfassessmentdue` (Date)
- `adc_documentstatus` (Choice: Missing/Submitted/Validated/Rejected)
- `adc_validationoutcome` (Choice)
- `adc_maturityscore` (Decimal)
- `adc_reportgeneratedon` (DateTime)
- `adc_pshendorsementstatus` (Choice)
- `adc_directorendorsementstatus` (Choice)
- `adc_certificateissuedon` (DateTime)
- `adc_closedon` (DateTime)

## Supporting tables

- `adc_eligibilityresponse` (1:N from Application)
- `adc_selfassessment` (1:1 or 1:N depending on design)
- `adc_supportingdocument` (1:N; document metadata)
- `adc_reviewdecision` (history/audit for manual approvals/rejections)
- `adc_notificationlog` (optional tracking)

---

## 4) Process Mapping (from your diagrams)

## Phase A: EOI + Eligibility

1. User browses service and submits EOI + eligibility questions.
2. System runs automatic eligibility criteria checks:
   - Years in operation
   - Number of employees
   - Regulatory compliance
   - No breach in recent years
   - Leadership commitment
   - Required documentation available
3. If all criteria pass and no flags:
   - Auto-approve EOI
   - Grant access to self-assessment
4. If any criteria fail/flag:
   - Request additional information
   - User submits explanation
   - Flag for manual review by Products Section Head
   - Decision:
     - Reject EOI (close application), or
     - Override rejection and proceed

## Phase B: Self-Assessment + Document Validation

5. User completes self-assessment questionnaire (SLA target: 15 days).
6. Products Section Head validates completeness.
7. If incomplete:
   - Return for missing information
   - User resubmits documentation (SLA target: 5 days)
   - Secondary review
8. Validation outcomes:
   - Rejected -> close application
   - Partially validated -> proceed with score adjustments
   - Fully validated -> proceed

## Phase C: Scoring + Reporting + Endorsements

9. System calculates maturity scores.
10. System generates maturity assessment report.
11. Products Section Head endorsement (SLA target: 3 days).
12. Director endorsement (SLA target: 3 days).
13. If approved: issue certificate + maturity report and close application.
14. If rejected: close application as rejected.

---

## 5) Workflow/Automation Design in Dynamics CRM

Use a layered approach:

- **Business Process Flow (BPF):** user-facing stage progression.
- **Real-time workflow/plugin:** deterministic state transitions, validation gates.
- **Background workflow/Power Automate:** asynchronous notifications, reminders, document-ready alerts, report/certificate distribution.

## Suggested BPF stages

1. EOI Submitted
2. Eligibility Check
3. Manual Review (if flagged)
4. Self-Assessment
5. Document Validation
6. Secondary Review
7. Scoring & Report
8. PSH Endorsement
9. Director Endorsement
10. Closure

## Trigger examples

- On create of `adc_application` -> run eligibility evaluation.
- On `adc_isflagged = Yes` -> create review task + notify PSH.
- On self-assessment submitted -> set due date and queue validation.
- On document status change -> branch to return/resubmission or scoring.
- On endorsement decision -> approve/reject closure logic.

---

## 6) Implementation Steps (Unmanaged Solution)

1. **Create publisher and unmanaged solution** in target environment.
2. Add tables, columns, relationships, forms, and views.
3. Build choice sets for stage, decision, and outcome fields.
4. Build BPF for end-to-end lifecycle.
5. Create classic workflows / Power Automate flows:
   - Eligibility evaluation
   - Additional-info request notifications
   - Review assignment notifications
   - SLA reminders/escalations
   - Endorsement notifications
   - Certificate/report dispatch
6. Add plugins/custom actions for:
   - Weighted maturity scoring
   - Final report generation orchestration
7. Configure security roles:
   - Applicant (portal)
   - Products Section Head
   - Business Connect/Services Director
   - System Admin
8. Add dashboards for queue/status/SLA breach monitoring.
9. Perform UAT with all branch scenarios (eligible, flagged-approved, rejected, resubmitted, endorsed/rejected).
10. Export unmanaged solution backup/version snapshot regularly.

---

## 7) SLA and Governance Controls

- Self-assessment completion SLA: 15 days.
- Resubmission SLA: 5 days.
- PSH endorsement SLA: 3 days.
- Director endorsement SLA: 3 days.

Recommended controls:

- Timed cloud-flow reminders at T-2 and T-0.
- Escalation to supervisor if overdue.
- Field-level audit enabled for decisions and endorsements.
- Mandatory reason fields for all rejection/override actions.

---

## 8) Suggested Notification Events

Send email/in-app notifications on:

- EOI submitted
- Eligibility auto-approved
- Additional information required
- Manual review requested
- EOI rejected / overridden
- Access granted to self-assessment
- Documents incomplete (return for correction)
- Documents validated
- Report generated
- Endorsement requested / completed
- Final approval and certificate issued
- Application closed/rejected

---

## 9) Recommended Packaging and ALM

Because this is unmanaged development:

- Keep unmanaged solution only in development.
- Use source control for all customizations (solution unpack with PAC CLI if available).
- Promote using managed builds to higher environments when governance requires it.
- Maintain a versioned change log per release.

---

## 10) Acceptance Checklist

- [ ] End-to-end process executes for eligible and flagged paths.
- [ ] All decision points match process diagrams.
- [ ] SLA reminders and escalations trigger correctly.
- [ ] Security roles enforce separation of duties.
- [ ] Report and certificate are generated and stored.
- [ ] Closure status and audit history are complete.

