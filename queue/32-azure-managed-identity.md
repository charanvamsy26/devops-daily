# {{DATE}} — Azure managed identities vs service principals

**Area:** Azure / Security · **Tags:** `azure` `entra-id` `identity`

## The core difference

Both are identities in Microsoft Entra ID that apps use to access Azure resources. The difference is who manages the credential:

- **Service principal (app registration)** — you create a client secret or certificate, store it somewhere, inject it into the app, and rotate it before expiry. Every secret is something that can leak.
- **Managed identity** — a special kind of service principal whose credentials are managed and rotated entirely by the platform. Your code never sees a secret; it asks the local Azure instance metadata endpoint for a token.

## System-assigned vs user-assigned

- **System-assigned**: enabled directly on a resource (VM, App Service, AKS, Function App). Lifecycle is tied to the resource — delete the VM, the identity goes with it. 1:1.
- **User-assigned**: a standalone resource you create once and attach to many resources. Survives independently and is the right choice when a fleet shares the same permissions.

```bash
# system-assigned on a VM
az vm identity assign --name web-vm --resource-group rg-app

# user-assigned, shareable
az identity create --name app-workload-id --resource-group rg-app
az vm identity assign --name web-vm --resource-group rg-app \
  --identities /subscriptions/<sub>/resourceGroups/rg-app/providers/Microsoft.ManagedIdentity/userAssignedIdentities/app-workload-id
```

Grant access with normal Azure RBAC role assignments on the identity's principal, e.g. `Key Vault Secrets User` on a vault.

## Using it from code

The SDK credential chain picks managed identity up automatically:

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

client = SecretClient(vault_url="https://kv-app.vault.azure.net",
                      credential=DefaultAzureCredential())
```

Under the hood the token comes from the IMDS endpoint (`169.254.169.254`) — no connection string, no secret in config.

## When you still need a service principal

Managed identities only work for workloads running **on Azure resources that support them**. For external systems (e.g. CI runners outside Azure) use an app registration — ideally with **workload identity federation** (OIDC) rather than a client secret, which gets you the same "no stored secret" property for GitHub Actions and Kubernetes workloads.

## Takeaway

If the workload runs on Azure, use a managed identity and eliminate the credential entirely; reserve service principals for external callers, and even then prefer federated credentials over client secrets.

**Source:** [Managed identities for Azure resources](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
