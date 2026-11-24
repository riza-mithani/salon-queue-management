# Salon Queue Management System — Flows & Business Rules

**File:** `docs/03-flows-rules.md`  
**Status:** Ready for Review  
**References:** `docs/01-brief.md`, `docs/02-screens.md`, `Salon_Queue_Management_Vibe_Coding_Guide.pdf`  
**Target Stack:** Streamlit (Python 3.12), single-file architecture (`app.py`), shared multi-user state.

---

## 1. System Entities & Queue Lifecycle State Machine

### 1.1 Queue Status Transitions
Queue tickets progress strictly forward through the following lifecycle. Tickets must **never** move backwards.

```
[Customer Joins / Walk-in]
           │
           ▼
       WAITING ────────────► CANCELLED (Customer self-cancels or Reception cancels)
           │
      (Call Next)
           ▼
        CALLED ────────────► NO-SHOW (Customer does not show within grace period)
           │
     (Barber: Start)
           ▼
      IN_SERVICE
           │
     (Barber: Done)
           ▼
      COMPLETED
```

- **WAITING:** Ticket is active in line. Waiting for a barber to become available.
- **CALLED:** Barber or receptionist tapped "Call Next". Customer is alerted to report to the chair; TV chimes and flashes token.
- **IN_SERVICE:** Customer is seated; barber tapped "Start". Timer is running.
- **COMPLETED:** Barber tapped "Done" and confirmed. Service is complete; ticket leaves the active queue.
- **CANCELLED:** Terminal status. Customer tapped "Cancel My Spot" or Receptionist cancelled the ticket while still in WAITING.
- **NO-SHOW:** Terminal status. Customer was CALLED but did not arrive within the 10-minute grace period.

### 1.2 Barber Operational Statuses
Each barber/stylist has one of the following live states:
- **FREE / AVAILABLE:** On duty and currently not serving any customer. Eligible to receive or call next customer.
- **BUSY / IN SERVICE:** Currently serving a customer with timer active. Only one customer in chair per barber at any time.
- **ON BREAK:** On duty, but temporarily resting/unavailable. Cannot be assigned new customers.
- **OFF DUTY:** Configured as off duty by Salon Owner. Not available in barber selector and excluded from queue calculations.

---

## 2. Customer Queue Joining Flow (Online)

1. **Access:** Customer opens `/` (Home) or navigates to `/join` on mobile or desktop browser without login.
2. **Pre-check:** System checks whether the online queue is **Open**:
   - If **Closed**, the Join Queue button on Home is disabled, and `/join` displays an informative banner: *"Online queue is currently closed. Walk-ins are welcome at the reception desk."*
3. **Form Input:**
   - **Full Name:** Required, trimmed text.
   - **Phone Number:** Required, exactly 10 digits (digits only, e.g. Indian mobile number format `^[0-9]{10}$`).
   - **Service Selection:** Must choose between 1 and 3 active services. Selecting a 4th service is prevented with an explanatory alert.
   - **Barber Preference:** Default is **"Any Barber (Fastest)"**. Alternatively, customer may choose a specific on-duty, active barber from photo cards.
4. **Active Spot Check (Anti-Duplicate Rule):**
   - A customer (identified by phone number) can have only **one active spot** at a time (`WAITING`, `CALLED`, or `IN_SERVICE`).
   - If an active spot already exists for the entered phone number, the system does not create a duplicate token. Instead, it alerts the customer: *"You already have an active spot in the queue (Token: S-XX)"* and redirects directly to their existing `/status/:id` page.
5. **Token Generation:**
   - On submission, system validates inputs and creates a unique token: `S-1`, `S-2`, `S-3`, ..., sequential per day.
   - Entry is stored in the shared queue state with timestamp, customer details, selected services, preference, and initial status `WAITING`.
6. **Redirect:** The customer is immediately navigated to `/status/:id`.

---

## 3. Service Selection and Pricing Rules

1. **Approved Services:** Only four services are supported in the entire system:
   - Haircut
   - Hair Styling
   - Hair Spa
   - Hair Colouring
   *(Note: Beard Trim from the PDF guide sample is explicitly excluded per 01-brief.md and 02-screens.md).*
2. **Selection Bounds:**
   - Minimum: 1 service.
   - Maximum: 3 services.
3. **Price & Duration Calculations:**
   - Each service has an Owner-configured active price and estimated duration (in minutes).
   - Validation constraints: All prices must fall strictly within the approved range of **₹250 to ₹1,200**.
   - `Total Service Price = Sum of active prices of selected services`.
   - `Total Service Duration = Sum of active durations of selected services`.
4. **Inactive Services:**
   - Inactive services toggled by the Owner are hidden from the Join Queue screen and cannot be selected.
   - If an active service has an invalid or missing price/duration, booking is prevented with a clear administrative error message.

---

## 4. Barber Assignment Rules

1. **Preference Options:**
   - **Any Barber (Fastest):** The customer is kept in the general pool. They are served by whichever eligible barber becomes free first.
   - **Specific Barber (e.g., Barber X):** The customer is dedicated strictly to Barber X.
2. **Binding Rule:**
   - A customer who chose a specific barber (Barber X) is **never** assigned to another barber, even if other barbers are free or waiting.
3. **Call Next Resolution Algorithm:**
   When Barber X becomes FREE (or Receptionist / Barber taps "Call Next" for Barber X):
   - The system inspects all customers currently in `WAITING` status in strict chronological order of arrival (First-Come, First-Served / FCFS).
   - The system finds the **earliest waiting customer** whose preference is either **Barber X** OR **"Any Barber (Fastest)"**.
   - That customer's status transitions from `WAITING` to `CALLED`, with assigned barber locked to **Barber X**.
   - If no customer in `WAITING` matches Barber X or 'Any', Barber X remains FREE with an empty-queue message.
4. **Single Customer in Chair Constraint:**
   - A barber can have **at most one** customer with status `IN_SERVICE` at any time. A barber cannot start another service until the current customer is marked `COMPLETED`.

---

## 5. Queue Position and Waiting-Time Calculation

### 5.1 Queue Position Rule
- Queue position represents how many customers are ahead of this customer in line for their service.
- **For a customer who selected "Any Barber":**
  - Position = Number of active `WAITING` customers who joined before them (FCFS) + 1.
- **For a customer who selected Specific Barber X:**
  - Position = Number of active `WAITING` customers ahead of them who chose Barber X or chose 'Any Barber' and will be served by Barber X + 1.

### 5.2 Waiting-Time Calculation Formula
Waiting time is always presented as an **estimate** (e.g., `~35 min`), calculated dynamically from real shared queue data:

1. **For Customer with "Any Barber (Fastest)":**
   $$\text{Estimated Wait (min)} = \left\lceil \frac{\text{Total remaining service minutes of all customers ahead} + \sum \text{remaining minutes of in-service customers}}{\text{Number of Active Barbers on Duty (Free + Busy)}} \right\rceil$$
   - If no barbers are currently working (all off duty or on break), display: *"Wait time currently unavailable (No active barbers on duty)"*.
   - If position is 1st in line and a barber is free: `Estimated Wait ≈ 0–5 min` ("You're next!").

2. **For Customer with "Specific Barber X":**
   $$\text{Estimated Wait (min)} = (\text{Remaining minutes of Barber X's current in-chair customer}) + \sum (\text{Service duration of customers ahead assigned to Barber X})$$
   - If Barber X is currently on break, include the estimated remaining break duration.

---

## 6. Start and Done Service Workflow

1. **Screen:** Managed via `/barber/:name` (Barber View) or monitored via `/reception`.
2. **Start Service:**
   - When the called customer sits in the chair, the barber clicks **[Start]**.
   - Ticket status changes from `CALLED` to `IN_SERVICE`.
   - Barber status changes to `BUSY`.
   - A live digital elapsed timer starts in format `HH:MM:SS`.
   - The TV display updates Barber X's card to show `Now: S-XX`.
   - Customer's `/status/:id` page updates to indicate service is in progress.
3. **Done (Complete) Service:**
   - Barber clicks **[Done]**.
   - A confirmation dialog appears: *"Confirm service completion for [Customer Name] (Token [Token])?"*
   - Upon confirmation:
     - Ticket status changes from `IN_SERVICE` to `COMPLETED`.
     - Timer stops. Completed timestamp is recorded for daily statistics.
     - Barber status reverts to `FREE / AVAILABLE`.
     - Active queue updates immediately across all screens within 5 seconds.
     - Customer leaves the active queue.

---

## 7. No-Show and Cancellation Rules

### 7.1 Customer Self-Cancellation
- Allowed only while ticket status is `WAITING`.
- On `/status/:id`, customer clicks **[Cancel My Spot]**.
- A confirmation pop-up displays: *"Are you sure you want to cancel your queue spot?"* with options `[Keep My Spot]` and `[Confirm Cancellation]`.
- Upon confirmation:
  - Ticket status becomes `CANCELLED`.
  - Ticket is immediately removed from the active waiting list.
  - Waiting times and queue positions for all customers behind automatically recalculate.

### 7.2 Receptionist Cancellation
- Receptionist can cancel any `WAITING` customer from the Waiting List on Screen 4.
- Requires confirmation modal before updating status to `CANCELLED`.

### 7.3 No-Show Rule
- **Grace Period:** 10 minutes after a customer's token is transitioned to `CALLED`.
- If the called customer does not arrive at the barber station within 10 minutes:
  - Receptionist (or Barber) can mark the customer as **[No-show]**.
  - System prompts confirmation: *"Mark [Customer Name] (Token) as No-show?"*.
  - Upon confirmation, ticket status changes to `NO-SHOW` (terminal).
  - Barber becomes `FREE` and is immediately able to call the next waiting customer.
- **Re-arrival Policy:**
  - If a customer marked `NO-SHOW` subsequently arrives at the salon, they **cannot** reclaim their old position or token.
  - Receptionist must register them as a new walk-in. They join at the **very end** of the active queue with a **new sequential token**.

---

## 8. Walk-In Registration Flow

1. **Access:** Exclusively handled via Screen 4 (`/reception`) by Receptionist or Owner using the **[+ Add Walk-in]** button.
2. **Availability:** Walk-ins are **always permitted**, even when the online queue is toggled `Closed` by the Owner.
3. **Data Collected:**
   - Customer Name (required)
   - Phone Number (required, 10 digits; existing active-spot check applies)
   - Service Selection (1 to 3 active services)
   - Barber Preference ("Any Barber" or specific on-duty barber)
4. **Queue Insertion:**
   - Walk-in customer is assigned the next sequential token (`S-XX`).
   - Customer is appended to the **end of the active queue** in strict FCFS order. Walk-ins do not receive unfair priority over online waiting customers.
   - Receptionist can hand the token number to the customer or display it on the Waiting Area TV.

---

## 9. Online Queue Open / Closed Behaviour

1. **Owner Control:**
   - Controlled via Screen 7 (`/admin`) toggle: **Queue Switch: Open / Closed**.
2. **Behavior when Open:**
   - Customer can join online via `/join`.
   - Home screen displays active "Open" status and active "Join Queue" button.
3. **Behavior when Closed:**
   - Online joining is disabled.
   - Home screen displays a "Closed" badge.
   - Join Queue button is disabled or redirects with message: *"Online queue joining is currently closed. Please visit reception for walk-in availability."*
   - Existing active customers in the queue continue through their normal service lifecycle unaffected.
   - Receptionists can still register in-person walk-ins.
4. **Closing Time Buffer:**
   - If a salon closing time is configured, online joining automatically closes 30 minutes before closing time to prevent customers joining when they cannot be served. Walk-ins at reception remain subject to staff discretion.

---

## 10. Staff Availability, Shifts, and Breaks

1. **Owner Shift Toggle (Screen 7):**
   - Owner sets staff as **On Duty** or **Off Duty**.
   - If a barber is toggled **Off Duty**:
     - They cannot receive new assignments.
     - They do not appear as selectable in the customer barber-picker.
     - If the barber currently has an active `IN_SERVICE` customer, they must finish that customer; duty status change takes effect upon completion.
2. **Barber Break Toggle (Screen 5):**
   - A barber can toggle between **Available** and **On Break**.
   - **Safety Invariant:** A barber **cannot** go on break while in the middle of serving an active customer (`IN_SERVICE`). If they request a break while serving, the status change is queued and takes effect immediately after clicking `Done`.
3. **Break Impact on Queue & UI:**
   - Barber's status chip displays `On Break` across Home, Reception, Barber View, and TV.
   - Customers waiting who specifically selected this barber see an alert: *"[Barber Name] is currently on a short break. Your estimated wait accounts for this."*
   - "Call Next" is disabled for that barber until they switch back to `Available`.

---

## 11. Customer Notifications & Waiting Area TV Display

### 11.1 Customer Status Notifications (`/status/:id`)
- **Real-time updates:** The page automatically refreshes shared queue data (e.g. every 3–5 seconds).
- **Proximity Notification (2nd in line):**
  - When the customer reaches **2nd in line** (position = 2), a prominent amber notice is shown:
    > **"Start coming to the salon! You are 2nd in line."**
- **Turn Notification (Called):**
  - When status changes to `CALLED`, the screen transforms into a full-screen golden alert (`#EFB11D` background with bold contrast text):
    > **"It's your turn! Please go to [Barber / Stylist Name]."**
  - Includes a gentle vibration alert on mobile devices where supported by browser APIs.

### 11.2 Waiting Area TV Display (`/display`)
- Designed for unattended 1080p landscape display in the waiting lobby.
- **Top Row (Active Stations):**
  - Grid/row of team cards for all on-duty professionals with photo, name, status, and current token (e.g. `Now: S-12` or `Free` or `On Break`).
- **Bottom Section (Up Next):**
  - Displays the next **5 waiting tokens** in order, with service name and estimated wait minutes.
- **Newly Called Token Alert:**
  - When any customer transitions to `CALLED`:
    - The token flashes in gold on the screen for 10 seconds.
    - An audible chime sounds.
    - Fallback: If autoplay audio is blocked by the browser, the visual golden flash alert remains fully functional without crashing.

---

## 12. Edge Cases & Resilience Rules

1. **Zero Barbers On Duty:**
   - If all barbers are Off Duty or On Break, online queue joining is temporarily blocked with notice: *"No barbers currently available to take appointments. Please check back shortly."*
2. **Last Customer in Queue Finishes:**
   - Screens transition cleanly to friendly empty state: *"No one waiting — walk right in!"*
3. **Barber Finishes Faster / Slower than Scheduled:**
   - Waiting times dynamically recalculate based on remaining queue items. If a service runs over duration, timer continues counting up in red/warning font, and downstream estimates adjust.
4. **Customer Closes / Refreshes Phone Browser:**
   - The token and status URL `/status/:id` is deterministic and persistent. Returning to the link or entering the phone number at `/join` recovers their active session immediately.
5. **Simultaneous "Call Next" from Reception & Barber:**
   - Race conditions are guarded by atomic queue state transitions. If two calls occur concurrently, the first call locks the earliest matching customer; the second call automatically receives the next eligible customer.
6. **Customer Waits > 60 Minutes:**
   - On the Reception Dashboard waiting list, rows where `Wait Time > 60 min` are highlighted in amber to draw staff attention for service recovery.
7. **Bilingual Dynamic Content:**
   - All static labels, alerts, button text, and service names must load from the bilingual dictionary (English/Gujarati). No text hardcoded in presentation logic.

---

## 13. Testing & Verification Checklist

Before considering implementation complete, the following 14 test scenarios must pass:

- [ ] **TC-01 (Service Selection):** Joining queue allows 1, 2, or 3 services; prevents selecting 4 services; shows correct summed price and duration.
- [ ] **TC-02 (Price Boundary):** Service prices in Owner Settings strictly validate between ₹250 and ₹1,200; invalid values are rejected.
- [ ] **TC-03 (Duplicate Prevention):** Submitting with a phone number that already has an active token (`WAITING`, `CALLED`, `IN_SERVICE`) redirects to existing token status without creating a duplicate.
- [ ] **TC-04 (Any Barber Allocation):** Customer who picked "Any Barber" is called by the first barber who clicks "Call Next".
- [ ] **TC-05 (Specific Barber Isolation):** Customer who chose Barber A is never assigned to Barber B, even if Barber B calls next with an empty queue.
- [ ] **TC-06 (Order Priority FCFS):** When Barber A calls next, if both Customer 1 (Any Barber) and Customer 2 (Barber A) are waiting, Customer 1 is called first if Customer 1 joined earlier.
- [ ] **TC-07 (Proximity Banner):** Customer at position 2 sees the "Start coming to the salon" banner.
- [ ] **TC-08 (Called Alert & TV Chime):** When marked `CALLED`, customer sees full-screen golden alert "It's your turn!", and TV displays flashing token with chime.
- [ ] **TC-09 (Timer & Lifecycle):** Barber clicks "Start" -> status becomes `IN_SERVICE`, timer increments in `HH:MM:SS`. Barber clicks "Done" -> confirmation dialog -> status becomes `COMPLETED`, barber becomes `FREE`.
- [ ] **TC-10 (No-Show Re-entry):** Marking a customer as No-show changes status to `NO-SHOW`. Adding them again via Reception walk-in assigns a new token and places them at the end of the queue.
- [ ] **TC-11 (Online Queue Closed):** Closing online queue disables online Join Queue button; receptionist can still add walk-ins successfully.
- [ ] **TC-12 (Break Protection):** Barber cannot transition to `On Break` while a customer is `IN_SERVICE`.
- [ ] **TC-13 (Wait Over 60 Min Highlight):** Customers waiting longer than 60 minutes are styled with an amber highlight on the Reception Dashboard.
- [ ] **TC-14 (Language Toggle):** Toggling language between English and Gujarati updates all customer, receptionist, barber, and TV screens instantly.

---

## 14. Open Questions & Undecided Business Decisions

The following items are not finalized in `docs/01-brief.md` or `docs/02-screens.md` and are documented here for owner/client resolution:

1. **Staff PIN Assignment:**
   - Are staff PINs individual per barber (e.g., Amit: `1111`, Ravi: `2222`), or is there one universal Barber PIN shared by all barbers alongside separate Receptionist and Owner PINs?
2. **Grace Period Customization:**
   - Is the 10-minute no-show grace period fixed, or should the Owner be able to configure it in Owner Settings?
3. **Actual Salon Operating Hours:**
   - What are the official opening and closing times of the salon for automatic queue closure (e.g., 9:00 AM to 9:00 PM)?
4. **Estimated Wait Multiplier for Break Times:**
   - When a barber goes on break, what is the default assumed break duration (e.g. 15 minutes, 30 minutes) used in downstream wait-time calculations?
5. **Customer Cancellation Token Reuse:**
   - When a token is cancelled or marked no-show, should its token number be retired for the day, or should sequential numbering continue strictly incrementally without reusing numbers? *(Recommended: keep sequential without reusing numbers for audit integrity).*
