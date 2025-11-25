#!/usr/bin/env python3
"""
Generate STARS.md from GitHub starred repositories.

Usage:
    python3 generate_stars.py <input_json> <output_md>

Input JSON format (from GitHub API):
    [{
        "name": "owner/repo",
        "description": "...",
        "language": "Go",
        "stars": 1234,
        "url": "https://github.com/owner/repo",
        "topics": ["kubernetes", "devops"]
    }]
"""

import json
import sys
from typing import Dict, List, Any


def load_repos(input_file: str) -> List[Dict[str, Any]]:
    """Load starred repositories from JSON file."""
    with open(input_file, 'r') as f:
        return json.load(f)


def categorize_repos(repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize repositories based on topics and language."""

    # Define categories with keywords for matching
    categories = {
        'Kubernetes & Container Orchestration': {
            'keywords': ['kubernetes', 'k8s', 'helm', 'operator', 'kustomize', 'openshift', 'oci'],
            'repos': []
        },
        'Cloud & Infrastructure': {
            'keywords': ['terraform', 'aws', 'azure', 'gcp', 'cloud', 'pulumi', 'hcloud', 'infrastructure'],
            'repos': []
        },
        'GitOps & CI/CD': {
            'keywords': ['gitops', 'argocd', 'flux', 'gitlab', 'github-actions', 'jenkins', 'tekton', 'ci', 'cd', 'continuous-integration', 'continuous-delivery'],
            'repos': []
        },
        'Configuration Management': {
            'keywords': ['puppet', 'ansible', 'chef', 'salt'],
            'repos': []
        },
        'Monitoring & Observability': {
            'keywords': ['prometheus', 'grafana', 'monitoring', 'observability', 'metrics', 'logging', 'tracing', 'alerting'],
            'repos': []
        },
        'Security & Compliance': {
            'keywords': ['security', 'vault', 'cert-manager', 'certificate', 'authentication', 'authorization', 'rbac', 'encryption'],
            'repos': []
        },
        'Development Tools': {
            'keywords': ['cli', 'automation', 'developer-tools', 'devtools', 'productivity'],
            'repos': []
        },
        'Networking': {
            'keywords': ['network', 'dns', 'ingress', 'service-mesh', 'istio', 'envoy', 'vpn', 'load-balancer'],
            'repos': []
        },
        'Go Projects': {
            'keywords': ['go', 'golang'],
            'repos': []
        },
        'Python Projects': {
            'keywords': ['python'],
            'repos': []
        },
        'AI & Machine Learning': {
            'keywords': ['ai', 'machine-learning', 'ml', 'llm', 'artificial-intelligence', 'deep-learning'],
            'repos': []
        },
        'Other': {
            'keywords': [],
            'repos': []
        }
    }

    # Categorize each repository
    for repo in repos:
        topics = repo.get('topics', [])
        language = repo.get('language', '').lower() if repo.get('language') else ''

        # Convert to lowercase for matching
        topics_lower = [t.lower() for t in topics]
        all_keywords = topics_lower + [language]

        categorized = False

        # Try to match to a category (skip 'Other')
        for cat_name, cat_data in list(categories.items())[:-1]:
            for keyword in cat_data['keywords']:
                if keyword in all_keywords:
                    cat_data['repos'].append(repo)
                    categorized = True
                    break
            if categorized:
                break

        # If not categorized, add to Other
        if not categorized:
            categories['Other']['repos'].append(repo)

    return categories


def generate_markdown(repos: List[Dict[str, Any]], categories: Dict[str, List[Dict[str, Any]]]) -> str:
    """Generate markdown content for STARS.md."""

    output = []
    output.append("# Starred Repositories")
    output.append("")
    output.append(f"A curated collection of {len(repos):,} repositories I've starred on GitHub.")
    output.append("")
    output.append("Last updated: " + "<!--DATE-->")
    output.append("")
    output.append("**Categories:**")

    # Generate table of contents
    for cat_name, cat_data in categories.items():
        count = len(cat_data['repos'])
        if count > 0:
            anchor = cat_name.lower().replace(' & ', '-').replace(' ', '-').replace('/', '')
            output.append(f"- [{cat_name}](#{anchor}) ({count:,})")

    output.append("")
    output.append("---")
    output.append("")

    # Generate category sections
    for cat_name, cat_data in categories.items():
        repos_in_cat = cat_data['repos']
        if len(repos_in_cat) == 0:
            continue

        # Sort by stars descending
        repos_in_cat.sort(key=lambda x: x.get('stars', 0), reverse=True)

        output.append(f"## {cat_name}")
        output.append("")

        for repo in repos_in_cat:
            name = repo['name']
            url = repo['url']
            desc = repo.get('description', 'No description available')
            stars = repo.get('stars', 0)
            language = repo.get('language', 'Unknown')

            if desc is None:
                desc = 'No description available'

            output.append(f"### [{name}]({url})")
            output.append(f"⭐ {stars:,} | 📝 {language}")
            output.append("")
            output.append(desc)
            output.append("")

        output.append("---")
        output.append("")

    return '\n'.join(output)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_json> <output_md>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Load and process repositories
    repos = load_repos(input_file)
    print(f"Loaded {len(repos):,} repositories")

    # Categorize
    categories = categorize_repos(repos)
    active_categories = sum(1 for cat in categories.values() if len(cat['repos']) > 0)
    print(f"Categorized into {active_categories} categories")

    # Generate markdown
    markdown = generate_markdown(repos, categories)

    # Replace date placeholder
    from datetime import datetime
    markdown = markdown.replace('<!--DATE-->', datetime.now().strftime('%Y-%m-%d'))

    # Write output
    with open(output_file, 'w') as f:
        f.write(markdown)

    print(f"✓ Generated {output_file}")


if __name__ == '__main__':
    main()
