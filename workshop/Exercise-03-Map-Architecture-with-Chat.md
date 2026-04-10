# Exercise 03 — Map the Architecture with Chat
## ShopSphere Workshop · Time: 5 min · Feature: Copilot Chat + multiple `#file`

> **OPTIONAL** — Deeper exploration of the codebase. Complete after the mandatory exercises if time allows.

---

### Objective
Before touching any code, map the full request flow through the codebase using multiple `#file` references. Know the blast radius before you write a single line of fix.

---

### Why This Matters
Debugging without a map leads to random code changes that make things worse.  
Copilot Chat can build the architecture map **for you** in seconds.

---

### Step 1 — Open Copilot Chat

Press `Ctrl+Alt+I`

---

### Step 2 — Paste This Prompt

```
📋 COPY AND PASTE INTO COPILOT CHAT:

I'm responding to a P0 checkout incident. Before I touch any code,
I need to understand the full request flow.

Using these four files:
#file:python-services/checkout-service/app/api/checkout_api.py
#file:python-services/checkout-service/app/service/checkout_service.py
#file:python-services/checkout-service/app/client/discount_client.py
#file:python-services/checkout-service/app/client/payment_client.py

Do the following:
1. Draw an ASCII diagram showing the request flow from POST /checkout
   to the external payment gateway
2. List every function call across the chain
3. For each call, state what it can return — including None, exceptions,
   and partial success cases
4. Highlight any place where a failure would be silently swallowed
```

---

### What You Should Receive

A diagram similar to:
```
POST /checkout
  └─ CheckoutService.process_checkout()
       ├─ DiscountClient.get_discount()   → float | None   ← can be None!
       └─ asyncio.create_task(            ← NOT awaited!
              PaymentClient.process_payment()
          )  → never surfaces result
```

And a list noting that `get_discount()` returns `None` for odd user IDs.

---

### Step 3 — Follow-Up Question

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Based on the flow you mapped, answer: if get_discount() returns None
for user_id=101, what happens on the very next line of checkout_service.py?
What Python error is raised?
```

---

### Checkpoint ✓

You can identify the exact line where the crash happens and name the Python exception type (`TypeError: unsupported operand type(s) for -: 'float' and 'NoneType'`).

**Next:** [Exercise 04 — Debug Live Error with @terminal](Exercise-04-Debug-Live-Error-with-Terminal.md)
