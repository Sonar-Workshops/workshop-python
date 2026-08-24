# SonarQube Cloud Python Scan Workshop — Design

## Purpose

Produce a small, self-contained Python repo that a workshop attendee can
clone, scan with SonarQube Cloud via the command-line scanner, and use to
learn:

1. How to read scan results (issues, coverage, quality gate).
2. How to customize a Quality Profile with a naming-convention rule.
3. How a Quality Gate failure shows up after introducing a rule violation.

## Base application

Source: `ado-python-sc/django-drf-project` (existing local repo), copied into
a new directory `workshop-python/`.

Discovery during setup: the copied scaffolding is incomplete — `views.py`
files are empty, `settings.py` and `manage.py` are empty, `urls.py` imports
per-app `urls.py` modules that don't exist, and `billing/serializers.py` +
`billing/tests.py` reference a `BillingData` model that was never defined
(the actual model is `Billing`). This will be rebuilt as a small working
Django REST Framework app, keeping the same three domains and field shapes:

- `customers` — `Customer` model (name, email, phone, address)
- `products` — `Product` model (name, price, description)
- `billing` — `Billing` model (customer FK, product FK, quantity, total_amount)

Each app gets a real `views.py` (DRF generic list/detail views), `urls.py`,
and a working `serializers.py`. `billing`'s serializer/tests will be fixed to
use `Billing`, not the nonexistent `BillingData`. Project-level `settings.py`
will be filled in with a minimal DRF+sqlite config, `urls.py` wires the three
apps, `manage.py` is restored to the standard Django entrypoint.

## Repository

- New GitHub repo: `Sonar-Workshops/workshop-python`, public, default branch
  `main`, matching the existing `Sonar-Workshops/workshop-java` convention.
- Local dir `workshop-python/` is `git init`-ed, pushed there via `gh`.

## Planted Sonar issues

Deliberately introduced in the rebuilt app code (not in tests), so a first
scan shows a handful of real, explainable findings:

- Hardcoded secret: a fake API key constant in `billing/views.py` (security
  hotspot).
- SQL built via string formatting instead of the ORM, in a small raw-query
  helper in `products/views.py` (vulnerability).
- Bare `except:` clause in a helper in `customers/views.py` (bug/code smell).
- Mutable default argument (`def f(items=[])`) in a small utility function
  (bug).
- Unused import left in one module (code smell).
- One identifier with an inconsistent naming style (e.g. a variable named
  `Total_Price` in `billing/views.py`) — deliberately **conformant** with the
  default "Sonar way" profile, reserved to violate the *customized* naming
  rule introduced later in the workshop.

All are small, single-purpose, and easy to point at during a walkthrough —
no attempt to be exhaustive or realistic-scale.

## Test coverage

- `pytest` + `pytest-django` as the test runner (not `manage.py test`), since
  `pytest-django` integrates cleanly with `coverage.py`'s XML output that
  SonarQube consumes directly.
- `coverage run -m pytest` + `coverage xml` → `coverage.xml`.
- `sonar-project.properties` sets
  `sonar.python.coverage.reportPaths=coverage.xml`.
- Tests cover the CRUD endpoints of all three apps at a level that yields
  partial, non-trivial coverage (not 0%, not artificially 100%) — using the
  existing `customers/tests.py` and `products/tests.py` as-is (already
  reasonable), and fixing `billing/tests.py` to use the real `Billing` model.

## Custom naming-convention rule mechanic

Rule: **`python:S117`** ("Local variable and function names should comply
with a naming convention") — built into Sonar way, takes a configurable
`format` regex.

Workshop steps (documented in README):
1. Duplicate/extend the default Python quality profile into a new profile.
2. Edit `python:S117`'s `format` parameter to a stricter regex that the
   pre-planted `Total_Price`-style identifier violates but ordinary
   `snake_case` names don't.
3. Assign the new profile to the project.

## Guaranteeing a deterministic Quality Gate failure

Rating-based gate conditions (e.g. "Maintainability Rating") are not
reliable for a single low-effort code smell in a small codebase — the debt
ratio may not cross a rating boundary. Instead, the README has the user
create a copy of the Sonar way Quality Gate with one added condition:

- **New Code Smells is greater than 0** (evaluated on New Code)

Because SonarQube Cloud's default New Code definition (e.g. 30-day window)
treats both scans in the workshop as "new," the single naming-rule violation
introduced on rerun will deterministically flip this condition and fail the
gate — independent of remediation-effort math.

## README structure

1. Prerequisites (Python 3.x, a SonarQube Cloud account in org
   `sonar-workshop-1`, GitHub account).
2. Clone the repo.
3. Install the `sonar-scanner` CLI (Homebrew on macOS, manual zip + PATH
   entry for Linux/Windows) and verify with `sonar-scanner -v`.
4. Create a new project in SonarQube Cloud under org `sonar-workshop-1`,
   generate a token.
5. Install Python deps, run tests with coverage to produce `coverage.xml`.
6. Run `sonar-scanner` with the token; point at `coverage.xml`.
7. Navigate the results: Issues tab (bugs/vulnerabilities/code smells/hotspots),
   Measures (coverage %), Quality Gate (passing).
8. Customize the quality profile: adjust `python:S117`'s naming regex,
   assign the profile to the project.
9. Customize the quality gate: add "New Code Smells > 0".
10. Rerun the scan, observe the naming violation and the resulting Quality
    Gate failure; explain why (new code smell count > 0 on New Code).

## Out of scope

- No CI/CD pipeline (GitHub Actions) — this is a manual CLI-scan workshop.
- No attempt to make the Django app deployable/production-ready — sqlite,
  `DEBUG=True`-style dev settings are fine and expected for a workshop.
- No Docker packaging.
