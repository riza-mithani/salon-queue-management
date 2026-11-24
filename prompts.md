# Antigravity Prompt Log – SALT N' PEPPER

This file contains the prompts I used while developing my Salon Queue Management System.

## 1. Project Documentation

### Prompt 1 – Create Project Documents

We have completed the first two project documents:

- docs/01-brief.md
- docs/02-screens.md

Read both documents completely. Also read Salon_Queue_Management_Vibe_Coding_Guide.pdf, especially its instructions for the remaining project documents.

Our approved technology is Streamlit with Python 3.12, using one main Python file for the application.

Your tasks:

1. Review both documents and identify any missing or conflicting requirements.
2. Prepare docs/03-flows-rules.md covering:
   - Customer queue joining
   - Service selection and pricing
   - Barber assignment
   - Queue position and waiting-time calculation
   - Start and Done service workflow
   - No-show and cancellation
   - Walk-in registration
   - Online queue open/closed behaviour
   - Staff availability and breaks
   - Customer notifications and TV updates
   - Important edge cases and testing checklist

3. Prepare AGENTS.md in the project root with:
   - Streamlit and Python 3.12 requirements
   - One-main-Python-file architecture
   - Approved colour palette
   - English and Gujarati support
   - Beginner-friendly coding instructions
   - Instructions to read docs before coding
   - Do not invent missing business decisions

IMPORTANT:
- Do not start coding yet.
- Do not change 01-brief.md or 02-screens.md.
- Do not add new services or screens.
- Do not invent service prices, durations, salon name or staff details.
- If any business rule is unclear, list it under Open Questions.

After creating the two documents, explain what you created and show me the project folder structure. Wait for my approval before coding.

## 2. Initial Application Development

### Prompt 2 – Create Initial App Foundation

We have accepted the following project documents:

- docs/01-brief.md
- docs/02-screens.md
- docs/03-flows-rules.md
- AGENTS.md

Now begin Phase 4: Application Development.

Before coding:
1. Read all four documents.
2. Check the existing project structure and Python virtual environment.
3. Verify Streamlit is installed.

Development requirements:
- Use Python 3.12 and Streamlit.
- Keep the application in one main file: app.py.
- Follow the approved five-colour palette.
- Support English and Gujarati.
- Follow all seven approved screen designs.
- Use beginner-friendly, readable Python.
- Do not invent business details.
- Do not add unapproved features.

Start with Step 1 only:
Create the initial app.py foundation with:
- Streamlit page configuration.
- Approved colour theme and basic styling.
- BEAUTY SALON wordmark.
- English/Gujarati language selector.
- Navigation structure for all seven screens.
- Basic placeholder content for each screen.

Do not implement the complete queue logic yet.

After finishing:
- Run the application.
- Fix any startup errors.
- Show me how to open it in my browser.
- Explain what files you created or changed.
- Wait for my approval before implementing the next feature.

### Prompt 3 – Improve Home Screen Design

We have reviewed the first version of app.py in the browser.

The application works, and English/Gujarati switching works. However, the visual design needs significant improvement.

I want you to redesign the visual foundation and Home screen before implementing application functionality.

IMPORTANT: Read docs/01-brief.md and docs/02-screens.md again. Follow the approved designs.

DESIGN REQUIREMENTS:

1. Overall appearance
- Create a premium, elegant beauty salon website.
- Do not make it look like a generic Streamlit dashboard.
- Use spacious layouts, elegant typography and professional photographs.
- Use serif typography for BEAUTY SALON and major headings.
- Use clean, readable typography for other content.

2. Approved colour palette
- Cream: #FFFDD0
- Orange-red: #E43D12
- Rose pink: #D6536D
- Light pink: #FFA2B6
- Golden yellow: #EFB11D

Use these colours in a balanced way. Avoid making the entire page beige.

3. Header
- BEAUTY SALON wordmark.
- Navigation: Home, About, Services, Join Queue.
- English/Gujarati selector.
- Clean, minimal header.

4. Hero section
- Split layout.
- Text on the left.
- Large, high-quality female beauty/hair styling photograph on the right.
- Elegant heading and short introduction.
- Small live queue card beside the hero content.
- Prominent gold Join Queue button.
- Salon Open/Closed status.

5. Services
- Four individual photographic cards:
  Haircut
  Hair Styling
  Hair Spa
  Hair Colouring
- Do not use emoji illustrations.
- Use consistent rectangular photographs.

6. Team
- Rectangular profile cards.
- Include male barbers and female hairstylists.
- Show photograph, name, role and availability.

7. About section
- Short introduction with an attractive salon photograph.

8. Remove unnecessary elements
- Remove the visible Palette Check box from the customer-facing interface.
- Remove decorative emojis used as substitutes for photographs.
- Do not display developer/debug information to customers.

TECHNICAL REQUIREMENTS:
- Continue using Python 3.12 and Streamlit.
- Keep the main application in app.py.
- Preserve all seven existing screen navigation options.
- Preserve working English/Gujarati switching.
- Do not implement queue functionality yet.
- Do not change the approved requirements or business rules.
- You may create an assets folder for image files if needed.

FIRST TASK:
Redesign the Home screen and shared visual styling only.

Run the application and show me the updated Home screen.

Do not proceed to Join Queue or other screen implementation until I review and approve the new Home screen.

## 3. Join Queue Development

### Prompt 4 – Implement Screen 2

We are now implementing Screen 2 — Join Queue.

Before making changes, read:
- docs/01-brief.md
- docs/02-screens.md
- docs/03-flows-rules.md
- AGENTS.md

Also inspect the existing app.py and preserve the working Home screen.

IMPORTANT APPROVED DESIGN DECISION:
Customers must select their services FIRST and choose their barber/hairstylist SECOND.

## 1. Customer details

Create a clean form containing:
- Full Name (required)
- Phone Number (required, exactly 10 digits)

Show clear validation messages.

## 2. Service selection

Show exactly four services using individual professional photographs:

1. Haircut
2. Hair Styling
3. Hair Spa
4. Hair Colouring

Requirements:
- Attractive rectangular image cards.
- Display service name, price and duration.
- Allow customers to select multiple services.
- Minimum selection: 1.
- Maximum selection: 3.
- Clearly highlight selected cards.
- Allow customers to deselect services.

IMPORTANT:
Read service prices and durations from the project's configured data. Do not invent final prices or durations. The approved price range is ₹250–₹1,200 per service.

## 3. Barber and hairstylist selection

This section must appear AFTER service selection.

Show:
- Any Barber (Fastest) as the default selection.
- Available male barbers.
- Available female hairstylists.

Each professional card should contain:
- Individual photograph.
- Name.
- Role.
- Availability.

Only available professionals can be selected.

## 4. Booking summary

Update the summary whenever the customer changes a selection.

Display:
- Customer name.
- Phone number.
- Selected services.
- Total price.
- Total service duration.
- Selected barber/hairstylist.
- Estimated waiting time, where queue data is available.

## 5. Confirm & Join Queue

Create a prominent confirmation button.

On submission:
- Validate all required fields.
- Validate service selections.
- Validate professional availability.
- Follow the queue creation rules in docs/03-flows-rules.md.
- Create a unique queue token.
- Navigate to Screen 3 — My Status.

Do not create duplicate queue entries if the button is pressed more than once.

## 6. Design

- Follow the existing approved salon design direction.
- Keep the current colour palette for now.
- Use professional service and staff photographs, not emojis.
- Maintain the premium, spacious appearance.
- Ensure mobile, tablet and desktop responsiveness.
- Keep English and Gujarati translations working.

## 7. Technical requirements

- Python 3.12 and Streamlit.
- Keep the application in app.py.
- Reuse existing application structure and shared data.
- Do not break the Home screen.
- Do not implement other screens in this task.
- Do not add unapproved services or features.

## 8. Testing

Test:
- Empty name.
- Invalid phone number.
- No service selected.
- Four services selected.
- Barber unavailable.
- Online queue closed.
- Successful queue registration.
- Duplicate submission prevention.
- English/Gujarati switching.

After implementation:
1. Run the application.
2. Fix errors.
3. Show me the completed Join Queue screen.
4. Explain what you implemented.
5. Wait for my review and approval before proceeding to Screen 3.

Do not modify the approved project documents.

### Prompt 5 – Debug Join Queue Screen

Screen 2 — Join Queue needs debugging and corrections. Do not proceed to Screen 3.

I tested the page in the browser and found several problems.

First, inspect the existing app.py and identify the actual causes. Do not simply change the appearance.

#### 1. Fix all service photographs
- All four service photographs must appear immediately when the Join Queue page opens.
- Photographs must remain visible whether a service is selected or not.
- Fix the Haircut card, which currently displays raw HTML code instead of its photograph.
- Use Streamlit's proper image-rendering method.
- Ensure image paths and assets work after application reruns.
- Do not display HTML or Python code inside service cards.

#### 2. Fix staff information
- Inspect the staff data and correct the male barber/female hairstylist role assignments.
- A male barber must not be displayed with the name Pooja.
- Do not invent actual staff names or personal details. Use neutral placeholders until confirmed staff information is available.
- Show the correct photograph, name, role and availability on each card.

#### 3. Fix ALL buttons and interactions
Test every interactive element:
- Service selection and deselection.
- Maximum three selected services.
- Barber/hairstylist selection.
- Any Barber (Fastest) default selection.
- Name and phone inputs.
- Confirm & Join Queue.
- Back/Home navigation.
- English/Gujarati selector.

Make sure Streamlit reruns do not unexpectedly reset selections or form values.

#### 4. Fix the booking summary
- Update the summary immediately when selections change.
- Correctly calculate total price and duration.
- Display the selected professional.
- Keep the approved ₹250–₹1,200 inclusive price range per service.
- Ensure the estimated waiting time is based on queue data, not a fixed number.

#### 5. Check the entire page
- Ensure all sections are visible and properly aligned.
- Improve spacing between service cards.
- Make photographs consistent in size and aspect ratio.
- Ensure buttons have clear hover and selected states.
- Preserve the existing approved visual theme.

#### 6. Test the complete workflow

Perform these tests:

1. Open Join Queue with no selections.
2. Verify all four photographs appear.
3. Select Haircut.
4. Deselect Haircut.
5. Select three different services.
6. Try selecting a fourth service.
7. Select Any Barber (Fastest).
8. Select an individual available professional.
9. Change the language to Gujarati.
10. Enter valid customer details.
11. Submit a booking.
12. Verify that a unique token is generated.
13. Verify duplicate submission is prevented.

Do not modify the Home screen or approved project documents.

After fixing everything:
- Run the application.
- Report which bugs were fixed.
- Report which tests passed and failed.
- Show me the updated Join Queue screen.

Do not implement Screen 3 until I explicitly approve Screen 2.

### Prompt 6 – Fix Home and Join Queue

Fix the existing Home and Join Queue screens in app.py. Do not rebuild the application.
1. Use consistent, professional salon photographs across both screens. Keep image sizes, aspect ratios and visual styles consistent.
2. Fix the service cards. Use a clean, properly aligned 2-column grid with equal-sized cards.
3. Fix Confirm & Join Queue. Validate customer details and selections, create a queue token and navigate to My Status.
4. Fix spacing, alignment and excessive blank space.
5. Make sure images load immediately, not only after selection.
Do not change project documents. Do not add features. Do not redesign unrelated screens.
Test the buttons and booking workflow yourself. Run the app and fix errors before reporting completion.
Keep changes minimal. Prioritise working functionality over decorative design.

### Prompt 7 – Fix Staff Card Layout

Fix only the staff card layout on the Join Queue page. Display all four cards in one evenly spaced row with equal widths and heights. Keep photographs consistent in size, align names, roles, availability and buttons. Make it responsive. Do not change anything else.

## 4. Navigation and Bug Fixes

### Prompt 8 – Fix Navigation Error

Fix the navigation error in app.py.

These three buttons must work:
1. Back to Home (Join Queue page).
2. Confirm & Join Queue (navigate to My Status after successful booking).
3. Join Live Queue (Home page).

Fix the StreamlitWidgetAlreadyInstantiatedError in navigate_to(). Do not modify screen_nav_radio after its widget is created. Use a proper Streamlit callback or safe navigation state handling.

Test all three buttons. Ensure no error appears.

Do not change layouts, colours, images or other functionality.

### Prompt 9 – Fix Navigation Bug Only

Fix only the navigation bug in `app.py`. Inspect `navigate_to()` and the three button callbacks. Correct the Streamlit session-state error without changing any other code. Test the three navigation buttons.

## 5. Remaining Screen Development

### Prompt 10 – Implement Screen 3: My Status

Implement Screen 3 — My Status in `app.py` according to `docs/02-screens.md`.

Include:

- Customer name and queue token.
- Selected services, total price and assigned barber/hairstylist.
- Current queue position and estimated waiting time.
- Large circular countdown timer.
- Live booking status.
- Cancel Booking button with confirmation popup.
- Show the "It's your turn!" alert when the customer is called.

Connect it to the existing booking data from Screen 2.

Preserve the existing design, navigation and English/Gujarati switching. Do not modify other screens.

Test the screen and show me the result.

Follow the testing checklist in `docs/03-flows-rules.md`.

Keep the required queue testing actions: Call Next, Start/Done, No-show and Cancel. Allow manual testing of queue scenarios.

Keep these testing controls separate from the customer-facing screens. Do not add features beyond the PDF requirements or modify existing screen designs.

### Prompt 11 – Implement Screen 4: Reception Dashboard

Implement Screen 4 — Reception Dashboard in `app.py` according to `docs/02-screens.md`.

Include:
- Summary cards at the top.
- Barber cards below with status, current customer and Call Next button.
- Waiting list with token, customer, services, preferred barber and waiting time.
- Add Walk-in popup.
- No-show and Cancel confirmation popups.
- Highlight customers waiting over 60 minutes.

Connect everything to the existing queue data.

Preserve the design, navigation and English/Gujarati switching. Do not modify other screens.

Run a basic compile check and show me the result.

### Prompt 12 – Implement Screen 5: Barber View

Implement Screen 5 — Barber View in `app.py` according to `docs/02-screens.md` and the original PDF.

Include:
- Barber photo, name and current customer details.
- Customer's selected services.
- Timer showing service time.
- Start and Done buttons.
- Next customer preview.
- On Break / Available toggle.

Connect it to the existing queue data so updates reflect on the Reception Dashboard.

Preserve the existing design, navigation and English/Gujarati switching. Do not modify other screens.

Run a basic compile check and show me the result.

### Prompt 13 – Fix Staff Availability Bug

Fix the bug triggered when clicking "Set Available" for Stylist 2 in Screen 5 — Barber View. The action must update availability without breaking the app or blanking the Home page. Check the related callback and session state. Preserve all existing screens, designs and queue data. Do not make unrelated changes.

### Prompt 14 – Implement Screen 6: Waiting Area TV

Implement Screen 6 — Waiting Area TV in `app.py` according to `docs/02-screens.md` and the original PDF.

Include:
- Barber cards with photo, name and current customer token.
- Up Next list showing the next 5 queue tokens and estimated times.
- Highlight newly called tokens with a gold flashing effect and chime.

Connect it to the existing queue data so updates reflect automatically.

Preserve the existing design, navigation and English/Gujarati switching. Do not modify other screens.

Run a basic compile check and show me the result.

### Prompt 15 – Implement Screen 7: Owner Settings

Implement Screen 7 — Owner Settings in `app.py` according to `docs/02-screens.md` and the original PDF.

Include:
- Manage services: English/Gujarati names, price, duration and active status.
- Manage barbers/hairstylists and their duty status.
- Open/Close online queue toggle.
- Today's statistics: customers served, average waiting time and no-shows.
- Save button with confirmation.

Connect settings to the existing app data.

Preserve the existing design, navigation and language switching. Do not modify other screens.

Run a basic compile check and show me the result.

## 6. Final Visual Improvements

### Prompt 16 – Apply Approved Colour Palette

Apply the following colour palette consistently across all 7 screens in `app.py`.

**Colours:**
- Main background: Creamy Ivory `#FFF4D6`
- Cards and sections: Warm Cream `#FFFAEA`
- Headings and text: Espresso Brown `#30251F`
- Primary buttons: Bright Terracotta `#D9684F`
- Secondary accents: Soft Dusty Rose `#E39A9E`
- Queue tokens and alerts: Champagne Gold `#E6B957`
- Available and success status: Fresh Sage `#879B78`

**Important instructions:**
1. Change colours and shades only.
2. Do NOT modify layouts, spacing, dimensions, fonts, images or card arrangements.
3. Do NOT change button labels, actions or functionality.
4. Do NOT modify backend logic, queue data, navigation or session state.
5. Keep all 7 screens and English/Gujarati support working.
6. Replace the displayed salon name "BEAUTY SALON" with "SALt N' PEPPER" wherever it appears. Do not change the layout.
7. Preserve all existing functionality.

After applying changes, run a compile check and verify all 7 screens.

### Prompt 17 – Fix Visual Alignment

Fix the visual alignment of these three screens only:

**Home:**
- Replace the headline with "Sculpting Styles, Reflecting Individuality."
- Fix