# Automated Vulnerability Scanner for Model Serving Endpoints

Automated vulnerability scanning for AI endpoints using [garak](https://github.com/leondz/garak), focused on OWASP Top 10 for LLMs.

## Features

- 🔍 Automated scanning of AI endpoints for security vulnerabilities
- 🛡️ Mapped to OWASP Top 10 for Large Language Models
- 🤖 GitHub Actions automation for scheduled scans
- 📊 Detailed vulnerability reports

## Setup

### Prerequisites
- Python 3.11+
- GitHub CLI (for repository management)

### Installation

1. Clone the repository
2. Create a virtual environment and install dependencies

## Configuration

Edit `config/endpoints.yaml` to add your AI endpoints and configure probes.

## Usage

(To be updated)

## OWASP LLM Top 10 Coverage

This scanner tests for:
- **LLM01**: Prompt Injection
- **LLM02**: Insecure Output Handling
- **LLM03**: Training Data Poisoning
- **LLM06**: Sensitive Information Disclosure
- **LLM07**: Insecure Plugin Design

## License

MIT License
