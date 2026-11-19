#!/usr/bin/env bash
# Assert the Pages layout we migrated to: the user site exists, and the three
# project repositories no longer serve their own Pages sites. This catches a
# re-enabled Pages setting before it starts shadowing the central copies.
set -euo pipefail

owner="noelbennettz"
user_site="$owner.github.io"

if ! gh api "repos/$owner/$user_site/pages" >/dev/null 2>&1; then
  echo "::error::$user_site has no Pages site" >&2
  exit 1
fi

status=0
for project in Hy2droid amneziawg-ui imail; do
  if gh api "repos/$owner/$project/pages" >/dev/null 2>&1; then
    echo "::error::$project has a Pages site again; it would shadow the central copy" >&2
    status=1
  else
    echo "$project: Pages disabled"
  fi
done
exit "$status"
