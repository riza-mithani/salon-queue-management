# Salon Queue Management System — Screens & Features

**File:** `docs/02-screens.md`  
**Status:** All seven screen designs approved  
**Reference:** `Salon_Queue_Management_Vibe_Coding_Guide.pdf`, especially page 3  
**Implementation direction:** Beginner-friendly Streamlit app with one main Python file.

## Project-wide design decisions

### Look and feel
Use the approved palette consistently:
- Warm cream: `#EBE9E1`
- Orange-red: `#E43D12`
- Rose pink: `#D6536D`
- Light pink: `#FFA2B6`
- Golden yellow: `#EFB11D`

Use elegant serif typography for the **BEAUTY SALON** wordmark and major headings, with clean readable body text. The actual salon business name remains undecided; do not invent one. Use salon-appropriate photographs for the Home hero, four service cards, and staff profiles. Provide placeholders if images are unavailable.

### Languages and roles
- Support English and Gujarati throughout customer-facing labels, buttons, statuses and service names.
- Customer: no staff PIN; can join queue and view own status.
- Receptionist: staff PIN; manages queue and adds walk-ins.
- Barber / hairstylist: staff PIN; manages assigned customers and service progress.
- Salon Owner: staff PIN; manages services, staff duty and online queue availability.
- Retain “Barber” where the PDF uses it, while allowing male barbers and female hairstylists in the actual team.

### Shared behaviour
- All operational screens must use shared queue data. Updates in one role's screen must appear in the relevant customer, reception, barber and TV screens.
- Do not hardcode illustrative customer names, tokens, staff availability, statistics or live waiting times as real data.
- Clearly label demo data.
- Keep the implementation beginner-friendly and in one main Streamlit Python file unless the user later approves a different structure.
- Do not add unrelated features.

---

# Screen 1: Home

**URL:** `/`  
**Users:** Customers and visitors  
**Purpose:** Introduce the salon, show queue and staff information, and direct customers to join.

## Layout and UI elements, top to bottom
1. Header with BEAUTY SALON wordmark, navigation (Home, About, Services, Join Queue), and English/Gujarati selector.
2. Split hero: text and queue information on the left; large beauty photograph on the right.
3. Open/Closed badge and configured closing time. The PDF's “Closes 9 PM” is an example, not a confirmed business hour.
4. Small live queue card beside hero content showing people waiting and estimated wait.
5. Prominent gold **Join Queue** button.
6. Team section with rectangular photo cards for male barbers and female hairstylists. Show name, role and Busy / Free / On Break status.
7. About section with a short introduction.
8. Four photographed service cards: Haircut, Hair Styling, Hair Spa, Hair Colouring.
9. Footer with salon information and navigation.

## Actions
- Home returns to `/`.
- About and Services navigate to their sections.
- Join Queue opens `/join`.
- Language selector switches English/Gujarati.

## Responsive behaviour
- Mobile: stack hero text and photo; keep queue card and Join Queue visible; stack or horizontally scroll team cards.
- Tablet: split hero where space allows; compact service grid.
- Desktop: spacious split hero and grids.

## Empty/error states
- Queue unavailable: explain that live queue information is temporarily unavailable; do not invent a count.
- No professionals available: show a clear availability message.
- Missing photo: show a neutral placeholder.
- Salon closed: show configured status and do not imply online joining is open.

## PDF checklist
Salon name/logo, Open/closing badge, live queue card, barber availability and large gold Join Queue button are included.

---

# Screen 2: Join Queue

**URL:** `/join`  
**Users:** Customers  
**Purpose:** Collect customer details, service choices and barber preference, calculate the summary and create a queue entry.

## Approved services
Only these four services:
1. Haircut
2. Hair Styling
3. Hair Spa
4. Hair Colouring

Do not add Beard Trim. It appears in the PDF example, but the user explicitly approved only the four services above.

## Fields and validation
- Full name: required.
- Phone: required; exactly 10 digits.
- Services: individual image cards; multi-select, minimum one and maximum three.
- Barber preference: **Any Barber (Fastest)** selected by default, or an individual available professional's photo card.
- Show all available male barbers and female hairstylists with name, role and availability.

## Service cards and prices
Each service card has its own photograph, name, configured duration and configured price. The approved price range is **₹250–₹1,200 per service**. Exact prices and durations have not been finalized; the Owner configures them in Screen 7. Do not invent final values. Do not allow booking of an active service with missing or invalid price/duration.

## Live summary
Automatically update selected services, total duration, total price and expected waiting time from current queue information. Do not use static example values as live results.

## Actions
- Service card selects/deselects the service.
- Prevent a fourth selection and explain the maximum of three.
- Any Barber selects automatic assignment to the earliest suitable available professional.
- Professional card selects that professional.
- **Confirm & Join Queue** validates data, creates a unique queue token and navigates to `/status/:id`.
- Back to Home returns to `/`.

## Responsive behaviour
- Mobile: single-column form, two-column service cards, compact professional cards.
- Tablet: wider form and service grid.
- Desktop: four service cards in a row where space allows; summary clearly visible.

## Empty/error states
No service selected; invalid phone; more than three services; no available professionals; online queue closed; missing service price/duration; submission failure. Explain the issue, preserve entered data where possible, and allow retry where appropriate.

## PDF checklist
Name and validated phone, multi-select maximum-three service cards, Any Barber/photo picker, live duration/price/wait summary, and Confirm to My Status are included.

---

# Screen 3: My Status

**URL:** `/status/:id`  
**Users:** Customers with a queue entry  
**Purpose:** Track queue position, estimated waiting time and assignment.

## UI elements
1. BEAUTY SALON header and language selector.
2. Large unique token, e.g. `S-14`.
3. Queue position, e.g. `4th in line`.
4. Circular countdown with remaining estimated minutes in the centre; updates automatically.
5. Booking details: selected services, assigned professional and relevant booking details.
6. At second in line, show **“Start coming to the salon”**.
7. When called, show a full-screen gold message: **“It's your turn! Go to [professional name]”**.
8. **Cancel My Spot** button.

## Actions
- Cancel My Spot opens a confirmation popup.
- Keep My Spot closes the popup without changing the queue.
- Confirm Cancellation cancels the active entry and updates the queue.
- Language selector switches language.

## Responsive behaviour
- Mobile: large token and circular countdown, vertically stacked details.
- Tablet: token and countdown may sit side by side.
- Desktop: centered status panel and booking details.

## Empty/error states
Invalid queue ID; completed booking; cancelled booking; unavailable waiting-time data; connection loss; cancellation failure. Show clear messages, last-update information where relevant, and retry where appropriate.

## PDF checklist
Large token/position, circular auto-updating countdown, second-in-line banner, full-screen gold called notification, and cancel confirmation are included.

---

# Screen 4: Reception Dashboard

**URL:** `/reception`  
**Users:** Receptionist and Salon Owner  
**Purpose:** Manage the live queue, staff cards, walk-ins and waiting customers.  
**Primary device:** 10-inch tablet, landscape.

## Approved layout
The user chose this order instead of the PDF's side-by-side arrangement:
1. Header and queue status.
2. Small summary cards.
3. Barber/stylist cards.
4. Waiting list.

Keep all PDF functionality.

## Header and summary
Show BEAUTY SALON / Reception Dashboard, queue status, and today's counts for Waiting, In Service, Completed and No-shows.

## Add Walk-in
A prominent **+ Add Walk-in** button opens a popup with:
- Customer name.
- Phone number.
- Service selection (only the four approved services; maximum three).
- Preferred professional, with Any Barber (Fastest) available.
- Add to Queue and Cancel actions.

Walk-ins remain allowed when online joining is closed. Add valid walk-ins to the end of the active queue.

## Team cards
Show male barbers and female hairstylists together. Each card includes photo, name, role, Busy / Free / On Break status, current customer (if any), time remaining (if serving), and **Call Next**.

## Waiting list
Show customers in queue order with token, customer name, selected services, preferred professional, waiting time, and **No-show** / **Cancel** actions. Highlight customers waiting more than 60 minutes in amber.

## Actions
- Add Walk-in opens popup.
- Add to Queue validates and adds the walk-in.
- Call Next calls the next eligible customer for that professional.
- No-show opens confirmation; confirmation marks No-show and updates queue.
- Cancel opens confirmation; confirmation cancels the active entry and updates queue.
- Queue indicator displays current state; Owner Settings controls the online queue switch.

## Responsive behaviour
- Tablet landscape: summary, team cards, then waiting list.
- Desktop: same order with wider cards and more visible queue information.
- Mobile: compact summary, horizontally scrollable team cards, stacked waiting list.

## Empty/error states
Empty waiting list; no staff on duty; no active customer; queue load failure; walk-in validation failure; Call Next failure; duplicate no-show/cancel; connection loss. Show clear messages and do not silently change queue state on failure.

## PDF checklist
Team cards with current customer/time left/Call Next; ordered waiting list with required fields and No-show/Cancel; Add Walk-in form; amber highlight over 60 minutes; tablet landscape support.

---

# Screen 5: Barber View

**URL:** `/barber/:name`  
**Users:** Barbers and hairstylists  
**Purpose:** Manage current and next assigned customers.  
**Primary device:** Mobile phone.

## UI elements
1. BEAUTY SALON header.
2. Professional's photograph and name at the top.
3. Availability indicator.
4. Current customer name, token, services and large digital timer in `HH:MM:SS`.
5. Large **Start** button.
6. **Done** button.
7. “Next for you” with next customer's token, name and service.
8. Available / On Break control.

## Actions
- Start marks the service In Service and starts the timer.
- Done opens a confirmation popup. After confirmation, mark completed, stop timer and update shared queue.
- Availability can change to On Break only after the current customer is completed. Do not interrupt active service.

## Responsive behaviour
- Mobile: vertically stacked cards and large touch-friendly buttons.
- Tablet: wider current/next customer sections.
- Desktop: centered compact workspace.

## Empty/error states
No current customer; no next customer; on break; Start failure; Done failure; duplicate completion; connection loss; expired staff session. Preserve the last valid state on failures and provide clear feedback.

## PDF checklist
Current customer name/services/timer, Start → Done, next customer information and On Break/Available are included.

---

# Screen 6: Waiting Area TV

**URL:** `/display`  
**Users:** Customers waiting inside the salon  
**Purpose:** Display live service progress and upcoming queue tokens.  
**Primary device:** Landscape television.

## Approved layout
1. Salon logo, heading and queue status at the top.
2. Team cards in a row at the top.
3. “Up Next” below, with five compact rows.
4. Thank-you footer.

## Team cards
For each professional show photograph, name, and current token (e.g. `Now: S-12`) and availability/status.

## Up Next
Show the next five queue tokens in compact rows, each with estimated waiting time.

## Newly called notification
The newly called token flashes gold and a chime plays. If TV/browser audio is blocked, retain the visual alert and do not rely on sound alone.

## Actions
Primarily a public display; no queue-management controls. Refresh from shared queue data.

## Responsive behaviour
- TV landscape: large readable team cards and five compact rows.
- Desktop: similar layout with smaller spacing.
- Tablet landscape: compact team row and upcoming list.
- Mobile: stack team cards and upcoming tokens.

## Empty/error states
No active services; no upcoming customers; no professionals on duty; queue closed; connection lost; chime blocked; missing photo. Clearly label unavailable/stale data and show a reconnecting message when needed.

## PDF checklist
Row per professional with photo/name/current token; five upcoming tokens with estimates; newly called token flashes gold with chime.

---

# Screen 7: Owner Settings

**URL:** `/admin`  
**Users:** Salon Owner  
**Purpose:** Manage services, staff duty, online queue availability and today's statistics.  
**Access:** Owner staff PIN login.

## Today's statistics
Display customers served, average waiting time and no-shows, calculated from that day's queue records. Do not hardcode sample statistics.

## Manage services
Show exactly four existing services:
- Haircut
- Hair Styling
- Hair Spa
- Hair Colouring

For each, allow Owner to edit English name, Gujarati name, duration in minutes, price in rupees and Active/Inactive status.

Enforce the approved price range **₹250–₹1,200 per service**. Exact prices and durations remain to be entered. Any values shown in mockups are illustrative, not final decisions. Inactive services must not be available to customers.

## Staff on duty
Show male barbers and female hairstylists together. Owner can toggle each professional On Duty / Off Duty. Off-duty professionals must not receive new assignments. Do not interrupt an active service when changing duty status.

## Queue management
Open / Closed switch for online joining:
- Open: customers may join online.
- Closed: new online bookings are disabled.
- Receptionist walk-ins remain allowed when online joining is closed.

## Save changes
A **Save Changes** button validates and saves edits, then displays a success confirmation. On failure, preserve unsaved edits and allow retry.

## Actions
Edit service fields; toggle service Active/Inactive; toggle staff On Duty/Off Duty; open/close online joining; Save Changes; Logout.

## Responsive behaviour
- Desktop: spacious dashboard.
- Tablet: stacked management cards.
- Mobile: compact cards and touch-friendly controls.

## Empty/error states
No services configured; no staff on duty; zero customers served; zero no-shows; invalid price; invalid duration; missing translation; save failure; queue update failure; staff update failure. Preserve previous saved state on failure and explain the issue.

## PDF checklist
Bilingual service list with minutes/price/on-off; staff-on-duty toggle; online queue Open/Closed; customers served, average wait and no-shows are included.

---

## Final project-wide acceptance checklist

- [ ] All seven screens exist and are navigable.
- [ ] All URLs above work within the Streamlit navigation approach.
- [ ] Customer, Receptionist, Barber/hairstylist and Owner experiences are separated appropriately.
- [ ] Staff PIN login exists for Receptionist, Barber/hairstylist and Owner.
- [ ] English/Gujarati switching works.
- [ ] Approved five-colour palette is consistent.
- [ ] Actual salon business name remains undecided; use BEAUTY SALON as the wordmark.
- [ ] Only four approved services exist.
- [ ] Service price validation enforces ₹250–₹1,200.
- [ ] Owner can configure exact service prices and durations.
- [ ] Customers can select one to three services.
- [ ] Any Barber (Fastest) is selected by default.
- [ ] Queue updates are reflected across customer status, reception, barber and TV screens.
- [ ] Waiting time is calculated from queue data and presented as an estimate.
- [ ] Receptionist can add walk-ins when online joining is closed.
- [ ] Waiting over 60 minutes is highlighted amber.
- [ ] Barber timer uses HH:MM:SS.
- [ ] Barber confirms Done.
- [ ] Barber cannot go on break before completing the current customer.
- [ ] TV shows five upcoming tokens and gold called-token alert with chime where permitted.
- [ ] Owner can edit bilingual service names, durations, prices and active status.
- [ ] Owner can toggle staff duty and online joining.
- [ ] Empty, validation, loading, connection and error states are handled.
- [ ] Do not silently add unsupported features or invent business rules.

## Items intentionally left configurable or undecided

- Actual salon business name.
- Exact price and duration for each service (price must be ₹250–₹1,200).
- Actual staff names, roles, photographs and PINs.
- Actual opening and closing hours.
- Detailed queue calculation and assignment rules, to be documented in `03-flows-rules.md`.
- Persistent storage approach, to be selected during implementation without unnecessary setup burden.

**Implementation instruction:** Treat this document and `docs/01-brief.md` as project requirements. If a detail is undecided, ask the user or leave it configurable; do not invent a final business decision.
