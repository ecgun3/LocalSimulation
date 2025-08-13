# ERecon: Email Reconnaissance CLI

ERecon is a comprehensive email reconnaissance tool that integrates MX lookup, BuiltWith API, Holehe, and Genesys Cloud user search. It collects domain information, infers email patterns, and aggregates service data for actionable insights in OSINT, security research, and lead intelligence.

## Features
- MX records lookup with provider heuristics
- BuiltWith domain technology profile via API
- Holehe integration (subprocess) to check email usage across sites
- Genesys Cloud user search (client credentials OAuth2)
- Aggregated JSON or human-readable output

## Quick start
1. Create and populate a `.env` file based on `.env.example`.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the CLI:
```bash
python -m erecon.cli --domain example.com
python -m erecon.cli --email alice@example.com
```

## Configuration
Configuration is read from environment variables (or `.env`):

- BUILTWITH_API_KEY: BuiltWith API key
- BUILTWITH_API_URL: BuiltWith API base URL (default `https://api.builtwith.com/v21/api.json`)
- GENESYS_LOGIN_URL: Genesys OAuth login URL (e.g., `https://login.mypurecloud.com`)
- GENESYS_API_URL: Genesys API URL (e.g., `https://api.mypurecloud.com`)
- GENESYS_CLIENT_ID: Genesys OAuth client id (Client Credentials)
- GENESYS_CLIENT_SECRET: Genesys OAuth client secret
- HOLEHE_CMD: Command to invoke Holehe (default `holehe`, try `python -m holehe` if not installed globally)
- REQUESTS_TIMEOUT: HTTP timeout in seconds (default `20`)

## Examples
- Domain recon only:
```bash
python -m erecon.cli --domain example.com
```

- Email recon (runs domain recon + Holehe + Genesys search if configured):
```bash
python -m erecon.cli --email alice@example.com
```

- JSON output:
```bash
python -m erecon.cli --email alice@example.com --json
```

## Notes
- BuiltWith and Genesys features require valid API credentials.
- Holehe must be installed in your environment for that feature to work; otherwise it will be skipped gracefully.
- Genesys Cloud environments vary by region; set the correct `GENESYS_LOGIN_URL` and `GENESYS_API_URL` for your org.