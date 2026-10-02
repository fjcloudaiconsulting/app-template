# Contributing

Pull request titles are Conventional Commits (`type(scope): summary`); merges are squash-only and release-please
turns them into releases.

## Deviations from the release contract

- No lockfile yet: the placeholder backend has no dependencies. When adding the first one, start uv
  (`pyproject.toml` plus `uv.lock`, installed with `uv sync --locked` in CI and the Dockerfile), per section 10.
