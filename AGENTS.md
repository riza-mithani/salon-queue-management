# AGENTS.md — Salon Queue Management System

A web-based queue management application for salons: customers join the queue from their phone, track position and wait time, and get called; receptionists and barbers manage live queues; waiting-area TV displays real-time turns.

---

## Read First Before Writing Any Code

Always read and follow the project specifications in `docs/` before making any changes:

- **`docs/01-brief.md`**: Project scope, user roles, must-have features, boundaries, and the **Don't Build** list.
- **`docs/02-screens.md`**: Detailed specifications for all 7 screens, UI layouts, actions, and device-specific behaviours.
- **`docs/03-flows-rules.md`**: Lifecycle state machines, queue formulas, barber assignment, walk-in rules, edge cases, and the 14-point test checklist.

---

## Approved Technology Stack & Architecture

- **Language & Runtime:** Python 3.12
- **Framework:** Streamlit (`streamlit run app.py`)
- **Single-File Architecture:** The entire application must be built within **one main Python file** (`app.py`) in the project root.
- **Shared Multi-Client State:** Since Streamlit sessions are isolated per browser tab by default, use a shared data manager (e.g. `@st.cache_resource` singleton, local thread-safe state, or SQLite/JSON file store) so that customer phones, reception tablets, barber phones, and the TV display remain synchronized in real time.
- **No Complex Frameworks:** Avoid introducing external microservice frameworks, heavy databases, or complex build tooling.

---

## Approved Colour Palette & Visual Design

Strictly adhere to the approved five-colour salon palette:

- **Warm Cream (`#EBE9E1`):** Primary page backgrounds, card surfaces, and neutral backgrounds.
- **Orange-Red (`#E43D12`):** Primary calls-to-action, prominent headings, and active buttons.
- **Golden Yellow (`#EFB11D`):** Highlights, "It's your turn" banner, token alerts, and badges.
- **Rose Pink (`#D6536D`):** Secondary accents, status badges, and borders.
- **Soft Pink (`#FFA2B6`):** Subtle card backgrounds, tags, and secondary highlights.

Typography: Elegant serif styling for the `BEAUTY SALON` wordmark and major headers, with clean, readable sans-serif typography for body text and queue metrics.

---

## Bilingual Support (English & Gujarati)

- Full support for **English** and **Gujarati** across all customer, reception, barber, and TV screens.
- **No Hard-Coded UI Text:** All labels, button texts, statuses, service names, and notifications must be defined in a centralized bilingual translation dictionary inside `app.py`.
- Dynamic language switcher toggle must be accessible on customer and shared screens.

---

## Critical Boundaries & Constraints (Do Not Invent)

1. **Do Not Invent Business Decisions:**
   - Salon business name is undecided: Use `BEAUTY SALON` as the placeholder wordmark.
   - Exact service prices and durations are not finalized: Use Owner Settings (Screen 7) configuration within the approved price range (**₹250 to ₹1,200** per service).
   - Staff names, roles, photos, and PINs are undecided: Keep them configurable in state or use clearly marked placeholder/demo defaults.
2. **Approved Services Only:**
   - Exactly four services: **Haircut**, **Hair Styling**, **Hair Spa**, **Hair Colouring**.
   - Do **NOT** add Beard Trim or other services.
3. **Approved Screens Only (7 Screens):**
   - Screen 1: Home (`/`)
   - Screen 2: Join Queue (`/join`)
   - Screen 3: My Status (`/status/:id`)
   - Screen 4: Reception Dashboard (`/reception`)
   - Screen 5: Barber View (`/barber/:name`)
   - Screen 6: Waiting Area TV (`/display`)
   - Screen 7: Owner Settings (`/admin`)
4. **Don't Build List:**
   - Online payments
   - Future-date appointments
   - SMS or WhatsApp integrations
   - Loyalty or reward points
   - Multiple salon branches

---

## Beginner-Friendly Coding Instructions

- **Code Readability:** Write clean, readable, self-explanatory Python with clear function names, inline comments, and type hints.
- **Modular Functions:** Organize `app.py` logically:
  1. Configuration & Styling (CSS injection for the 5-colour palette)
  2. Internationalization (Bilingual EN/GU dictionary)
  3. Shared State & Storage Management
  4. Queue Logic & Calculation Helpers
  5. Screen Components (one dedicated render function per screen)
  6. Routing & Navigation Controller
- **Controlled Step-by-Step Changes:**
  - Build one screen or one feature per task.
  - Test and verify against the checklist in `docs/03-flows-rules.md` after each step.
  - Report changed code and exact manual verification steps after every task.
