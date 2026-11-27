"""Live evidence-freshness checks.

These tests compare the committed evidence ledgers and vulnerability
exceptions with today's UTC date. They are expected to fail once evidence
passes its refresh date, which is the signal to re-verify sources or upgrade
dependencies. They are excluded from the default suite (see pyproject.toml)
so that logic tests stay deterministic, and they run in their own CI job:

    python -m pytest -m freshness

The release gate (scripts/release.py) enforces the same freshness rules live,
so a stale snapshot can never be released regardless of this split.
"""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

import pytest

from super_ads_core.product_status import evaluate_product_status
from tests.audit.test_source_grounding import assert_grounding_claims_fresh

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.freshness


def _today():
    return datetime.now(timezone.utc).date()


def _release_module():
    name = "super_ads_release_freshness"
    if name in sys.modules:
        return sys.modules[name]
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts/release.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_load_bearing_claims_and_sources_are_fresh_today():
    assert_grounding_claims_fresh(ROOT, _today())


def test_product_status_reports_no_stale_claims_today():
    result = evaluate_product_status(ROOT, as_of=_today())
    assert result["evidence"]["stale_load_bearing_claims"] == []
    assert result["evidence"]["unverified_load_bearing_claims"] == []


def test_vulnerability_exceptions_are_unexpired_today():
    release = _release_module()
    release._check_vulnerability_exceptions(ROOT, _today())
