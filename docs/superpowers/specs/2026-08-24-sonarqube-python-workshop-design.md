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

All are small, single-purpose, and easy to point at during a walkthrough —
no attempt to be exhaustive or realistic-scale.

Note: the naming-convention violation used later in the workshop is
deliberately **not** pre-planted here — see "Custom naming-convention rule
mechanic" below. It's introduced as a live edit during the workshop instead,
so it's unambiguously "new code" on the second scan regardless of the
org's New Code Definition setting.

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
- `coverage.xml` is generated once during setup and **committed to the
  repo**. Attendees do not need Python, pytest, or Django installed to run
  the workshop scan — the scanner just reads the checked-in report. The
  README calls out that this is a static, pre-generated artifact (fine for
  a fixed workshop codebase) and includes an optional/advanced section for
  attendees who want to install Python and regenerate it themselves.

## Custom naming-convention rule mechanic

Rule: **`python:S117`** ("Local variable and function names should comply
with a naming convention") — built into Sonar way, takes a configurable
`format` regex.

Workshop steps (documented in README, with exact click-path and regex spelled
out — no "customize as you see fit" hand-waving):
1. In SonarQube Cloud: **Organization → Quality Profiles → Python → Sonar
   way → "..." menu → Copy**, name it e.g. `Workshop Python`.
2. Open the new profile, search for rule `S117`, open its parameters, and
   set `format` from the Sonar way default (`^[_a-z][a-z0-9_]*$`, i.e. any
   lowercase snake_case name) to a stricter minimum-length variant:
   `^[a-z][a-z0-9_]{2,}$` — same snake_case shape, but now requires at
   least 3 characters total. This is the concrete value the README tells
   the attendee to paste in; it's picked specifically so ordinary
   identifiers in the codebase are unaffected and only the one renamed
   variable (next section) trips it.
3. **Quality Profiles → Projects → assign** the new profile to this project
   (or set it as the org default for Python).
4. Back in the code, rename one existing variable to violate the new rule
   (see next section) before rerunning the scan.

## Guaranteeing a deterministic Quality Gate failure

Rating-based gate conditions (e.g. "Maintainability Rating") are not
reliable for a single low-effort code smell in a small codebase — the debt
ratio may not cross a rating boundary. Instead, the README has the user
create a copy of the Sonar way Quality Gate with one added condition:

- **New Code Smells is greater than 0** (evaluated on New Code)

To make this deterministic regardless of the org's New Code Definition
(previous version / number of days / reference branch), the workshop has
the attendee make an actual source edit between the two scans: rename an
existing compliant variable (e.g. `total_price` in `billing/views.py`) to a
too-short name (e.g. `tp`) that still matches the *default* S117 format but
violates the new minimum-length regex. Because the line is genuinely
changed, it's counted as new code under any New Code Definition strategy,
so the resulting S117 issue reliably flips the "New Code Smells > 0"
condition on rerun — independent of remediation-effort math or the org's
New Code window.

## README structure

1. Prerequisites (Python 3.x, a SonarQube Cloud account in org
   `sonar-workshop-1`, GitHub account). (COMMENT: Ideally they don't have to install python - I'd liek to make this as frictionless as possible)
2. Clone the repo.
3. Install the `sonar-scanner` CLI (Homebrew on macOS, manual zip + PATH
   entry for Linux/Windows) and verify with `sonar-scanner -v`. (COMMENT: let's make sure to add explicit steps for htis based on documentation)
4. Create a new project in SonarQube Cloud under org `sonar-workshop-1`,
   generate a token.
5. Install Python deps, run tests with coverage to produce `coverage.xml`. (COMMENT: again, let's see if we can get away with no python install by committing the test report to repo)
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
