# Auth Prerequisites

Supported auth modes:

- delegated user auth
- service principal auth

Use delegated auth when:

- you want the safest notebook flow
- you need results in real user context
- you plan to use `executeQueries` with minimal tenant-policy friction

Use service principal auth when:

- you are testing automation-style access
- tenant admin settings and workspace membership are already in place
- dataset features are compatible with app-only access

Common service principal blockers:

- tenant settings do not allow Power BI API access for the app
- security-group allow lists exclude the app
- the service principal lacks workspace membership
- dataset features such as RLS or SSO make app-only query paths invalid
