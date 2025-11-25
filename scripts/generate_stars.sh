#!/usr/bin/env bash
set -euo pipefail

# Generate STARS.md from GitHub starred repositories
# Requires: gh (GitHub CLI), jq, python3

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEMP_DIR=$(mktemp -d)

trap "rm -rf ${TEMP_DIR}" EXIT

echo "Fetching starred repositories from GitHub..."
gh api user/starred --paginate --jq '.[] | {name: .full_name, description: .description, language: .language, stars: .stargazers_count, url: .html_url, topics: .topics}' | jq -s '.' > "${TEMP_DIR}/starred_repos.json"

REPO_COUNT=$(jq 'length' "${TEMP_DIR}/starred_repos.json")
echo "Found ${REPO_COUNT} starred repositories"

echo "Categorizing and generating STARS.md..."
python3 "${SCRIPT_DIR}/generate_stars.py" "${TEMP_DIR}/starred_repos.json" "${REPO_ROOT}/STARS.md"

echo "✓ STARS.md generated successfully at ${REPO_ROOT}/STARS.md"
