> Built for the generation that ships with Cursor and deploys without reading the code.

### Category 1 — What AI Writes Wrong
*Patterns commonly introduced by Cursor, Claude, Copilot when scaffolding SaaS apps*

| # | Vulnerability | Detection Method |
|---|--------------|-----------------|
| 1 | Hardcoded API keys, secrets, DB URLs | Regex |
| 2 | Debug mode left enabled | Regex + AST |
| 3 | Verbose error handlers exposing stack traces | AST |
| 4 | Wildcard CORS with credentials enabled | AST |
| 5 | Missing auth decorators on routes | AST |
| 6 | Plaintext or weakly hashed passwords | AST |
| 7 | Unsafe file upload handling | AST |
| 8 | SQL built via string concatenation | Taint |
| 9 | eval() / exec() on external input | Taint |
| 10 | No rate limiting on login/signup endpoints | AST |
| 11 | No HTTPS enforcement / missing HSTS | Regex + AST |
| 12 | Secrets committed in config files | Regex |
| 13 | Directory listing enabled in config | Regex |

### Category 2 — LLM Runtime Risks
*Vulnerabilities that only exist because AI is in the runtime loop*

| # | Vulnerability | Detection Method |
|---|--------------|-----------------|
| 14 | User input concatenated into system prompt | Taint |
| 15 | LLM output reaching subprocess / eval / os.system | Taint |
| 16 | LLM output used as auth/boolean decision | Taint + AST |
| 17 | json.loads / eval on raw LLM response | AST |
| 18 | System prompt exposed in API response or logs | Taint |
| 19 | No output schema validation on LLM response | AST |

### Category 3 — Agent Architecture Risks
*Structural risks in autonomous agent systems*

| # | Vulnerability | Detection Method |
|---|--------------|-----------------|
| 20 | Unbounded agent loop (while True + LLM call) | AST |
| 21 | LLM directly connected to DB/shell/payment API | AST |
| 22 | LLM output trusted as role/permission authority | Taint + AST |
| 23 | Tool response fed back into model unsanitized | Taint |
| 24 | Conversation memory reused without sanitization | AST |

**Total: 24 AI-centric vulnerability classes**
