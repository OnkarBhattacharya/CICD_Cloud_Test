## Pipeline and AKS setup (snippet)

This project uses Azure DevOps pipelines to build, push, and deploy a Docker image to AKS.

Required Azure DevOps service connections and AKS setup:

- **Azure Container Registry (ACR)**
  - Create an ACR (e.g. `myacr`) in the same subscription/tenant as your AKS cluster.
  - In Azure DevOps, create a **service connection** for the ACR (choose `Azure Resource Manager` when appropriate) and note its name. Set `containerRegistryServiceConnection` in the pipeline variables to that name.
  - Set the pipeline variable `containerRegistry` to the ACR login server (e.g. `myacr.azurecr.io`).

- **AKS / Azure subscription service connection**
  - In Azure DevOps, create a service connection that allows pipelines to access your AKS cluster. You can create a service connection of type **Azure Resource Manager** and authorize it.
  - Note the service connection name and set `kubernetesServiceConnection` in the pipeline variables.
  - Also set `azureResourceGroup` and `kubernetesCluster` pipeline variables to the resource group and AKS cluster name.

Image pull secret / private registry access (AKS)

- The pipeline will create/update a docker registry secret in the target namespace when you run the `kubectl apply` step using `secretType: dockerRegistry` (this uses the ACR/service connection info). If you prefer to create the secret manually, run:

```bash
kubectl create secret docker-registry regcred \
  --docker-server=myacr.azurecr.io \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email> \
  -n default
```

Replace the values above with your ACR login details. For production, consider using Managed Identities or `az aks update` to attach ACR to AKS for automatic image pulls instead of storing credentials.

How the pipeline updates the deployment

- The pipeline builds and pushes an image tagged with `$(buildId)` (variable). After applying the manifest it runs an idempotent check and then `kubectl set image` against the deployment referenced by `$(k8sDeployment)` to update the container image to `$(containerRegistry)/$(imageName):$(buildId)`.

Tips

- Ensure the `metadata.name` in `infra/kubernetes/deployment.yaml` matches the pipeline variable `k8sDeployment` (default `azure-devops-cicd-demo`). The pipeline targets this name when updating the image and waiting for rollout.
- If you use a different namespace, update `kubernetesNamespace` in the pipeline variables or pass the correct namespace when creating the secret.
- For advanced deployments use Helm or add health checks and rollout strategies to the manifest.
