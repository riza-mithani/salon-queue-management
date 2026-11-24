# SALT N' PEPPER -- Salon Queue Management System

**Live demo:** https://salt-n-pepper-salon-202612114.streamlit.app/?page=home
**Hosted on:** Streamlit Community Cloud
**Staff demo PIN:** `2026`

## About

SALT N' PEPPER is a salon queue management web application built with
Python and Streamlit. It helps customers join the salon queue and check
their booking status, while salon staff can manage customers, services
and queue activity through staff screens.

## Features

-   Seven application screens:
    1.  Home
    2.  Join Queue
    3.  My Status
    4.  Reception Dashboard
    5.  Barber View
    6.  Waiting Area TV
    7.  Owner Settings
-   Customer queue registration and booking status.
-   Service selection and staff assignment.
-   Queue management for reception and salon staff.
-   Waiting Area TV view for queue updates.
-   Owner settings for services, staff and online queue status.
-   English and Gujarati language support.
-   PIN protection for Reception Dashboard, Barber View and Owner
    Settings.
-   Responsive layouts for desktop and mobile.
-   Desktop sidebar expands on mouse hover; mobile navigation uses tap.

## Technology Used

-   Python 3.12
-   Streamlit
-   Streamlit Community Cloud for hosting

The main application is maintained in `app.py`.

## Run Locally

1.  Clone this repository:

    ``` bash
    git clone https://github.com/riza-mithani/salon-queue-management.git
    ```

2.  Open the project folder:

    ``` bash
    cd salon-queue-management
    ```

3.  Create and activate a virtual environment (Windows PowerShell):

    ``` powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

4.  Install the dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

5.  Start the application:

    ``` bash
    streamlit run app.py
    ```

6.  Open the local address shown in the terminal, usually
    `http://localhost:8501`.

## Staff Access

The following screens require the shared demo PIN:

-   Reception Dashboard
-   Barber View
-   Owner Settings

**Demo PIN:** `2026`

The Home, Join Queue, My Status and Waiting Area TV screens are publicly
accessible.

## Project Structure

``` text
salon-queue-management/
├── app.py
├── requirements.txt
├── README.md
├── prompts.md
├── .gitignore
└── docs/
    ├── 01-brief.md
    ├── 02-screens.md
    └── 03-flows-rules.md
```

## Notes

This is a demonstration project. The shared staff PIN is intended for
demo access and should not be treated as production-grade
authentication.
