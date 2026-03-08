# Troubleshooting

## AADSTS Errors

### Symptom

MSAL returns an `AADSTS...` error during sign-in.

### Likely causes

- the app registration is missing delegated Power BI permissions
- admin consent is required but not granted
- browser auth is used without a matching redirect URI
- public client flow is not enabled for the chosen delegated path

### What to check

1. Confirm `TENANT_ID` and `CLIENT_ID` are correct.
2. Confirm the Entra app registration has the delegated Power BI permissions used by this repo.
3. If using browser auth, confirm `REDIRECT_URI` matches the app registration.
4. If using device code flow, switch `USE_DEVICE_CODE=true`.

If you are using the legacy all-in-one notebook, the same values may also appear under `PBI_*` aliases. The repo now treats the canonical `.env` names as the source of truth.

## Missing Admin Consent

### Symptom

Sign-in works poorly or API calls fail with consent-related errors.

### What to check

1. Open the app registration.
2. Review the Power BI Service API permissions.
3. Grant admin consent if your tenant requires it.

## Power BI API Returns 401

### Symptom

The API returns `401 Unauthorized`.

### What to check

1. Confirm the token was acquired for the Power BI resource.
2. Confirm the token is not expired.
3. Confirm the correct auth path is being used for the endpoint.
4. Delete the local token cache in `.local/` and sign in again if needed.

## Power BI API Returns 403

### Symptom

The API returns `403 Forbidden`.

### Likely causes

- the caller does not have workspace access
- the caller does not have dataset permissions
- service principal usage is blocked by tenant admin settings
- the service principal is not in the allowed Entra security group

### What to check

1. Confirm workspace membership.
2. Confirm dataset `Read` and `Build` for `executeQueries`.
3. Confirm tenant settings allow service principals to use the APIs.

## Workspace Not Found

### Symptom

The API returns `404` for the workspace.

### What to check

1. Confirm `WORKSPACE_ID`.
2. Confirm the workspace belongs to the same tenant.
3. Confirm the caller can actually see that workspace.

## Dataset Not Found

### Symptom

The API returns `404` for the dataset.

### What to check

1. Confirm `DATASET_ID`.
2. Confirm the dataset is in the workspace you are querying.
3. Confirm you are targeting a semantic model, not the wrong item type.

## Service Principal Cannot See the Workspace

### Symptom

Delegated auth can list the workspace, but service principal auth cannot.

### Likely causes

- tenant admin settings do not allow service principals
- the service principal is not in the allowed security group
- the service principal is not a workspace member

### What to check

1. Review Power BI / Fabric tenant settings.
2. Review Entra group membership.
3. Add the service principal to the workspace as `Member` or `Admin`.

## Execute Queries Fails Because Build Permission Is Missing

### Symptom

Listing works, but `executeQueries` fails.

### What to check

1. Confirm the caller has `Read` and `Build` on the dataset.
2. Confirm the tenant setting for Dataset Execute Queries REST API is enabled if required by your tenant.

## Execute Queries Fails Because the Dataset Has RLS or SSO

### Symptom

Service principal auth fails when running `executeQueries`.

### Explanation

This is a known limitation area. For a demo, switch back to delegated auth for that dataset or use a simpler demo dataset without those identity features.

## Trial Workspace Exists but the User License Is Still Insufficient

### Symptom

The Fabric Trial workspace exists, but the user still cannot create, access, or share content the way you expected.

### Explanation

A trial capacity and a Power BI user license are not the same thing. A workspace can exist while the presenter or audience account still lacks the correct Power BI user entitlement for a specific action.

### What to do

1. Test the presenter account before the session.
2. Use delegated auth with the exact account that will run the notebook.
3. Keep the demo inside one known-good workspace and one known-good dataset.
