# Exercise 07 — Fix Bug #1 with `#selection`
## ShopSphere Workshop · Time: 5 min · Feature: `#selection` in Copilot Chat

> **MANDATORY** — Fix Bug #1. First real code change; verify with `python demo.py` after.

---

### Objective
Fix the null discount crash (Bug #1) using `#selection` — the fastest way to
ask Copilot about a specific block of code without switching context.

---

### How `#selection` Works
Select code in the editor, then in Copilot Chat type `#selection`.  
Copilot receives exactly the lines you highlighted — no file path needed.

---

### The Bug

Open `python-services/checkout-service/app/service/checkout_service.py`

Find this block (around line 28):
```python
discount = self.discount_client.get_discount(user_id)

# BUG 1: No null/None check on discount
final_amount = amount - discount   # crashes when discount is None
```

---

### Step 1 — Select the Buggy Lines

In the editor, highlight these three lines:
```python
discount = self.discount_client.get_discount(user_id)
# BUG 1: No null/None check on discount
final_amount = amount - discount
```

---

### Step 2 — Paste This into Copilot Chat

```
📋 COPY AND PASTE INTO COPILOT CHAT (with the lines selected):

#selection

The selected code crashes with TypeError when get_discount() returns None.
This happens for all odd user_ids (new signups, B2B accounts, trial users).

Fix it so that:
- If discount is None, treat it as 0.0 (no discount applies)
- Keep the fix to one line — do not restructure the method
- Show me only the changed lines in a diff format
```

---

### Step 3 — Apply the Fix

Copilot should suggest:
```python
discount = self.discount_client.get_discount(user_id)
discount = discount if discount is not None else 0.0
final_amount = amount - discount
```

Accept the suggestion or use the `Apply in Editor` button.

---

### Step 4 — Verify

```bash
python demo.py
```

Expected: odd user IDs (`101`, `103`, `105`, `201`, `301`) now show
`processing` instead of `failed`.  
Failure rate should drop from 50% → ~25% (payment failures still exist).

---

### Checkpoint ✓

`python demo.py` no longer crashes for odd user IDs.  
`user_id=101` returns `{"status": "processing"}` — not `{"status": "failed"}`.

**Next:** [Exercise 08 — Fix the Race Condition with Agent Mode](Exercise-08-Fix-Async-and-Exceptions-Agent-Mode.md)
