# {{DATE}} — GitHub Actions environments and deployment protection

**Area:** CI/CD · **Tags:** `github-actions` `deployments` `environments`

## What an environment gives you

An environment (`dev`, `staging`, `production`) is a named deployment target with its own protection rules, secrets, and variables. A job opts in with the `environment` key — and only then can it read that environment's secrets:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com   # shown on the deployment in the UI
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}  # production-scoped secret
```

Environment secrets override repository secrets of the same name, so `DEPLOY_TOKEN` can hold a different value per environment with no workflow changes.

## Protection rules

Configured per environment under Settings → Environments:

- **Required reviewers** — up to 6 people/teams; the job pauses until one approves, giving you a manual gate for production.
- **Wait timer** — delay the job up to 30 days after triggering (bake time for staging soak).
- **Deployment branches and tags** — restrict which refs may deploy, e.g. only `main` or tags matching `v*` can target `production`.

```yaml
# Typical promotion pipeline: staging deploys freely,
# production waits for a human approval on the same run
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps: [ ... ]

  deploy-prod:
    needs: deploy-staging
    environment: production   # required-reviewer rule pauses here
    runs-on: ubuntu-latest
    steps: [ ... ]
```

## Why this beats hand-rolled gates

The pause happens *before* the job starts, so no runner minutes burn while waiting; secrets stay locked until protection rules pass; and every approval is recorded on the deployment timeline for audit. Combined with branch restrictions, a leaked workflow file on a feature branch cannot deploy to production because the environment itself refuses the ref.

## Takeaway

Environments move deployment policy out of workflow YAML and into repo settings — approvals, branch restrictions, and scoped secrets are enforced by GitHub before the job runs, not by conventions inside the pipeline.

**Source:** [Using environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
