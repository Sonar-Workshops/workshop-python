# SonarQube Cloud Python Workshop

A small Django REST Framework app (customers / products / billing) used to
walk through scanning a Python project with SonarQube Cloud from the command
line: run a scan, read the results, then customize a Quality Profile with a
naming-convention rule and watch a Quality Gate fail.

A pre-generated `coverage.xml` is committed to this repo, so you do **not**
need Python installed to complete the core workshop — you only need `git`
and the `sonar-scanner` CLI. An optional section at the end shows how to
regenerate coverage yourself if you want to.

## 1. Prerequisites

- `git`
- A SonarQube Cloud account with access to the **`sonar-workshop-1`**
  organization (ask your workshop host for an invite if you don't have one)
- Java 17+ available on your machine (the scanner needs it to run; on
  scanner CLI 7.2+ it can auto-provision a JRE for you, but having a system
  Java avoids surprises)

## 2. Clone the repo

```bash
git clone https://github.com/Sonar-Workshops/workshop-python.git
cd workshop-python
```

## 3. Install the sonar-scanner CLI

**macOS (Homebrew):**

```bash
brew install sonar-scanner
sonar-scanner -v
```

**Linux / Windows (manual install):**

1. Download the zip for your platform from
   `https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/`, e.g.
   `sonar-scanner-cli-8.1.0.6389-linux-x64.zip` or
   `sonar-scanner-cli-8.1.0.6389-windows-x64.zip`
   (check the page for the current latest version number).
2. Unzip it somewhere permanent, e.g. `~/tools/sonar-scanner`. This is your
   `$install_directory`.
3. Add `$install_directory/bin` to your `PATH`:
   - macOS/Linux: append `export PATH="$HOME/tools/sonar-scanner/bin:$PATH"`
     to your `~/.zshrc` or `~/.bashrc`, then `source` it (or open a new
     terminal).
   - Windows: add `<install_directory>\bin` to your user `PATH` environment
     variable, then open a new PowerShell window.
4. Verify in a **new shell**:
   ```bash
   sonar-scanner -h        # macOS/Linux
   sonar-scanner.bat -h    # Windows
   ```
5. macOS Gatekeeper note: if macOS blocks the binary as "from an
   unidentified developer," run:
   ```bash
   sudo xattr -dr com.apple.quarantine /path/to/sonar-scanner-*-macosx-aarch64
   ```

## 4. Create the project in SonarQube Cloud

1. Go to [sonarcloud.io](https://sonarcloud.io) and make sure you're in the
   **`sonar-workshop-1`** organization (top-left org switcher).
2. Click **+ → Analyze new project**, choose **workshop-python** if it's
   listed from GitHub, or create it manually with:
   - **Project key:** `workshop-python`
   - **Display name:** `SonarQube Cloud Python Workshop`
3. Choose analysis method **"Locally"** / **"Other CI"** (i.e. not GitHub
   Actions) — we're scanning from the command line.
4. Generate a token when prompted (or via **My Account → Security →
   Generate Token**). Copy it — you won't see it again.

This repo's `sonar-project.properties` already sets
`sonar.organization=sonar-workshop-1` and `sonar.projectKey=workshop-python`
to match, so you shouldn't need to pass those on the command line.

## 5. Run the scan

Export your token and run the scanner from the repo root:

```bash
export SONAR_TOKEN=<the token you generated>
sonar-scanner
```

This picks up `sonar-project.properties`, including
`sonar.python.coverage.reportPaths=coverage.xml`, which points at the
coverage report already committed in this repo.

Wait for `EXECUTION SUCCESS` in the output, then follow the printed link
(or go back to sonarcloud.io) to view the results.

## 6. Read the results

On the project page in SonarQube Cloud:

- **Issues** tab — the handful of planted findings in this codebase:
  - a hardcoded credential-like constant in `billing/views.py` (Security
    Hotspot)
  - a SQL query built with string formatting in `products/views.py`
    (Vulnerability)
  - a bare `except:` clause in `customers/views.py` (Code Smell / Bug)
  - a mutable default argument (`def f(items=[])`) in `billing/views.py`
    (Bug)
  - an unused import in `products/views.py` (Code Smell)

  Click into a couple of them — each shows the rule rationale and where in
  the code it fires.
- **Measures** tab — coverage percentage (from the committed `coverage.xml`),
  duplication, size.
- **Quality Gate** — should currently show **Passed**. The default "Sonar
  way" gate only fails on rating/coverage/duplication thresholds for *new*
  code, and this first scan doesn't trip any of them.

## 7. Customize the Quality Profile with a naming-convention rule

We'll tighten rule `python:S117` ("Local variable and function names should
comply with a naming convention"), which takes a configurable regex.

1. In SonarQube Cloud: **Organization → Quality Profiles → Python**.
2. Find **Sonar way**, open its **"..."** menu, and choose **Copy**. Name
   the copy `Workshop Python`.
3. Open `Workshop Python`, search for rule **S117**, and open its
   parameters.
4. The default `format` is `^[_a-z][a-z0-9_]*$` (plain lowercase
   snake_case). Replace it with:
   ```
   ^[a-z][a-z0-9_]{2,}$
   ```
   This keeps the same snake_case shape but now requires names to be at
   least 3 characters long.
5. Go to **Quality Profiles → Workshop Python → Projects**, and assign it
   to `workshop-python` (or set `Workshop Python` as the org default for
   Python).

## 8. Introduce the naming violation

In `billing/views.py`, find the `total_price` variable inside
`BillingListCreateView.create()`:

```python
total_price = product.price * quantity
```

Rename it to something too short for the new rule, e.g. `tp`:

```python
tp = product.price * quantity
tp = apply_discount_codes(tp, request.data.get("discount_codes", []))
serializer.save(total_amount=tp)
```

(`tp` still matches the *default* S117 format — it's valid lowercase — but
fails the minimum-length regex you just set on `Workshop Python`.)

## 9. Add a Quality Gate condition and rerun

Rating-based gate conditions can be too forgiving to reliably fail on a
single new code smell in a small project, so we'll add an explicit
condition instead:

1. **Organization → Quality Gates**, copy **Sonar way** into a new gate,
   e.g. `Workshop Gate`.
2. Add a condition: **New Code Smells is greater than 0** (evaluated
   `On New Code`).
3. Assign `Workshop Gate` to the `workshop-python` project.
4. Commit your edit from step 8, then rerun:
   ```bash
   sonar-scanner
   ```

Because you actually changed a line of source, it's counted as new code
under any New Code Definition strategy your org uses. The renamed `tp`
variable now violates `S117` under the `Workshop Python` profile, which
adds exactly one new code smell — tripping the condition you just added.

## 10. See the failure

Refresh the project page: **Quality Gate** now shows **Failed**, with the
"New Code Smells" condition highlighted. Click into **Issues → New Code**
to see the single flagged `tp` naming violation directly. This is the same
mechanism real teams use to keep code quality from regressing over time:
new rules (or tightened parameters) apply going forward, and the gate turns
red the moment new code doesn't meet the bar.

---

## Optional: regenerate the coverage report yourself

If you want to install Python and see how `coverage.xml` was produced:

```bash
python3 -m venv .venv
source .venv/bin/activate        # .venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
coverage run -m pytest
coverage xml
```

This regenerates `coverage.xml` in place; rerun `sonar-scanner` afterward to
pick up the refreshed numbers.
