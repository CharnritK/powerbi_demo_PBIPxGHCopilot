# Authentication Decision Guide

## Default Recommendation

Use delegated auth first.

It is the better fit when:

- the audience is non-developer or mixed
- you want a predictable notebook demo
- the presenter already has workspace and dataset access
- you want the API results to match a normal signed-in user

Use service principal auth when:

- you are explaining unattended automation
- you want to contrast user-context access with app-only access
- your tenant admin settings are already in place
- you can tolerate more setup and more failure modes

## What Works Well in a Trial or Demo Environment

Delegated auth usually works well because:

- device code flow avoids redirect URI friction
- no client secret is required
- workspace access is easier to reason about
- demo troubleshooting is usually simpler

Service principal auth usually works only when:

- tenant admin settings explicitly allow it
- the service principal is in the right allowed group, if required
- the service principal has workspace membership
- the target dataset does not hit unsupported identity constraints

## What Usually Fails

- missing API permissions or missing admin consent
- service principal blocked by tenant admin settings
- service principal not added to the workspace
- `executeQueries` failing because the caller lacks dataset `Build`
- `executeQueries` failing for service principal because the dataset uses RLS or SSO
- assuming a Fabric Trial workspace automatically solves licensing for every user scenario

## Comparison Table

| Topic | Delegated Auth | Service Principal Auth |
|---|---|---|
| Setup effort | Lower | Higher |
| Best for demo | Yes | Usually no |
| Best for automation | Limited | Yes |
| Admin dependency | Moderate | High |
| Workspace access model | Signed-in user | App-only identity |
| Secret required | No | Yes |
| Device code support | Yes | No |
| Browser auth support | Yes | Not applicable |
| Execute queries caveats | Needs dataset Read + Build | Also affected by admin settings and unsupported dataset identity scenarios |
| RLS / SSO caveats | User-context behavior applies | `executeQueries` is not supported for some RLS / SSO scenarios |

## Practical Advice for This Repo

Use this order:

1. Run the delegated notebook with device code flow.
2. Show the same REST calls under the signed-in user identity.
3. Only then show the service principal notebook as an optional appendix.

If something fails under service principal auth, do not hide it. Explain that app-only Power BI access depends on tenant controls that live in the admin portal, not in Python code.
