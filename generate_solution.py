import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import zipfile
import shutil

NS = uuid.UUID("a1b2c3d4-e5f6-7890-abcd-ef1234567890")

def guid(name):
    return str(uuid.uuid5(NS, name))

def g(name):
    return "{" + guid(name) + "}"

PUBLISHER_PREFIX = "adcci"

APPLICATION_STATUS = {
    "name": f"{PUBLISHER_PREFIX}_esgapplicationstatus",
    "display": "ESG Application Status",
    "options": [
        (100000000, "Draft"),
        (100000001, "EOI Submitted"),
        (100000002, "EOI Flagged - Awaiting Info"),
        (100000003, "EOI Under Manual Review"),
        (100000004, "EOI Approved"),
        (100000005, "EOI Rejected"),
        (100000006, "Self-Assessment In Progress"),
        (100000007, "Self-Assessment Submitted"),
        (100000008, "Under Document Validation"),
        (100000009, "Returned for Missing Info"),
        (100000010, "Validated"),
        (100000011, "Partially Validated"),
        (100000012, "Validation Rejected"),
        (100000013, "Scoring Complete"),
        (100000014, "Report Generated"),
        (100000015, "Report Endorsed"),
        (100000016, "Pending Final Approval"),
        (100000017, "Approved"),
        (100000018, "Rejected"),
        (100000019, "Certificate Issued"),
        (100000020, "Completed"),
    ]
}

LABEL_TIER = {
    "name": f"{PUBLISHER_PREFIX}_esglabeltier",
    "display": "ESG Label Tier",
    "options": [
        (100000000, "Bronze"),
        (100000001, "Silver"),
        (100000002, "Gold"),
        (100000003, "Diamond"),
    ]
}

REVIEW_TYPE = {
    "name": f"{PUBLISHER_PREFIX}_esgreviewtype",
    "display": "ESG Review Type",
    "options": [
        (100000000, "EOI Manual Review"),
        (100000001, "Document Validation"),
        (100000002, "Secondary Document Review"),
        (100000003, "Report Endorsement"),
        (100000004, "Final Approval"),
    ]
}

REVIEW_DECISION = {
    "name": f"{PUBLISHER_PREFIX}_esgreviewdecision",
    "display": "ESG Review Decision",
    "options": [
        (100000000, "Approve"),
        (100000001, "Reject"),
        (100000002, "Return for Missing Information"),
        (100000003, "Endorse"),
        (100000004, "Partially Validate"),
        (100000005, "Override Rejection"),
    ]
}

DOCUMENT_TYPE = {
    "name": f"{PUBLISHER_PREFIX}_esgdocumenttype",
    "display": "ESG Document Type",
    "options": [
        (100000000, "Expression of Commitment"),
        (100000001, "Supporting Evidence"),
        (100000002, "Maturity Report"),
        (100000003, "Certificate"),
        (100000004, "Other"),
    ]
}

DOCUMENT_VALIDATION_STATUS = {
    "name": f"{PUBLISHER_PREFIX}_esgdocvalidationstatus",
    "display": "ESG Document Validation Status",
    "options": [
        (100000000, "Pending Review"),
        (100000001, "Validated"),
        (100000002, "Rejected"),
        (100000003, "Missing"),
        (100000004, "Resubmission Required"),
    ]
}

REPORT_STATUS = {
    "name": f"{PUBLISHER_PREFIX}_esgreportstatus",
    "display": "ESG Report Status",
    "options": [
        (100000000, "Generated"),
        (100000001, "Pending Endorsement"),
        (100000002, "Endorsed"),
        (100000003, "Pending Final Approval"),
        (100000004, "Approved"),
        (100000005, "Rejected"),
        (100000006, "Returned for Recalculation"),
    ]
}

NOTIFICATION_EVENT = {
    "name": f"{PUBLISHER_PREFIX}_esgnotificationevent",
    "display": "ESG Notification Event",
    "options": [
        (100000000, "N-01: EOI Submitted"),
        (100000001, "N-02: EOI Auto-Approved"),
        (100000002, "N-03: EOI Flagged"),
        (100000003, "N-04: Explanation Submitted"),
        (100000004, "N-05: EOI Rejected (Manual)"),
        (100000005, "N-06: EOI Approved (Manual)"),
        (100000006, "N-07: Questionnaire Mid-SLA Reminder"),
        (100000007, "N-08: Questionnaire Submitted"),
        (100000008, "N-09: Returned for Info"),
        (100000009, "N-10: Resubmission Received"),
        (100000010, "N-11: Application Rejected (Validation)"),
        (100000011, "N-12: Report Endorsed"),
        (100000012, "N-13: Final Decision Made"),
        (100000013, "N-14: Certificate Issued"),
        (100000014, "N-15: Application Closed"),
    ]
}

NOTIFICATION_STATUS = {
    "name": f"{PUBLISHER_PREFIX}_esgnotificationstatus",
    "display": "ESG Notification Status",
    "options": [
        (100000000, "Pending"),
        (100000001, "Sent"),
        (100000002, "Failed"),
    ]
}

INDUSTRY_SECTOR = {
    "name": f"{PUBLISHER_PREFIX}_esgindustrysector",
    "display": "Industry Sector",
    "options": [
        (100000000, "Agriculture & Food"),
        (100000001, "Banking & Financial Services"),
        (100000002, "Construction & Real Estate"),
        (100000003, "Education"),
        (100000004, "Energy & Utilities"),
        (100000005, "Healthcare & Pharmaceuticals"),
        (100000006, "Hospitality & Tourism"),
        (100000007, "Information Technology"),
        (100000008, "Manufacturing"),
        (100000009, "Oil & Gas"),
        (100000010, "Professional Services"),
        (100000011, "Retail & Consumer Goods"),
        (100000012, "Telecommunications"),
        (100000013, "Transportation & Logistics"),
        (100000014, "Other"),
    ]
}

MATURITY_LEVEL = {
    "name": f"{PUBLISHER_PREFIX}_esgmaturitylevel",
    "display": "ESG Maturity Level",
    "options": [
        (100000000, "Compliance"),
        (100000001, "Awareness & Reporting"),
        (100000002, "Risk Management"),
        (100000003, "Value Creation"),
        (100000004, "Purpose Driven"),
    ]
}

ALL_OPTIONSETS = [
    APPLICATION_STATUS, LABEL_TIER, REVIEW_TYPE, REVIEW_DECISION,
    DOCUMENT_TYPE, DOCUMENT_VALIDATION_STATUS, REPORT_STATUS,
    NOTIFICATION_EVENT, NOTIFICATION_STATUS, INDUSTRY_SECTOR, MATURITY_LEVEL
]

def attr_text(name, display, required="none", maxlen=200, desc="", fmt="text"):
    return {"type": "nvarchar", "name": name, "display": display, "required": required, "maxlen": maxlen, "desc": desc, "format": fmt}

def attr_memo(name, display, required="none", maxlen=10000, desc=""):
    return {"type": "memo", "name": name, "display": display, "required": required, "maxlen": maxlen, "desc": desc}

def attr_int(name, display, required="none", minval=0, maxval=2147483647, desc=""):
    return {"type": "int", "name": name, "display": display, "required": required, "min": minval, "max": maxval, "desc": desc}

def attr_decimal(name, display, required="none", minval=0, maxval=999999, precision=2, desc=""):
    return {"type": "decimal", "name": name, "display": display, "required": required, "min": minval, "max": maxval, "precision": precision, "desc": desc}

def attr_bool(name, display, required="none", true_label="Yes", false_label="No", desc=""):
    return {"type": "bool", "name": name, "display": display, "required": required, "true_label": true_label, "false_label": false_label, "desc": desc}

def attr_datetime(name, display, required="none", desc=""):
    return {"type": "datetime", "name": name, "display": display, "required": required, "desc": desc}

def attr_optionset(name, display, optionset_ref, required="none", desc=""):
    return {"type": "optionset", "name": name, "display": display, "required": required, "optionset": optionset_ref, "desc": desc}

def attr_lookup(name, display, target_entity, required="none", desc=""):
    return {"type": "lookup", "name": name, "display": display, "required": required, "target": target_entity, "desc": desc}

P = PUBLISHER_PREFIX

ESG_APPLICATION = {
    "schema": f"{P}_esgapplication",
    "display": "ESG Application",
    "display_plural": "ESG Applications",
    "description": "Tracks the full lifecycle of an ESG Sustainability Label application from EOI to certification.",
    "primary_field": f"{P}_name",
    "primary_display": "Application Reference",
    "attributes": [
        attr_text(f"{P}_organisationname", "Organisation Name", "required", 300, "Legal name of the applying organisation."),
        attr_text(f"{P}_tradelicensenumber", "Trade License Number", "required", 100, "Trade license number of the organisation."),
        attr_text(f"{P}_organisationemail", "Organisation Email", "required", 100, "Primary email address of the organisation.", "email"),
        attr_text(f"{P}_primarycontactname", "Primary Point of Contact", "required", 200, "Name of the primary contact person."),
        attr_text(f"{P}_contactemail", "Contact Email Address", "required", 100, "Email address of the primary contact.", "email"),
        attr_text(f"{P}_contactphone", "Contact Phone Number", "required", 50, "Phone number of the primary contact.", "phone"),
        attr_int(f"{P}_yearsinoperation", "Number of Years in Operation", "required", 0, 500, "Flag if < 5 years."),
        attr_int(f"{P}_numberofemployees", "Number of Employees", "required", 0, 10000000, "Flag if < 25."),
        attr_optionset(f"{P}_industrysector", "Industry / Sector", INDUSTRY_SECTOR, "required", "Primary industry sector."),
        attr_text(f"{P}_countriesofoperation", "Countries of Operation", "required", 500, "Countries where the organisation operates."),
        attr_memo(f"{P}_shareholdersandowners", "Shareholders and Owners", "none", 10000, "Details of shareholders and owners."),
        attr_memo(f"{P}_boardmembers", "Board Members", "required", 10000, "List of board members."),
        attr_bool(f"{P}_compliancewithregulations", "Compliance with Regulations", "required", "Yes", "No", "Has the organisation operated in compliance? Flag if No."),
        attr_bool(f"{P}_breachofregulations", "Breach of Regulations (Past 5 Years)", "required", "Yes", "No", "Found in breach in past 5 years? Flag if Yes."),
        attr_bool(f"{P}_leadershipcommitment", "Leadership Commitment", "required", "Yes", "No", "Does the org have leadership commitment? Flag if No."),
        attr_bool(f"{P}_abilitytoprovidedocs", "Ability to Provide Documentation", "required", "Yes", "No", "Can provide supporting documentation? Flag if No."),
        attr_bool(f"{P}_declarationofaccuracy", "Declaration of Accuracy", "required", "Yes", "No", "Applicant declares all information is accurate."),
        attr_memo(f"{P}_contextforconsideration", "Context for Consideration", "none", 10000, "Additional context for flagged criteria."),
        attr_optionset(f"{P}_applicationstatus", "Application Status", APPLICATION_STATUS, "required", "Current status of the ESG application."),
        attr_int(f"{P}_eligibilityscore", "Eligibility Score", "none", 0, 6, "Number of eligibility criteria met (max 6)."),
        attr_int(f"{P}_flagcount", "Flag Count", "none", 0, 6, "Number of eligibility flags raised."),
        attr_datetime(f"{P}_eoisubmissiondate", "EOI Submission Date", "none", "Date when the EOI was submitted."),
        attr_datetime(f"{P}_eoiapprovaldate", "EOI Approval Date", "none", "Date when the EOI was approved."),
        attr_datetime(f"{P}_assessmentdeadline", "Assessment Deadline", "none", "Deadline for self-assessment (15 days from EOI approval)."),
        attr_datetime(f"{P}_assessmentsubmissiondate", "Assessment Submission Date", "none", "Date when the self-assessment was submitted."),
        attr_decimal(f"{P}_overallmaturityscore", "Overall Maturity Score", "none", 0, 100, 2, "Final calculated maturity score."),
        attr_optionset(f"{P}_labeltier", "Label Tier", LABEL_TIER, "none", "Awarded label tier based on maturity score."),
        attr_lookup(f"{P}_applicantid", "Applicant", "Contact", "none", "Contact record for the applicant."),
    ],
    "form_tabs": [
        {"name": "tab_eoi", "label": "Expression of Interest", "sections": [
            {"name": "sec_orginfo", "label": "Organisation Information", "fields": [
                f"{P}_organisationname", f"{P}_tradelicensenumber", f"{P}_organisationemail",
                f"{P}_industrysector", f"{P}_countriesofoperation", f"{P}_applicantid"]},
            {"name": "sec_contact", "label": "Contact Information", "fields": [
                f"{P}_primarycontactname", f"{P}_contactemail", f"{P}_contactphone"]},
            {"name": "sec_governance", "label": "Governance & Ownership", "fields": [
                f"{P}_boardmembers", f"{P}_shareholdersandowners"]}]},
        {"name": "tab_eligibility", "label": "Eligibility Screening", "sections": [
            {"name": "sec_criteria", "label": "Eligibility Criteria", "fields": [
                f"{P}_yearsinoperation", f"{P}_numberofemployees", f"{P}_compliancewithregulations",
                f"{P}_breachofregulations", f"{P}_leadershipcommitment", f"{P}_abilitytoprovidedocs"]},
            {"name": "sec_eligresults", "label": "Eligibility Results", "fields": [
                f"{P}_eligibilityscore", f"{P}_flagcount", f"{P}_declarationofaccuracy",
                f"{P}_contextforconsideration"]}]},
        {"name": "tab_status", "label": "Status & Scoring", "sections": [
            {"name": "sec_appstatus", "label": "Application Status", "fields": [
                f"{P}_applicationstatus", f"{P}_eoisubmissiondate", f"{P}_eoiapprovaldate",
                f"{P}_assessmentdeadline", f"{P}_assessmentsubmissiondate"]},
            {"name": "sec_scoring", "label": "Scoring & Certification", "fields": [
                f"{P}_overallmaturityscore", f"{P}_labeltier"]}]},
    ],
    "view_columns": [
        (f"{P}_name", "Application Reference", 200),
        (f"{P}_organisationname", "Organisation", 200),
        (f"{P}_applicationstatus", "Status", 150),
        (f"{P}_labeltier", "Label Tier", 100),
        ("createdon", "Created On", 125),
    ],
}

ELIGIBILITY_CHECK = {
    "schema": f"{P}_eligibilitycheck",
    "display": "Eligibility Check",
    "display_plural": "Eligibility Checks",
    "description": "Individual eligibility criteria evaluation for an ESG application.",
    "primary_field": f"{P}_name",
    "primary_display": "Criteria Name",
    "attributes": [
        attr_lookup(f"{P}_applicationid", "ESG Application", f"{P}_esgapplication", "required", "Parent ESG application."),
        attr_text(f"{P}_criteriadescription", "Criteria Description", "none", 500, "Description of the eligibility criterion."),
        attr_bool(f"{P}_criteriamet", "Criteria Met", "none", "Yes", "No", "Whether the criterion was met."),
        attr_bool(f"{P}_flagged", "Flagged", "none", "Yes", "No", "Whether this criterion raised a flag."),
        attr_text(f"{P}_flagreason", "Flag Reason", "none", 500, "Reason the criterion was flagged."),
        attr_datetime(f"{P}_checkdate", "Check Date", "none", "Date when the check was performed."),
    ],
    "form_tabs": [
        {"name": "tab_general", "label": "General", "sections": [
            {"name": "sec_details", "label": "Check Details", "fields": [
                f"{P}_name", f"{P}_applicationid", f"{P}_criteriadescription",
                f"{P}_criteriamet", f"{P}_flagged", f"{P}_flagreason", f"{P}_checkdate"]}]}],
    "view_columns": [
        (f"{P}_name", "Criteria Name", 200), (f"{P}_applicationid", "Application", 200),
        (f"{P}_criteriamet", "Met", 80), (f"{P}_flagged", "Flagged", 80), (f"{P}_checkdate", "Check Date", 125)],
}

ASSESSMENT_RESPONSE = {
    "schema": f"{P}_assessmentresponse",
    "display": "Self-Assessment Response",
    "display_plural": "Self-Assessment Responses",
    "description": "Individual questionnaire response for an ESG self-assessment.",
    "primary_field": f"{P}_name",
    "primary_display": "Response Reference",
    "attributes": [
        attr_lookup(f"{P}_applicationid", "ESG Application", f"{P}_esgapplication", "required", "Parent ESG application."),
        attr_int(f"{P}_themenumber", "Theme Number", "required", 1, 33, "Sustainability theme number (1-33)."),
        attr_text(f"{P}_themename", "Theme Name", "required", 300, "Name of the sustainability theme."),
        attr_int(f"{P}_questionnumber", "Question Number", "required", 1, 999, "Question number within the theme."),
        attr_memo(f"{P}_questiontext", "Question Text", "required", 5000, "Full text of the assessment question."),
        attr_memo(f"{P}_answer", "Answer", "none", 10000, "Applicant response to the question."),
        attr_decimal(f"{P}_existsscore", "Exists Score", "none", 0, 100, 2, "Score for the Exists dimension."),
        attr_decimal(f"{P}_usedscore", "Used Score", "none", 0, 100, 2, "Score for the Used dimension."),
        attr_decimal(f"{P}_effectivescore", "Effective Score", "none", 0, 100, 2, "Score for the Effective dimension."),
        attr_optionset(f"{P}_maturitylevel", "Maturity Level", MATURITY_LEVEL, "none", "Assessed maturity level for this theme."),
    ],
    "form_tabs": [
        {"name": "tab_general", "label": "General", "sections": [
            {"name": "sec_question", "label": "Question Details", "fields": [
                f"{P}_name", f"{P}_applicationid", f"{P}_themenumber", f"{P}_themename",
                f"{P}_questionnumber", f"{P}_questiontext", f"{P}_answer"]},
            {"name": "sec_scoring", "label": "Scoring", "fields": [
                f"{P}_existsscore", f"{P}_usedscore", f"{P}_effectivescore", f"{P}_maturitylevel"]}]}],
    "view_columns": [
        (f"{P}_name", "Reference", 150), (f"{P}_applicationid", "Application", 150),
        (f"{P}_themename", "Theme", 200), (f"{P}_questionnumber", "Q#", 60), (f"{P}_maturitylevel", "Maturity", 120)],
}

ESG_DOCUMENT = {
    "schema": f"{P}_esgdocument",
    "display": "ESG Document",
    "display_plural": "ESG Documents",
    "description": "Document uploaded as part of an ESG application or self-assessment.",
    "primary_field": f"{P}_name",
    "primary_display": "Document Name",
    "attributes": [
        attr_lookup(f"{P}_applicationid", "ESG Application", f"{P}_esgapplication", "required", "Parent ESG application."),
        attr_lookup(f"{P}_assessmentresponseid", "Assessment Response", f"{P}_assessmentresponse", "none", "Related assessment response."),
        attr_optionset(f"{P}_documenttype", "Document Type", DOCUMENT_TYPE, "required", "Type of document."),
        attr_text(f"{P}_filename", "File Name", "none", 500, "Original file name of the uploaded document."),
        attr_int(f"{P}_filesizekb", "File Size (KB)", "none", 0, 10485760, "File size in kilobytes."),
        attr_optionset(f"{P}_validationstatus", "Validation Status", DOCUMENT_VALIDATION_STATUS, "none", "Current validation status."),
        attr_memo(f"{P}_reviewercomments", "Reviewer Comments", "none", 5000, "Comments from the reviewer on this document."),
        attr_datetime(f"{P}_uploaddate", "Upload Date", "none", "Date when the document was uploaded."),
    ],
    "form_tabs": [
        {"name": "tab_general", "label": "General", "sections": [
            {"name": "sec_docinfo", "label": "Document Information", "fields": [
                f"{P}_name", f"{P}_applicationid", f"{P}_assessmentresponseid",
                f"{P}_documenttype", f"{P}_filename", f"{P}_filesizekb", f"{P}_uploaddate"]},
            {"name": "sec_validation", "label": "Validation", "fields": [
                f"{P}_validationstatus", f"{P}_reviewercomments"]}]}],
    "view_columns": [
        (f"{P}_name", "Document Name", 200), (f"{P}_applicationid", "Application", 150),
        (f"{P}_documenttype", "Type", 120), (f"{P}_validationstatus", "Status", 120), (f"{P}_uploaddate", "Uploaded", 125)],
}

ESG_REVIEW = {
    "schema": f"{P}_esgreview",
    "display": "ESG Review",
    "display_plural": "ESG Reviews",
    "description": "Manual review or approval record for an ESG application.",
    "primary_field": f"{P}_name",
    "primary_display": "Review Reference",
    "attributes": [
        attr_lookup(f"{P}_applicationid", "ESG Application", f"{P}_esgapplication", "required", "Parent ESG application."),
        attr_optionset(f"{P}_reviewtype", "Review Type", REVIEW_TYPE, "required", "Type of review being performed."),
        attr_text(f"{P}_reviewername", "Reviewer Name", "none", 200, "Name of the person who performed the review."),
        attr_optionset(f"{P}_decision", "Decision", REVIEW_DECISION, "required", "Decision made by the reviewer."),
        attr_memo(f"{P}_comments", "Comments", "required", 10000, "Detailed comments and rationale for the decision."),
        attr_datetime(f"{P}_reviewdate", "Review Date", "none", "Date when the review was performed."),
        attr_text(f"{P}_sladays", "SLA (Days)", "none", 10, "Service Level Agreement days for this review type."),
    ],
    "form_tabs": [
        {"name": "tab_general", "label": "General", "sections": [
            {"name": "sec_reviewinfo", "label": "Review Information", "fields": [
                f"{P}_name", f"{P}_applicationid", f"{P}_reviewtype", f"{P}_reviewername",
                f"{P}_decision", f"{P}_comments", f"{P}_reviewdate", f"{P}_sladays"]}]}],
    "view_columns": [
        (f"{P}_name", "Reference", 150), (f"{P}_applicationid", "Application", 150),
        (f"{P}_reviewtype", "Type", 150), (f"{P}_decision", "Decision", 120), (f"{P}_reviewdate", "Date", 125)],
}

MATURITY_REPORT = {
    "schema": f"{P}_maturityreport",
    "display": "Maturity Report",
    "display_plural": "Maturity Reports",
    "description": "Auto-generated Sustainability Maturity Report with scores and recommendations.",
    "primary_field": f"{P}_name",
    "primary_display": "Report Title",
    "attributes": [
        attr_lookup(f"{P}_applicationid", "ESG Application", f"{P}_esgapplication", "required", "Parent ESG application."),
        attr_decimal(f"{P}_overallscore", "Overall Score", "none", 0, 100, 2, "Final overall maturity score."),
        attr_optionset(f"{P}_labeltier", "Label Tier", LABEL_TIER, "none", "Awarded label tier."),
        attr_optionset(f"{P}_reportstatus", "Report Status", REPORT_STATUS, "required", "Current status of the report."),
        attr_datetime(f"{P}_generationdate", "Generation Date", "none", "Date the report was auto-generated."),
        attr_text(f"{P}_endorsedbyname", "Endorsed By", "none", 200, "Name of the Products Section Head who endorsed."),
        attr_datetime(f"{P}_endorseddate", "Endorsed Date", "none", "Date when the report was endorsed."),
        attr_text(f"{P}_approvedbyname", "Approved By", "none", 200, "Name of the Director who approved."),
        attr_datetime(f"{P}_approveddate", "Approved Date", "none", "Date when the report received final approval."),
        attr_memo(f"{P}_scoreadjustmentnotes", "Score Adjustment Notes", "none", 5000, "Notes about any score adjustments."),
        attr_memo(f"{P}_recommendations", "Recommendations", "none", 50000, "Personalized recommendations and actionable insights."),
    ],
    "form_tabs": [
        {"name": "tab_general", "label": "General", "sections": [
            {"name": "sec_reportinfo", "label": "Report Information", "fields": [
                f"{P}_name", f"{P}_applicationid", f"{P}_overallscore",
                f"{P}_labeltier", f"{P}_reportstatus", f"{P}_generationdate"]},
            {"name": "sec_approval", "label": "Endorsement & Approval", "fields": [
                f"{P}_endorsedbyname", f"{P}_endorseddate", f"{P}_approvedbyname",
                f"{P}_approveddate", f"{P}_scoreadjustmentnotes"]},
            {"name": "sec_recommendations", "label": "Recommendations", "fields": [
                f"{P}_recommendations"]}]}],
    "view_columns": [
        (f"{P}_name", "Report", 200), (f"{P}_applicationid", "Application", 150),
        (f"{P}_overallscore", "Score", 80), (f"{P}_labeltier", "Tier", 100), (f"{P}_reportstatus", "Status", 120)],
}

ESG_CERTIFICATE = {
    "schema": f"{P}_esgcertificate",
    "display": "ESG Certificate",
    "display_plural": "ESG Certificates",
    "description": "Official ADCCI Sustainability Label Certificate issued upon final approval.",
    "primary_field": f"{P}_name",
    "primary_display": "Certificate ID",
    "attributes": [
        attr_lookup(f"{P}_applicationid", "ESG Application", f"{P}_esgapplication", "required", "Parent ESG application."),
        attr_lookup(f"{P}_reportid", "Maturity Report", f"{P}_maturityreport", "required", "Associated maturity report."),
        attr_text(f"{P}_organisationname", "Organisation Name", "required", 300, "Name of the certified organisation."),
        attr_optionset(f"{P}_labeltier", "Label Tier", LABEL_TIER, "required", "Awarded sustainability label tier."),
        attr_datetime(f"{P}_issuedate", "Issue Date", "required", "Date the certificate was issued."),
        attr_datetime(f"{P}_expirydate", "Expiry Date", "none", "Certificate expiration date."),
    ],
    "form_tabs": [
        {"name": "tab_general", "label": "General", "sections": [
            {"name": "sec_certinfo", "label": "Certificate Information", "fields": [
                f"{P}_name", f"{P}_applicationid", f"{P}_reportid",
                f"{P}_organisationname", f"{P}_labeltier", f"{P}_issuedate", f"{P}_expirydate"]}]}],
    "view_columns": [
        (f"{P}_name", "Certificate ID", 150), (f"{P}_organisationname", "Organisation", 200),
        (f"{P}_labeltier", "Tier", 100), (f"{P}_issuedate", "Issued", 125), (f"{P}_expirydate", "Expires", 125)],
}

ESG_NOTIFICATION = {
    "schema": f"{P}_esgnotification",
    "display": "ESG Notification",
    "display_plural": "ESG Notifications",
    "description": "Log of automated notifications sent during the ESG application lifecycle.",
    "primary_field": f"{P}_name",
    "primary_display": "Notification Reference",
    "attributes": [
        attr_lookup(f"{P}_applicationid", "ESG Application", f"{P}_esgapplication", "none", "Related ESG application."),
        attr_optionset(f"{P}_eventtype", "Event Type", NOTIFICATION_EVENT, "required", "Type of notification event."),
        attr_text(f"{P}_recipientemail", "Recipient Email", "required", 100, "Email of the notification recipient.", "email"),
        attr_text(f"{P}_recipientname", "Recipient Name", "none", 200, "Name of the recipient."),
        attr_text(f"{P}_subject", "Subject", "required", 500, "Notification subject line."),
        attr_memo(f"{P}_messagebody", "Message Body", "none", 50000, "Full notification message content."),
        attr_optionset(f"{P}_notificationstatus", "Notification Status", NOTIFICATION_STATUS, "required", "Delivery status of the notification."),
        attr_datetime(f"{P}_sentdate", "Sent Date", "none", "Date and time the notification was sent."),
    ],
    "form_tabs": [
        {"name": "tab_general", "label": "General", "sections": [
            {"name": "sec_notifinfo", "label": "Notification Details", "fields": [
                f"{P}_name", f"{P}_applicationid", f"{P}_eventtype", f"{P}_recipientname",
                f"{P}_recipientemail", f"{P}_subject", f"{P}_messagebody",
                f"{P}_notificationstatus", f"{P}_sentdate"]}]}],
    "view_columns": [
        (f"{P}_name", "Reference", 150), (f"{P}_eventtype", "Event", 200),
        (f"{P}_recipientemail", "Recipient", 200), (f"{P}_notificationstatus", "Status", 100), (f"{P}_sentdate", "Sent", 125)],
}

ALL_ENTITIES = [
    ESG_APPLICATION, ELIGIBILITY_CHECK, ASSESSMENT_RESPONSE,
    ESG_DOCUMENT, ESG_REVIEW, MATURITY_REPORT,
    ESG_CERTIFICATE, ESG_NOTIFICATION
]

CONTROL_CLASSIDS = {
    "nvarchar": "{4273EDBD-AC1D-40d3-9FB2-095C621B552D}",
    "memo": "{E0DECE4B-6FC8-4a8f-A065-082708572369}",
    "int": "{C6D124CA-7EDA-4a60-AEA3-7F0A0BE7CF71}",
    "decimal": "{C3EFE0C3-0EC6-42be-8349-CBD9079DFD8E}",
    "bool": "{B0C6723A-8503-4fd7-BB28-C8A06AC933C2}",
    "datetime": "{5B773807-9FB2-42db-97C3-7A91EFF8ADFF}",
    "optionset": "{3EF39988-22BB-4f0b-BBBE-64B5A3748AEE}",
    "lookup": "{270BD3DB-D9AF-4782-9025-509E298DEC0A}",
}


def build_attribute_xml(attr_def, entity_schema=""):
    a = attr_def
    name = a["name"]
    atype = a["type"]
    attr_el = ET.Element("attribute", PhysicalName=name)
    type_map = {"nvarchar": "nvarchar", "memo": "ntext", "int": "int", "decimal": "decimal",
                "bool": "bit", "datetime": "datetime", "optionset": "picklist", "lookup": "lookup"}
    ET.SubElement(attr_el, "Type").text = type_map.get(atype, atype)
    ET.SubElement(attr_el, "Name").text = name
    ET.SubElement(attr_el, "LogicalName").text = name.lower()
    ET.SubElement(attr_el, "RequiredLevel").text = a.get("required", "none")
    ET.SubElement(attr_el, "DisplayMask").text = "ValidForAdvancedFind|ValidForForm|ValidForGrid"
    ET.SubElement(attr_el, "ImeMode").text = "auto"
    ET.SubElement(attr_el, "ValidForUpdateApi").text = "1"
    ET.SubElement(attr_el, "ValidForReadApi").text = "1"
    ET.SubElement(attr_el, "ValidForCreateApi").text = "1"
    ET.SubElement(attr_el, "IsCustomField").text = "1"
    ET.SubElement(attr_el, "IsAuditEnabled").text = "1"
    ET.SubElement(attr_el, "IsSecured").text = "0"
    ET.SubElement(attr_el, "IntroducedVersion").text = "1.1.0.0"
    ET.SubElement(attr_el, "IsCustomizable").text = "1"
    ET.SubElement(attr_el, "IsRenameable").text = "1"
    ET.SubElement(attr_el, "CanModifySearchSettings").text = "1"
    ET.SubElement(attr_el, "CanModifyRequirementLevelSettings").text = "1"
    ET.SubElement(attr_el, "CanModifyAdditionalSettings").text = "1"
    ET.SubElement(attr_el, "SourceType").text = "0"
    ET.SubElement(attr_el, "IsGlobalFilterEnabled").text = "0"
    ET.SubElement(attr_el, "IsSortableEnabled").text = "0"
    ET.SubElement(attr_el, "CanModifyGlobalFilterSettings").text = "1"
    ET.SubElement(attr_el, "CanModifyIsSortableSettings").text = "1"
    ET.SubElement(attr_el, "IsDataSourceSecret").text = "0"
    ET.SubElement(attr_el, "AutoNumberFormat")
    ET.SubElement(attr_el, "IsSearchable").text = "0"
    ET.SubElement(attr_el, "IsFilterable").text = "1"
    ET.SubElement(attr_el, "IsRetrievable").text = "1"
    ET.SubElement(attr_el, "IsLocalizable").text = "0"
    if atype == "nvarchar":
        maxlen = a.get("maxlen", 200)
        ET.SubElement(attr_el, "Format").text = a.get("format", "text")
        ET.SubElement(attr_el, "MaxLength").text = str(maxlen)
        ET.SubElement(attr_el, "Length").text = str(maxlen * 2)
    elif atype == "memo":
        maxlen = a.get("maxlen", 10000)
        ET.SubElement(attr_el, "Format").text = "text"
        ET.SubElement(attr_el, "MaxLength").text = str(maxlen)
        ET.SubElement(attr_el, "Length").text = str(maxlen * 2)
    elif atype == "int":
        ET.SubElement(attr_el, "Format").text = "none"
        ET.SubElement(attr_el, "MinValue").text = str(a.get("min", -2147483648))
        ET.SubElement(attr_el, "MaxValue").text = str(a.get("max", 2147483647))
    elif atype == "decimal":
        ET.SubElement(attr_el, "MinValue").text = str(a.get("min", 0))
        ET.SubElement(attr_el, "MaxValue").text = str(a.get("max", 999999))
        ET.SubElement(attr_el, "Precision").text = str(a.get("precision", 2))
    elif atype == "bool":
        ET.SubElement(attr_el, "AppDefaultValue").text = "0"
        entity_logical = entity_schema.lower() if entity_schema else "adcci_entity"
        attr_suffix = name.lower().replace("adcci_", "")
        optset_name = f"adcci_{entity_logical}_{attr_suffix}"
        optset = ET.SubElement(attr_el, "optionset", Name=optset_name)
        ET.SubElement(optset, "OptionSetType").text = "bit"
        ET.SubElement(optset, "IntroducedVersion").text = "1.1.0.0"
        ET.SubElement(optset, "IsCustomizable").text = "1"
        os_dn = ET.SubElement(optset, "displaynames")
        ET.SubElement(os_dn, "displayname", description="Local Enumeration", languagecode="1033")
        os_desc = ET.SubElement(optset, "Descriptions")
        ET.SubElement(os_desc, "Description", description="", languagecode="1033")
        options_el = ET.SubElement(optset, "options")
        true_opt = ET.SubElement(options_el, "option", value="1", IsHidden="0")
        tl = ET.SubElement(true_opt, "labels")
        ET.SubElement(tl, "label", description=a.get("true_label", "Yes"), languagecode="1033")
        false_opt = ET.SubElement(options_el, "option", value="0", IsHidden="0")
        fl = ET.SubElement(false_opt, "labels")
        ET.SubElement(fl, "label", description=a.get("false_label", "No"), languagecode="1033")
    elif atype == "datetime":
        ET.SubElement(attr_el, "Format").text = a.get("format", "datetime")
        ET.SubElement(attr_el, "CanChangeDateTimeBehavior").text = "1"
        ET.SubElement(attr_el, "Behavior").text = "1"
    elif atype == "optionset":
        optref = a.get("optionset", {})
        ET.SubElement(attr_el, "AppDefaultValue").text = "-1"
        ET.SubElement(attr_el, "OptionSetName").text = optref.get("name", "")
    elif atype == "lookup":
        ET.SubElement(attr_el, "LookupStyle").text = "single"
        ET.SubElement(attr_el, "LookupTypes")
    dn = ET.SubElement(attr_el, "displaynames")
    ET.SubElement(dn, "displayname", description=a["display"], languagecode="1033")
    desc_el = ET.SubElement(attr_el, "Descriptions")
    ET.SubElement(desc_el, "Description", description=a.get("desc", ""), languagecode="1033")
    return attr_el


def build_form_xml(entity_def):
    form = ET.Element("form")
    tabs = ET.SubElement(form, "tabs")
    for tab_def in entity_def.get("form_tabs", []):
        tab = ET.SubElement(tabs, "tab", name=tab_def["name"],
            id=g(f"form_tab_{entity_def['schema']}_{tab_def['name']}"), IsUserDefined="1", locklevel="0")
        lbls = ET.SubElement(tab, "labels")
        ET.SubElement(lbls, "label", description=tab_def["label"], languagecode="1033")
        columns = ET.SubElement(tab, "columns")
        column = ET.SubElement(columns, "column", width="100%")
        sections = ET.SubElement(column, "sections")
        for sec_def in tab_def.get("sections", []):
            section = ET.SubElement(sections, "section", name=sec_def["name"], showlabel="true",
                showbar="false", locklevel="0", id=g(f"form_sec_{entity_def['schema']}_{sec_def['name']}"),
                IsUserDefined="1", layout="varwidth", columns="2", labelwidth="115", celllabelposition="Left")
            slbls = ET.SubElement(section, "labels")
            ET.SubElement(slbls, "label", description=sec_def["label"], languagecode="1033")
            rows = ET.SubElement(section, "rows")
            for field_name in sec_def.get("fields", []):
                row = ET.SubElement(rows, "row")
                cell = ET.SubElement(row, "cell", id=g(f"form_cell_{entity_def['schema']}_{field_name}"),
                    showlabel="true", locklevel="0")
                clbls = ET.SubElement(cell, "labels")
                field_display = field_name
                for a in entity_def.get("attributes", []):
                    if a["name"] == field_name:
                        field_display = a["display"]
                        break
                if field_name == entity_def["primary_field"]:
                    field_display = entity_def["primary_display"]
                ET.SubElement(clbls, "label", description=field_display, languagecode="1033")
                atype = "nvarchar"
                for a in entity_def.get("attributes", []):
                    if a["name"] == field_name:
                        atype = a["type"]
                        break
                classid = CONTROL_CLASSIDS.get(atype, CONTROL_CLASSIDS["nvarchar"])
                ET.SubElement(cell, "control", id=field_name, classid=classid, datafieldname=field_name, disabled="false")
    return ET.tostring(form, encoding="unicode")


def build_view_xml(entity_def):
    schema = entity_def["schema"]
    view_cols = entity_def.get("view_columns", [])
    fetch = ET.Element("fetch", version="1.0", mapping="logical", distinct="false")
    fetch.set("output-format", "xml-platform")
    ent = ET.SubElement(fetch, "entity", name=schema)
    for col_name, _, _ in view_cols:
        ET.SubElement(ent, "attribute", name=col_name)
    ET.SubElement(ent, "order", attribute=view_cols[0][0] if view_cols else f"{P}_name", descending="false")
    filt = ET.SubElement(ent, "filter", type="and")
    ET.SubElement(filt, "condition", attribute="statecode", operator="eq", value="0")
    fetchxml = ET.tostring(fetch, encoding="unicode")
    grid = ET.Element("grid", name="resultset", select="1", icon="1", preview="1")
    grid.set("jump", view_cols[0][0] if view_cols else f"{P}_name")
    row = ET.SubElement(grid, "row", name="result", id=f"{schema}id")
    for col_name, _, width in view_cols:
        ET.SubElement(row, "cell", name=col_name, width=str(width))
    layoutxml = ET.tostring(grid, encoding="unicode")
    return fetchxml, layoutxml


def build_entity_xml(entity_def, existing_entities_el):
    schema = entity_def["schema"]
    display = entity_def["display"]
    display_plural = entity_def["display_plural"]
    entity_el = ET.SubElement(existing_entities_el, "Entity")
    name_el = ET.SubElement(entity_el, "Name", LocalizedName=display, OriginalName=display)
    name_el.text = schema
    einfo = ET.SubElement(entity_el, "EntityInfo")
    ent = ET.SubElement(einfo, "entity", Name=schema)
    pk_name = schema + "id"
    ln = ET.SubElement(ent, "LocalizedNames")
    ET.SubElement(ln, "LocalizedName", description=display, languagecode="1033")
    lnp = ET.SubElement(ent, "LocalizedCollectionNames")
    ET.SubElement(lnp, "LocalizedCollectionName", description=display_plural, languagecode="1033")
    desc_el = ET.SubElement(ent, "Descriptions")
    ET.SubElement(desc_el, "Description", description=entity_def.get("description", ""), languagecode="1033")
    attrs_el = ET.SubElement(ent, "attributes")
    pk = ET.SubElement(attrs_el, "attribute", PhysicalName=pk_name)
    for tag, val in [("Type", "primarykey"), ("Name", pk_name),
        ("LogicalName", pk_name.lower()), ("RequiredLevel", "systemrequired"),
        ("DisplayMask", "ValidForAdvancedFind|RequiredForGrid"), ("ImeMode", "auto"),
        ("ValidForUpdateApi", "0"), ("ValidForReadApi", "1"), ("ValidForCreateApi", "1"),
        ("IsCustomField", "0"), ("IsAuditEnabled", "0"), ("IsSecured", "0"),
        ("IntroducedVersion", "1.1.0.0"), ("IsCustomizable", "1"), ("IsRenameable", "1"),
        ("CanModifySearchSettings", "1"), ("CanModifyRequirementLevelSettings", "0"),
        ("CanModifyAdditionalSettings", "1"),
        ("SourceType", "0"),
        ("IsGlobalFilterEnabled", "1"), ("IsSortableEnabled", "1"),
        ("CanModifyGlobalFilterSettings", "1"), ("CanModifyIsSortableSettings", "1"),
        ("IsDataSourceSecret", "0"),
        ("IsSearchable", "0"), ("IsFilterable", "1"), ("IsRetrievable", "1"),
        ("IsLocalizable", "0")]:
        ET.SubElement(pk, tag).text = val
    ET.SubElement(pk, "AutoNumberFormat")
    pkdn = ET.SubElement(pk, "displaynames")
    ET.SubElement(pkdn, "displayname", description=display, languagecode="1033")
    pkdd = ET.SubElement(pk, "Descriptions")
    ET.SubElement(pkdd, "Description", description="Unique identifier for entity instances", languagecode="1033")
    pf = ET.SubElement(attrs_el, "attribute", PhysicalName=entity_def["primary_field"])
    for tag, val in [("Type", "nvarchar"), ("Name", entity_def["primary_field"]),
        ("LogicalName", entity_def["primary_field"].lower()), ("RequiredLevel", "required"),
        ("DisplayMask", "PrimaryName|ValidForAdvancedFind|ValidForForm|ValidForGrid|RequiredForForm"),
        ("ImeMode", "auto"),
        ("ValidForUpdateApi", "1"), ("ValidForReadApi", "1"), ("ValidForCreateApi", "1"),
        ("IsCustomField", "1"), ("IsAuditEnabled", "1"), ("IsSecured", "0"),
        ("IntroducedVersion", "1.1.0.0"), ("IsCustomizable", "1"), ("IsRenameable", "1"),
        ("CanModifySearchSettings", "1"), ("CanModifyRequirementLevelSettings", "1"),
        ("CanModifyAdditionalSettings", "1"),
        ("SourceType", "0"),
        ("IsGlobalFilterEnabled", "0"), ("IsSortableEnabled", "0"),
        ("CanModifyGlobalFilterSettings", "1"), ("CanModifyIsSortableSettings", "1"),
        ("IsDataSourceSecret", "0"),
        ("IsSearchable", "1"), ("IsFilterable", "0"), ("IsRetrievable", "1"),
        ("IsLocalizable", "0"),
        ("Format", "text"), ("MaxLength", "200"), ("Length", "400")]:
        ET.SubElement(pf, tag).text = val
    ET.SubElement(pf, "AutoNumberFormat")
    pfdn = ET.SubElement(pf, "displaynames")
    ET.SubElement(pfdn, "displayname", description=entity_def["primary_display"], languagecode="1033")
    pfdd = ET.SubElement(pf, "Descriptions")
    ET.SubElement(pfdd, "Description", description="Required name field", languagecode="1033")
    for attr_def in entity_def.get("attributes", []):
        attrs_el.append(build_attribute_xml(attr_def, entity_schema=schema))
    ET.SubElement(ent, "EntitySetName").text = schema + "s"
    for tag, val in [("IsDuplicateCheckSupported", "0"), ("IsBusinessProcessEnabled", "0"),
        ("IsRequiredOffline", "0"), ("IsInteractionCentricEnabled", "0"),
        ("IsCollaboration", "0"), ("AutoRouteToOwnerQueue", "0"),
        ("IsConnectionsEnabled", "0"), ("EntityColor", "#0078D4"),
        ("IsDocumentManagementEnabled", "0"), ("AutoCreateAccessTeams", "0"),
        ("IsOneNoteIntegrationEnabled", "0"), ("IsKnowledgeManagementEnabled", "0"),
        ("IsSLAEnabled", "0"), ("IsDocumentRecommendationsEnabled", "0"),
        ("IsBPFEntity", "0"), ("OwnershipTypeMask", "UserOwned"),
        ("IsAuditEnabled", "0"), ("IsRetrieveAuditEnabled", "0"),
        ("IsRetrieveMultipleAuditEnabled", "0"),
        ("IsActivity", "0"), ("ActivityTypeMask", "CommunicationActivity"),
        ("IsActivityParty", "0"),
        ("IsReplicated", "0"), ("IsReplicationUserFiltered", "0"),
        ("IsMailMergeEnabled", "0"),
        ("IsVisibleInMobile", "1"), ("IsVisibleInMobileClient", "1"),
        ("IsReadOnlyInMobileClient", "0"), ("IsOfflineInMobileClient", "0"),
        ("DaysSinceRecordLastModified", "0"),
        ("IsMapiGridEnabled", "1"), ("IsReadingPaneEnabled", "1"),
        ("IsQuickCreateEnabled", "1"),
        ("SyncToExternalSearchIndex", "0"),
        ("IntroducedVersion", "1.1.0.0"),
        ("IsCustomizable", "1"), ("IsRenameable", "1"), ("IsMappable", "1"),
        ("CanModifyAuditSettings", "1"),
        ("CanModifyMobileVisibility", "1"), ("CanModifyMobileClientVisibility", "1"),
        ("CanModifyMobileClientReadOnly", "1"), ("CanModifyMobileClientOffline", "1"),
        ("CanModifyConnectionSettings", "1"),
        ("CanModifyDuplicateDetectionSettings", "1"), ("CanModifyMailMergeSettings", "1"),
        ("CanModifyQueueSettings", "1"),
        ("CanCreateAttributes", "1"), ("CanCreateForms", "1"),
        ("CanCreateCharts", "1"), ("CanCreateViews", "1"),
        ("CanModifyAdditionalSettings", "1"),
        ("CanEnableSyncToExternalSearchIndex", "1"),
        ("EnforceStateTransitions", "0"),
        ("CanChangeHierarchicalRelationship", "1"),
        ("EntityHelpUrlEnabled", "0"),
        ("ChangeTrackingEnabled", "0"), ("CanChangeTrackingBeEnabled", "1"),
        ("IsEnabledForExternalChannels", "0"),
        ("IsMSTeamsIntegrationEnabled", "0"),
        ("IsSolutionAware", "0"),
        ("HasRelatedNotes", "True")]:
        ET.SubElement(ent, tag).text = val
    for tag in ["MobileOfflineFilters", "IconSmallName", "IconMediumName", "EntityHelpUrl"]:
        ET.SubElement(ent, tag)
    forms_el = ET.SubElement(entity_el, "FormXml")
    forms_cont = ET.SubElement(forms_el, "forms", type="main")
    systemform = ET.SubElement(forms_cont, "systemform")
    ET.SubElement(systemform, "formid").text = g(f"form_{schema}_main")
    ET.SubElement(systemform, "IntroducedVersion").text = "1.1.0.0"
    ET.SubElement(systemform, "FormPresentation").text = "1"
    ET.SubElement(systemform, "FormActivationState").text = "1"
    form_el = ET.SubElement(systemform, "form")
    form_el.set("shownavigationbar", "true")
    form_el.set("showImage", "false")
    form_el.set("maxWidth", "1920")
    form_inner = ET.fromstring(build_form_xml(entity_def))
    for child in form_inner:
        form_el.append(child)
    dc = ET.SubElement(form_el, "DisplayConditions", Order="0", FallbackForm="true")
    ET.SubElement(dc, "Everyone")
    ET.SubElement(systemform, "IsCustomizable").text = "1"
    ET.SubElement(systemform, "CanBeDeleted").text = "1"
    ln2 = ET.SubElement(systemform, "LocalizedNames")
    ET.SubElement(ln2, "LocalizedName", description="Information", languagecode="1033")
    desc2 = ET.SubElement(systemform, "Descriptions")
    ET.SubElement(desc2, "Description", description=f"Main information form for {display}.", languagecode="1033")
    qc_forms = ET.SubElement(forms_el, "forms", type="quick")
    qc_sys = ET.SubElement(qc_forms, "systemform")
    ET.SubElement(qc_sys, "formid").text = g(f"form_{schema}_quick")
    ET.SubElement(qc_sys, "IntroducedVersion").text = "1.1.0.0"
    ET.SubElement(qc_sys, "FormPresentation").text = "1"
    ET.SubElement(qc_sys, "FormActivationState").text = "1"
    qc_form_el = ET.SubElement(qc_sys, "form")
    qc_tabs = ET.SubElement(qc_form_el, "tabs")
    qc_tab = ET.SubElement(qc_tabs, "tab", verticallayout="true",
        id=g(f"form_qctab_{schema}"), IsUserDefined="1")
    qc_tab_lbls = ET.SubElement(qc_tab, "labels")
    ET.SubElement(qc_tab_lbls, "label", description="", languagecode="1033")
    qc_cols = ET.SubElement(qc_tab, "columns")
    qc_col = ET.SubElement(qc_cols, "column", width="100%")
    qc_secs = ET.SubElement(qc_col, "sections")
    qc_sec = ET.SubElement(qc_secs, "section", showlabel="false", showbar="false",
        IsUserDefined="0", id=g(f"form_qcsec_{schema}"))
    qc_sec_lbls = ET.SubElement(qc_sec, "labels")
    ET.SubElement(qc_sec_lbls, "label", description="GENERAL", languagecode="1033")
    qc_rows = ET.SubElement(qc_sec, "rows")
    qc_row = ET.SubElement(qc_rows, "row")
    qc_cell = ET.SubElement(qc_row, "cell", id=g(f"form_qccell_{schema}_name"))
    qc_cell_lbls = ET.SubElement(qc_cell, "labels")
    ET.SubElement(qc_cell_lbls, "label", description=entity_def["primary_display"], languagecode="1033")
    ET.SubElement(qc_cell, "control", id=entity_def["primary_field"],
        classid=CONTROL_CLASSIDS["nvarchar"], datafieldname=entity_def["primary_field"])
    ET.SubElement(qc_sys, "IsCustomizable").text = "1"
    ET.SubElement(qc_sys, "CanBeDeleted").text = "1"
    qc_ln = ET.SubElement(qc_sys, "LocalizedNames")
    ET.SubElement(qc_ln, "LocalizedName", description="Quick Create", languagecode="1033")
    views_el = ET.SubElement(entity_el, "SavedQueries")
    fetchxml, layoutxml = build_view_xml(entity_def)
    sq = ET.SubElement(views_el, "savedquery")
    ET.SubElement(sq, "savedqueryid").text = g(f"view_{schema}_active")
    ET.SubElement(sq, "IsDefault").text = "1"
    ET.SubElement(sq, "IsQuickFindQuery").text = "0"
    ET.SubElement(sq, "IsUserDefined").text = "0"
    ET.SubElement(sq, "IsCustomizable").text = "1"
    vln = ET.SubElement(sq, "LocalizedNames")
    ET.SubElement(vln, "LocalizedName", description=f"Active {display_plural}", languagecode="1033")
    vdesc = ET.SubElement(sq, "Descriptions")
    ET.SubElement(vdesc, "Description", description=f"Shows all active {display_plural.lower()}.", languagecode="1033")
    ET.SubElement(sq, "fetchxml").text = fetchxml
    ET.SubElement(sq, "layoutxml").text = layoutxml
    ribbon = ET.SubElement(entity_el, "RibbonDiffXml")
    ET.SubElement(ribbon, "CustomActions")
    tpls = ET.SubElement(ribbon, "Templates")
    ET.SubElement(tpls, "RibbonTemplates", Id="Mscrm.Templates")
    ET.SubElement(ribbon, "CommandDefinitions")
    rules = ET.SubElement(ribbon, "RuleDefinitions")
    ET.SubElement(rules, "TabDisplayRules")
    ET.SubElement(rules, "DisplayRules")
    ET.SubElement(rules, "EnableRules")
    ET.SubElement(ribbon, "LocLabels")


def build_relationship_xml(relationships_el, rel_name, referencing_entity, referenced_entity, referencing_attr, desc=""):
    rel = ET.SubElement(relationships_el, "EntityRelationship", Name=rel_name)
    ET.SubElement(rel, "EntityRelationshipType").text = "OneToMany"
    ET.SubElement(rel, "IntroducedVersion").text = "1.1.0.0"
    ET.SubElement(rel, "IsHierarchical").text = "0"
    ET.SubElement(rel, "ReferencingEntityName").text = referencing_entity
    ET.SubElement(rel, "ReferencedEntityName").text = referenced_entity
    ET.SubElement(rel, "CascadeAssign").text = "NoCascade"
    ET.SubElement(rel, "CascadeDelete").text = "RemoveLink"
    ET.SubElement(rel, "CascadeArchive").text = "NoCascade"
    ET.SubElement(rel, "CascadeReparent").text = "NoCascade"
    ET.SubElement(rel, "CascadeShare").text = "NoCascade"
    ET.SubElement(rel, "CascadeUnshare").text = "NoCascade"
    ET.SubElement(rel, "CascadeRollupView").text = "NoCascade"
    ET.SubElement(rel, "IsValidForAdvancedFind").text = "1"
    ET.SubElement(rel, "ReferencingAttributeName").text = referencing_attr
    rd = ET.SubElement(rel, "RelationshipDescription")
    dds = ET.SubElement(rd, "Descriptions")
    ET.SubElement(dds, "Description", description=desc, languagecode="1033")
    roles = ET.SubElement(rel, "EntityRelationshipRoles")
    role1 = ET.SubElement(roles, "EntityRelationshipRole")
    ET.SubElement(role1, "NavPaneDisplayOption").text = "UseCollectionName"
    ET.SubElement(role1, "NavPaneArea").text = "Details"
    ET.SubElement(role1, "NavPaneOrder").text = "10000"
    ET.SubElement(role1, "NavigationPropertyName").text = referencing_attr
    cl1 = ET.SubElement(role1, "CustomLabels")
    ET.SubElement(cl1, "CustomLabel", description="", languagecode="1033")
    ET.SubElement(role1, "RelationshipRoleType").text = "1"
    role2 = ET.SubElement(roles, "EntityRelationshipRole")
    ET.SubElement(role2, "RelationshipRoleType").text = "0"


def build_optionset_xml(optionsets_el, optset_def):
    os_el = ET.SubElement(optionsets_el, "optionset", Name=optset_def["name"],
        localizedName=optset_def["display"], description="")
    ET.SubElement(os_el, "OptionSetType").text = "picklist"
    ET.SubElement(os_el, "IsGlobal").text = "1"
    ET.SubElement(os_el, "IntroducedVersion").text = "1.1.0.0"
    ET.SubElement(os_el, "IsCustomizable").text = "1"
    dn = ET.SubElement(os_el, "displaynames")
    ET.SubElement(dn, "displayname", description=optset_def["display"], languagecode="1033")
    descs = ET.SubElement(os_el, "Descriptions")
    ET.SubElement(descs, "Description", description="", languagecode="1033")
    options = ET.SubElement(os_el, "options")
    for val, label in optset_def["options"]:
        opt = ET.SubElement(options, "option", value=str(val))
        lbls = ET.SubElement(opt, "labels")
        ET.SubElement(lbls, "label", description=label, languagecode="1033")


def build_security_role_xml(roles_el, role_name, role_desc, privileges):
    role = ET.SubElement(roles_el, "Role", name=role_name, id=g(f"role_{role_name}"))
    ET.SubElement(role, "IntroducedVersion").text = "1.1.0.0"
    rln = ET.SubElement(role, "LocalizedNames")
    ET.SubElement(rln, "LocalizedName", description=role_name, languagecode="1033")
    rd = ET.SubElement(role, "Descriptions")
    ET.SubElement(rd, "Description", description=role_desc, languagecode="1033")
    privs = ET.SubElement(role, "RolePrivileges")
    for priv_name, depth in privileges:
        ET.SubElement(privs, "RolePrivilege", name=priv_name, level=depth)


def generate_customizations_xml():
    tree = ET.parse("/tmp/esg-solution/existing_solution/customizations.xml")
    root = tree.getroot()
    entities_el = root.find("Entities")
    relationships_el = root.find("EntityRelationships")
    roles_el = root.find("Roles")
    optionsets_el = root.find("optionsets")
    for os_def in ALL_OPTIONSETS:
        build_optionset_xml(optionsets_el, os_def)
    for entity_def in ALL_ENTITIES:
        build_entity_xml(entity_def, entities_el)
    new_rels = [
        (f"{P}_esgapplication_contact", f"{P}_esgapplication", "Contact", f"{P}_applicantid",
         "Contact (Applicant) associated with ESG Application."),
        (f"{P}_eligibilitycheck_esgapplication", f"{P}_eligibilitycheck", f"{P}_esgapplication", f"{P}_applicationid",
         "ESG Application associated with Eligibility Check."),
        (f"{P}_assessmentresponse_esgapplication", f"{P}_assessmentresponse", f"{P}_esgapplication", f"{P}_applicationid",
         "ESG Application associated with Self-Assessment Response."),
        (f"{P}_esgdocument_esgapplication", f"{P}_esgdocument", f"{P}_esgapplication", f"{P}_applicationid",
         "ESG Application associated with ESG Document."),
        (f"{P}_esgdocument_assessmentresponse", f"{P}_esgdocument", f"{P}_assessmentresponse", f"{P}_assessmentresponseid",
         "Assessment Response associated with ESG Document."),
        (f"{P}_esgreview_esgapplication", f"{P}_esgreview", f"{P}_esgapplication", f"{P}_applicationid",
         "ESG Application associated with ESG Review."),
        (f"{P}_maturityreport_esgapplication", f"{P}_maturityreport", f"{P}_esgapplication", f"{P}_applicationid",
         "ESG Application associated with Maturity Report."),
        (f"{P}_esgcertificate_esgapplication", f"{P}_esgcertificate", f"{P}_esgapplication", f"{P}_applicationid",
         "ESG Application associated with ESG Certificate."),
        (f"{P}_esgcertificate_maturityreport", f"{P}_esgcertificate", f"{P}_maturityreport", f"{P}_reportid",
         "Maturity Report associated with ESG Certificate."),
        (f"{P}_esgnotification_esgapplication", f"{P}_esgnotification", f"{P}_esgapplication", f"{P}_applicationid",
         "ESG Application associated with ESG Notification."),
    ]
    for rel_name, referencing, referenced, ref_attr, desc in new_rels:
        build_relationship_xml(relationships_el, rel_name, referencing, referenced, ref_attr, desc)
    applicant_privs = []
    for ent in ALL_ENTITIES:
        schema = ent["schema"]
        if schema in (f"{P}_esgapplication", f"{P}_assessmentresponse", f"{P}_esgdocument"):
            applicant_privs.extend([
                (f"prvCreate{schema}", "Basic"), (f"prvRead{schema}", "Basic"),
                (f"prvWrite{schema}", "Basic"), (f"prvAppend{schema}", "Basic"), (f"prvAppendTo{schema}", "Basic")])
        else:
            applicant_privs.append((f"prvRead{schema}", "Basic"))
    build_security_role_xml(roles_el, "ESG Applicant",
        "Role for external applicants applying for the ESG Sustainability Label. Can create and manage own applications, submit EOI and self-assessment, upload documents, and view certificates and reports.",
        applicant_privs)
    psh_privs = []
    for ent in ALL_ENTITIES:
        schema = ent["schema"]
        psh_privs.extend([
            (f"prvCreate{schema}", "Global"), (f"prvRead{schema}", "Global"),
            (f"prvWrite{schema}", "Global"), (f"prvDelete{schema}", "Global"),
            (f"prvAppend{schema}", "Global"), (f"prvAppendTo{schema}", "Global"),
            (f"prvAssign{schema}", "Global"), (f"prvShare{schema}", "Global")])
    build_security_role_xml(roles_el, "ESG Products Section Head",
        "Role for the ADCCI Products Section Head. Can review flagged EOIs, validate documents, request additional information, endorse maturity reports, and manage all ESG applications.",
        psh_privs)
    director_privs = []
    for ent in ALL_ENTITIES:
        schema = ent["schema"]
        director_privs.extend([
            (f"prvRead{schema}", "Global"), (f"prvWrite{schema}", "Global"),
            (f"prvAppend{schema}", "Global"), (f"prvAppendTo{schema}", "Global")])
    director_privs.extend([
        (f"prvCreate{P}_esgreview", "Global"), (f"prvCreate{P}_esgcertificate", "Global")])
    build_security_role_xml(roles_el, "ESG Business Connect Director",
        "Role for the ADCCI Business Connect & Services Director. Can view all applications, provide final approval for maturity reports, and authorize certificate issuance.",
        director_privs)
    return root


def generate_solution_xml():
    tree = ET.parse("/tmp/esg-solution/existing_solution/solution.xml")
    root = tree.getroot()
    manifest = root.find("SolutionManifest")
    manifest.find("Version").text = "1.1.0.0"
    root_comps = manifest.find("RootComponents")
    for entity_def in ALL_ENTITIES:
        ET.SubElement(root_comps, "RootComponent", type="1", schemaName=entity_def["schema"], behavior="0")
    for os_def in ALL_OPTIONSETS:
        ET.SubElement(root_comps, "RootComponent", type="9", schemaName=os_def["name"], behavior="0")
    for role_name in ["ESG Applicant", "ESG Products Section Head", "ESG Business Connect Director"]:
        role_id = g(f"role_{role_name}")
        ET.SubElement(root_comps, "RootComponent", type="20", id=role_id, behavior="0")
    return root


def prettify(root):
    rough = ET.tostring(root, encoding="unicode", xml_declaration=False)
    dom = minidom.parseString(rough)
    pretty = dom.toprettyxml(indent="  ", encoding=None)
    lines = pretty.split("\n")
    if lines and lines[0].startswith("<?xml"):
        lines = lines[1:]
    return "\n".join(lines)


def main():
    output_dir = "/tmp/esg-solution/new_solution"
    os.makedirs(output_dir, exist_ok=True)
    print("Generating customizations.xml...")
    cust_root = generate_customizations_xml()
    with open(os.path.join(output_dir, "customizations.xml"), "w", encoding="utf-8") as f:
        f.write(prettify(cust_root))
    print("Generating solution.xml...")
    sol_root = generate_solution_xml()
    with open(os.path.join(output_dir, "solution.xml"), "w", encoding="utf-8") as f:
        f.write(prettify(sol_root))
    shutil.copy("/tmp/esg-solution/existing_solution/[Content_Types].xml",
        os.path.join(output_dir, "[Content_Types].xml"))
    zip_name = "ADCCIDEVINAIV1_1_1_0_0.zip"
    zip_path = os.path.join("/tmp/esg-solution", zip_name)
    print(f"Packaging {zip_name}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fname in ["customizations.xml", "solution.xml", "[Content_Types].xml"]:
            zf.write(os.path.join(output_dir, fname), fname)
    print(f"Solution package created: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for info in zf.infolist():
            print(f"  {info.filename}: {info.file_size:,} bytes")
    print(f"\nSolution Statistics:")
    print(f"  Custom Entities: {len(ALL_ENTITIES)}")
    total_attrs = sum(len(e.get('attributes', [])) for e in ALL_ENTITIES)
    print(f"  Custom Attributes: {total_attrs}")
    print(f"  Global Option Sets: {len(ALL_OPTIONSETS)}")
    print(f"  Security Roles: 3")
    print(f"  Entity Relationships: 10")


if __name__ == "__main__":
    main()
