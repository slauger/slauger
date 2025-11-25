# Scripts

Automation scripts for maintaining this GitHub profile.

## generate_stars.sh

Generates `STARS.md` from your starred GitHub repositories.

**Requirements:**
- [GitHub CLI](https://cli.github.com/) (`gh`)
- `jq` (JSON processor)
- Python 3

**Usage:**
```bash
cd scripts
./generate_stars.sh
```

**What it does:**
1. Fetches all your starred repositories via GitHub API
2. Categorizes them based on topics and programming language
3. Sorts by star count within each category
4. Generates `STARS.md` in the repository root

**Categories:**
- Kubernetes & Container Orchestration
- Cloud & Infrastructure
- GitOps & CI/CD
- Configuration Management
- Monitoring & Observability
- Security & Compliance
- Development Tools
- Networking
- Go Projects
- Python Projects
- AI & Machine Learning
- Other

**Customization:**

To modify categories or keywords, edit `generate_stars.py` in the `categorize_repos()` function.

Example:
```python
'Your Category': {
    'keywords': ['keyword1', 'keyword2'],
    'repos': []
}
```
