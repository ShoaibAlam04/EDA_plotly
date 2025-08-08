from pydantic import BaseModel
from typing import Optional, List

# ------------------------
# 1. Mandate Information
# ------------------------

class MandateDataSchema(BaseModel):
    account_number: str
    sort_code: str
    entity_name: str
    type_of_mandate: str
    action_to_perform: str
    signatory_details: List[str]
    authorised_signatories: List[str]
    signing_rules: str
    signatures: List[str]

class MandateValidationSchema(BaseModel):
    all_fields_present: bool
    missing_fields: Optional[List[str]]
    is_authorised_signatory_present: bool
    is_signature_valid: bool
    next_step: Optional[str] = "Proceed"

# ------------------------
# 2. Back Office Check
# ------------------------

class BackOfficeDataSchema(BaseModel):
    entity_name: str
    customer_segment: Optional[str]
    based_at: Optional[str]
    legal_status: str
    additional_accounts: Optional[List[str]]
    cin: Optional[str]
    relationship_manager: Optional[str]
    legal_status_type: Optional[str]
    has_personal_account: Optional[bool]
    sci_markers: Optional[str]
    kyc_status: Optional[str]
    last_12_months_txns: Optional[str]
    contact_type_email: Optional[str]

class BackOfficeValidationSchema(BaseModel):
    basic_fields_valid: bool
    cin_present: bool
    kyc_valid: bool
    active_txn_found: bool
    proceed: bool

# ------------------------
# 3. Company / Charity / FCA Check
# ------------------------

class CompanyCharityFCADataSchema(BaseModel):
    entity_type: str
    application_type: str
    company_name: str
    company_status: Optional[str]
    people: Optional[List[str]]
    designations: Optional[List[str]]
    charity_exists: Optional[bool]
    charity_name_match: Optional[bool]

class CompanyCharityFCAValidationSchema(BaseModel):
    is_entity_name_matched: bool
    is_status_valid: Optional[bool]
    is_charity_verified: Optional[bool]
    skip_check: Optional[bool] = False

# ------------------------
# 4. ISV Check
# ------------------------

class ISVDataSchema(BaseModel):
    account_number: str
    sort_code: str
    signing_rules: str
    signatory_list: List[str]
    mandate_signatories: List[str]
    mandate_signatures: List[str]

class ISVValidationSchema(BaseModel):
    is_signatory_matched: bool
    is_signature_matched: bool
    is_signing_rule_valid: Optional[bool]

# ------------------------
# 5. KYC Memo Check
# ------------------------

class KYCMemoDataSchema(BaseModel):
    cin: str
    kyc_status: str
    kyc_completion_date: Optional[str]

class KYCMemoValidationSchema(BaseModel):
    is_kyc_completed: bool
    valid_cin_found: bool

# ------------------------
# 6. ID&V Check
# ------------------------

class IDVDataSchema(BaseModel):
    legal_status: str
    has_cin: bool
    has_personal_account: bool
    sci_markers: Optional[str]
    kyc_status: str
    has_active_transaction_in_12_months: bool

class IDVValidationSchema(BaseModel):
    is_entity_eligible: bool
    kyc_ok: bool
    proceed_with_request: bool

# ------------------------
# 7. UKIA Check
# ------------------------

class UKIADataSchema(BaseModel):
    entity_type: str
    isv_signatories_count: int
    pia_status: str  # PASSED / FAILED

class UKIAValidationSchema(BaseModel):
    pia_check_passed: bool
    is_under_threshold: bool
    raise_exception: Optional[bool] = False
