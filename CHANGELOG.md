# Changelog

All notable changes to Super Ads are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Redesigned README with a demo video (GIF and MP4) recorded from real
  `super-ads-core` output, an HTML report screenshot, a generated architecture
  diagram (light and dark), and Mermaid diagrams of the audit lifecycle,
  evidence verdicts, and the mutation gate. Media sources live in `docs/media/`.
* `tests/freshness` and a CI "Evidence freshness" job (`pytest -m freshness`)
  that compare committed evidence with today's date. Release verification
  requires the job.

### Changed

* Dependabot version updates are disabled for GitHub Actions as well as pip
  (`open-pull-requests-limit: 0`), so no update branches are created.
  Security updates are unaffected.

### Fixed

* Pinned git installs (`--ref`) failed on git 2.43 because
  `checkout --detach --end-of-options <sha> --` is rejected there. The installers
  now check out the already validated hex SHA with `checkout --detach <sha> --`.
* Logic tests no longer fail when the calendar passes an evidence refresh date;
  they evaluate the committed 2.1.0 evidence snapshot at its own date. Live
  freshness stays enforced by the release gate and the freshness suite.
* Dependency-audit test expects the sorted guarded-code scope after the rename.

## [2.1.0] - 2026-11-27

First Super Ads release by Buckleson.

### Added

* Super Ads branding across the plugin, marketplace, skills, agents, core
  package (`super_ads_core`), Cockpit companion (`mods/super-ads-cockpit`),
  schemas (`urn:buckleson:super-ads:*`), environment variables (`SUPER_ADS_*`),
  installers, CI, and documentation.
* New README with quickstart, command reference, and security summary.

### Security

* Full line-by-line security review of skills, agents, scripts, core package,
  Cockpit hooks, installers, CI workflows, evals, control-plane data, and tests.
  No malicious code, prompt injection, telemetry, or data exfiltration was found.
* `fetch_page.py` streams responses and enforces a 10 MiB decoded-body ceiling,
  which also bounds gzip/deflate decompression bombs.
* URL validation now rejects deprecated IPv6 site-local space (`fec0::/10`),
  which Python's `is_global` still treats as public.
* Guarded Playwright contexts close every WebSocket, since HTTP routing does not
  see WebSocket upgrades.
* PDF rendering in `super_ads_core.reporting` disables WeasyPrint's URL fetcher
  so rendered HTML can never reach the network or local files.
* The release-gate `git rev-parse` call ignores system git config, hooks, and
  fsmonitor helpers from the inspected checkout.
* `uninstall.sh` accepts a recursive ownership record only for the managed venv,
  so a tampered manifest cannot recursively delete a sibling skill.
* Skills and report instructions ban promotional copy, community links, and
  referral links in deliverables outright. Only operator white-label branding
  is allowed.

### Fixed

* Replicate image generation works with `replicate>=1.0` `FileOutput` results.
* Batch image generation validates `prompt`, `ratio`, and `output` types up front
  instead of aborting mid-batch.
* Landing-page analysis handles JSON-LD `@type` arrays and nested graphs.
* PDF report chart temp files are cleaned up even when rendering fails.
* CSV and native export adapters reject rows with more cells than headers instead
  of silently dropping data.
* Scoring-profile weight totals use `Decimal`, matching the scoring engine.
* `install.ps1` uses a portable temp directory on Linux and macOS PowerShell.
* `uninstall.sh` recognizes the managed venv when the skill root is a symlink.
* Cockpit `/ads-cockpit` no longer throws when invoked without arguments.

### Removed

* Upstream-only governance tooling that cannot apply to this repository: the
  live ecosystem reconciliation job, `audit_ecosystem_live.py`, the third-party
  fork census and ecosystem disposition ledgers, and their release-gate check.
* Dead `render_mermaid` helper in `generate_report.py`, which shelled out to an
  `mmdc` binary found on `PATH`.
* Community-mirror, membership, and promotional links.
