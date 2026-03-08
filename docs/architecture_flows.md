# Architecture and Flow Content

## High-level architecture

**Notebook / Python script**
→ **MSAL authentication**
→ **Microsoft Entra token**
→ **Power BI REST API**
→ **Workspace / Dataset metadata**
→ **DAX query execution**
→ **Tabular results returned to notebook or terminal**

## Service principal request flow

1. Notebook or script loads tenant, client ID, and client secret.
2. MSAL confidential client acquires an app token.
3. Power BI validates tenant settings and workspace membership.
4. Script calls:
   - `GET /groups`
   - `GET /groups/{workspaceId}/datasets`
   - `POST /groups/{workspaceId}/datasets/{datasetId}/executeQueries`
5. Results return to the notebook or terminal.
6. Because this is app-only context, it is best suited to automation and controlled service access.

## Delegated user request flow

1. Notebook or script loads tenant and client ID.
2. User signs in through device code or interactive browser flow.
3. MSAL public client acquires a user-delegated token.
4. Power BI evaluates the signed-in user's permissions.
5. Script calls the same API sequence:
   - `GET /groups`
   - `GET /groups/{workspaceId}/datasets`
   - `POST /groups/{workspaceId}/datasets/{datasetId}/executeQueries`
6. Results reflect the user's accessible context.

## Behind-the-scenes engine flow

**Notebook UI layer**
- Buttons/cells for: choose auth, list workspaces, list datasets, run DAX

**Reusable script layer**
- `config_loader.py`
- `auth_service_principal.py`
- `auth_delegated_user.py`
- `list_workspaces.py`
- `list_datasets.py`
- `execute_dax_query.py`

**Power BI service boundary**
- REST API for metadata and DAX query execution

**Semantic model boundary**
- Power BI semantic model receives DAX query
- Returns one result table to the caller

## Diagram text block for slides

### Diagram 1 — high-level
User / Presenter  
→ Notebook Demo  
→ Python Helper Scripts  
→ Microsoft Entra Authentication  
→ Power BI REST API  
→ Workspace + Semantic Model  
→ DAX Results

### Diagram 2 — service principal
Notebook  
→ MSAL Confidential Client  
→ Entra Token (App Identity)  
→ Power BI REST API  
→ Workspace Access (Service Principal)  
→ Dataset  
→ Execute DAX Query  
→ Results

### Diagram 3 — delegated user
Notebook  
→ MSAL Public Client  
→ User Sign-In  
→ Entra Token (User Identity)  
→ Power BI REST API  
→ Workspace Access (User Context)  
→ Dataset  
→ Execute DAX Query  
→ Results

### Diagram 4 — behind the scenes
Notebook cell click  
→ `list_workspaces.py`  
→ `list_datasets.py`  
→ `execute_dax_query.py`  
→ Power BI REST API  
→ Semantic model  
→ Table result  
→ Display as DataFrame / chart
