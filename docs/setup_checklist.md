# Setup Checklist

This checklist covers the manual portal tasks that code cannot solve for you.

Use delegated auth as the default path for a simple Fabric Trial demo. Use service principal auth only if you specifically want to show an automation-oriented identity model.

## A) Manual Azure / Entra Setup

### Delegated auth prerequisites

1. Open your existing Microsoft Entra app registration for this demo.
2. Under `API permissions`, add the Power BI Service delegated permissions needed for the selected demo endpoints:
   - `Workspace.Read.All`
   - `Dataset.Read.All`
   - `Report.Read.All`
3. Grant admin consent if your tenant requires it for these delegated permissions.
4. For browser-based local auth, configure one of these in the app registration if needed:
   - a public client / mobile and desktop flow
   - a localhost redirect URI such as `http://localhost`
5. For device code flow, note that a redirect URI is not required. This is why the delegated notebook uses device code by default.
6. Confirm the signed-in user can access the Fabric Trial workspace.
7. Confirm the signed-in user has `Read` plus `Build` on the target semantic model if you want `executeQueries` to succeed.

### Service principal prerequisites

1. Create a client secret for the existing app registration.
2. Store the secret locally in `.env`. Do not commit it.
3. If Power BI tenant settings only allow specific groups, add the service principal to the allowed Entra security group.
4. Confirm the app registration is intended for app-only usage in your tenant.
5. Remember that some APIs and item types may still have identity-specific limitations even after the app is configured.
6. Do not treat service principal auth as the default path for a simple Fabric Trial demo. It has more tenant and admin dependencies.

## B) Manual Fabric / Power BI Admin Setup

### Delegated auth prerequisites

1. Confirm the signed-in user has access to the Fabric Trial workspace.
2. Confirm the target dataset exists in that workspace.
3. Confirm the user has dataset `Read` and `Build` permissions for `executeQueries`.
4. Confirm the tenant setting for the Dataset Execute Queries REST API is enabled if your tenant controls it centrally.

### Service principal prerequisites

1. In the Power BI / Fabric admin portal, enable the tenant settings required for service principals to call Power BI / Fabric public APIs.
2. If your tenant uses allowed security groups for this setting, confirm the service principal is in that allowed group.
3. Add the service principal to the workspace as `Member` or `Admin` if the demo endpoints require it.
4. Confirm the semantic model and workspace are visible to that app-only identity.
5. Clearly expect some API paths to remain limited by identity behavior, item support, or dataset configuration.

### Licensing and trial notes

Plain-language explanation for a demo audience:

- A Fabric Trial workspace gives you trial capacity for Fabric workloads, but it does not automatically remove every Power BI licensing requirement for every user action.
- A user may still need the appropriate Power BI license to create, access, or share items in workspaces outside `My workspace`.
- In practice, this means a trial workspace can exist and still not be enough for every person or every sharing scenario.
- For a live demo, test with the exact presenter account ahead of time.

## What to Fill In Locally

After the manual setup is complete, copy `.env.example` to `.env` and fill in:

- `TENANT_ID`
- `CLIENT_ID`
- `CLIENT_SECRET` for service principal only
- `WORKSPACE_ID`
- `DATASET_ID`
- `DAX_QUERY`
- `IMPERSONATED_USER_NAME` only if you have a valid use case

Canonical docs and samples use these names. Legacy `PBI_*` aliases are still accepted by the older notebook and `scripts/` helpers, but they are no longer the primary documented path.

## Recommended Run Order

1. Delegated notebook with device code flow
2. Delegated notebook with browser flow, only if you have configured localhost redirect
3. Optional service principal notebook

## Microsoft Guidance Used

This checklist aligns with Microsoft Learn guidance for:

- Power BI REST API group, dataset, report, and executeQueries endpoints
- device code and interactive delegated flows in MSAL
- service principal access to Power BI APIs
- executeQueries identity caveats for RLS and SSO datasets
