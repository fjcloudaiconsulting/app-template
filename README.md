# app-template

Starter for new apps on the FJ Consulting release contract
([RELEASE_CONTRACT.md](https://github.com/fjcloudaiconsulting/.github/blob/main/RELEASE_CONTRACT.md)).
Backend only: a stdlib health endpoint, a `prod` and a `migrations` image, CI on the shared workflows,
release-please, and the post-release smoke test. Click "Use this template"; Actions are disabled in the
template itself.

## Owner checklist for each new repo

1. Install the release GitHub App on the repo.
2. Create the `release` environment (deployment branches: `main` only, no required reviewers, since the
   release job runs on every `main` push) and set its two secrets:
   `gh secret set RELEASE_APP_ID --env release` and `gh secret set RELEASE_APP_PRIVATE_KEY --env release`.
3. Repo settings: squash-merge only (merge commits and rebase off), delete branch on merge.
4. Protect `main` (branch protection or a ruleset): require a pull request, require the checks `Backend Checks`
   and `pr-title / check`, block force pushes and deletion; approvals 0, or 1 with the owner on the bypass list.
5. Select the repo in the Mend Renovate app.
   Also turn on secret scanning, push protection and Dependabot alerts (Settings > Advanced Security); the
   template does not copy them:
   `gh api -X PATCH repos/<org>/<repo> -f 'security_and_analysis[secret_scanning][status]=enabled' -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'`
   and `gh api -X PUT repos/<org>/<repo>/vulnerability-alerts`.
6. Add the repo to the conformance probe TARGETS.

The first run on `main` is red by design (the image build has no `HEAD^` to diff against), and `release`
fails until the App from step 1 exists.

## Secrets and configuration

GitHub holds only what a workflow needs to run: credentials for CI, release and deploy steps (the two
`release` secrets above, a deploy token such as `CLOUDFLARE_API_TOKEN`). Every value the app reads at
runtime, secret or not, lives in [aws-infra](https://github.com/fjcloudaiconsulting/aws-infra) `clusters/`
and reaches the pods through Flux: secrets in a SOPS-encrypted Secret, everything else as plain `env` in the
app's manifests. Never add an app runtime value as an Actions secret or variable: GitHub never
shows a secret back, so it cannot be recovered or checked. Each GitHub secret or variable must have a
workflow that reads it; delete it when that workflow goes. Rule and inventory: aws-infra
[docs/configuration-map.md](https://github.com/fjcloudaiconsulting/aws-infra/blob/main/docs/configuration-map.md#actions-secrets-and-variables).

## Layout

- `backend/`: `app.py` (`GET /api/healthz` returns status, version, revision), its test, and the Dockerfile
  (`prod`, and a placeholder `migrations` target to replace with the project's tool; it must be idempotent).
- `compose.yaml`: local dev. `compose.smoke.yaml`: published images by tag, used by the shared smoke test.
- `.env.example`: configuration uses the `APP_` prefix.
- `CONTRIBUTING.md`: deviations from the contract, with reasons.

## When you add a database

Replace the `migrations` placeholder (`CMD ["true"]`) with the project's migration tool, and run it twice
against an empty database in the `test` job so CI proves it is idempotent (contract section 6). Add the
database to `compose.yaml` and `compose.smoke.yaml`.

## Adding a frontend

Follow [ziftbook](https://github.com/fjcloudaiconsulting/ziftbook): a `frontend/` directory, a `frontend`
image in the `image` matrix, `frontend` in the `release` job's `images`, a `Frontend Checks` gate (and in the
`release` job's `needs`), and a frontend service in `compose.smoke.yaml`.
