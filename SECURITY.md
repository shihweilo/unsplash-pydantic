# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |
| < 0.1   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in unsplash-pydantic, please report it privately to help us address it before public disclosure.

### How to Report

1. **Email**: Send details to **shihwei@gmail.com** with the subject line "SECURITY: [Brief Description]"

2. **Include the following information**:
   - Type of vulnerability (e.g., injection, authentication bypass, information disclosure)
   - Full paths of source file(s) related to the vulnerability
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the vulnerability, including how an attacker might exploit it

3. **Expected Response Time**:
   - Initial response: Within 48 hours
   - Status update: Within 7 days
   - Fix timeline: Depends on severity, typically 30-90 days

### What to Expect

- We will acknowledge your email within 48 hours
- We will provide a more detailed response within 7 days, including next steps
- We will keep you informed about the progress toward a fix
- We will notify you when the vulnerability is fixed
- We may ask for additional information or guidance

### Disclosure Policy

- We will coordinate with you on the disclosure timeline
- We prefer to fully remediate vulnerabilities before public disclosure
- Once fixed, we will publish a security advisory on GitHub
- We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices for Users

When using unsplash-pydantic:

1. **Protect Your API Keys**
   ```python
   # ❌ Bad: Never hardcode API keys
   client = UnsplashClient(access_key="abc123...")
   
   # ✅ Good: Use environment variables
   import os
   client = UnsplashClient(access_key=os.getenv("UNSPLASH_ACCESS_KEY"))
   ```

2. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade unsplash-pydantic
   ```

3. **Use HTTPS Only**
   - The library uses HTTPS by default
   - Never configure it to use HTTP endpoints

4. **Validate User Input**
   - If passing user input to API calls, validate and sanitize it first
   - Use Pydantic models for automatic validation

5. **Rate Limiting**
   - Respect Unsplash API rate limits
   - Implement exponential backoff for retries

## Known Security Considerations

### API Key Security
- API keys are transmitted via HTTP headers
- Never log or expose API keys in error messages
- Rotate keys periodically

### Data Validation
- All API responses are validated using Pydantic models
- Unexpected data structures will raise validation errors

### Dependencies
- We regularly update dependencies to address security vulnerabilities
- See `pyproject.toml` for current dependency versions

## Security Updates

Security updates will be released as patch versions (e.g., 0.2.1) and announced via:
- GitHub Security Advisories
- GitHub Release notes
- PyPI release descriptions

## Scope

This security policy applies to the following:

**In Scope:**
- The unsplash-pydantic library code
- Dependencies we directly control
- Our documentation and examples

**Out of Scope:**
- Unsplash API itself (report to Unsplash directly)
- Third-party dependencies (report to respective maintainers)
- Issues related to misuse of the library

## Contact

For security concerns: shihwei@gmail.com

For general issues: https://github.com/shihweilo/unsplash-pydantic/issues

## Attribution

This security policy is adapted from the [Electron Security Policy](https://github.com/electron/electron/blob/main/SECURITY.md).
