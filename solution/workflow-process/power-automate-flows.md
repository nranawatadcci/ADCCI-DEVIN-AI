# Power Automate Flow Set for ADCCI ESG Workflow

This package defines the minimum cloud flows to implement the process in the unmanaged solution.

## Flow 1 — EOI Intake and Eligibility Evaluation
- **Trigger:** Dataverse row added on `adcci_esgapplication`.
- **Logic:**
  1. Read eligibility fields.
  2. Evaluate criteria (years, employees, compliance, breach history, leadership, documents).
  3. Set `adcci_eligibilityscore`.
  4. If any fail -> `adcci_applicationstatus = EOI Flagged - Awaiting Info`; else approved.
- **Outputs:** status update, notification, and optional review record creation.

## Flow 2 — Additional Information Request & Reminder
- **Trigger:** `adcci_applicationstatus` changed to `EOI Flagged - Awaiting Info`.
- **Logic:**
  1. Send request-for-information email with due date.
  2. Create reminder jobs at T-2 and T-0.
  3. Escalate overdue cases to Products Section Head.

## Flow 3 — Self-Assessment SLA Monitor
- **Trigger:** `adcci_applicationstatus` changed to `Self-Assessment In Progress`.
- **Logic:**
  1. Compute due date (+15 days from approval).
  2. Send reminders at day 10, day 13, and due day.
  3. On breach, flag `adcci_slabreach = true` and notify reviewer.

## Flow 4 — Validation and Resubmission Cycle
- **Trigger:** Document state transitions on `adcci_esgdocument`.
- **Logic:**
  1. If incomplete -> mark app `Returned for Missing Information` and notify applicant.
  2. If resubmitted -> route to secondary review queue.
  3. For rejected/partial/validated outcomes, synchronize app status and notify next actor.

## Flow 5 — Score, Report, Endorsements
- **Trigger:** Validation outcome moved to partial/validated.
- **Logic:**
  1. Call custom action/plugin to compute maturity score.
  2. Generate report artifact and create `adcci_maturityreport` row.
  3. Send endorsement task to Products Section Head, then Director.
  4. On final approval, call certificate issuance flow.

## Flow 6 — Certificate Issuance and Closure
- **Trigger:** Director endorsement approved.
- **Logic:**
  1. Generate certificate number and certificate document.
  2. Link report + certificate to application.
  3. Send final notification package.
  4. Close application (`statecode=Inactive`).

## Dataverse Notification Template Mapping
- `N-01` EOI Submitted
- `N-02` EOI Auto-Approved
- `N-03` EOI Flagged (Additional info required)
- `N-05` EOI Rejected (Manual)
- `N-06` EOI Approved (Manual Override)

## Deployment Notes
- Keep these flows inside the unmanaged solution and set connection references before import to UAT.
- Use environment variables for email sender, portal URL, report storage location, and SLA defaults.
