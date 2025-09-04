# Jira-Zephyr Coverage Checker

This tool checks whether a Jira requirement is 100% covered by Zephyr test steps using Jira REST API, Zephyr API, and OpenAI LLM.

## Features
- Fetch Jira issue description
- Fetch linked Zephyr test cases and steps
- Use OpenAI LLM to compare requirement vs. test steps
- Report coverage gaps or confirm 100% coverage

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env` file:
   ```env
   JIRA_BASE_URL=https://your-jira-instance.atlassian.net
   JIRA_EMAIL=your_email
   JIRA_API_TOKEN=your_api_token
   ZEPHYR_BASE_URL=https://your-zephyr-instance.com
   ZEPHYR_TOKEN=your_zephyr_token
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Run the script:
   ```bash
   python main.py PROJ-123
   ```

## Output
- Prints whether requirement is fully covered or shows gaps in test coverage.
