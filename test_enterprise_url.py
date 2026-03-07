"""
Smoke Test #5: Enterprise GitHub / Custom Base URL
Tests _derive_api_url_from_base_domain and _determine_github_api_base_url
without making real API calls.
"""
import os
import sys

# Ensure we're using the local branch
sys.path.insert(0, r"C:\Users\19194\Documents\python-semantic-release\src")

from semantic_release.hvcs.github import Github

FAKE_REMOTE = "https://github.com/lilfetz22/psr-test-sandbox.git"
FAKE_ENT_REMOTE = "https://github.mycompany.com/lilfetz22/psr-test-sandbox.git"

passed = 0
failed = 0

def check(label, actual, expected):
    global passed, failed
    if actual == expected:
        print(f"  PASS  {label}")
        print(f"        got: {actual!r}")
        passed += 1
    else:
        print(f"  FAIL  {label}")
        print(f"        expected: {expected!r}")
        print(f"        got:      {actual!r}")
        failed += 1

print("\n=== Case 1: Standard github.com (cloud) ===")
g = Github(remote_url=FAKE_REMOTE, token="fake")
check("hvcs_domain",              g.hvcs_domain.url,              "https://github.com")
check("api_url",                  g.api_url.url,                  "https://api.github.com")
check("_determine_github_api_base_url() returns None for cloud",
      g._determine_github_api_base_url(), None)

print("\n=== Case 2: GitHub Enterprise Server via hvcs_domain kwarg ===")
g_ent = Github(remote_url=FAKE_ENT_REMOTE, token="fake",
               hvcs_domain="https://github.mycompany.com")
check("hvcs_domain",  g_ent.hvcs_domain.url,  "https://github.mycompany.com")
check("api_url path contains /api/v3",
      g_ent.api_url.url, "https://github.mycompany.com/api/v3")
check("_determine_github_api_base_url() returns enterprise url",
      g_ent._determine_github_api_base_url(), "https://github.mycompany.com/api/v3")

print("\n=== Case 3: Enterprise via GITHUB_SERVER_URL env var ===")
os.environ["GITHUB_SERVER_URL"] = "https://github.mycompany.com"
os.environ.pop("GITHUB_API_URL", None)
g_env = Github(remote_url=FAKE_ENT_REMOTE, token="fake")
check("hvcs_domain from env",  g_env.hvcs_domain.url,  "https://github.mycompany.com")
check("api_url from derived",  g_env.api_url.url,        "https://github.mycompany.com/api/v3")
del os.environ["GITHUB_SERVER_URL"]

print("\n=== Case 4: Enterprise with explicit GITHUB_API_URL env var ===")
os.environ["GITHUB_SERVER_URL"] = "https://github.mycompany.com"
os.environ["GITHUB_API_URL"]    = "https://github.mycompany.com/api/v3"
g_env2 = Github(remote_url=FAKE_ENT_REMOTE, token="fake")
check("api_url from GITHUB_API_URL env",
      g_env2.api_url.url, "https://github.mycompany.com/api/v3")
del os.environ["GITHUB_SERVER_URL"]
del os.environ["GITHUB_API_URL"]

print("\n=== Case 5: Cloud with wrong hvcs_api_domain kwarg must raise ValueError ===")
try:
    g_bad = Github(remote_url=FAKE_REMOTE, token="fake",
                   hvcs_api_domain="https://api.mycompany.com")
    check("ValueError raised", False, True)
except ValueError as e:
    check("ValueError raised", True, True)
    print(f"        error msg: {e}")

print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
