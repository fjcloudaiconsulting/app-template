# app-template

Starter for new apps on the FJ Consulting release contract
([RELEASE_CONTRACT.md](https://github.com/fjcloudaiconsulting/.github/blob/main/RELEASE_CONTRACT.md)).
Backend only: a stdlib health endpoint, a `prod` and a `migrations` image, CI on the shared workflows,
release-please, and the post-release smoke test. Click "Use this template"; Actions are disabled in the
template itself.

## Owner checklist for each new repo

1. Install the release GitHub App on the repo.
2. Create the `release` environment and set its two secrets:
   `gh secret set RELEASE_APP_ID --env release` and `gh secret set RELEASE_APP_PRIVATE_KEY --env release`.
3. Repo settings: squash-merge only (merge commits and rebase off), delete branch on merge.
4. Branch protection on `main`: require `Backend Checks` and `pr-title / check`.
5. Select the repo in the Mend Renovate app.
6. Add the repo to the conformance probe TARGETS.

The first run on `main` is red by design (the image build has no `HEAD^` to diff against), and `release`
fails until the App from step 1 exists.

## Layout

- `backend/`: `app.py` (`GET /api/healthz` returns status, version, revision), its test, and the Dockerfile
  (`prod`, and a placeholder `migrations` target to replace with the project's tool; it must be idempotent).
- `compose.yaml`: local dev. `compose.smoke.yaml`: published images by tag, used by the shared smoke test.
- `.env.example`: configuration uses the `APP_` prefix.

## Adding a frontend

Follow [ziftbook](https://github.com/fjcloudaiconsulting/ziftbook): a `frontend/` directory, a `frontend`
image in the `image` matrix, `promote` images, a `Frontend Checks` gate, and a frontend service in
`compose.smoke.yaml`.
