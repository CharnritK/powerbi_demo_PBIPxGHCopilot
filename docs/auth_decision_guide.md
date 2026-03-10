# Authentication Decision Guide

Choose the auth mode based on what you are trying to trust in production and what is safe to demonstrate live.

## Default Recommendation

Use delegated auth first.

It is the better fit when:

- you want a predictable notebook demo
- you want the results to reflect a real signed-in user's access
- you are validating user-context access rather than unattended automation
- you want the lowest-friction way to show REST metadata calls and a small DAX query

Use service principal auth when:

- you are explaining unattended automation
- you want to contrast user-context access with app-only access
- your tenant admin settings are already in place
- the target dataset does not hit unsupported identity constraints such as RLS or SSO for `executeQueries`

## What Works Well in a Demo or Validation Context

Delegated auth usually works well because:

- device code flow avoids redirect URI friction
- no client secret is required
- workspace access is easier to reason about
- demo troubleshooting is usually simpler

Service principal auth usually works well only when:

- tenant admin settings explicitly allow it
- the service principal is in the right allowed group, if required
- the service principal has workspace membership
- the target dataset is appropriate for app-only access

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
| Best for live demo | Yes | Usually no |
| Best for automation | Limited | Yes |
| Admin dependency | Moderate | High |
| Workspace access model | Signed-in user | App-only identity |
| Secret required | No | Yes |
| Device code support | Yes | No |
| Browser auth support | Yes | Not applicable |
| Best fit in this repo narrative | Trusted live default | Automation comparison |
| Execute queries caveats | Needs dataset Read + Build | Also affected by admin settings and unsupported dataset identity scenarios |
| RLS / SSO caveats | User-context behavior applies | `executeQueries` is not supported for some RLS / SSO scenarios |

## Practical Advice for This Repo

Use this order:

1. Run the delegated notebook with device code flow.
2. Show the same metadata calls under the signed-in user identity.
3. Use that as the trusted baseline for the live demo.
4. Only then show the service principal notebook as an optional appendix.

If something fails under service principal auth, do not hide it. Explain that app-only Power BI access depends on tenant controls and dataset capabilities that live outside the notebook code.
