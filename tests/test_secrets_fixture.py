# =============================================================================
# SYNTHETIC TEST FIXTURE — NOT REAL CREDENTIALS
# =============================================================================
# Every "secret" below is fake/randomly generated for testing SecretShield's
# pattern engine and entropy analysis. None of these are live keys.
# Safe to commit, safe to scan, safe for a reviewer to open and inspect.
#
# Run against this file with:
#   python main.py scan tests/test_secrets_fixture.py
#
# Expected: the scanner should report a finding for every block below.
# =============================================================================

# --- AWS Access Key (CRITICAL) ---
testaws_access_key = "AKIAABCDEFGHIJKLMNOP"

# --- AWS Secret Key (CRITICAL) ---
testaws_secret_key = "wJalrXUtnFEMIfakeKEYbPxRfiCYEXAMPLEKEY123"

# --- GCP API Key (CRITICAL) ---
testgcp_api_key = "AIzaSyDfakeGCPkeyEXAMPLE1234567890abcd"

# --- Stripe Secret Key (CRITICAL) ---
teststripe_key = "sk_live_FAKE1234567890abcdefghijklmno"

# --- Razorpay Key (HIGH) ---
testrazorpay_key = "rzp_live_FAKEKEY1234567890"

# --- Generic JWT (MEDIUM) ---
testjwt_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmYWtlIn0.fakeSignatureValueHere123"

# --- Database URL with credentials (HIGH) ---
testdatabase_url = "postgres://fakeuser:fakepassword123@db.example.com:5432/mydb"

# --- Generic API Key Assignment (MEDIUM) ---
testapi_key = "sk_test_THISISAFAKEKEYNOTAREALONE123"

# --- High-entropy random string (no pattern match, should trigger entropy check) ---
testrandom_token = "x7F$kPq2!mZ9vL4nR8wT1cY6bN3dQ5jU0"

# --- Should NOT trigger anything (plain English, low entropy) ---
testnormal_comment = "this is just a regular comment with no secrets in it"
