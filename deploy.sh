#!/usr/bin/env bash
#
# Deploy + SELF-VERIFY the rdschool app. No deploy is "done" until the health
# check passes — so a regression is caught here, not by a user.
#
# Run on the bench server as the frappe user:
#     cd ~/frappe-bench && bash apps/rdschool/deploy.sh [site]
#
# Default site: rdschool.localhost
set -euo pipefail

SITE="${1:-rdschool.localhost}"
export PATH="$HOME/.local/bin:$PATH"

echo "==> [1/6] Pull latest rdschool (upstream/main)"
( cd apps/rdschool && git pull upstream main )

echo "==> [2/6] Migrate $SITE (imports fixtures; after_migrate re-localizes link_filters)"
bench --site "$SITE" migrate

echo "==> [3/6] Build assets"
bench build --app rdschool

echo "==> [4/6] Reconcile roles + permissions (idempotent)"
bench --site "$SITE" execute rdschool.setup_data.assign_full_profile_roles
bench --site "$SITE" execute rdschool.setup_data.rebuild_school_docperms
bench --site "$SITE" execute rdschool.setup_data.ensure_company_user_permissions

echo "==> [5/6] Restart"
bench restart || true

echo "==> [6/6] HEALTH CHECK (gates the deploy)"
OUT="$(bench --site "$SITE" execute rdschool.setup_data.verify_deployment 2>&1 || true)"
echo "$OUT"
if echo "$OUT" | grep -q "HEALTHCHECK PASS"; then
    echo "==> DEPLOY OK ✅  ($SITE)"
else
    echo "==> DEPLOY FAILED HEALTH CHECK ❌ — review the [FAIL] lines above. Site may need a fix before users rely on it." >&2
    exit 1
fi
