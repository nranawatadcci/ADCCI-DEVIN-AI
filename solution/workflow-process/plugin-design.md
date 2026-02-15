# Plugin / Custom Action Design (for unmanaged solution)

## 1) `adcci_CalculateMaturityScore` (Custom Action)

### Input
- `ApplicationId` (GUID)

### Output
- `OverallScore` (Decimal)
- `MaturityLevel` (OptionSet)

### Execution
1. Retrieve all `adcci_assessmentresponse` records for the application.
2. Apply weighting per ESG theme.
3. Apply review adjustments from `adcci_esgreview`.
4. Persist score to `adcci_esgapplication.adcci_overallmaturityscore`.
5. Return score and maturity band.

### Registration
- **Message:** Custom Action execution
- **Mode:** Synchronous
- **Stage:** PostOperation

## 2) `adcci_GenerateMaturityReport` (Plugin)

### Trigger
- Update on `adcci_esgapplication` when validation outcome becomes Partial or Validated.

### Execution
1. Ensure score exists (invoke `adcci_CalculateMaturityScore` if needed).
2. Create/Update `adcci_maturityreport` record.
3. Render report content template (Word/PDF pipeline).
4. Set report generation timestamp.
5. Move application to endorsement stage.

## 3) `adcci_IssueCertificate` (Plugin)

### Trigger
- Update on `adcci_maturityreport` when director endorsement status becomes Approved.

### Execution
1. Generate sequential certificate number.
2. Create `adcci_esgcertificate` record.
3. Attach maturity report reference.
4. Mark application approved and closed.
5. Publish notification event for final communication.

## Error Handling Rules
- Throw explicit `InvalidPluginExecutionException` for missing mandatory relationships.
- Persist recoverable errors in `adcci_esgnotification`/audit log for operational follow-up.
- Prevent duplicate report/certificate creation via idempotency checks on application id.
