# Static Code Analysis Issues — ticket_booking_system.py

The three tools used were **Pylint**, **Flake8**, and **Bandit**.  
All issues below were detected in the *original* file and are fixed in the submitted `ticket_booking_system.py`.

---

## Tool: Pylint

| # | Location | Code | Message | Severity |
|---|----------|------|---------|----------|
| 1 | Line 6 | W0611 | Unused import `math` | Warning |
| 2 | Line 15 | C0103 | Function name `reserveSeat` doesn't conform to snake_case naming style | Convention |
| 3 | Line 15 | C0116 | Missing function or method docstring (`reserveSeat`) | Convention |
| 4 | Line 15 | W0102 | Dangerous default value `[]` as argument (`order_history`) | Warning |
| 5 | Line 19 | C0209 | Formatting a regular string which could be an f-string | Convention |
| 6 | Line 23 | C0116 | Missing function or method docstring (`cancel_seat`) | Convention |
| 7 | Line 26 | W0702 | No exception type(s) specified (bare except) | Warning |
| 8 | Line 30 | C0116 | Missing function or method docstring (`check_seat_status`) | Convention |
| 9 | Line 31 | W0612 | Unused variable `booking_fee` | Warning |
| 10 | Line 32 | C0121 | Comparison to `None` should use `is None` | Convention |
| 11 | Line 37 | C0103 | Function name `computeDiscountedPrice` doesn't conform to snake_case | Convention |
| 12 | Line 37 | C0116 | Missing function or method docstring (`computeDiscountedPrice`) | Convention |
| 13 | Line 38 | W0612 | Unused variable `base_price` | Warning |
| 14 | Line 39 | W0123 | Use of `eval` | Warning |
| 15 | Line 43 | C0116 | Missing docstring (`generate_ticket_hash`) | Convention |
| 16 | Line 47 | C0116 | Missing docstring (`generate_booking_pin`) | Convention |
| 17 | Line 51 | C0116 | Missing docstring (`export_seating_chart`) | Convention |
| 18 | Line 52 | W1514 | Using `open` without explicitly specifying an encoding | Warning |
| 19 | Line 57 | C0116 | Missing docstring (`get_theater_summary`) | Convention |
| 20 | Line 59 | W0612 | Unused variable `seat` (loop variable not used) | Warning |
| 21 | Line 60 | C0121 | Comparison to `True` should use `is True` or just test truthiness | Convention |
| 22 | Line 65 | C0116 | Missing docstring (`main`) | Convention |

**Original rating: 5.69/10 → Fixed rating: 10.00/10**

---

## Tool: Flake8

| # | Location | Code | Message |
|---|----------|------|---------|
| 1 | Line 6 | F401 | `math` imported but unused |
| 2 | Line 19 | E501 | Line too long (82 > 79 characters) |
| 3 | Line 26 | E722 | Do not use bare `except` |
| 4 | Line 31 | F841 | Local variable `booking_fee` is assigned to but never used |
| 5 | Line 32 | E711 | Comparison to `None` — should be `if cond is None:` |
| 6 | Line 38 | F841 | Local variable `base_price` is assigned to but never used |
| 7 | Line 60 | E712 | Comparison to `True` should be `if cond is True:` or `if cond:` |

**Fixed file: 0 Flake8 warnings**

---

## Tool: Bandit (Security)

| # | Location | Issue ID | Description | Severity | Confidence |
|---|----------|----------|-------------|----------|------------|
| 1 | Line 26 | B110 | `try/except/pass` — silently swallowing exceptions | Low | High |
| 2 | Line 39 | B307 | Use of `eval()` — arbitrary code execution risk (CWE-78) | Medium | High |
| 3 | Line 44 | B324 | Use of weak MD5 hash for security purposes (CWE-327) | High | High |
| 4 | Line 48 | B311 | `random.randint` is not suitable for cryptographic use (CWE-330) | Low | High |
| 5 | Line 54 | B605 | `os.system()` with string concatenation — shell injection risk (CWE-78) | High | High |

**Fixed file: 0 Bandit issues**

---

## Summary of Fixes Applied

| Issue | Original Code | Fixed Code |
|-------|--------------|------------|
| Mutable default argument | `order_history=[]` | `order_history=None` + guard |
| Bare `except` | `except:` | `except KeyError:` |
| `None` comparison | `== None` | `is None` |
| Unused variable `booking_fee` | Present but unused | Removed |
| `eval()` use | `eval(formula)` | Replaced with explicit `discount_rate` float param |
| MD5 hash | `hashlib.md5(...)` | `hashlib.sha256(...)` |
| Insecure random | `random.randint(...)` | `secrets.randbelow(...)` |
| Shell injection | `os.system("echo ..." + filename)` | `print(...)` |
| Unused import | `import math` | Removed |
| Naming convention | `reserveSeat`, `computeDiscountedPrice` | `reserve_seat`, `compute_discounted_price` |
| Missing docstrings | All functions | All functions documented |
| `True` comparison | `== True` | Truthiness check `if details["is_sold"]:` |
| Unused loop variable | `for seat, details in ...` | `for details in seats.values()` |
| Open without encoding | `open(filename, "w")` | `open(filename, "w", encoding="utf-8")` |
| f-string | `% (seat_id, customer)` | f-string |
| Module-level constant | lowercase `theater_seats` | `THEATER_SEATS` |
