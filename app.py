"""
Salon Queue Management System
=============================
Main application entry point adhering to single-file architecture.

Tech Stack: Streamlit (Python 3.12)
Approved Colour Palette:
  - Main Background:            #FFF4D6 (Creamy Ivory)
  - Cards & Sections:           #FFFAEA (Warm Cream)
  - Headings & Text:            #30251F (Espresso Brown)
  - Primary Buttons:            #D9684F (Bright Terracotta)
  - Secondary Accents:          #E39A9E (Soft Dusty Rose)
  - Queue Tokens & Alerts:      #E6B957 (Champagne Gold)
  - Available & Success Status: #879B78 (Fresh Sage)

Screens:
  1. Home (/)
  2. Join Queue (/join)
  3. My Status (/status/:id)
  4. Reception Dashboard (/reception)
  5. Barber View (/barber/:name)
  6. Waiting Area TV (/display)
  7. Owner Settings (/admin)
"""

import base64
import math
import re
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. PAGE CONFIGURATION & STYLING
# ==============================================================================

st.set_page_config(
    page_title="SALt N' PEPPER — Luxury Queue Experience",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def get_image_base64(image_path: str) -> str:
    """Helper to load local image file as Base64 URI for crisp HTML embeds."""
    path = Path(image_path)
    if path.exists():
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = path.suffix.lower().replace(".", "")
            mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
            return f"data:image/{mime};base64,{encoded}"
    return ""


SALON_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --cream: #FFFAEA;
        --main-bg: #FFF4D6;
        --orange-red: #D9684F;
        --golden-yellow: #E6B957;
        --rose-pink: #E39A9E;
        --light-pink: #F4C8CB;
        --charcoal-dark: #30251F;
        --charcoal-muted: #64554B;
        --sage-green: #879B78;
        --pure-white: #FFFAEA;
        --card-border: rgba(227, 154, 158, 0.35);
    }

    .stApp {
        background: #FFF4D6 !important;
        color: var(--charcoal-dark);
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Container cards default to Warm Cream #FFFAEA and soft dusty rose border */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #FFFAEA !important;
        border-color: var(--card-border) !important;
    }

    .salon-wordmark {
        font-family: 'Playfair Display', Georgia, serif;
        font-weight: 700;
        letter-spacing: 3px;
        color: var(--orange-red);
        text-transform: uppercase;
        margin: 0;
        line-height: 1.1;
    }

    .salon-heading-serif {
        font-family: 'Playfair Display', Georgia, serif;
        font-weight: 700;
        color: var(--charcoal-dark);
        letter-spacing: -0.5px;
        line-height: 1.25;
    }

    .section-eyebrow {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--rose-pink);
        margin-bottom: 0.35rem;
        display: block;
    }

    .nav-link-item {
        color: var(--charcoal-dark);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: color 0.2s ease;
    }

    .nav-link-item:hover {
        color: var(--orange-red);
    }

    /* Buttons */
    .btn-gold-cta > button {
        background: linear-gradient(135deg, #D9684F 0%, #C2543C 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.5px !important;
        padding: 0.75rem 2rem !important;
        border-radius: 35px !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(217, 104, 79, 0.35) !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
    }

    .btn-gold-cta > button:hover {
        background: linear-gradient(135deg, #E0775F 0%, #D9684F 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 24px rgba(217, 104, 79, 0.45) !important;
        color: #FFFFFF !important;
    }

    .stButton > button {
        background-color: var(--orange-red) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #C2543C !important;
        box-shadow: 0 4px 14px rgba(217, 104, 79, 0.28) !important;
        transform: translateY(-1px) !important;
    }

    .hero-queue-card {
        background: #FFFAEA;
        border: 1px solid var(--card-border);
        border-left: 4px solid var(--golden-yellow);
        border-radius: 12px;
        padding: 0.85rem 1.15rem;
        margin: 1.25rem 0;
        display: flex;
        align-items: center;
        gap: 1.15rem;
    }

    /* Badges */
    .badge-status-open {
        background-color: rgba(135, 155, 120, 0.18);
        color: #4F6340;
        padding: 0.3rem 0.85rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .badge-status-closed {
        background-color: rgba(217, 104, 79, 0.12);
        color: var(--orange-red);
        padding: 0.3rem 0.85rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .badge-avail-free {
        background-color: rgba(135, 155, 120, 0.18);
        color: #4F6340;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 12px;
        display: inline-block;
    }

    .badge-avail-busy {
        background-color: rgba(217, 104, 79, 0.12);
        color: var(--orange-red);
        font-weight: 600;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 12px;
        display: inline-block;
    }

    .badge-avail-break {
        background-color: rgba(230, 185, 87, 0.22);
        color: #7D5B15;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 12px;
        display: inline-block;
    }

    .badge-selected-pill {
        background-color: var(--golden-yellow);
        color: #30251F;
        font-weight: 700;
        font-size: 0.8rem;
        padding: 4px 12px;
        border-radius: 12px;
        display: inline-block;
    }

    .screen-banner {
        border-left: 4px solid var(--orange-red);
        padding-left: 0.85rem;
        margin-bottom: 1.25rem;
    }

    .summary-card {
        background: #FFFAEA;
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 4px 16px rgba(48, 37, 31, 0.05);
    }

    /* Screen 3: My Status Luxury Styling */
    .gold-called-banner {
        background: linear-gradient(135deg, #E6B957 0%, #D8A944 50%, #C99831 100%);
        color: #30251F;
        border-radius: 20px;
        padding: 2.2rem 2rem;
        text-align: center;
        margin: 0.8rem 0 2rem 0;
        box-shadow: 0 12px 35px rgba(230, 185, 87, 0.5);
        border: 3px solid #FFFAEA;
        animation: pulseGold 2.2s infinite ease-in-out;
    }

    @keyframes pulseGold {
        0% { box-shadow: 0 0 15px rgba(230, 185, 87, 0.35); transform: scale(1); }
        50% { box-shadow: 0 0 35px rgba(230, 185, 87, 0.7); transform: scale(1.008); }
        100% { box-shadow: 0 0 15px rgba(230, 185, 87, 0.35); transform: scale(1); }
    }

    .proximity-alert-banner {
        background: linear-gradient(135deg, rgba(230, 185, 87, 0.2) 0%, rgba(255, 250, 234, 0.85) 100%);
        border: 2px solid var(--golden-yellow);
        border-left: 6px solid var(--golden-yellow);
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1.15rem;
    }

    .circular-countdown {
        width: 175px;
        height: 175px;
        border-radius: 50%;
        border: 7px solid var(--golden-yellow);
        background: radial-gradient(circle, #FFFAEA 65%, #FFF4D6 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 1.5rem auto;
        box-shadow: 0 8px 25px rgba(230, 185, 87, 0.25);
    }

    .detail-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 0;
        border-bottom: 1px solid rgba(227, 154, 158, 0.25);
        font-size: 0.92rem;
    }
    .detail-row:last-child {
        border-bottom: none;
    }
    .detail-label {
        color: var(--charcoal-muted);
        font-weight: 500;
    }
    .detail-value {
        color: var(--charcoal-dark);
        font-weight: 700;
        text-align: right;
    }

    /* Screen 4: Reception Dashboard Luxury Styling */
    .reception-summary-box, .reception-summary-card {
        background: #FFFAEA;
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 1.1rem 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(48, 37, 31, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .reception-summary-box:hover, .reception-summary-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(48, 37, 31, 0.08);
    }
    .reception-summary-val {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--orange-red);
        line-height: 1;
        margin: 0.2rem 0;
    }
    .reception-summary-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: var(--charcoal-muted);
        font-weight: 700;
    }

    .waiting-card-row {
        background: #FFFAEA;
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 8px rgba(48, 37, 31, 0.03);
    }
    .waiting-card-amber {
        background: linear-gradient(135deg, rgba(230, 185, 87, 0.2) 0%, rgba(255, 250, 234, 0.7) 100%) !important;
        border: 2px solid var(--golden-yellow) !important;
        border-left: 6px solid var(--golden-yellow) !important;
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 14px rgba(230, 185, 87, 0.22) !important;
    }

    /* Screen 5: Barber View Styles */
    .digital-timer-box {
        background: var(--charcoal-dark);
        border: 2px solid var(--golden-yellow);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(48, 37, 31, 0.25);
        margin: 1rem 0 1.25rem 0;
    }
    .digital-timer-value {
        font-family: 'Courier New', Courier, monospace;
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--golden-yellow);
        letter-spacing: 4px;
        line-height: 1;
        text-shadow: 0 0 12px rgba(230, 185, 87, 0.45);
    }
    .digital-timer-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--cream);
        margin-top: 0.5rem;
        font-weight: 600;
    }
    .barber-hero-card {
        background: #FFFAEA;
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 4px 16px rgba(48, 37, 31, 0.05);
        margin-bottom: 1.25rem;
    }
    .barber-customer-card {
        background: #FFFAEA;
        border: 2px solid var(--rose-pink);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 6px 20px rgba(227, 154, 158, 0.12);
        margin-bottom: 1.25rem;
    }
    .next-preview-card {
        background: linear-gradient(135deg, rgba(227, 154, 158, 0.15) 0%, rgba(255, 250, 234, 0.6) 100%);
        border: 1px dashed var(--rose-pink);
        border-radius: 14px;
        padding: 1.2rem;
        margin-top: 1rem;
    }

    /* Screen 6: Waiting Area TV Styles */
    @keyframes goldPulse {
        0% {
            background-color: #E6B957;
            box-shadow: 0 0 0 0 rgba(230, 185, 87, 0.7);
            transform: scale(1);
        }
        50% {
            background-color: #FFF4D6;
            box-shadow: 0 0 25px 10px rgba(230, 185, 87, 0.6);
            transform: scale(1.02);
        }
        100% {
            background-color: #E6B957;
            box-shadow: 0 0 0 0 rgba(230, 185, 87, 0);
            transform: scale(1);
        }
    }

    .tv-called-banner {
        animation: goldPulse 1.8s infinite ease-in-out;
        border: 3px solid #D9684F !important;
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
        background: var(--golden-yellow);
    }

    .tv-station-card {
        background: #FFFAEA;
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 1.1rem;
        box-shadow: 0 4px 14px rgba(48, 37, 31, 0.05);
        text-align: center;
        transition: transform 0.2s ease;
    }

    .tv-token-now {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--orange-red);
        background: rgba(217, 104, 79, 0.1);
        border: 1px solid var(--orange-red);
        border-radius: 8px;
        padding: 0.25rem 0.55rem;
        margin-top: 0.4rem;
        display: inline-block;
    }

    .tv-upnext-row {
        background: #FFFAEA;
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 0.85rem 1.25rem;
        margin-bottom: 0.6rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(48, 37, 31, 0.03);
    }

    .tv-upnext-token {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--charcoal-dark);
        background: var(--cream);
        border: 1px solid var(--golden-yellow);
        border-radius: 8px;
        padding: 0.2rem 0.7rem;
    }

    /* Staff Cards - Home Page Grid (Equal widths, equal heights, aligned contents) */
    [data-testid="stColumn"] div.stVerticalBlock:has(.home-staff-content) {
        background: #FFFAEA !important;
        border: 1px solid rgba(227, 154, 158, 0.35) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        height: 330px !important;
        min-height: 330px !important;
        max-height: 330px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-shadow: 0 4px 14px rgba(48, 37, 31, 0.04) !important;
        box-sizing: border-box !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    [data-testid="stColumn"] div.stVerticalBlock:has(.home-staff-content):hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(227, 154, 158, 0.22) !important;
    }

    .home-staff-content {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .home-staff-content .home-staff-img-frame {
        width: 100%;
        height: 190px;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 8px;
        background: #FFF4D6;
    }

    .home-staff-content .home-staff-img-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center top;
        display: block;
    }

    .home-staff-content .home-staff-name {
        text-align: center;
        font-weight: 700;
        font-size: 1.05rem;
        color: var(--charcoal-dark);
        height: 24px;
        line-height: 24px;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .home-staff-content .home-staff-role {
        text-align: center;
        color: var(--rose-pink);
        font-size: 0.82rem;
        font-weight: 600;
        height: 34px;
        line-height: 1.25;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 6px;
        overflow: hidden;
    }

    .home-staff-content .home-staff-status {
        text-align: center;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Staff Cards - Join Queue Grid (Equal widths, equal heights, aligned buttons) */
    [data-testid="stColumn"] div.stVerticalBlock:has(.join-staff-content) {
        background: #FFFAEA !important;
        border: 1px solid rgba(227, 154, 158, 0.35) !important;
        border-radius: 12px !important;
        padding: 8px !important;
        height: 295px !important;
        min-height: 295px !important;
        max-height: 295px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-shadow: 0 2px 8px rgba(48, 37, 31, 0.04) !important;
        box-sizing: border-box !important;
    }

    [data-testid="stColumn"] div.stVerticalBlock:has(.join-staff-content.is-selected) {
        border: 2px solid var(--golden-yellow) !important;
        background: rgba(230, 185, 87, 0.12) !important;
        box-shadow: 0 4px 14px rgba(230, 185, 87, 0.22) !important;
    }

    /* Staff Cards - Waiting Area TV (Equal widths, equal heights, aligned contents) */
    [data-testid="stColumn"] div.stVerticalBlock:has(.tv-station-card-inner) {
        background: #FFFAEA !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 14px !important;
        padding: 12px !important;
        height: 330px !important;
        min-height: 330px !important;
        max-height: 330px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-sizing: border-box !important;
        box-shadow: 0 4px 14px rgba(48, 37, 31, 0.04) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .tv-station-card-inner {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .tv-station-img-frame {
        width: 100%;
        height: 155px;
        border-radius: 10px;
        overflow: hidden;
        background: #FFF4D6;
        margin-bottom: 8px;
    }

    .tv-station-img-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center top;
        display: block;
    }

    .tv-station-name {
        text-align: center;
        font-weight: 700;
        font-size: 1.05rem;
        height: 24px;
        line-height: 24px;
        margin-bottom: 2px;
        color: var(--charcoal-dark);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .tv-station-role {
        text-align: center;
        color: var(--rose-pink);
        font-size: 0.8rem;
        font-weight: 600;
        height: 24px;
        line-height: 24px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .tv-station-status-box {
        height: 54px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        box-sizing: border-box;
    }

    .join-staff-content {
        width: 100%;
    }

    .join-staff-content .join-staff-img-frame {
        width: 100%;
        height: 125px;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 6px;
        background: #FFF4D6;
    }

    .join-staff-content .join-staff-img-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center top;
        display: block;
    }

    .join-staff-content .join-staff-name {
        text-align: center;
        font-weight: 700;
        font-size: 0.92rem;
        color: var(--charcoal-dark);
        height: 22px;
        line-height: 22px;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .join-staff-content .join-staff-role {
        text-align: center;
        color: var(--rose-pink);
        font-size: 0.76rem;
        font-weight: 600;
        height: 32px;
        line-height: 1.2;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 4px;
        overflow: hidden;
    }

    .join-staff-content .join-staff-status {
        text-align: center;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 4px;
    }

    /* Target all Join Staff action buttons directly via st-key */
    div[class*="st-key-btn_staff"] .stButton {
        width: 100% !important;
        margin-top: auto !important;
    }

    div[class*="st-key-btn_staff"] button {
        height: 32px !important;
        min-height: 32px !important;
        max-height: 32px !important;
        padding: 2px 4px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        width: 100% !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    div[class*="st-key-btn_staff"] button p,
    div[class*="st-key-btn_staff"] button div,
    div[class*="st-key-btn_staff"] button span {
        font-size: 0.75rem !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow-wrap: normal !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Unavailable / Disabled staff buttons */
    div[class*="st-key-btn_staff_disabled"] button,
    div[class*="st-key-btn_staff"] button:disabled {
        background-color: #EFECE6 !important;
        color: #7A7269 !important;
        border: 1px solid #DCD6CA !important;
        cursor: not-allowed !important;
        opacity: 1 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    div[class*="st-key-btn_staff_disabled"] button p,
    div[class*="st-key-btn_staff"] button:disabled p {
        color: #7A7269 !important;
    }

    /* Selected staff button (golden yellow highlight) */
    div[class*="st-key-btn_staff_sel"] button {
        background-color: var(--golden-yellow) !important;
        color: #30251F !important;
        border: 1px solid #CCA03D !important;
        font-weight: 700 !important;
        cursor: default !important;
        opacity: 1 !important;
        box-shadow: 0 2px 8px rgba(230, 185, 87, 0.25) !important;
    }

    div[class*="st-key-btn_staff_sel"] button p {
        color: #30251F !important;
        font-weight: 700 !important;
    }

    /* Staff PIN Authentication Card */
    [data-testid="stColumn"] div.stVerticalBlock:has(.pin-card-wrapper) {
        background: #FFFAEA !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 20px !important;
        padding: 2.25rem 2rem 1.85rem 2rem !important;
        box-shadow: 0 16px 40px rgba(48, 37, 31, 0.08) !important;
        box-sizing: border-box !important;
        text-align: center !important;
        margin-top: 1.5rem !important;
        margin-bottom: 2rem !important;
    }

    .pin-card-wrapper {
        width: 100%;
        text-align: center;
    }

    .pin-card-header .salon-wordmark {
        font-size: 1.65rem;
        color: #30251F;
        margin-bottom: 0.35rem;
    }

    .pin-access-badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #D9684F;
        background: rgba(217, 104, 79, 0.08);
        border: 1px solid rgba(217, 104, 79, 0.25);
        border-radius: 20px;
        padding: 0.22rem 0.8rem;
        margin-bottom: 0.75rem;
    }

    .pin-main-heading {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: #30251F;
        margin: 0 0 0.35rem 0;
        line-height: 1.2;
    }

    .pin-instruction-text {
        font-size: 0.95rem;
        color: var(--charcoal-muted);
        line-height: 1.5;
        margin: 0 0 1.25rem 0;
    }

    .pin-error-box {
        background: rgba(217, 104, 79, 0.1);
        border: 1px solid #D9684F;
        border-radius: 10px;
        padding: 0.65rem 0.85rem;
        margin-bottom: 1rem;
        color: #C2543C;
        font-size: 0.88rem;
        font-weight: 600;
        text-align: center;
        line-height: 1.4;
    }

    div[data-testid="stTextInput"]:has(input[type="password"]) input {
        text-align: center !important;
        font-size: 1.5rem !important;
        letter-spacing: 8px !important;
        font-weight: 700 !important;
        color: #30251F !important;
        background: #FFF4D6 !important;
        border: 1.5px solid rgba(217, 104, 79, 0.35) !important;
        border-radius: 12px !important;
        height: 52px !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stTextInput"]:has(input[type="password"]) input:focus {
        border-color: #D9684F !important;
        box-shadow: 0 0 0 3px rgba(217, 104, 79, 0.2) !important;
    }

    /* Back to Home subtle button on PIN screen */
    div[class*="st-key-pin_back_home_btn"] button {
        background: transparent !important;
        color: var(--charcoal-muted) !important;
        border: 1px solid var(--card-border) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border-radius: 10px !important;
        margin-top: 0.5rem !important;
        height: 38px !important;
    }

    div[class*="st-key-pin_back_home_btn"] button:hover {
        background: #FFF4D6 !important;
        color: var(--charcoal-dark) !important;
        border-color: var(--rose-pink) !important;
    }

    /* Desktop Sidebar Smooth Hover Expand/Collapse Animation */
    @media (min-width: 769px) and (hover: hover) and (pointer: fine) {
        section[data-testid="stSidebar"] {
            transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                        width 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                        box-shadow 0.32s ease !important;
            box-shadow: 4px 0 28px rgba(48, 37, 31, 0.12) !important;
        }

        button[data-testid="stExpandSidebarButton"],
        button[aria-label="Expand sidebar"] {
            transition: all 0.25s ease !important;
            border-radius: 8px !important;
        }

        button[data-testid="stExpandSidebarButton"]:hover,
        button[aria-label="Expand sidebar"]:hover {
            background-color: rgba(217, 104, 79, 0.12) !important;
            color: var(--orange-red) !important;
            transform: scale(1.08) !important;
        }
    }

    /* ==========================================================================
       COMPREHENSIVE MOBILE RESPONSIVE SUITE (375px, 390px, 430px & viewports <= 768px)
       ========================================================================== */
    @media screen and (max-width: 768px) {
        /* 1. Viewport & Body Sizing - Prevent Horizontal Scrolling */
        html, body {
            overflow-x: hidden !important;
            max-width: 100vw !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }

        .main .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 0.75rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 100vw !important;
            width: 100% !important;
            box-sizing: border-box !important;
            overflow-x: hidden !important;
        }

        /* 2. Fluid Layout & Universal Multi-Column Vertical Stacking */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
            width: 100% !important;
            max-width: 100% !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 0.35rem !important;
            box-sizing: border-box !important;
        }

        /* 3. Cards & Container Boundaries */
        div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stVerticalBlock"] {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
        }

        .summary-card,
        .barber-hero-card,
        .barber-customer-card,
        .reception-summary-box,
        .reception-summary-card,
        .waiting-card-row,
        .waiting-card-amber,
        .tv-station-card {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            padding: 1rem !important;
        }

        /* 4. Staff & Station Card Resizing on Mobile */
        [data-testid="stColumn"] div.stVerticalBlock:has(.home-staff-content) {
            height: auto !important;
            min-height: 0 !important;
            max-height: none !important;
            padding: 1rem !important;
            margin-bottom: 0.75rem !important;
        }
        .home-staff-content .home-staff-img-frame {
            height: 200px !important;
        }

        [data-testid="stColumn"] div.stVerticalBlock:has(.join-staff-content) {
            height: auto !important;
            min-height: 0 !important;
            max-height: none !important;
            padding: 1rem !important;
            margin-bottom: 0.75rem !important;
        }
        .join-staff-content .join-staff-img-frame {
            height: 165px !important;
        }

        [data-testid="stColumn"] div.stVerticalBlock:has(.tv-station-card-inner) {
            height: auto !important;
            min-height: 0 !important;
            max-height: none !important;
            padding: 1rem !important;
            margin-bottom: 0.75rem !important;
        }
        .tv-station-img-frame {
            height: 165px !important;
        }

        /* 5. Typography Scaling */
        .salon-heading-serif {
            font-size: 1.65rem !important;
            line-height: 1.25 !important;
        }
        h1.salon-heading-serif,
        h1 {
            font-size: 1.85rem !important;
            line-height: 1.2 !important;
        }
        h2.salon-heading-serif,
        h2 {
            font-size: 1.45rem !important;
            line-height: 1.25 !important;
        }
        h3.salon-heading-serif,
        h3 {
            font-size: 1.2rem !important;
            line-height: 1.3 !important;
        }
        .salon-wordmark {
            font-size: 1.45rem !important;
            letter-spacing: 1.2px !important;
        }
        .section-eyebrow {
            font-size: 0.72rem !important;
            letter-spacing: 1.5px !important;
        }

        /* 6. Touch Targets & Form Inputs (Min 44px Height) */
        .stButton > button,
        .btn-gold-cta > button,
        .stFormSubmitButton > button {
            min-height: 44px !important;
            height: auto !important;
            font-size: 0.95rem !important;
            padding: 0.65rem 1rem !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }

        div[class*="st-key-btn_staff"] button {
            height: 44px !important;
            min-height: 44px !important;
            max-height: none !important;
            font-size: 0.88rem !important;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSelectbox"] select {
            min-height: 44px !important;
            font-size: 1rem !important;
            box-sizing: border-box !important;
        }

        /* 7. Header Top Bar on Mobile */
        .top-brand-header {
            text-align: center !important;
            margin-bottom: 0.35rem !important;
        }
        .top-nav-links {
            gap: 0.75rem !important;
            padding-top: 0.2rem !important;
            margin-bottom: 0.4rem !important;
            justify-content: center !important;
        }
        .nav-link-item {
            font-size: 0.85rem !important;
            padding: 0.25rem 0.4rem !important;
        }
        div[data-testid="stRadio"]:has(input[name*="lang_toggle_radio"]) {
            display: flex !important;
            justify-content: center !important;
            margin-top: 0.2rem !important;
        }
        div[data-testid="stRadio"]:has(input[name*="lang_toggle_radio"]) > div {
            justify-content: center !important;
        }

        /* 8. Home Screen Hero Adjustments */
        .home-hero-sanctuary-frame {
            height: 220px !important;
            margin-top: 0.85rem !important;
        }
        .hero-queue-card {
            padding: 0.75rem 1rem !important;
            margin: 0.75rem 0 !important;
        }

        /* 9. Join Queue Banner & Card Adjustments */
        .screen-banner {
            padding-left: 0.75rem !important;
            margin-bottom: 1rem !important;
        }

        /* 10. My Status Countdown & Proximity Alert */
        .circular-countdown {
            width: 140px !important;
            height: 140px !important;
            margin: 1rem auto !important;
        }
        .proximity-alert-banner {
            flex-direction: column !important;
            text-align: center !important;
            padding: 1rem !important;
            gap: 0.5rem !important;
        }
        .gold-called-banner {
            padding: 1.4rem 1rem !important;
        }

        /* 11. Reception Dashboard Metrics & Actions */
        .reception-summary-val {
            font-size: 1.85rem !important;
        }
        .reception-summary-box, .reception-summary-card {
            padding: 0.85rem 0.75rem !important;
        }

        /* 12. Barber View Digital Timer Box */
        .digital-timer-box {
            padding: 1rem !important;
            margin: 0.75rem 0 1rem 0 !important;
        }
        .digital-timer-value {
            font-size: 2.2rem !important;
            letter-spacing: 3px !important;
        }

        /* 13. Waiting Area TV Header & Called Banner */
        .tv-header-status-wrapper {
            text-align: left !important;
            margin-top: 0.4rem !important;
        }
        .tv-called-banner {
            padding: 1.25rem 0.85rem !important;
        }
        .tv-called-banner div:nth-child(2) {
            font-size: 2.1rem !important;
        }
        .tv-upnext-time-wrapper {
            text-align: left !important;
            margin-top: 0.25rem !important;
        }

        /* 14. Staff PIN Card on Mobile */
        [data-testid="stColumn"] div.stVerticalBlock:has(.pin-card-wrapper) {
            padding: 1.5rem 1.15rem !important;
            margin-top: 0.85rem !important;
            margin-bottom: 1.5rem !important;
            border-radius: 16px !important;
        }
        .pin-main-heading {
            font-size: 1.75rem !important;
        }

        /* 15. Sidebar Navigation on Mobile */
        [data-testid="stSidebar"] {
            max-width: 85vw !important;
            width: 85vw !important;
        }
    }
</style>
"""
st.markdown(SALON_THEME_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. SHARED MULTI-CLIENT DATA MANAGER (SINGLETON)
# ==============================================================================

class SalonDataManager:
    """Thread-safe multi-client data manager shared across all browser sessions."""

    def __init__(self):
        self.lock = threading.RLock()
        self.queue_open: bool = True
        self.closing_time: str = "09:00 PM"

        # 4 Approved Services (Standardized 600x400 photography)
        self.services: Dict[str, Dict[str, Any]] = {
            "haircut": {
                "id": "haircut",
                "name_en": "Haircut",
                "name_gu": "હેરકટ",
                "duration": 30,  # minutes
                "price": 350,    # within ₹250–₹1,200
                "active": True,
                "image": "assets/service_haircut.jpg",
                "desc_en": "Tailored precision cuts, consultation, and polished styling.",
                "desc_gu": "ચોકસાઈભર્યું કટિંગ, નિષ્ણાત સલાહ અને ઉત્તમ ફિનિશિંગ ટચ.",
            },
            "styling": {
                "id": "styling",
                "name_en": "Hair Styling",
                "name_gu": "હેર સ્ટાઇલિંગ",
                "duration": 25,
                "price": 400,
                "active": True,
                "image": "assets/service_styling.jpg",
                "desc_en": "Signature blowouts, soft waves, and modern thermal sculpting.",
                "desc_gu": "બ્લોઆઉટ, સોફ્ટ વેવ્સ અને ખાસ પ્રસંગો માટે મોર્ડન સ્ટાઇલિંગ.",
            },
            "spa": {
                "id": "spa",
                "name_en": "Hair Spa",
                "name_gu": "હેર સ્પા",
                "duration": 45,
                "price": 800,
                "active": True,
                "image": "assets/service_spa.jpg",
                "desc_en": "Deep scalp rejuvenation, infusions, pressure massage, and hydration.",
                "desc_gu": "ઊંડાણપૂર્વક સ્કેલ્પ રિજુવિનેશન, મસાજ અને ગહન હાઇડ્રેશન થેરાપી.",
            },
            "colouring": {
                "id": "colouring",
                "name_en": "Hair Colouring",
                "name_gu": "હેર કલરિંગ",
                "duration": 60,
                "price": 950,
                "active": True,
                "image": "assets/service_colouring.jpg",
                "desc_en": "Dimensional balayage, radiant root coverage, and bespoke hues.",
                "desc_gu": "ડાયમેન્શનલ બાલાયેજ, ગ્લોઇંગ રૂટ કવરેજ અને કસ્ટમ કલર બ્લેન્ડિંગ.",
            },
        }

        # Staff Members (Neutral Placeholders & Standardized 400x480 portraits)
        self.staff: Dict[str, Dict[str, Any]] = {
            "barber_1": {
                "id": "barber_1",
                "name": "Barber 1",
                "role_en": "Master Barber",
                "role_gu": "માસ્ટર બાર્બર",
                "gender": "male",
                "image": "assets/staff_barber1.jpg",
                "on_duty": True,
                "status": "In Service",
                "current_token": "S-12",
                "time_remaining": 12,
            },
            "stylist_1": {
                "id": "stylist_1",
                "name": "Stylist 1",
                "role_en": "Senior Hairstylist",
                "role_gu": "સીનિયર હેરસ્ટાઈલિસ્ટ",
                "gender": "female",
                "image": "assets/staff_stylist1.jpg",
                "on_duty": True,
                "status": "Available",
                "current_token": None,
                "time_remaining": 0,
            },
            "barber_2": {
                "id": "barber_2",
                "name": "Barber 2",
                "role_en": "Creative Barber",
                "role_gu": "ક્રિએટિવ બાર્બર",
                "gender": "male",
                "image": "assets/staff_barber2.jpg",
                "on_duty": True,
                "status": "In Service",
                "current_token": "S-13",
                "time_remaining": 18,
            },
            "stylist_2": {
                "id": "stylist_2",
                "name": "Stylist 2",
                "role_en": "Colour & Spa Specialist",
                "role_gu": "કલર અને સ્પા નિષ્ણાત",
                "gender": "female",
                "image": "assets/staff_stylist2.jpg",
                "on_duty": True,
                "status": "On Break",
                "current_token": None,
                "time_remaining": 0,
            },
        }

        # Queue Tickets
        self.token_counter: int = 15
        self.queue: List[Dict[str, Any]] = [
            {
                "token": "S-10",
                "customer_name": "Kunal Joshi",
                "phone": "9825100001",
                "services": ["haircut"],
                "barber_pref": "any",
                "status": "WAITING",
                "created_at": "09:45 AM",
                "total_duration": 30,
                "total_price": 350,
            },
            {
                "token": "S-11",
                "customer_name": "Dhaval Shah",
                "phone": "9825100002",
                "services": ["spa", "haircut"],
                "barber_pref": "barber_1",
                "status": "WAITING",
                "created_at": "09:55 AM",
                "total_duration": 75,
                "total_price": 1150,
            },
            {
                "token": "S-14",
                "customer_name": "Ananya Patel",
                "phone": "9825100003",
                "services": ["haircut", "styling"],
                "barber_pref": "stylist_1",
                "status": "WAITING",
                "created_at": "10:15 AM",
                "total_duration": 55,
                "total_price": 750,
            },
            {
                "token": "S-12",
                "customer_name": "Rohan Mehra",
                "phone": "9825100004",
                "services": ["haircut"],
                "barber_pref": "barber_1",
                "assigned_barber": "barber_1",
                "status": "IN_SERVICE",
                "created_at": "09:30 AM",
                "started_at": "10:00 AM",
                "started_timestamp": time.time() - 720,
                "total_duration": 30,
                "total_price": 350,
            },
            {
                "token": "S-13",
                "customer_name": "Aditya Verma",
                "phone": "9825100005",
                "services": ["styling"],
                "barber_pref": "barber_2",
                "assigned_barber": "barber_2",
                "status": "IN_SERVICE",
                "created_at": "09:35 AM",
                "started_at": "09:55 AM",
                "started_timestamp": time.time() - 1080,
                "total_duration": 25,
                "total_price": 400,
            },
        ]

    def get_services(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            return self.services.copy()

    def get_staff(self) -> Dict[str, Dict[str, Any]]:
        with self.lock:
            return self.staff.copy()

    def is_online_queue_open(self) -> bool:
        with self.lock:
            return self.queue_open

    def get_active_ticket_by_phone(self, phone: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            clean_phone = re.sub(r"\D", "", phone)
            for ticket in self.queue:
                if ticket["phone"] == clean_phone and ticket["status"] in ["WAITING", "CALLED", "IN_SERVICE"]:
                    return ticket.copy()
            return None

    def get_ticket(self, token: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            for ticket in self.queue:
                if ticket["token"] == token:
                    return ticket.copy()
            return None

    def calculate_estimated_wait(self, service_ids: List[str], barber_pref: str) -> int:
        if not service_ids:
            return 0

        with self.lock:
            active_barbers = [
                s for s in self.staff.values()
                if s["on_duty"] and s["status"] in ["Available", "In Service"]
            ]
            num_barbers = max(1, len(active_barbers))
            in_service_remainder = sum(s.get("time_remaining", 0) for s in active_barbers)
            waiting_tickets = [t for t in self.queue if t["status"] == "WAITING"]

            if barber_pref == "any":
                minutes_ahead = sum(t.get("total_duration", 30) for t in waiting_tickets)
                total_min = minutes_ahead + in_service_remainder
                return max(5, math.ceil(total_min / num_barbers))
            else:
                target_staff = self.staff.get(barber_pref)
                barber_rem = target_staff.get("time_remaining", 0) if target_staff else 0
                matching_ahead = [
                    t for t in waiting_tickets
                    if t["barber_pref"] in [barber_pref, "any"]
                ]
                wait_min = barber_rem + sum(t.get("total_duration", 30) for t in matching_ahead)
                return max(5, wait_min)

    def add_queue_entry(self, customer_name: str, phone: str, service_ids: List[str], barber_pref: str) -> Dict[str, Any]:
        with self.lock:
            clean_phone = re.sub(r"\D", "", phone)
            token = f"S-{self.token_counter}"
            self.token_counter += 1

            total_duration = sum(self.services[sid]["duration"] for sid in service_ids if sid in self.services)
            total_price = sum(self.services[sid]["price"] for sid in service_ids if sid in self.services)

            entry = {
                "token": token,
                "customer_name": customer_name.strip(),
                "phone": clean_phone,
                "services": service_ids,
                "barber_pref": barber_pref,
                "status": "WAITING",
                "created_at": datetime.now().strftime("%I:%M %p"),
                "total_duration": total_duration,
                "total_price": total_price,
            }
            self.queue.append(entry)
            return entry.copy()

    def get_ticket_position(self, token: str) -> int:
        """Calculates 1-based queue position among active WAITING customers."""
        with self.lock:
            target = None
            for t in self.queue:
                if t["token"] == token:
                    target = t
                    break
            if not target or target["status"] != "WAITING":
                return 0

            ahead_count = 0
            for t in self.queue:
                if t["status"] == "WAITING":
                    if t["token"] == token:
                        break
                    if target["barber_pref"] != "any":
                        if t["barber_pref"] in [target["barber_pref"], "any"]:
                            ahead_count += 1
                    else:
                        ahead_count += 1

            return ahead_count + 1

    def get_ticket_wait_time(self, token: str) -> int:
        """Calculates dynamic estimated wait time in minutes for a specific ticket."""
        with self.lock:
            target = None
            for t in self.queue:
                if t["token"] == token:
                    target = t
                    break
            if not target:
                return 0
            if target["status"] in ["CALLED", "IN_SERVICE", "COMPLETED", "CANCELLED"]:
                return 0

            active_barbers = [
                s for s in self.staff.values()
                if s["on_duty"] and s["status"] in ["Available", "In Service"]
            ]
            num_barbers = max(1, len(active_barbers))
            in_service_remainder = sum(s.get("time_remaining", 0) for s in active_barbers)

            tickets_ahead = []
            for t in self.queue:
                if t["status"] == "WAITING":
                    if t["token"] == token:
                        break
                    if target["barber_pref"] != "any":
                        if t["barber_pref"] in [target["barber_pref"], "any"]:
                            tickets_ahead.append(t)
                    else:
                        tickets_ahead.append(t)

            pos = len(tickets_ahead) + 1

            if target["barber_pref"] == "any":
                has_available = any(s["status"] == "Available" for s in active_barbers)
                if pos == 1 and has_available:
                    return 2
                minutes_ahead = sum(t.get("total_duration", 30) for t in tickets_ahead)
                total_min = minutes_ahead + in_service_remainder
                return max(5, math.ceil(total_min / num_barbers))
            else:
                target_staff = self.staff.get(target["barber_pref"])
                barber_rem = target_staff.get("time_remaining", 0) if target_staff else 0
                if pos == 1 and target_staff and target_staff.get("status") == "Available":
                    return 2
                wait_min = barber_rem + sum(t.get("total_duration", 30) for t in tickets_ahead)
                return max(5, wait_min)

    def cancel_ticket(self, token: str) -> bool:
        """Cancels a waiting queue ticket per Screen 3 rules."""
        with self.lock:
            for t in self.queue:
                if t["token"] == token:
                    if t["status"] == "WAITING":
                        t["status"] = "CANCELLED"
                        t["cancelled_at"] = datetime.now().strftime("%I:%M %p")
                        return True
            return False

    def update_ticket_status(self, token: str, new_status: str, assigned_barber: Optional[str] = None) -> bool:
        """Updates ticket status and assigned barber (for testing and lifecycle transitions)."""
        with self.lock:
            for t in self.queue:
                if t["token"] == token:
                    t["status"] = new_status
                    if assigned_barber:
                        t["assigned_barber"] = assigned_barber
                    return True
            return False

    def call_next(self, barber_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Calls the next eligible waiting customer per docs/03-flows-rules.md Section 3.2."""
        with self.lock:
            calling_barber = None
            if barber_id and barber_id in self.staff:
                calling_barber = self.staff[barber_id]
            else:
                for s in self.staff.values():
                    if s["on_duty"] and s["status"] == "Available":
                        calling_barber = s
                        barber_id = s["id"]
                        break

            if not calling_barber:
                barber_id = barber_id or "barber_1"
                calling_barber = self.staff.get(barber_id)

            selected_ticket = None
            for t in self.queue:
                if t["status"] == "WAITING":
                    if t["barber_pref"] in [barber_id, "any"]:
                        selected_ticket = t
                        break

            if selected_ticket:
                selected_ticket["status"] = "CALLED"
                selected_ticket["assigned_barber"] = barber_id
                selected_ticket["called_at"] = datetime.now().strftime("%I:%M %p")
                if calling_barber:
                    calling_barber["status"] = "In Service"
                    calling_barber["current_token"] = selected_ticket["token"]
                return selected_ticket.copy()
            return None

    def start_service(self, token: str) -> bool:
        """Transitions a CALLED ticket to IN_SERVICE per docs/03-flows-rules.md Section 6."""
        with self.lock:
            for t in self.queue:
                if t["token"] == token and t["status"] in ["CALLED", "WAITING"]:
                    t["status"] = "IN_SERVICE"
                    t["started_at"] = datetime.now().strftime("%I:%M %p")
                    t["started_timestamp"] = time.time()
                    assigned = t.get("assigned_barber") or "barber_1"
                    t["assigned_barber"] = assigned
                    if assigned in self.staff:
                        self.staff[assigned]["status"] = "In Service"
                        self.staff[assigned]["current_token"] = token
                    return True
            return False

    def complete_service(self, token: str) -> bool:
        """Transitions an IN_SERVICE ticket to COMPLETED and frees the barber per docs/03-flows-rules.md."""
        with self.lock:
            for t in self.queue:
                if t["token"] == token:
                    t["status"] = "COMPLETED"
                    t["completed_at"] = datetime.now().strftime("%I:%M %p")
                    assigned = t.get("assigned_barber")
                    if assigned and assigned in self.staff:
                        if self.staff[assigned].get("queued_break", False):
                            self.staff[assigned]["status"] = "On Break"
                            self.staff[assigned]["queued_break"] = False
                        else:
                            self.staff[assigned]["status"] = "Available"
                        self.staff[assigned]["current_token"] = None
                        self.staff[assigned]["time_remaining"] = 0
                    return True
            return False

    def mark_no_show(self, token: str) -> bool:
        """Transitions a CALLED ticket to NO-SHOW per docs/03-flows-rules.md Section 7.3 and frees the barber."""
        with self.lock:
            for t in self.queue:
                if t["token"] == token and t["status"] in ["CALLED", "WAITING"]:
                    t["status"] = "NO-SHOW"
                    t["no_show_at"] = datetime.now().strftime("%I:%M %p")
                    assigned = t.get("assigned_barber")
                    if assigned and assigned in self.staff:
                        self.staff[assigned]["status"] = "Available"
                        self.staff[assigned]["current_token"] = None
                        self.staff[assigned]["time_remaining"] = 0
                    return True
            return False

    def reset_queue(self) -> None:
        """Resets the queue to initial demo state."""
        with self.lock:
            self.token_counter = 15
            self.queue = [
                {
                    "token": "S-10",
                    "customer_name": "Kunal Joshi",
                    "phone": "9825100001",
                    "services": ["haircut"],
                    "barber_pref": "any",
                    "status": "WAITING",
                    "created_at": "09:45 AM",
                    "total_duration": 30,
                    "total_price": 350,
                },
                {
                    "token": "S-11",
                    "customer_name": "Dhaval Shah",
                    "phone": "9825100002",
                    "services": ["spa", "haircut"],
                    "barber_pref": "barber_1",
                    "status": "WAITING",
                    "created_at": "09:55 AM",
                    "total_duration": 75,
                    "total_price": 1150,
                },
                {
                    "token": "S-14",
                    "customer_name": "Ananya Patel",
                    "phone": "9825100003",
                    "services": ["haircut", "styling"],
                    "barber_pref": "stylist_1",
                    "status": "WAITING",
                    "created_at": "10:15 AM",
                    "total_duration": 55,
                    "total_price": 750,
                },
                {
                    "token": "S-12",
                    "customer_name": "Rohan Mehra",
                    "phone": "9825100004",
                    "services": ["haircut"],
                    "barber_pref": "barber_1",
                    "assigned_barber": "barber_1",
                    "status": "IN_SERVICE",
                    "created_at": "09:30 AM",
                    "started_at": "10:00 AM",
                    "started_timestamp": time.time() - 720,
                    "total_duration": 30,
                    "total_price": 350,
                },
                {
                    "token": "S-13",
                    "customer_name": "Aditya Verma",
                    "phone": "9825100005",
                    "services": ["styling"],
                    "barber_pref": "barber_2",
                    "assigned_barber": "barber_2",
                    "status": "IN_SERVICE",
                    "created_at": "09:35 AM",
                    "started_at": "09:55 AM",
                    "started_timestamp": time.time() - 1080,
                    "total_duration": 25,
                    "total_price": 400,
                },
            ]
            self.staff["barber_1"]["status"] = "In Service"
            self.staff["barber_1"]["current_token"] = "S-12"
            self.staff["stylist_1"]["status"] = "Available"
            self.staff["stylist_1"]["current_token"] = None
            self.staff["barber_2"]["status"] = "In Service"
            self.staff["barber_2"]["current_token"] = "S-13"
            self.staff["stylist_2"]["status"] = "On Break"
            self.staff["stylist_2"]["current_token"] = None

    def set_position_2_scenario(self, token: str) -> None:
        """Configures queue so that `token` is exactly 2nd in line for proximity testing (TC-07)."""
        with self.lock:
            for t in self.queue:
                if t["token"] == "S-10":
                    t["status"] = "WAITING"
                elif t["token"] == token:
                    t["status"] = "WAITING"
                else:
                    t["status"] = "CANCELLED"

    def get_summary_counts(self) -> Dict[str, int]:
        """Calculates live queue counts for Waiting, In Service, Completed and No-shows."""
        with self.lock:
            waiting = sum(1 for t in self.queue if t["status"] == "WAITING")
            in_service = sum(1 for t in self.queue if t["status"] in ["IN_SERVICE", "CALLED"])
            completed = sum(1 for t in self.queue if t["status"] == "COMPLETED")
            no_show = sum(1 for t in self.queue if t["status"] == "NO-SHOW")
            return {
                "waiting": waiting,
                "in_service": in_service,
                "completed": completed,
                "no_show": no_show,
            }

    def get_current_customer_for_staff(self, staff_id: str) -> Optional[Dict[str, Any]]:
        """Resolves the active ticket currently being called or served by a specific staff member."""
        with self.lock:
            for t in self.queue:
                if t.get("assigned_barber") == staff_id and t["status"] in ["CALLED", "IN_SERVICE"]:
                    return t.copy()
            curr_tok = self.staff.get(staff_id, {}).get("current_token")
            if curr_tok:
                for t in self.queue:
                    if t["token"] == curr_tok:
                        return t.copy()
            return None

    def get_next_customer_for_staff(self, staff_id: str) -> Optional[Dict[str, Any]]:
        """Finds the next upcoming waiting customer eligible for this staff member per Section 3.2."""
        with self.lock:
            for t in self.queue:
                if t["status"] == "WAITING":
                    if t["barber_pref"] in [staff_id, "any"]:
                        return t.copy()
            return None

    def toggle_barber_break(self, barber_id: str, want_break: bool) -> Tuple[bool, str]:
        """Toggles a barber between Available and On Break respecting Section 10.2 safety invariants."""
        with self.lock:
            s = self.staff.get(barber_id)
            if not s:
                return False, "Staff not found"

            curr_customer = None
            for t in self.queue:
                if t.get("assigned_barber") == barber_id and t.get("status") in ["CALLED", "IN_SERVICE"]:
                    curr_customer = t
                    break
            if not curr_customer and s.get("current_token"):
                for t in self.queue:
                    if t.get("token") == s.get("current_token") and t.get("status") in ["CALLED", "IN_SERVICE"]:
                        curr_customer = t
                        break

            if curr_customer and curr_customer.get("status") == "IN_SERVICE":
                if want_break:
                    s["queued_break"] = True
                    return True, "Break request queued. Will activate immediately after finishing current customer."
                else:
                    s["queued_break"] = False
                    return True, "Queued break cancelled."

            if want_break:
                s["status"] = "On Break"
                s["queued_break"] = False
                return True, "Status updated to On Break."
            else:
                s["status"] = "Available"
                s["queued_break"] = False
                return True, "Status updated to Available."

    def set_online_queue_status(self, is_open: bool) -> None:
        """Sets the online queue joining open or closed per Screen 7."""
        with self.lock:
            self.queue_open = is_open

    def update_services(self, updated_services: Dict[str, Dict[str, Any]]) -> Tuple[bool, str]:
        """Updates service definitions, prices and active status enforcing TC-02 price range."""
        with self.lock:
            for sid, sdata in updated_services.items():
                price = sdata.get("price", 0)
                if price < 250 or price > 1200:
                    return False, f"Price for {sdata.get('name_en', sid)} must be strictly between ₹250 and ₹1,200 (TC-02)."
                if sdata.get("duration", 0) <= 0:
                    return False, f"Duration for {sdata.get('name_en', sid)} must be positive."

            for sid, sdata in updated_services.items():
                if sid in self.services:
                    self.services[sid]["name_en"] = sdata.get("name_en", self.services[sid]["name_en"])
                    self.services[sid]["name_gu"] = sdata.get("name_gu", self.services[sid]["name_gu"])
                    self.services[sid]["price"] = sdata.get("price", self.services[sid]["price"])
                    self.services[sid]["duration"] = sdata.get("duration", self.services[sid]["duration"])
                    self.services[sid]["active"] = sdata.get("active", self.services[sid]["active"])
            return True, "Services updated successfully."

    def update_staff_duty(self, updated_duty: Dict[str, bool]) -> Tuple[bool, str]:
        """Updates on-duty status for staff members respecting active services."""
        with self.lock:
            for sid, on_duty in updated_duty.items():
                if sid in self.staff:
                    self.staff[sid]["on_duty"] = on_duty
                    if not on_duty:
                        if self.staff[sid]["status"] == "Available":
                            self.staff[sid]["status"] = "Off Duty"
                    else:
                        if self.staff[sid]["status"] == "Off Duty":
                            self.staff[sid]["status"] = "Available"
            return True, "Staff duty roster updated."

    def get_today_statistics(self) -> Dict[str, Any]:
        """Calculates dynamic daily salon statistics from actual queue tickets."""
        with self.lock:
            served = sum(1 for t in self.queue if t.get("status") == "COMPLETED")
            noshows = sum(1 for t in self.queue if t.get("status") == "NO-SHOW")
            waiting = sum(1 for t in self.queue if t.get("status") == "WAITING")
            in_service = sum(1 for t in self.queue if t.get("status") in ["IN_SERVICE", "CALLED"])

            completed_tickets = [t for t in self.queue if t.get("status") == "COMPLETED"]
            if completed_tickets:
                avg_wait = sum(t.get("total_duration", 30) for t in completed_tickets) // len(completed_tickets)
            else:
                avg_wait = 18

            return {
                "served": served,
                "noshows": noshows,
                "waiting": waiting,
                "in_service": in_service,
                "avg_wait": avg_wait,
            }


@st.cache_resource
def get_data_manager() -> SalonDataManager:
    return SalonDataManager()


# ==============================================================================
# 3. CENTRALIZED BILINGUAL TRANSLATION DICTIONARY
# ==============================================================================

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "app_wordmark": {
        "en": "SALt N' PEPPER",
        "gu": "SALt N' PEPPER",
    },
    "tagline": {
        "en": "Luxury Hair Care & Styling Sanctuary",
        "gu": "લક્ઝરી હેર કેર અને સ્ટાઇલિંગ સેન્ચ્યુરી",
    },
    # Navigation
    "nav_home": {
        "en": "Home",
        "gu": "હોમ",
    },
    "nav_about": {
        "en": "About",
        "gu": "અમારા વિશે",
    },
    "nav_services": {
        "en": "Services",
        "gu": "સેવાઓ",
    },
    "nav_join": {
        "en": "Join Queue",
        "gu": "કતારમાં જોડાઓ",
    },
    "nav_status": {
        "en": "My Status",
        "gu": "મારું સ્ટેટસ",
    },
    "nav_reception": {
        "en": "Reception Dashboard",
        "gu": "રિસેપ્શન ડેશબોર્ડ",
    },
    "nav_barber": {
        "en": "Barber View",
        "gu": "બાર્બર વ્યૂ",
    },
    "nav_display": {
        "en": "Waiting Area TV",
        "gu": "વેઇટિંગ એરિયા ટીવી",
    },
    "nav_admin": {
        "en": "Owner Settings",
        "gu": "માલિક સેટિંગ્સ",
    },
    "back_to_home": {
        "en": "← Back to Home",
        "gu": "← હોમ પર પાછા જાઓ",
    },
    # Staff PIN Authentication
    "pin_staff_access": {
        "en": "STAFF ACCESS",
        "gu": "સ્ટાફ એક્સેસ",
    },
    "pin_welcome_back": {
        "en": "Welcome Back",
        "gu": "સ્વાગત છે",
    },
    "pin_enter_instruction": {
        "en": "Enter your staff PIN to continue.",
        "gu": "આગળ વધવા માટે તમારો સ્ટાફ પિન દાખલ કરો.",
    },
    "pin_input_label": {
        "en": "Staff PIN",
        "gu": "સ્ટાફ પિન",
    },
    "pin_input_placeholder": {
        "en": "••••",
        "gu": "••••",
    },
    "pin_btn_unlock": {
        "en": "Unlock Dashboard",
        "gu": "ડેશબોર્ડ અનલૉક કરો",
    },
    "pin_err_incorrect": {
        "en": "Incorrect PIN. Please try again.",
        "gu": "ખોટો પિન. કૃપા કરીને ફરી પ્રયાસ કરો.",
    },
    "pin_back_to_home": {
        "en": "← Back to Home",
        "gu": "← હોમ પર પાછા જાઓ",
    },
    "pin_staff_logged_in": {
        "en": "Staff Session Active",
        "gu": "સ્ટાફ સત્ર સક્રિય છે",
    },
    "pin_btn_logout": {
        "en": "Log Out",
        "gu": "લૉગ આઉટ",
    },
    # Home Screen
    "status_open": {
        "en": "Open · Closes 9:00 PM",
        "gu": "ખુલ્લું છે · રાત્રે 9:00 વાગ્યે બંધ થશે",
    },
    "hero_title": {
        "en": "Sculpting Styles, Reflecting Individuality.",
        "gu": "શૈલીનું સર્જન, વ્યક્તિત્વનું પ્રતિબિંબ.",
    },
    "hero_subtitle": {
        "en": "Experience bespoke haircuts, transformative styling, and revitalizing hair spa therapies. Seamlessly join our live digital queue from your phone and arrive relaxed.",
        "gu": "અનુભવો શ્રેષ્ઠ હેરકટ, આકર્ષક સ્ટાઇલિંગ અને તાજગીભરી હેર સ્પા થેરાપી. તમારા ફોનથી જ લાઇવ ડિજિટલ કતારમાં જોડાવો અને નિરાંતે પધારો.",
    },
    "hero_waiting_count": {
        "en": "4 Guests Waiting",
        "gu": "4 ગ્રાહકો પ્રતીક્ષામાં",
    },
    "hero_estimated_wait": {
        "en": "Estimated Wait: ~35 min",
        "gu": "અંદાજિત પ્રતીક્ષા સમય: ~35 મિનિટ",
    },
    "btn_join_queue_cta": {
        "en": "Join Live Queue",
        "gu": "કતારમાં જોડાઓ",
    },
    "services_eyebrow": {
        "en": "Our Signature Offerings",
        "gu": "અમારી વિશિષ્ટ સેવાઓ",
    },
    "services_title": {
        "en": "Artisanal Hair & Scalp Services",
        "gu": "કારીગરી હેર અને સ્કેલ્પ સેવાઓ",
    },
    "services_subtitle": {
        "en": "Every appointment is customized to complement your unique features and personal style.",
        "gu": "દરેક મુલાકાત તમારી વ્યક્તિગત શૈલી અને સુંદરતાને અનુરૂપ બનાવવામાં આવે છે.",
    },
    "team_eyebrow": {
        "en": "Meet The Artists",
        "gu": "અમારા નિષ્ણાત કલાકારો",
    },
    "team_title": {
        "en": "Master Stylists & Barbers On Duty",
        "gu": "ડ્યુટી પર હાજર માસ્ટર સ્ટાઈલિસ્ટ અને બાર્બર",
    },
    "team_subtitle": {
        "en": "Our talented team blends classic barbering finesse with contemporary salon aesthetics.",
        "gu": "અમારી કુશળ ટીમ ક્લાસિક બાર્બરિંગ અને આધુનિક સલૂન આર્ટિસ્ટ્રીનું અદભુત મિશ્રણ ધરાવે છે.",
    },
    "about_eyebrow": {
        "en": "Our Philosophy",
        "gu": "અમારો અભિગમ",
    },
    "about_title": {
        "en": "Redefining the Salon Experience Without the Wait",
        "gu": "લાંબી રાહ જોયા વગર સલૂનનો અદભુત અનુભવ",
    },
    "about_text_p1": {
        "en": "At SALt N' PEPPER, we believe self-care should be unhurried, comfortable, and dignified. We eliminated chaotic waiting lobbies with our intelligent live queue system, giving you freedom to spend your time your way.",
        "gu": "SALt N' PEPPER માં અમે માનીએ છીએ કે ગ્રૂમિંગ અનુભવ આરામદાયક અને સન્માનજનક હોવો જોઈએ. અમે સ્માર્ટ ડિજિટલ કતાર દ્વારા ભીડભાડ દૂર કરી છે, જેથી તમે તમારો સમય તમારી રીતે માણી શકો.",
    },
    "about_text_p2": {
        "en": "Our salon features state-of-the-art ergonomic stations, medical-grade hygiene protocols, and an artisan team dedicated to healthy hair transformations.",
        "gu": "અમારા સલૂનમાં ઉત્તમ આરામદાયક ચેર, ઉચ્ચ સ્તરની સ્વચ્છતા અને તમારા વાળની કુદરતી સુંદરતા જાળવતી સમર્પિત ટીમ ઉપલબ્ધ છે.",
    },
    "footer_rights": {
        "en": "All rights reserved. Digital Queue Management System.",
        "gu": "સર્વ હક સુરક્ષિત. ડિજિટલ કતાર વ્યવસ્થાપન સિસ્ટમ.",
    },
    "footer_hours": {
        "en": "Operating Hours: Tue – Sun: 9:00 AM – 9:00 PM | Mon: Closed",
        "gu": "સમય: મંગળ – રવિ: સવારે 9:00 થી રાત્રે 9:00 | સોમવાર: રજા",
    },
    # Screen 2: Join Queue Specific Labels
    "join_title": {
        "en": "Join The Live Queue",
        "gu": "લાઇવ કતારમાં જોડાઓ",
    },
    "join_subtitle": {
        "en": "Select your desired hair services first, then choose your preferred stylist or barber.",
        "gu": "પહેલા તમારી પસંદગીની સેવાઓ પસંદ કરો, પછી તમારા મનપસંદ સ્ટાઈલિસ્ટ અથવા વાળંદ પસંદ કરો.",
    },
    "step_customer_details": {
        "en": "Customer Details",
        "gu": "ગ્રાહકની વિગતો",
    },
    "full_name_label": {
        "en": "Full Name",
        "gu": "પૂરું નામ",
    },
    "full_name_placeholder": {
        "en": "e.g. Ramesh Patel",
        "gu": "દા.ત. રમેશ પટેલ",
    },
    "phone_label": {
        "en": "Phone Number (10 Digits)",
        "gu": "મોબાઇલ નંબર (૧૦ અંક)",
    },
    "phone_placeholder": {
        "en": "e.g. 9876543210",
        "gu": "દા.ત. 9876543210",
    },
    "step_select_services": {
        "en": "Select Services (Choose 1 to 3 Services)",
        "gu": "સેવાઓ પસંદ કરો (૧ થી ૩ સેવાઓ પસંદ કરો)",
    },
    "step_choose_barber": {
        "en": "Choose Stylist or Barber",
        "gu": "સ્ટાઈલિસ્ટ અથવા વાળંદ પસંદ કરો",
    },
    "barber_any_title": {
        "en": "Any Barber (Fastest Available)",
        "gu": "ગમે તે ઉપલબ્ધ વાળંદ (સૌથી ઝડપી)",
    },
    "barber_any_desc": {
        "en": "Get served by the earliest available master barber or hairstylist.",
        "gu": "સૌથી પહેલા ઉપલબ્ધ થનાર નિષ્ણાત દ્વારા સેવા મેળવો.",
    },
    "booking_summary_title": {
        "en": "Booking Summary",
        "gu": "બુકિંગ સારાંશ",
    },
    "btn_confirm_join": {
        "en": "Confirm & Join Queue",
        "gu": "કતારમાં જોડાવાની પુષ્ટિ કરો",
    },
    "btn_select": {
        "en": "Select Service",
        "gu": "સેવા પસંદ કરો",
    },
    "btn_deselect": {
        "en": "Deselect Service",
        "gu": "સેવા દૂર કરો",
    },
    "btn_select_stylist": {
        "en": "Select",
        "gu": "પસંદ કરો",
    },
    "btn_selected_stylist": {
        "en": "Selected",
        "gu": "પસંદ કરેલ",
    },
    "btn_unavailable_stylist": {
        "en": "Unavailable",
        "gu": "ઉપલબ્ધ નથી",
    },
    "err_name_required": {
        "en": "Please enter your full name.",
        "gu": "કૃપા કરીને તમારું પૂરું નામ દાખલ કરો.",
    },
    "err_phone_invalid": {
        "en": "Please enter a valid 10-digit mobile number.",
        "gu": "કૃપા કરીને માન્ય ૧૦ અંકનો મોબાઇલ નંબર દાખલ કરો.",
    },
    "err_services_min": {
        "en": "Please select at least 1 service before joining the queue.",
        "gu": "કતારમાં જોડાવા માટે કૃપા કરીને ઓછામાં ઓછી ૧ સેવા પસંદ કરો.",
    },
    "err_services_max": {
        "en": "You can select at most 3 services. Please deselect one first.",
        "gu": "તમે વધુમાં વધુ ૩ સેવાઓ પસંદ કરી શકો છો. કૃપા કરીને પહેલા એક દૂર કરો.",
    },
    "err_barber_unavailable": {
        "en": "The selected professional is currently unavailable. Please choose an available stylist or 'Any Barber (Fastest)'.",
        "gu": "પસંદ કરેલ પ્રોફેશનલ હાલમાં ઉપલબ્ધ નથી. કૃપા કરીને ઉપલબ્ધ સ્ટાઈલિસ્ટ અથવા 'ગમે તે ઉપલબ્ધ વાળંદ' પસંદ કરો.",
    },
    "err_queue_closed": {
        "en": "Online queue is currently closed. Walk-ins are welcome at the reception desk.",
        "gu": "ઓનલાઇન કતાર હાલમાં બંધ છે. રિસેપ્શન ડેસ્ક પર વોક-ઇન સ્વાગત છે.",
    },
    "msg_duplicate_spot": {
        "en": "You already have an active spot in the queue (Token: {token}). Navigating to your status...",
        "gu": "તમારું કતારમાં પહેલેથી જ સક્રિય સ્થાન છે (ટોકન: {token}). તમારા સ્ટેટસ પર જઈ રહ્યા છીએ...",
    },
    "status_available": {
        "en": "Available",
        "gu": "ઉપલબ્ધ",
    },
    "status_in_service": {
        "en": "In Service",
        "gu": "સેવા ચાલુ",
    },
    "status_on_break": {
        "en": "On Break",
        "gu": "વિરામ પર",
    },
    # Screen 3: My Status Bilingual Translations
    "status_banner_eyebrow": {
        "en": "Queue Tracking",
        "gu": "કતાર ટ્રેકિંગ",
    },
    "status_title": {
        "en": "My Status",
        "gu": "મારું સ્ટેટસ",
    },
    "status_token_label": {
        "en": "Token",
        "gu": "ટોકન",
    },
    "status_pos_1": {
        "en": "You're Next! (1st in Line)",
        "gu": "હવે તમારો વારો છે! (કતારમાં ૧લા)",
    },
    "status_pos_2": {
        "en": "2nd in Line",
        "gu": "કતારમાં ૨જા",
    },
    "status_pos_3": {
        "en": "3rd in Line",
        "gu": "કતારમાં ૩જા",
    },
    "status_pos_nth": {
        "en": "{n}th in Line",
        "gu": "કતારમાં {n}મા",
    },
    "status_turn_alert_title": {
        "en": "It's your turn!",
        "gu": "હવે તમારો વારો છે!",
    },
    "status_turn_alert_msg": {
        "en": "Please proceed to {barber}. Your chair is ready!",
        "gu": "કૃપા કરીને {barber} પાસે જાઓ. તમારી ખુરશી તૈયાર છે!",
    },
    "status_proximity_banner": {
        "en": "Start coming to the salon! You are 2nd in line.",
        "gu": "સલૂન પર આવવાનું શરૂ કરો! તમે કતારમાં બીજા નંબરે છો.",
    },
    "status_proximity_desc": {
        "en": "Please make your way toward the salon so your stylist can begin immediately when called.",
        "gu": "કૃપા કરીને સલૂન તરફ આગળ વધો જેથી તમારો વારો આવતાં જ સ્ટાઈલિસ્ટ સેવા શરૂ કરી શકે.",
    },
    "status_inservice_banner": {
        "en": "Your service is currently in progress with {barber}. Relax and enjoy!",
        "gu": "{barber} સાથે તમારી સેવા હાલમાં ચાલુ છે. નિરાંતે આનંદ માણો!",
    },
    "status_completed_banner": {
        "en": "Service Completed! Thank you for choosing SALt N' PEPPER.",
        "gu": "સેવા પૂર્ણ થઈ ગઈ છે! SALt N' PEPPER પસંદ કરવા બદલ આભાર.",
    },
    "status_cancelled_banner": {
        "en": "This queue spot has been cancelled.",
        "gu": "આ કતાર સ્પોટ રદ કરવામાં આવ્યો છે.",
    },
    "status_est_wait": {
        "en": "Estimated Wait Time",
        "gu": "અંદાજિત પ્રતીક્ષા સમય",
    },
    "status_wait_minutes": {
        "en": "~{min} min",
        "gu": "~{min} મિનિટ",
    },
    "status_wait_ready": {
        "en": "Ready Now",
        "gu": "હવે તૈયાર",
    },
    "status_wait_note": {
        "en": "Live wait time dynamically calculated from active salon chairs.",
        "gu": "સલૂનની ચાલુ ચેર અને બાર્બર પ્રવૃત્તિ પરથી લાઇવ ગણતરી.",
    },
    "status_booking_details": {
        "en": "Booking Summary & Details",
        "gu": "બુકિંગ સારાંશ અને વિગતો",
    },
    "status_guest": {
        "en": "Guest Name",
        "gu": "ગ્રાહકનું નામ",
    },
    "status_phone": {
        "en": "Phone Number",
        "gu": "મોબાઇલ નંબર",
    },
    "status_services": {
        "en": "Selected Services",
        "gu": "પસંદ કરેલ સેવાઓ",
    },
    "status_stylist": {
        "en": "Stylist / Barber",
        "gu": "સ્ટાઈલિસ્ટ / વાળંદ",
    },
    "status_duration": {
        "en": "Total Duration",
        "gu": "કુલ સમય",
    },
    "status_price": {
        "en": "Total Price",
        "gu": "કુલ કિંમત",
    },
    "status_live_state": {
        "en": "Live Status",
        "gu": "લાઇવ સ્ટેટસ",
    },
    "status_joined_at": {
        "en": "Joined At",
        "gu": "જોડાવાનો સમય",
    },
    "status_btn_cancel": {
        "en": "Cancel My Spot",
        "gu": "મારો સ્પોટ રદ કરો",
    },
    "status_cancel_help": {
        "en": "Need to cancel or reschedule? You can cancel your spot while still in waiting status.",
        "gu": "રદ કરવું છે? તમે હજુ પ્રતીક્ષા સ્થિતિમાં હોવ ત્યાં સુધી તમારો સ્પોટ રદ કરી શકો છો.",
    },
    "status_cancel_confirm_q": {
        "en": "Are you sure you want to cancel your queue spot?",
        "gu": "શું તમે ખરેખર તમારો કતાર સ્પોટ રદ કરવા માંગો છો?",
    },
    "status_btn_keep_spot": {
        "en": "Keep My Spot",
        "gu": "સ્પોટ ચાલુ રાખો",
    },
    "status_btn_confirm_cancel": {
        "en": "Confirm Cancellation",
        "gu": "રદ કરવાની પુષ્ટિ કરો",
    },
    "status_cancel_success_msg": {
        "en": "Your spot has been successfully cancelled. The queue has been updated.",
        "gu": "તમારો સ્પોટ સફળતાપૂર્વક રદ કરવામાં આવ્યો છે. કતાર અપડેટ થઈ ગઈ છે.",
    },
    "status_btn_join_again": {
        "en": "Join Queue Again",
        "gu": "ફરીથી કતારમાં જોડાઓ",
    },
    "status_not_found_heading": {
        "en": "No Active Queue Spot Found",
        "gu": "કોઈ સક્રિય કતાર સ્પોટ મળ્યો નથી",
    },
    "status_not_found_desc": {
        "en": "We couldn't locate an active booking with token \"{token}\". Please check your token or join the queue anew.",
        "gu": "ટોકન \"{token}\" સાથે કોઈ સક્રિય બુકિંગ મળી શકી નથી. કૃપા કરીને તમારું ટોકન તપાસો અથવા નવી કતારમાં જોડાવો.",
    },
    "status_state_waiting": {
        "en": "Waiting in Line",
        "gu": "કતારમાં પ્રતીક્ષા",
    },
    "status_state_called": {
        "en": "Called (Your Turn!)",
        "gu": "બોલાવ્યા (તમારો વારો!)",
    },
    "status_state_inservice": {
        "en": "In Service",
        "gu": "સેવા ચાલુ છે",
    },
    "status_state_completed": {
        "en": "Completed",
        "gu": "સેવા પૂર્ણ થયેલ",
    },
    "status_state_cancelled": {
        "en": "Cancelled",
        "gu": "રદ કરેલ",
    },
    "status_state_noshow": {
        "en": "Marked No-Show",
        "gu": "નો-શો તરીકે ચિહ્નિત",
    },
    "status_noshow_banner": {
        "en": "Token Voided (No-Show)",
        "gu": "ટોકન રદ થયેલ (ગેરહાજર)",
    },
    "status_noshow_desc": {
        "en": "The 10-minute arrival window elapsed. Per salon policy, please speak to reception to join as a new walk-in.",
        "gu": "10-મિનિટનો સમય પૂરો થયો. સલૂન નીતિ મુજબ, કૃપા કરીને નવા વૉક-ઇન તરીકે જોડાવા માટે રિસેપ્શન પર વાત કરો.",
    },
    "reception_title": {
        "en": "Reception Dashboard",
        "gu": "રિસેપ્શન ડેશબોર્ડ",
    },
    "reception_subtitle": {
        "en": "Live Salon Queue & Staff Operations",
        "gu": "લાઇવ સલૂન કતાર અને સ્ટાફ સંચાલન",
    },
    "reception_btn_add_walkin": {
        "en": "+ Add Walk-in",
        "gu": "+ વૉક-ઇન ઉમેરો",
    },
    "reception_summary_waiting": {
        "en": "Waiting in Line",
        "gu": "પ્રતીક્ષામાં",
    },
    "reception_summary_inservice": {
        "en": "In Service / Chairs",
        "gu": "સેવા ચાલુ / ચેર",
    },
    "reception_summary_completed": {
        "en": "Completed Today",
        "gu": "આજે પૂર્ણ થયેલ",
    },
    "reception_summary_noshow": {
        "en": "No-Shows",
        "gu": "ગેરહાજર",
    },
    "reception_team_heading": {
        "en": "Staff & Styling Stations",
        "gu": "સ્ટાફ અને સ્ટાઇલિંગ સ્ટેશન્સ",
    },
    "reception_waiting_heading": {
        "en": "Live Waiting Queue",
        "gu": "લાઇવ પ્રતીક્ષા કતાર",
    },
    "reception_col_token": {
        "en": "Token",
        "gu": "ટોકન",
    },
    "reception_col_customer": {
        "en": "Customer",
        "gu": "ગ્રાહક",
    },
    "reception_col_services": {
        "en": "Services",
        "gu": "સેવાઓ",
    },
    "reception_col_stylist": {
        "en": "Preferred Staff",
        "gu": "પસંદગીનો સ્ટાફ",
    },
    "reception_col_waittime": {
        "en": "Est. Wait",
        "gu": "અંદાજિત રાહ",
    },
    "reception_col_actions": {
        "en": "Actions",
        "gu": "ક્રિયાઓ",
    },
    "reception_btn_noshow": {
        "en": "No-show",
        "gu": "નો-શો",
    },
    "reception_btn_cancel": {
        "en": "Cancel",
        "gu": "રદ કરો",
    },
    "reception_btn_call_next": {
        "en": "Call Next",
        "gu": "આગળ બોલાવો",
    },
    "reception_empty_queue": {
        "en": "No customers currently waiting in line. Walk right in!",
        "gu": "હાલમાં કોઈ ગ્રાહક પ્રતીક્ષામાં નથી. સીધા અંદર આવી શકો છો!",
    },
    "reception_over_60_tag": {
        "en": "⚠️ Priority: Wait > 60 min",
        "gu": "⚠️ પ્રાથમિકતા: રાહ > 60 મિનિટ",
    },
    "walkin_dialog_title": {
        "en": "Register Walk-in Customer",
        "gu": "વૉક-ઇન ગ્રાહક નોંધણી",
    },
    "walkin_btn_submit": {
        "en": "Add to Queue",
        "gu": "કતારમાં ઉમેરો",
    },
    "walkin_btn_cancel": {
        "en": "Close",
        "gu": "બંધ કરો",
    },
    "noshow_dialog_title": {
        "en": "Confirm No-Show",
        "gu": "ગેરહાજર પુષ્ટિ કરો",
    },
    "noshow_btn_confirm": {
        "en": "Confirm No-Show",
        "gu": "ગેરહાજર ચિહ્નિત કરો",
    },
    "cancel_dialog_title": {
        "en": "Confirm Cancellation",
        "gu": "રદ કરવાની પુષ્ટિ કરો",
    },
    "cancel_btn_confirm": {
        "en": "Confirm Cancellation",
        "gu": "રદ કરવાની પુષ્ટિ કરો",
    },
    "dialog_btn_keep": {
        "en": "Keep in Queue",
        "gu": "કતારમાં ચાલુ રાખો",
    },
    # Screen 5: Barber View Translations
    "barber_view_title": {
        "en": "Barber & Stylist Workstation",
        "gu": "બાર્બર અને સ્ટાઈલિસ્ટ વર્કસ્ટેશન",
    },
    "barber_view_subtitle": {
        "en": "Live station management, active service stopwatch, and queue dispatching.",
        "gu": "લાઈવ સ્ટેશન સંચાલન, સેવા સ્ટોપવોચ અને કતાર નિયંત્રણ.",
    },
    "barber_station_select": {
        "en": "Select Station:",
        "gu": "સ્ટેશન પસંદ કરો:",
    },
    "barber_status_available": {
        "en": "Available",
        "gu": "ઉપલબ્ધ",
    },
    "barber_status_inservice": {
        "en": "In Service",
        "gu": "સેવામાં",
    },
    "barber_status_break": {
        "en": "On Break",
        "gu": "વિરામ પર",
    },
    "barber_toggle_take_break": {
        "en": "☕ Go On Break",
        "gu": "☕ વિરામ લો",
    },
    "barber_toggle_resume": {
        "en": "🟢 Set Available",
        "gu": "🟢 ઉપલબ્ધ થાઓ",
    },
    "barber_queued_break_alert": {
        "en": "Break request queued. Will activate automatically once current customer is finished.",
        "gu": "વિરામ વિનંતી નોંધાઈ ગઈ છે. વર્તમાન ગ્રાહક પૂર્ણ થતાં આપોઆપ સક્રિય થશે.",
    },
    "barber_queued_break_badge": {
        "en": "☕ Break Queued",
        "gu": "☕ વિરામ નોંધાયેલ છે",
    },
    "barber_cancel_queued_break": {
        "en": "Cancel Queued Break",
        "gu": "નોંધાયેલ વિરામ રદ કરો",
    },
    "barber_curr_customer_title": {
        "en": "Current In-Chair Customer",
        "gu": "વર્તમાન ગ્રાહક",
    },
    "barber_no_current_customer": {
        "en": "No customer currently at your station.",
        "gu": "તમારા સ્ટેશન પર હાલમાં કોઈ ગ્રાહક નથી.",
    },
    "barber_btn_call_next": {
        "en": "🔔 Call Next Customer",
        "gu": "🔔 આગળના ગ્રાહકને બોલાવો",
    },
    "barber_btn_start": {
        "en": "▶️ Start Service",
        "gu": "▶️ સેવા શરૂ કરો",
    },
    "barber_btn_done": {
        "en": "✅ Complete Service (Done)",
        "gu": "✅ સેવા પૂર્ણ કરો (સમાપ્ત)",
    },
    "barber_timer_elapsed": {
        "en": "Service Elapsed Time",
        "gu": "વીતેલો સેવા સમય",
    },
    "barber_timer_ready": {
        "en": "Timer starts automatically when you click Start",
        "gu": "સ્ટાર્ટ પર ક્લિક કરતાં ટાઈમર શરૂ થશે",
    },
    "barber_next_preview_title": {
        "en": "Next for You in Queue",
        "gu": "કતારમાં આગળનું સ્થાન",
    },
    "barber_no_next_customer": {
        "en": "No upcoming customers waiting for your station.",
        "gu": "તમારા સ્ટેશન માટે આગળ કોઈ ગ્રાહક પ્રતીક્ષામાં નથી.",
    },
    "barber_done_dialog_title": {
        "en": "Confirm Service Completion",
        "gu": "સેવા પૂર્ણતાની પુષ્ટિ કરો",
    },
    "barber_done_dialog_msg": {
        "en": "Confirm service completion for {name} (Token {token})?",
        "gu": "શું તમે {name} (ટોકન {token}) માટે સેવા પૂર્ણ કરવા માંગો છો?",
    },
    "barber_done_btn_confirm": {
        "en": "Yes, Complete Service",
        "gu": "હા, સેવા પૂર્ણ કરો",
    },
    "barber_done_btn_cancel": {
        "en": "Keep In Progress",
        "gu": "સેવા ચાલુ રાખો",
    },
    # Screen 6: Waiting Area TV Translations
    "display_view_title": {
        "en": "Waiting Area Live Display",
        "gu": "પ્રતીક્ષા વિસ્તાર લાઈવ ડિસ્પ્લે",
    },
    "display_view_subtitle": {
        "en": "Real-time service progress & upcoming queue order",
        "gu": "રીઅલ-ટાઇમ સેવા પ્રગતિ અને આગામી કતાર ક્રમ",
    },
    "display_now_calling": {
        "en": "🔔 NOW CALLING",
        "gu": "🔔 હવે બોલાવવામાં આવે છે",
    },
    "display_proceed_to": {
        "en": "Please proceed to {station} ({staff})",
        "gu": "કૃપા કરીને {station} ({staff}) પર જાઓ",
    },
    "display_active_stations_heading": {
        "en": "Stylist & Barber Stations",
        "gu": "સ્ટાઈલિસ્ટ અને બાર્બર સ્ટેશનો",
    },
    "display_station_now": {
        "en": "Now: {token}",
        "gu": "હવે: {token}",
    },
    "display_station_calling": {
        "en": "Calling: {token}",
        "gu": "બોલાવે છે: {token}",
    },
    "display_station_free": {
        "en": "Ready for Next",
        "gu": "આગળના માટે તૈયાર",
    },
    "display_station_break": {
        "en": "On Break",
        "gu": "વિરામ પર",
    },
    "display_upnext_heading": {
        "en": "Up Next in Queue (Next 5 Guests)",
        "gu": "કતારમાં આગળ (આગામી ૫ ગ્રાહકો)",
    },
    "display_empty_queue": {
        "en": "No customers currently waiting in line. Walk right in!",
        "gu": "હાલમાં કોઈ ગ્રાહક પ્રતીક્ષામાં નથી. સીધા અંદર આવી શકો છો!",
    },
    "display_footer_thanks": {
        "en": "✨ Thank you for choosing SALt N' PEPPER · Complimentary refreshments, herbal teas & high-speed Wi-Fi available at reception",
        "gu": "✨ SALt N' PEPPER પસંદ કરવા બદલ આભાર · રિસેપ્શન પર મફત નાસ્તો, હર્બલ ચા અને વાઇ-ફાઇ ઉપલબ્ધ છે",
    },
    "display_footer_hours": {
        "en": "Open Daily until 09:00 PM",
        "gu": "રોજ રાત્રે ૦૯:૦૦ વાગ્યા સુધી ખુલ્લું",
    },
    # Screen 7: Owner Settings Translations
    "admin_view_title": {
        "en": "Owner Dashboard & Settings",
        "gu": "માલિક ડેશબોર્ડ અને સેટિંગ્સ",
    },
    "admin_view_subtitle": {
        "en": "Manage salon services, team duty roster, online queue availability and daily metrics.",
        "gu": "સેવાઓ, સ્ટાફ ફરજ, ઓનલાઇન કતાર ઉપલબ્ધતા અને દૈનિક પરિણામોનું સંચાલન કરો.",
    },
    "admin_stats_heading": {
        "en": "Today's Salon Performance",
        "gu": "આજનું સલૂન પ્રદર્શન",
    },
    "admin_stat_served": {
        "en": "Customers Served",
        "gu": "સેવા આપેલ ગ્રાહકો",
    },
    "admin_stat_avg_wait": {
        "en": "Avg. Waiting Time",
        "gu": "સરેરાશ રાહ સમય",
    },
    "admin_stat_noshows": {
        "en": "No-Shows",
        "gu": "ગેરહાજર",
    },
    "admin_stat_queue_active": {
        "en": "Currently in Queue",
        "gu": "હાલમાં કતારમાં",
    },
    "admin_queue_control_heading": {
        "en": "Online Queue Access Control",
        "gu": "ઓનલાઇન કતાર પ્રવેશ નિયંત્રણ",
    },
    "admin_queue_status_label": {
        "en": "Online Queue Joining Status",
        "gu": "ઓનલાઇન કતાર જોડાણ સ્થિતિ",
    },
    "admin_queue_open_desc": {
        "en": "When Open, customers can join the live queue online via their mobile phones.",
        "gu": "ખુલ્લું હોય ત્યારે, ગ્રાહકો તેમના ફોન પરથી લાઈવ કતારમાં જોડાઈ શકે છે.",
    },
    "admin_queue_closed_desc": {
        "en": "When Closed, online bookings are stopped. Receptionist in-person walk-ins remain available.",
        "gu": "બંધ હોય ત્યારે, નવી ઓનલાઇન બુકિંગ અટકાવી દેવાય છે. રૂબરૂ વૉક-ઇન ચાલુ રહે છે.",
    },
    "admin_queue_toggle_open": {
        "en": "🟢 Open Online Queue",
        "gu": "🟢 ઓનલાઇન કતાર ખોલો",
    },
    "admin_queue_toggle_close": {
        "en": "🔴 Close Online Queue",
        "gu": "🔴 ઓનલાઇન કતાર બંધ કરો",
    },
    "admin_services_heading": {
        "en": "Manage Salon Services (₹250 – ₹1,200)",
        "gu": "સલૂન સેવાઓનું સંચાલન (₹૨૫૦ – ₹૧,૨૦૦)",
    },
    "admin_service_name_en": {
        "en": "Service Name (English)",
        "gu": "સેવાનું નામ (અંગ્રેજી)",
    },
    "admin_service_name_gu": {
        "en": "Service Name (Gujarati)",
        "gu": "સેવાનું નામ (ગુજરાતી)",
    },
    "admin_service_price": {
        "en": "Price (₹)",
        "gu": "કિંમત (₹)",
    },
    "admin_service_duration": {
        "en": "Duration (min)",
        "gu": "સમય (મિનિટ)",
    },
    "admin_service_status": {
        "en": "Active Status",
        "gu": "સક્રિય સ્થિતિ",
    },
    "admin_service_active": {
        "en": "Active",
        "gu": "સક્રિય",
    },
    "admin_service_inactive": {
        "en": "Inactive",
        "gu": "નિષ્ક્રિય",
    },
    "admin_staff_heading": {
        "en": "Staff Duty Roster",
        "gu": "સ્ટાફ ફરજ રોસ્ટર",
    },
    "admin_staff_duty_on": {
        "en": "On Duty",
        "gu": "ફરજ પર",
    },
    "admin_staff_duty_off": {
        "en": "Off Duty",
        "gu": "ફરજ બંધ",
    },
    "admin_btn_save_all": {
        "en": "💾 Save All Changes",
        "gu": "💾 બધા ફેરફારો સાચવો",
    },
    "admin_save_success": {
        "en": "Settings successfully updated and synchronized across all salon screens!",
        "gu": "સેટિંગ્સ સફળતાપૂર્વક અપડેટ થઈ ગયા છે અને બધા સ્ક્રીન પર સિંક થયા છે!",
    },
    "admin_save_dialog_title": {
        "en": "Confirm Settings Update",
        "gu": "સેટિંગ્સ અપડેટની પુષ્ટિ કરો",
    },
    "admin_save_dialog_msg": {
        "en": "Apply and synchronize these service prices, duty rosters, and queue settings across all screens?",
        "gu": "શું તમે આ સેવા કિંમતો, સ્ટાફ ફરજ અને કતાર સેટિંગ્સ લાગુ કરવા માંગો છો?",
    },
    "admin_save_dialog_btn_confirm": {
        "en": "Yes, Apply Changes",
        "gu": "હા, ફેરફારો લાગુ કરો",
    },
    "admin_save_dialog_btn_cancel": {
        "en": "Keep Editing",
        "gu": "ફેરફાર ચાલુ રાખો",
    },
}


def t(key: str, lang: str = "en") -> str:
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("en", key))


# ==============================================================================
# 4. STATE INITIALIZATION & RELIABLE NAVIGATION
# ==============================================================================

if "lang" not in st.session_state:
    st.session_state.lang = "en"

if "selected_services" not in st.session_state:
    st.session_state.selected_services = set()

if "selected_barber" not in st.session_state:
    st.session_state.selected_barber = "any"

if "cust_name" not in st.session_state:
    st.session_state.cust_name = ""

if "cust_phone" not in st.session_state:
    st.session_state.cust_phone = ""

if "service_limit_warning" not in st.session_state:
    st.session_state.service_limit_warning = False

if "staff_authenticated" not in st.session_state:
    st.session_state.staff_authenticated = False

if "pin_error" not in st.session_state:
    st.session_state.pin_error = None

STAFF_PIN = "2026"
PROTECTED_SCREENS = {"reception", "barber", "admin"}

SCREENS_LIST = [
    ("home", "nav_home", "🏠"),
    ("join", "nav_join", "📝"),
    ("status", "nav_status", "⏱️"),
    ("reception", "nav_reception", "📋"),
    ("barber", "nav_barber", "✂️"),
    ("display", "nav_display", "📺"),
    ("admin", "nav_admin", "⚙️"),
]


def navigate_to(screen_name: str, **params):
    """Safe navigation helper: updates state and query params without mutating instantiated widgets."""
    st.session_state.active_screen = screen_name
    st.query_params["page"] = screen_name
    for k, v in params.items():
        st.query_params[k] = str(v)
        if k == "id":
            st.session_state["active_token"] = str(v)
    st.session_state["pending_nav_screen"] = screen_name
    st.rerun()


# ==============================================================================
# 5. HEADER & SIDEBAR NAVIGATION
# ==============================================================================

def render_top_bar():
    """Renders the clean, minimal luxury salon header with navigation and language toggle."""
    lang = st.session_state.lang

    col_brand, col_nav, col_lang = st.columns([3, 4, 2])

    with col_brand:
        st.markdown(
            f"""
            <div class="top-brand-header" style="padding-top: 0.25rem;">
                <h1 class="salon-wordmark" style="font-size: 1.85rem;">{t('app_wordmark', lang)}</h1>
                <small style="font-size: 0.75rem; color: var(--charcoal-muted); letter-spacing: 1.2px; text-transform: uppercase;">
                    {t('tagline', lang)}
                </small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_nav:
        st.markdown(
            f"""
            <div class="top-nav-links" style="display: flex; gap: 1.25rem; align-items: center; justify-content: center; height: 100%; padding-top: 0.6rem; flex-wrap: wrap;">
                <a href="?page=home" class="nav-link-item"><strong>{t('nav_home', lang)}</strong></a>
                <a href="?page=home#about" class="nav-link-item">{t('nav_about', lang)}</a>
                <a href="?page=home#services" class="nav-link-item">{t('nav_services', lang)}</a>
                <a href="?page=join" class="nav-link-item" style="color: var(--orange-red); font-weight: 600;">{t('nav_join', lang)}</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_lang:
        selected_lang = st.radio(
            label="Language / ભાષા",
            options=["English", "ગુજરાતી"],
            index=0 if lang == "en" else 1,
            horizontal=True,
            label_visibility="collapsed",
            key="lang_toggle_radio",
        )
        new_lang = "en" if selected_lang == "English" else "gu"
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()

    st.markdown('<hr style="margin: 0.5rem 0 1.25rem 0; border: none; border-bottom: 1px solid rgba(227, 154, 158, 0.35);">', unsafe_allow_html=True)


def on_sidebar_nav_change():
    """Callback triggered whenever user clicks an option in the sidebar radio."""
    current_lang = st.session_state.get("lang", "en")
    nav_options = [f"{icon} {t(nav_key, current_lang)}" for _, nav_key, icon in SCREENS_LIST]
    screen_keys = [key for key, _, _ in SCREENS_LIST]

    selected_label = st.session_state.get("screen_nav_radio")
    if selected_label in nav_options:
        target_screen = screen_keys[nav_options.index(selected_label)]
        st.session_state.active_screen = target_screen
        st.query_params["page"] = target_screen


def render_desktop_sidebar_hover():
    """Desktop interaction: auto-expands sidebar on hover, auto-collapses on mouseleave.
    Mobile/touch devices: completely disabled, preserving native tap-to-open and tap-to-close."""
    components.html(
        """
        <script>
        (function() {
            try {
                const parentWin = window.parent;
                if (!parentWin || !parentWin.document) return;
                const parentDoc = parentWin.document;

                // STRICT DESKTOP CHECK: fine pointer (mouse), hover capability, and viewport width > 768px
                const isDesktop = parentWin.matchMedia('(min-width: 769px) and (hover: hover) and (pointer: fine)').matches;
                if (!isDesktop) return; // Do NOT attach hover listeners on mobile/touch devices

                // Cleanup any existing listeners
                if (parentWin.__salonSidebarCleanup) {
                    parentWin.__salonSidebarCleanup();
                }

                let collapseTimer = null;
                let isExpanding = false;

                function getSidebar() {
                    return parentDoc.querySelector('section[data-testid="stSidebar"]');
                }

                function getExpandButton() {
                    return parentDoc.querySelector('button[data-testid="stExpandSidebarButton"]') ||
                           parentDoc.querySelector('button[aria-label="Expand sidebar"]');
                }

                function getCollapseButton() {
                    const sb = getSidebar();
                    if (!sb) return null;
                    return sb.querySelector('button[aria-label="Collapse sidebar"]') ||
                           sb.querySelector('button[data-testid="stBaseButton-headerNoPadding"][aria-label="Collapse sidebar"]');
                }

                function isSidebarOpen() {
                    const sb = getSidebar();
                    if (!sb) return false;
                    const rect = sb.getBoundingClientRect();
                    return rect.width > 50 && rect.right > 50;
                }

                function expandSidebar() {
                    if (isSidebarOpen() || isExpanding) return;
                    const btn = getExpandButton();
                    if (btn) {
                        isExpanding = true;
                        btn.click();
                        setTimeout(() => { isExpanding = false; }, 350);
                    }
                }

                function collapseSidebar() {
                    if (!isSidebarOpen()) return;
                    const btn = getCollapseButton();
                    if (btn) {
                        btn.click();
                    }
                }

                function onMouseMove(e) {
                    const open = isSidebarOpen();

                    if (!open) {
                        // Mouse enters within 36px of left viewport edge or over the expand button
                        if (e.clientX <= 36 || (e.clientX <= 65 && e.clientY <= 65)) {
                            if (collapseTimer) {
                                clearTimeout(collapseTimer);
                                collapseTimer = null;
                            }
                            expandSidebar();
                        }
                    } else {
                        const sb = getSidebar();
                        if (sb) {
                            const rect = sb.getBoundingClientRect();
                            // Inside sidebar area
                            if (e.clientX <= rect.right + 15) {
                                if (collapseTimer) {
                                    clearTimeout(collapseTimer);
                                    collapseTimer = null;
                                }
                            } else {
                                // Mouse left sidebar area: start smooth collapse grace timer
                                if (!collapseTimer) {
                                    collapseTimer = setTimeout(() => {
                                        collapseSidebar();
                                        collapseTimer = null;
                                    }, 220);
                                }
                            }
                        }
                    }
                }

                parentDoc.addEventListener('mousemove', onMouseMove, { passive: true });

                parentWin.__salonSidebarCleanup = function() {
                    parentDoc.removeEventListener('mousemove', onMouseMove);
                    if (collapseTimer) clearTimeout(collapseTimer);
                };
            } catch (err) {
                // Graceful fallback
            }
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def render_navigation_sidebar() -> str:
    """Renders the developer and reviewer screen navigator in the sidebar."""
    render_desktop_sidebar_hover()
    current_lang = st.session_state.get("lang", "en")
    nav_options = [f"{icon} {t(nav_key, current_lang)}" for _, nav_key, icon in SCREENS_LIST]
    screen_keys = [key for key, _, _ in SCREENS_LIST]

    # Process pending navigation before instantiating the radio widget
    if "pending_nav_screen" in st.session_state:
        pending = st.session_state.pop("pending_nav_screen")
        if pending in screen_keys:
            st.session_state.active_screen = pending
            st.query_params["page"] = pending

    # Resolve active screen from query params or session state
    query_page = st.query_params.get("page", None)
    if query_page and query_page in screen_keys:
        active_screen = query_page
    else:
        active_screen = st.session_state.get("active_screen", "home")
        if active_screen not in screen_keys:
            active_screen = "home"

    st.session_state.active_screen = active_screen
    default_idx = screen_keys.index(active_screen)
    expected_label = nav_options[default_idx]

    # Safely synchronize widget state BEFORE the widget is created
    if st.session_state.get("screen_nav_radio") != expected_label:
        st.session_state["screen_nav_radio"] = expected_label

    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid rgba(217, 104, 79, 0.2); margin-bottom: 1rem;">
                <h3 class="salon-wordmark" style="font-size: 1.3rem;">{t('app_wordmark', current_lang)}</h3>
                <small style="color: var(--charcoal-muted);">Screen Navigator (All 7 Screens)</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.radio(
            "Select Screen",
            options=nav_options,
            label_visibility="collapsed",
            key="screen_nav_radio",
            on_change=on_sidebar_nav_change,
        )

        if st.session_state.get("staff_authenticated", False):
            st.markdown(
                f"""
                <div style="background: rgba(135, 155, 120, 0.15); border: 1px solid var(--fresh-sage); border-radius: 8px; padding: 0.45rem 0.65rem; margin-top: 0.85rem; margin-bottom: 0.4rem; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.78rem; font-weight: 700; color: #4B6338;">● {t('pin_staff_logged_in', current_lang)}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"🔒 {t('pin_btn_logout', current_lang)}", key="sidebar_staff_logout_btn", use_container_width=True):
                st.session_state.staff_authenticated = False
                st.session_state.pin_error = None
                st.rerun()

        # Dedicated testing and verification panel completely separated from customer screens
        render_queue_testing_panel()

        return active_screen


def render_queue_testing_panel():
    """Renders the testing & simulation controls in the sidebar, completely isolated from customer screens."""
    data_mgr = get_data_manager()
    active_token = st.session_state.get("active_token", "S-14")

    st.markdown("<hr style='margin: 1.25rem 0 0.8rem 0; border: none; border-bottom: 1px solid rgba(227, 154, 158, 0.35);'>", unsafe_allow_html=True)
    with st.expander("🧪 Queue Testing & Verification (docs/03-flows-rules.md)", expanded=False):
        st.markdown(
            """
            <small style='color: var(--charcoal-muted); line-height: 1.35; display: block;'>
            <strong>Testing Checklist Actions:</strong><br>
            Execute live queue lifecycle actions and manual test scenarios without altering customer-facing screen UI.
            </small>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)

        # Select target ticket to test
        all_tokens = [t["token"] for t in data_mgr.queue]
        if not all_tokens:
            st.caption("No tickets in queue.")
            if st.button("🔄 Reset Queue", key="sb_btn_reset_empty"):
                data_mgr.reset_queue()
                st.session_state["active_token"] = "S-14"
                st.rerun()
            return

        default_tok_idx = all_tokens.index(active_token) if active_token in all_tokens else 0
        target_token = st.selectbox(
            "Target Queue Token",
            options=all_tokens,
            index=default_tok_idx,
            key="sb_target_token_select",
        )

        target_ticket = data_mgr.get_ticket(target_token)
        if target_ticket:
            st.caption(f"Status: **{target_ticket['status']}** | Guest: **{target_ticket['customer_name']}** | Pref: **{target_ticket.get('barber_pref', 'any')}**")

        st.markdown("**1. Required Queue Actions:**")
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("🔔 Call Next", key="sb_btn_call_next", use_container_width=True):
                called_t = data_mgr.call_next()
                if called_t:
                    st.session_state["active_token"] = called_t["token"]
                st.rerun()
            if st.button("✂️ Start", key="sb_btn_start_service", use_container_width=True):
                data_mgr.start_service(target_token)
                st.session_state["active_token"] = target_token
                st.rerun()
        with col_act2:
            if st.button("✅ Done", key="sb_btn_complete_service", use_container_width=True):
                data_mgr.complete_service(target_token)
                st.session_state["active_token"] = target_token
                st.rerun()
            if st.button("⏱️ No-Show", key="sb_btn_no_show", use_container_width=True):
                data_mgr.mark_no_show(target_token)
                st.session_state["active_token"] = target_token
                st.rerun()

        if st.button("🚫 Cancel Spot", key="sb_btn_cancel_ticket", use_container_width=True):
            data_mgr.cancel_ticket(target_token)
            st.session_state["active_token"] = target_token
            st.rerun()

        st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
        st.markdown("**2. Manual Queue Scenarios:**")
        col_sc1, col_sc2 = st.columns(2)
        with col_sc1:
            if st.button("🚀 Pos 2 Alert", key="sb_btn_pos2_scenario", use_container_width=True):
                data_mgr.set_position_2_scenario(target_token)
                st.session_state["active_token"] = target_token
                st.rerun()
        with col_sc2:
            if st.button("🔄 Reset Queue", key="sb_btn_reset_full", use_container_width=True):
                data_mgr.reset_queue()
                st.session_state["active_token"] = "S-14"
                st.rerun()

        st.markdown(
            """
            <small style='color: var(--charcoal-muted); line-height: 1.3; display: block; margin-top: 0.4rem;'>
            ✓ TC-01 to TC-14 compliant.<br>
            ✓ Customer screens remain 100% pure & unadulterated.
            </small>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# 5B. STAFF AUTHENTICATION & SESSION MANAGEMENT
# ==============================================================================

def render_staff_session_bar():
    """Renders a sleek, unobtrusive staff session header bar with a Log Out button on staff screens."""
    lang = st.session_state.get("lang", "en")
    active_scr = st.session_state.get("active_screen", "staff")

    col_status, col_act = st.columns([8, 2.5], vertical_alignment="center")
    with col_status:
        st.markdown(
            f"""
            <div style="font-size: 0.82rem; font-weight: 600; color: #4B6338; display: flex; align-items: center; gap: 0.45rem; padding: 0.2rem 0;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--fresh-sage);"></span>
                <span>{t('pin_staff_logged_in', lang)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_act:
        if st.button(f"🔒 {t('pin_btn_logout', lang)}", key=f"staff_bar_logout_{active_scr}", use_container_width=True):
            st.session_state.staff_authenticated = False
            st.session_state.pin_error = None
            st.rerun()
    st.markdown('<hr style="margin: 0.25rem 0 0.85rem 0; border: none; border-bottom: 1px dashed rgba(227, 154, 158, 0.4);">', unsafe_allow_html=True)


def render_screen_staff_pin(target_screen: str):
    """Screen for staff PIN entry to protect Reception, Barber, and Admin screens."""
    lang = st.session_state.get("lang", "en")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 1.4, 1])
    with col_center:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="pin-card-wrapper">
                    <div class="pin-card-header">
                        <div class="salon-wordmark">{t('app_wordmark', lang)}</div>
                        <div style="margin-top: 0.25rem;">
                            <span class="pin-access-badge">{t('pin_staff_access', lang)}</span>
                        </div>
                        <h2 class="pin-main-heading">{t('pin_welcome_back', lang)}</h2>
                        <p class="pin-instruction-text">{t('pin_enter_instruction', lang)}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Display error message if incorrect PIN was submitted
            if st.session_state.get("pin_error"):
                st.markdown(
                    f"""
                    <div class="pin-error-box">
                        ⚠️ {st.session_state['pin_error']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.form("staff_pin_auth_form", clear_on_submit=False, border=False):
                pin_val = st.text_input(
                    label=t("pin_input_label", lang),
                    type="password",
                    max_chars=8,
                    placeholder=t("pin_input_placeholder", lang),
                    label_visibility="collapsed",
                    key="staff_pin_entry_input",
                )

                unlock_clicked = st.form_submit_button(
                    f"🔓 {t('pin_btn_unlock', lang)}",
                    type="primary",
                    use_container_width=True,
                )

                if unlock_clicked:
                    if pin_val.strip() == STAFF_PIN:
                        st.session_state.staff_authenticated = True
                        st.session_state.pin_error = None
                        st.rerun()
                    else:
                        st.session_state.staff_authenticated = False
                        st.session_state.pin_error = t("pin_err_incorrect", lang)
                        st.rerun()

            st.markdown("<div style='height: 0.25rem;'></div>", unsafe_allow_html=True)
            if st.button(t("pin_back_to_home", lang), key="pin_back_home_btn", use_container_width=True):
                st.session_state.pin_error = None
                navigate_to("home")

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)


# ==============================================================================
# 6. SCREEN 1: HOME (/) — PRESERVED & STREAMLINED LUXURY LANDING PAGE
# ==============================================================================

def render_screen_home():
    """Screen 1: Home (/) - Preserved luxury landing page."""
    lang = st.session_state.lang
    data_mgr = get_data_manager()

    # HERO SECTION
    hero_col_text, hero_col_photo = st.columns([6, 5], gap="large", vertical_alignment="center")

    with hero_col_text:
        is_open = data_mgr.is_online_queue_open()
        status_badge_html = f'<span class="badge-status-open"><span style="font-size: 0.6rem;">●</span> {t("status_open", lang)}</span>' if is_open else f'<span class="badge-status-closed">● {t("err_queue_closed", lang)}</span>'

        st.markdown(f'<div style="margin-bottom: 0.8rem;">{status_badge_html}</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <h1 class="salon-heading-serif" style="font-size: 3rem; margin: 0 0 1rem 0;">
                {t('hero_title', lang)}
            </h1>
            <p style="font-size: 1.1rem; line-height: 1.6; color: var(--charcoal-muted); margin-bottom: 1.25rem;">
                {t('hero_subtitle', lang)}
            </p>
            """,
            unsafe_allow_html=True,
        )

        # Small Live Queue Card
        st.markdown(
            f"""
            <div class="hero-queue-card">
                <div style="background-color: var(--golden-yellow); width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #30251F;">
                    4
                </div>
                <div>
                    <strong style="color: var(--charcoal-dark); font-size: 1rem; display: block;">
                        {t('hero_waiting_count', lang)}
                    </strong>
                    <span style="font-size: 0.88rem; color: var(--charcoal-muted);">
                        {t('hero_estimated_wait', lang)}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="btn-gold-cta">', unsafe_allow_html=True)
        if st.button("✨ " + t("btn_join_queue_cta", lang), key="hero_join_btn"):
            navigate_to("join")
        st.markdown('</div>', unsafe_allow_html=True)

    with hero_col_photo:
        hero_img_b64 = get_image_base64("assets/hero_beauty.jpg")
        st.markdown(
            f"""
            <div class="home-hero-sanctuary-frame" style="width: 100%; height: 380px; border-radius: 18px; overflow: hidden; border: 2px solid var(--card-border); box-shadow: 0 12px 36px rgba(48, 37, 31, 0.08); background: #FFF4D6;">
                <img src="{hero_img_b64}" style="width: 100%; height: 100%; object-fit: cover; object-position: center 30%; display: block;" alt="SALt N' PEPPER Sanctuary">
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # SERVICES SECTION (Consistent 600x400 photography)
    st.markdown('<div id="services"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; max-width: 700px; margin: 0 auto 2rem auto;">
            <span class="section-eyebrow">{t('services_eyebrow', lang)}</span>
            <h2 class="salon-heading-serif" style="font-size: 2.2rem; margin-top: 0.2rem;">
                {t('services_title', lang)}
            </h2>
            <p style="color: var(--charcoal-muted); font-size: 0.95rem; line-height: 1.5;">
                {t('services_subtitle', lang)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s1, s2, s3, s4 = st.columns(4, gap="medium")
    services = data_mgr.get_services()
    for col, (sid, sinfo) in zip([s1, s2, s3, s4], services.items()):
        with col:
            with st.container(border=True):
                st.image(sinfo["image"], use_container_width=True)
                s_name = sinfo[f"name_{lang}"]
                s_desc = sinfo[f"desc_{lang}"]
                st.markdown(f"<h4 style='color: var(--orange-red); margin: 0.5rem 0 0.2rem 0;'>{s_name}</h4>", unsafe_allow_html=True)
                st.markdown(f"**₹{sinfo['price']}** · <small style='color: #7D5B15;'>⏱️ {sinfo['duration']} min</small>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: var(--charcoal-muted); font-size: 0.85rem; line-height: 1.4; margin-top: 0.4rem; min-height: 60px;'>{s_desc}</p>", unsafe_allow_html=True)

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # TEAM SECTION (Consistent 400x480 photography & neutral placeholders)
    st.markdown(
        f"""
        <div style="text-align: center; max-width: 700px; margin: 0 auto 2rem auto;">
            <span class="section-eyebrow">{t('team_eyebrow', lang)}</span>
            <h2 class="salon-heading-serif" style="font-size: 2.2rem; margin-top: 0.2rem;">
                {t('team_title', lang)}
            </h2>
            <p style="color: var(--charcoal-muted); font-size: 0.95rem; line-height: 1.5;">
                {t('team_subtitle', lang)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t1, t2, t3, t4 = st.columns(4, gap="medium")
    staff_members = data_mgr.get_staff()
    for col, (st_id, st_info) in zip([t1, t2, t3, t4], staff_members.items()):
        img_b64 = get_image_base64(st_info["image"])
        role_name = st_info[f"role_{lang}"]
        st_status = st_info["status"]
        badge_class = "badge-avail-free" if st_status == "Available" else ("badge-avail-busy" if st_status == "In Service" else "badge-avail-break")
        status_text = t(f"status_{st_status.lower().replace(' ', '_')}", lang)

        with col:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="home-staff-content">
                        <div>
                            <div class="home-staff-img-frame">
                                <img src="{img_b64}" alt="{st_info['name']}">
                            </div>
                            <div class="home-staff-name">{st_info['name']}</div>
                            <div class="home-staff-role">{role_name}</div>
                        </div>
                        <div class="home-staff-status"><span class="{badge_class}">● {status_text}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # ABOUT SECTION
    st.markdown('<div id="about"></div>', unsafe_allow_html=True)
    ab_photo_col, ab_text_col = st.columns([5, 6], gap="large")

    with ab_photo_col:
        st.image("assets/about_salon.jpg", use_container_width=True)

    with ab_text_col:
        st.markdown(
            f"""
            <span class="section-eyebrow">{t('about_eyebrow', lang)}</span>
            <h2 class="salon-heading-serif" style="font-size: 2.2rem; margin: 0.2rem 0 1rem 0;">
                {t('about_title', lang)}
            </h2>
            <p style="font-size: 1rem; line-height: 1.6; color: var(--charcoal-muted); margin-bottom: 0.8rem;">
                {t('about_text_p1', lang)}
            </p>
            <p style="font-size: 1rem; line-height: 1.6; color: var(--charcoal-muted); margin-bottom: 1.5rem;">
                {t('about_text_p2', lang)}
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="btn-gold-cta">', unsafe_allow_html=True)
        if st.button("✨ " + t("btn_join_queue_cta", lang), key="about_join_btn"):
            navigate_to("join")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # FOOTER
    st.markdown(
        f"""
        <footer style="border-top: 1px solid rgba(227, 154, 158, 0.35); padding: 2rem 0 1rem 0; text-align: center; color: var(--charcoal-muted); font-size: 0.9rem;">
            <h3 class="salon-wordmark" style="font-size: 1.5rem; margin-bottom: 0.4rem;">{t('app_wordmark', lang)}</h3>
            <p style="margin: 0.2rem 0;">{t('footer_hours', lang)}</p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem;">© 2026 SALt N' PEPPER. {t('footer_rights', lang)}</p>
        </footer>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 7. SCREEN 2: JOIN QUEUE (/join) — CLEAN 2-COLUMN GRID & EQUAL SIZED CARDS
# ==============================================================================

def render_screen_join():
    """Screen 2: Join Queue (/join) - Clean 2-column grid and reliable workflow."""
    lang = st.session_state.lang
    data_mgr = get_data_manager()

    # Back to Home
    if st.button(t("back_to_home", lang), key="back_to_home_btn"):
        navigate_to("home")

    st.markdown(
        f"""
        <div style="background: #FFFAEA; border: 1px solid var(--card-border); border-left: 6px solid var(--orange-red); border-radius: 14px; padding: 1.25rem 1.75rem; margin: 0.75rem 0 1.5rem 0; box-shadow: 0 4px 16px rgba(48, 37, 31, 0.04); min-height: 105px; display: flex; flex-direction: column; justify-content: center;">
            <span class="section-eyebrow" style="margin-bottom: 0.2rem;">Digital Concierge</span>
            <h2 class="salon-heading-serif" style="font-size: 2.2rem; margin: 0.15rem 0 0.4rem 0; line-height: 1.2;">
                {t('join_title', lang)}
            </h2>
            <p style="color: var(--charcoal-muted); font-size: 1rem; margin: 0; line-height: 1.5;">
                {t('join_subtitle', lang)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not data_mgr.is_online_queue_open():
        st.error(f"🛑 {t('err_queue_closed', lang)}")
        return

    # Two-column layout: Form on Left (7.6 cols), Live Summary on Right (4.4 cols)
    form_col, summary_col = st.columns([7.6, 4.4], gap="large")

    services = data_mgr.get_services()
    staff_dict = data_mgr.get_staff()

    with form_col:
        # ----------------------------------------------------------------------
        # 1. CUSTOMER DETAILS
        # ----------------------------------------------------------------------
        with st.container(border=True):
            st.markdown(
                f"""
                <span class="section-eyebrow">Guest Information</span>
                <h3 class="salon-heading-serif" style="font-size: 1.3rem; color: var(--orange-red); margin: 0.15rem 0 0.6rem 0;">
                    1. {t('step_customer_details', lang)}
                </h3>
                """,
                unsafe_allow_html=True,
            )

            c_name_col, c_phone_col = st.columns(2)
            with c_name_col:
                st.session_state.cust_name = st.text_input(
                    f"{t('full_name_label', lang)} *",
                    value=st.session_state.get("cust_name", ""),
                    placeholder=t("full_name_placeholder", lang),
                    key="cust_name_field",
                )

            with c_phone_col:
                st.session_state.cust_phone = st.text_input(
                    f"{t('phone_label', lang)} *",
                    value=st.session_state.get("cust_phone", ""),
                    placeholder=t("phone_placeholder", lang),
                    key="cust_phone_field",
                    max_chars=10,
                )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # 2. SERVICE SELECTION (2-COLUMN GRID, EQUAL-SIZED CARDS)
        # ----------------------------------------------------------------------
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.5rem;">
                <h3 class="salon-heading-serif" style="font-size: 1.3rem; color: var(--orange-red); margin: 0;">
                    2. {t('step_select_services', lang)}
                </h3>
                <span class="badge-selected-pill">{len(st.session_state.selected_services)} / 3 Selected</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.service_limit_warning:
            st.warning(f"⚠️ {t('err_services_max', lang)}")

        # Clean 2-column grid: Row 1 (Haircut & Styling), Row 2 (Hair Spa & Colouring)
        service_items = list(services.items())
        r1_c1, r1_c2 = st.columns(2, gap="medium")
        r2_c1, r2_c2 = st.columns(2, gap="medium")
        grid_cols = [r1_c1, r1_c2, r2_c1, r2_c2]

        for col, (sid, sinfo) in zip(grid_cols, service_items):
            is_selected = sid in st.session_state.selected_services
            s_name = sinfo[f"name_{lang}"]
            s_desc = sinfo[f"desc_{lang}"]

            with col:
                with st.container(border=True):
                    # Immediate image load with standardized 600x400 aspect ratio
                    st.image(sinfo["image"], use_container_width=True)

                    c_title, c_price = st.columns([3, 2])
                    with c_title:
                        st.markdown(f"**{s_name}**")
                    with c_price:
                        st.markdown(f"<div style='text-align: right; color: var(--orange-red); font-weight: 700;'>₹{sinfo['price']}</div>", unsafe_allow_html=True)

                    st.markdown(f"<small style='color: #7D5B15;'>⏱️ {sinfo['duration']} min</small>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: var(--charcoal-muted); font-size: 0.83rem; line-height: 1.4; min-height: 48px; margin: 0.25rem 0 0.5rem 0;'>{s_desc}</p>", unsafe_allow_html=True)

                    if is_selected:
                        st.markdown('<div style="margin-bottom: 0.35rem;"><span class="badge-selected-pill">✓ Selected</span></div>', unsafe_allow_html=True)
                        if st.button(t("btn_deselect", lang), key=f"desel_{sid}", use_container_width=True):
                            st.session_state.selected_services.remove(sid)
                            st.session_state.service_limit_warning = False
                            st.rerun()
                    else:
                        if st.button(f"+ {t('btn_select', lang)}", key=f"sel_{sid}", use_container_width=True):
                            if len(st.session_state.selected_services) >= 3:
                                st.session_state.service_limit_warning = True
                                st.rerun()
                            else:
                                st.session_state.selected_services.add(sid)
                                st.session_state.service_limit_warning = False
                                st.rerun()

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # 3. BARBER AND HAIRSTYLIST SELECTION
        # ----------------------------------------------------------------------
        st.markdown(
            f"""
            <h3 class="salon-heading-serif" style="font-size: 1.3rem; color: var(--orange-red); margin-bottom: 0.5rem;">
                3. {t('step_choose_barber', lang)}
            </h3>
            """,
            unsafe_allow_html=True,
        )

        # Any Barber (Fastest) Card - Default
        is_any_selected = st.session_state.selected_barber == "any"
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="badge-status-open" style="margin-bottom: 0.2rem;">RECOMMENDED</span>
                        <h4 style="margin: 0; font-size: 1.1rem; color: var(--charcoal-dark); font-weight: 700;">
                            ⚡ {t('barber_any_title', lang)}
                        </h4>
                        <p style="margin: 0.15rem 0 0 0; color: var(--charcoal-muted); font-size: 0.85rem;">
                            {t('barber_any_desc', lang)}
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if is_any_selected:
                st.markdown('<span class="badge-selected-pill" style="margin-top: 0.4rem;">✓ Selected (Default)</span>', unsafe_allow_html=True)
            else:
                if st.button("Choose Any Barber (Fastest)", key="select_any_barber_btn", use_container_width=True):
                    st.session_state.selected_barber = "any"
                    st.rerun()

        st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)
        st.caption("Or choose an individual on-duty professional (Only available professionals can be selected):")

        # 4 Staff Columns (One evenly spaced row, equal widths & heights, perfectly aligned)
        b_c1, b_c2, b_c3, b_c4 = st.columns(4, gap="small")
        for col, (st_id, st_info) in zip([b_c1, b_c2, b_c3, b_c4], staff_dict.items()):
            is_st_selected = st.session_state.selected_barber == st_id
            st_status = st_info["status"]
            is_available = st_status == "Available"
            role_name = st_info[f"role_{lang}"]
            badge_class = "badge-avail-free" if st_status == "Available" else ("badge-avail-busy" if st_status == "In Service" else "badge-avail-break")
            status_text = t(f"status_{st_status.lower().replace(' ', '_')}", lang)
            img_b64 = get_image_base64(st_info["image"])
            sel_class = "is-selected" if is_st_selected else ""

            with col:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="join-staff-content {sel_class}">
                            <div class="join-staff-img-frame">
                                <img src="{img_b64}" alt="{st_info['name']}">
                            </div>
                            <div class="join-staff-name">{st_info['name']}</div>
                            <div class="join-staff-role">{role_name}</div>
                            <div class="join-staff-status"><span class="{badge_class}">● {status_text}</span></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Aligned button row across all 4 cards
                    if is_available:
                        if is_st_selected:
                            st.button(f"✓ " + t("btn_selected_stylist", lang), key=f"btn_staff_sel_{st_id}", disabled=True, use_container_width=True)
                        else:
                            if st.button(t("btn_select_stylist", lang), key=f"btn_staff_{st_id}", use_container_width=True):
                                st.session_state.selected_barber = st_id
                                st.rerun()
                    else:
                        st.button(t("btn_unavailable_stylist", lang), key=f"btn_staff_disabled_{st_id}", disabled=True, use_container_width=True)

    # --------------------------------------------------------------------------
    # 4. BOOKING SUMMARY & CONFIRMATION (Right Column)
    # --------------------------------------------------------------------------
    with summary_col:
        st.markdown(
            f"""
            <div class="summary-card">
                <span class="section-eyebrow">Real-Time Estimation</span>
                <h3 class="salon-heading-serif" style="font-size: 1.6rem; margin: 0.15rem 0 0.8rem 0;">
                    {t('booking_summary_title', lang)}
                </h3>
            """,
            unsafe_allow_html=True,
        )

        c_name_display = st.session_state.cust_name.strip() if st.session_state.cust_name.strip() else "—"
        c_phone_display = st.session_state.cust_phone.strip() if st.session_state.cust_phone.strip() else "—"

        st.markdown(
            f"""
            <div style="font-size: 0.92rem; line-height: 1.5; margin-bottom: 0.8rem; padding-bottom: 0.8rem; border-bottom: 1px solid rgba(227, 154, 158, 0.35);">
                <div><strong>{t('full_name_label', lang)}:</strong> {c_name_display}</div>
                <div><strong>{t('phone_label', lang)}:</strong> {c_phone_display}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sel_service_ids = list(st.session_state.selected_services)
        if sel_service_ids:
            st.markdown("<strong>Selected Services:</strong>", unsafe_allow_html=True)
            for sid in sel_service_ids:
                sinfo = services.get(sid, {})
                s_name = sinfo.get(f"name_{lang}", sid)
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; font-size: 0.88rem; margin: 0.2rem 0;">
                        <span>• {s_name} ({sinfo.get('duration', 0)} min)</span>
                        <strong>₹{sinfo.get('price', 0)}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("<p style='color: var(--orange-red); font-size: 0.88rem;'>⚠️ No services selected. Please select 1 to 3 services above.</p>", unsafe_allow_html=True)

        tot_duration = sum(services[sid]["duration"] for sid in sel_service_ids if sid in services)
        tot_price = sum(services[sid]["price"] for sid in sel_service_ids if sid in services)

        if st.session_state.selected_barber == "any":
            barber_display = f"⚡ {t('barber_any_title', lang)}"
        else:
            staff_info = staff_dict.get(st.session_state.selected_barber, {})
            barber_display = f"{staff_info.get('name', '')} ({staff_info.get(f'role_{lang}', '')})"

        est_wait = data_mgr.calculate_estimated_wait(sel_service_ids, st.session_state.selected_barber)

        st.markdown(
            f"""
            <div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid rgba(227, 154, 158, 0.35);">
                <div style="display: flex; justify-content: space-between; font-size: 0.95rem; margin-bottom: 0.3rem;">
                    <span>Total Service Time:</span>
                    <strong>{tot_duration} min</strong>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem; margin-bottom: 0.75rem; color: var(--orange-red);">
                    <span>Total Price:</span>
                    <strong>₹{tot_price}</strong>
                </div>
                <div style="font-size: 0.88rem; margin-bottom: 0.85rem;">
                    <strong>Stylist:</strong> {barber_display}
                </div>
                <div style="background-color: rgba(230, 185, 87, 0.2); border-left: 4px solid var(--golden-yellow); padding: 0.65rem 0.9rem; border-radius: 8px; margin-bottom: 1.25rem;">
                    <span style="font-size: 0.78rem; color: #7D5B15; font-weight: 700; text-transform: uppercase;">Estimated Waiting Time</span>
                    <div style="font-size: 1.6rem; font-weight: 700; color: #30251F;">
                        {"~" + str(est_wait) + " min" if sel_service_ids else "—"}
                    </div>
                    <small style="color: var(--charcoal-muted);">Based on active queue and on-duty artists</small>
                </div>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # 5. CONFIRM & JOIN QUEUE BUTTON
        # ----------------------------------------------------------------------
        st.markdown('<div class="btn-gold-cta">', unsafe_allow_html=True)
        if st.button("🎟️ " + t("btn_confirm_join", lang), key="confirm_join_queue_action"):
            c_name = st.session_state.cust_name.strip()
            if not c_name:
                st.error(f"❌ {t('err_name_required', lang)}")
                return

            c_phone = re.sub(r"\D", "", st.session_state.cust_phone)
            if len(c_phone) != 10:
                st.error(f"❌ {t('err_phone_invalid', lang)}")
                return

            if len(st.session_state.selected_services) < 1:
                st.error(f"❌ {t('err_services_min', lang)}")
                return
            if len(st.session_state.selected_services) > 3:
                st.error(f"❌ {t('err_services_max', lang)}")
                return

            chosen_barber = st.session_state.selected_barber
            if chosen_barber != "any":
                staff_mem = staff_dict.get(chosen_barber)
                if not staff_mem or staff_mem["status"] != "Available" or not staff_mem["on_duty"]:
                    st.error(f"❌ {t('err_barber_unavailable', lang)}")
                    return

            if not data_mgr.is_online_queue_open():
                st.error(f"❌ {t('err_queue_closed', lang)}")
                return

            # Anti-Duplicate Check
            existing_ticket = data_mgr.get_active_ticket_by_phone(c_phone)
            if existing_ticket:
                existing_tok = existing_ticket["token"]
                st.warning(f"🔔 {t('msg_duplicate_spot', lang).format(token=existing_tok)}")
                navigate_to("status", id=existing_tok)
                return

            # Add Queue Entry
            new_ticket = data_mgr.add_queue_entry(
                customer_name=c_name,
                phone=c_phone,
                service_ids=list(st.session_state.selected_services),
                barber_pref=chosen_barber,
            )

            # Navigate reliably to Screen 3
            navigate_to("status", id=new_ticket["token"])

        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# 8. SCREEN 3: MY STATUS (/status/:id)
# ==============================================================================

def render_screen_status():
    """Screen 3: My Status (/status/:id) - Real-time queue tracker and booking status."""
    lang = st.session_state.lang
    data_mgr = get_data_manager()

    # Back to Home
    if st.button(t("back_to_home", lang), key="status_back_home_btn"):
        navigate_to("home")

    active_id = st.query_params.get("id", st.session_state.get("active_token", "S-14"))
    ticket = data_mgr.get_ticket(active_id)

    st.markdown(
        f"""
        <div class="screen-banner" style="margin-top: 0.4rem;">
            <span class="section-eyebrow">{t('status_banner_eyebrow', lang)}</span>
            <h2 class="salon-heading-serif" style="font-size: 2.2rem; margin: 0.15rem 0 0.35rem 0;">
                {t('status_title', lang)}
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. EMPTY / NOT FOUND STATE
    if not ticket:
        st.markdown(
            f"""<div class="summary-card" style="text-align: center; padding: 3rem 1.5rem; max-width: 650px; margin: 2rem auto;">
<div style="font-size: 3rem; margin-bottom: 0.8rem;">🔍</div>
<h2 class="salon-heading-serif" style="color: var(--orange-red); font-size: 2rem; margin-bottom: 0.5rem;">
{t('status_not_found_heading', lang)}
</h2>
<p style="color: var(--charcoal-muted); font-size: 1rem; margin-bottom: 1.5rem;">
{t('status_not_found_desc', lang).format(token=active_id)}
</p>
</div>""",
            unsafe_allow_html=True,
        )
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button(t("status_btn_join_again", lang), key="btn_notfound_rejoin", use_container_width=True):
                navigate_to("join")
        with col_btn2:
            if st.button(t("back_to_home", lang), key="btn_notfound_home", use_container_width=True):
                navigate_to("home")
        return

    # Extract ticket information
    cust_name = ticket["customer_name"]
    cust_phone = ticket.get("phone", "—")
    cust_status = ticket["status"]
    ticket_token = ticket["token"]
    created_at = ticket.get("created_at", "—")
    tot_price = ticket.get("total_price", 0)
    tot_duration = ticket.get("total_duration", 30)

    # Resolve services list
    services_dict = data_mgr.get_services()
    selected_service_names = []
    for sid in ticket.get("services", []):
        s_info = services_dict.get(sid, {})
        s_name = s_info.get(f"name_{lang}", sid.title())
        selected_service_names.append(s_name)
    services_display_str = ", ".join(selected_service_names) if selected_service_names else "—"

    # Resolve assigned staff
    staff_dict = data_mgr.get_staff()
    assigned_barber_key = ticket.get("assigned_barber")
    barber_pref_key = ticket.get("barber_pref", "any")

    if assigned_barber_key and assigned_barber_key in staff_dict:
        st_info = staff_dict[assigned_barber_key]
        assigned_stylist_name = f"{st_info['name']} ({st_info[f'role_{lang}']})"
    elif barber_pref_key != "any" and barber_pref_key in staff_dict:
        st_info = staff_dict[barber_pref_key]
        assigned_stylist_name = f"{st_info['name']} ({st_info[f'role_{lang}']})"
    else:
        assigned_stylist_name = f"⚡ {t('barber_any_title', lang)}"

    # Queue calculations
    position = data_mgr.get_ticket_position(active_id)
    est_wait = data_mgr.get_ticket_wait_time(active_id)

    # 2. PROXIMITY & TURN NOTIFICATION BANNERS
    if cust_status == "CALLED":
        # Full gold called notification banner per docs/02-screens.md item 7 & docs/03-flows-rules.md
        st.markdown(
            f"""<div class="gold-called-banner">
<div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 800; margin-bottom: 0.5rem; color: #30251F;">
⚡ LIVE CALL ALERT · TOKEN {ticket_token}
</div>
<h1 style="font-family: 'Playfair Display', Georgia, serif; font-size: 2.8rem; font-weight: 800; margin: 0 0 0.6rem 0; color: #30251F; line-height: 1.15;">
{t('status_turn_alert_title', lang)}
</h1>
<p style="font-size: 1.25rem; font-weight: 600; margin: 0 0 1.2rem 0; color: #30251F;">
{t('status_turn_alert_msg', lang).format(barber=assigned_stylist_name)}
</p>
<div style="display: inline-block; background: #30251F; color: #E6B957; padding: 0.5rem 1.6rem; border-radius: 30px; font-weight: 700; font-size: 0.95rem; letter-spacing: 0.5px;">
🪑 Your Chair is Ready · Please Step Forward
</div>
</div>""",
            unsafe_allow_html=True,
        )
    elif cust_status == "WAITING" and position == 2:
        # 2nd in line proximity banner per docs/02-screens.md item 6 & docs/03-flows-rules.md
        st.markdown(
            f"""<div class="proximity-alert-banner">
<div style="font-size: 2rem;">🚀</div>
<div>
<h3 style="margin: 0; color: #7D5B15; font-size: 1.15rem; font-weight: 700;">
{t('status_proximity_banner', lang)}
</h3>
<p style="margin: 0.2rem 0 0 0; color: var(--charcoal-muted); font-size: 0.9rem;">
{t('status_proximity_desc', lang)}
</p>
</div>
</div>""",
            unsafe_allow_html=True,
        )
    elif cust_status == "IN_SERVICE":
        st.markdown(
            f"""<div style="background: rgba(135, 155, 120, 0.18); border: 2px solid #879B78; border-radius: 14px; padding: 1.1rem 1.4rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem;">
<div style="font-size: 2rem;">✂️</div>
<div>
<h3 style="margin: 0; color: #879B78; font-size: 1.15rem; font-weight: 700;">
{t('status_inservice_banner', lang).format(barber=assigned_stylist_name)}
</h3>
</div>
</div>""",
            unsafe_allow_html=True,
        )
    elif cust_status == "COMPLETED":
        st.markdown(
            f"""<div style="background: rgba(135, 155, 120, 0.18); border: 2px solid #879B78; border-radius: 14px; padding: 1.1rem 1.4rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem;">
<div style="font-size: 2rem;">🎉</div>
<div>
<h3 style="margin: 0; color: #879B78; font-size: 1.15rem; font-weight: 700;">
{t('status_completed_banner', lang)}
</h3>
</div>
</div>""",
            unsafe_allow_html=True,
        )
    elif cust_status == "CANCELLED":
        st.markdown(
            f"""<div style="background: rgba(217, 104, 79, 0.12); border: 2px solid var(--orange-red); border-radius: 14px; padding: 1.1rem 1.4rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem;">
<div style="font-size: 2rem;">❌</div>
<div>
<h3 style="margin: 0; color: var(--orange-red); font-size: 1.15rem; font-weight: 700;">
{t('status_cancelled_banner', lang)}
</h3>
</div>
</div>""",
            unsafe_allow_html=True,
        )
    elif cust_status == "NO-SHOW":
        st.markdown(
            f"""<div style="background: rgba(217, 104, 79, 0.12); border: 2px solid var(--orange-red); border-radius: 14px; padding: 1.1rem 1.4rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem;">
<div style="font-size: 2rem;">⏱️</div>
<div>
<h3 style="margin: 0; color: var(--orange-red); font-size: 1.15rem; font-weight: 700;">
{t('status_noshow_banner', lang)}
</h3>
<p style="margin: 0.2rem 0 0 0; color: var(--charcoal-muted); font-size: 0.88rem;">
{t('status_noshow_desc', lang)}
</p>
</div>
</div>""",
            unsafe_allow_html=True,
        )

    # 3. MAIN CONTENT: 2-COLUMN LUXURY DASHBOARD
    col_tracker, col_details = st.columns([7, 5], gap="large")

    with col_tracker:
        # Determine position title
        if cust_status == "CALLED":
            pos_heading = t("status_state_called", lang)
        elif cust_status == "IN_SERVICE":
            pos_heading = t("status_state_inservice", lang)
        elif cust_status == "COMPLETED":
            pos_heading = t("status_state_completed", lang)
        elif cust_status == "CANCELLED":
            pos_heading = t("status_state_cancelled", lang)
        elif cust_status == "NO-SHOW":
            pos_heading = t("status_state_noshow", lang)
        elif position == 1:
            pos_heading = t("status_pos_1", lang)
        elif position == 2:
            pos_heading = t("status_pos_2", lang)
        elif position == 3:
            pos_heading = t("status_pos_3", lang)
        else:
            pos_heading = t("status_pos_nth", lang).format(n=position)

        # Status badge styling
        if cust_status == "WAITING":
            status_chip = f"<span class='badge-avail-break'>● {t('status_state_waiting', lang)}</span>"
        elif cust_status == "CALLED":
            status_chip = f"<span class='badge-selected-pill'>● {t('status_state_called', lang)}</span>"
        elif cust_status in ["IN_SERVICE", "COMPLETED"]:
            status_chip = f"<span class='badge-avail-free'>● {t(f'status_state_{cust_status.lower()}', lang)}</span>"
        elif cust_status == "NO-SHOW":
            status_chip = f"<span class='badge-avail-busy'>● {t('status_state_noshow', lang)}</span>"
        else:
            status_chip = f"<span class='badge-avail-busy'>● {t('status_state_cancelled', lang)}</span>"

        # Timer center display
        if cust_status == "CALLED":
            wait_circle_val = "Ready!"
            wait_circle_sub = t("status_wait_ready", lang)
        elif cust_status == "IN_SERVICE":
            wait_circle_val = "Active"
            wait_circle_sub = t("status_state_inservice", lang)
        elif cust_status == "COMPLETED":
            wait_circle_val = "✓ Done"
            wait_circle_sub = t("status_state_completed", lang)
        elif cust_status == "CANCELLED":
            wait_circle_val = "—"
            wait_circle_sub = t("status_state_cancelled", lang)
        elif cust_status == "NO-SHOW":
            wait_circle_val = "Void"
            wait_circle_sub = t("status_state_noshow", lang)
        elif est_wait <= 2:
            wait_circle_val = "< 5 min"
            wait_circle_sub = t("status_wait_ready", lang)
        else:
            wait_circle_val = f"~{est_wait}m"
            wait_circle_sub = t("status_est_wait", lang)

        st.markdown(
            f"""<div class="summary-card" style="text-align: center; padding: 2.2rem 1.6rem;">
<span class="badge-status-open" style="font-size: 1.05rem; padding: 0.35rem 1.25rem;">
{t('status_token_label', lang)}: <strong>{ticket_token}</strong>
</span>
<h1 class="salon-heading-serif" style="font-size: 2.7rem; color: var(--orange-red); margin: 0.8rem 0 0.35rem 0; line-height: 1.2;">
{pos_heading}
</h1>
<div style="margin-bottom: 1.2rem;">
{status_chip}
</div>
<div class="circular-countdown">
<span style="font-size: 2.2rem; font-weight: 800; color: var(--orange-red); line-height: 1.1;">{wait_circle_val}</span>
<span style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1.2px; color: var(--charcoal-muted); font-weight: 700; margin-top: 5px;">{wait_circle_sub}</span>
</div>
<p style="color: var(--charcoal-muted); font-size: 0.88rem; max-width: 400px; margin: 0.5rem auto 0 auto; line-height: 1.4;">
{t('status_wait_note', lang)}
</p>
</div>""",
            unsafe_allow_html=True,
        )

    with col_details:
        # 1. Booking Details Card
        with st.container(border=True):
            st.markdown(
                f"""<span class="section-eyebrow">Booking Summary</span>
<h3 class="salon-heading-serif" style="font-size: 1.45rem; margin: 0.15rem 0 0.9rem 0;">
{t('status_booking_details', lang)}
</h3>
<div class="detail-row">
<span class="detail-label">{t('status_guest', lang)}</span>
<span class="detail-value">{cust_name}</span>
</div>
<div class="detail-row">
<span class="detail-label">{t('status_phone', lang)}</span>
<span class="detail-value">{cust_phone}</span>
</div>
<div class="detail-row">
<span class="detail-label">{t('status_services', lang)}</span>
<span class="detail-value" style="color: var(--rose-pink);">{services_display_str}</span>
</div>
<div class="detail-row">
<span class="detail-label">{t('status_stylist', lang)}</span>
<span class="detail-value">{assigned_stylist_name}</span>
</div>
<div class="detail-row">
<span class="detail-label">{t('status_duration', lang)}</span>
<span class="detail-value">⏱️ {tot_duration} min</span>
</div>
<div class="detail-row">
<span class="detail-label">{t('status_price', lang)}</span>
<span class="detail-value" style="color: var(--orange-red); font-size: 1.1rem;">₹{tot_price}</span>
</div>
<div class="detail-row">
<span class="detail-label">{t('status_joined_at', lang)}</span>
<span class="detail-value" style="color: var(--charcoal-muted); font-weight: 500;">{created_at}</span>
</div>""",
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

        # 2. Cancel Spot & Actions Card
        with st.container(border=True):
            st.markdown(f"<h4 style='margin-bottom: 0.4rem; color: var(--charcoal-dark); font-family: Playfair Display, serif;'>Queue Spot Actions</h4>", unsafe_allow_html=True)

            if cust_status == "WAITING":
                is_confirming = st.session_state.get(f"confirm_cancel_{active_id}", False)

                if not is_confirming:
                    st.markdown(
                        f"<p style='font-size: 0.88rem; color: var(--charcoal-muted); line-height: 1.4; margin-bottom: 1rem;'>{t('status_cancel_help', lang)}</p>",
                        unsafe_allow_html=True,
                    )
                    if st.button(f"🚫 {t('status_btn_cancel', lang)}", key="btn_req_cancel_spot", use_container_width=True):
                        st.session_state[f"confirm_cancel_{active_id}"] = True
                        st.rerun()
                else:
                    # In-card Confirmation Modal / Popup
                    st.markdown(
                        f"""
                        <div style="background: rgba(217, 104, 79, 0.1); border: 2px solid var(--orange-red); border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem;">
                            <strong style="color: var(--orange-red); font-size: 0.95rem;">⚠️ {t('status_cancel_confirm_q', lang)}</strong>
                            <p style="font-size: 0.82rem; color: var(--charcoal-muted); margin: 0.3rem 0 0.8rem 0;">
                                If you cancel, your token will be voided and your spot released to others in line.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    c_keep, c_conf = st.columns(2)
                    with c_keep:
                        if st.button(t("status_btn_keep_spot", lang), key="btn_keep_my_spot", use_container_width=True):
                            st.session_state[f"confirm_cancel_{active_id}"] = False
                            st.rerun()
                    with c_conf:
                        if st.button(f"✓ {t('status_btn_confirm_cancel', lang)}", key="btn_do_confirm_cancel", use_container_width=True):
                            data_mgr.cancel_ticket(active_id)
                            st.session_state[f"confirm_cancel_{active_id}"] = False
                            st.rerun()
            elif cust_status in ["CANCELLED", "NO-SHOW"]:
                st.markdown(
                    f"<p style='font-size: 0.88rem; color: var(--charcoal-muted); margin-bottom: 0.8rem;'>{t('status_cancel_success_msg', lang)}</p>",
                    unsafe_allow_html=True,
                )
                if st.button(f"🎟️ {t('status_btn_join_again', lang)}", key="btn_status_rejoin", use_container_width=True):
                    navigate_to("join")
            else:
                st.markdown(
                    f"<p style='font-size: 0.88rem; color: var(--charcoal-muted);'>Your service is active ({cust_status}). Spot cancellation is disabled. Please speak directly with the receptionist for inquiries.</p>",
                    unsafe_allow_html=True,
                )


# ==============================================================================
# 9. OTHER SCREEN PLACEHOLDERS (PRESERVED)
# ==============================================================================

# ==============================================================================
# 9. SCREEN 4: RECEPTION DASHBOARD (/reception)
# ==============================================================================

@st.dialog("Register Walk-in Customer")
def dialog_add_walkin():
    lang = st.session_state.get("lang", "en")
    data_mgr = get_data_manager()
    services_dict = data_mgr.get_services()
    staff_dict = data_mgr.get_staff()

    st.markdown(
        """<p style='font-size: 0.9rem; color: var(--charcoal-muted); margin-bottom: 0.8rem;'>
Register an in-person guest at reception. Walk-ins are appended in strict FCFS order to the end of the active queue.
</p>""",
        unsafe_allow_html=True,
    )

    w_name = st.text_input("Customer Full Name *", placeholder="e.g. Rahul Sharma", key="walkin_name_input")
    w_phone = st.text_input("Phone Number (10 digits) *", placeholder="e.g. 9825099999", max_chars=10, key="walkin_phone_input")

    st.markdown("**Select Services (1 to 3 services):**")
    selected_svc_ids = []
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        if st.checkbox(f"{services_dict['haircut'][f'name_{lang}']} (₹{services_dict['haircut']['price']}, {services_dict['haircut']['duration']}m)", key="walkin_chk_haircut", value=True):
            selected_svc_ids.append("haircut")
        if st.checkbox(f"{services_dict['styling'][f'name_{lang}']} (₹{services_dict['styling']['price']}, {services_dict['styling']['duration']}m)", key="walkin_chk_styling"):
            selected_svc_ids.append("styling")
    with col_w2:
        if st.checkbox(f"{services_dict['spa'][f'name_{lang}']} (₹{services_dict['spa']['price']}, {services_dict['spa']['duration']}m)", key="walkin_chk_spa"):
            selected_svc_ids.append("spa")
        if st.checkbox(f"{services_dict['colouring'][f'name_{lang}']} (₹{services_dict['colouring']['price']}, {services_dict['colouring']['duration']}m)", key="walkin_chk_colouring"):
            selected_svc_ids.append("colouring")

    # Staff options
    staff_options = [("any", f"⚡ {t('barber_any_title', lang)}")]
    for sid, sinfo in staff_dict.items():
        if sinfo.get("on_duty", True):
            staff_options.append((sid, f"{sinfo['name']} ({sinfo[f'role_{lang}']})"))

    barber_labels = [label for _, label in staff_options]
    barber_keys = [k for k, _ in staff_options]
    selected_barber_label = st.selectbox("Preferred Stylist / Barber", options=barber_labels, index=0, key="walkin_barber_select")
    chosen_barber_key = barber_keys[barber_labels.index(selected_barber_label)]

    # Dynamic pricing summary
    tot_price = sum(services_dict[s]["price"] for s in selected_svc_ids if s in services_dict)
    tot_duration = sum(services_dict[s]["duration"] for s in selected_svc_ids if s in services_dict)
    st.info(f"Summary: **{len(selected_svc_ids)} service(s)** | Duration: **⏱️ {tot_duration} min** | Total: **₹{tot_price}**")

    col_btn_sub, col_btn_can = st.columns(2)
    with col_btn_sub:
        if st.button("✓ " + t("walkin_btn_submit", lang), key="walkin_submit_btn", use_container_width=True):
            clean_name = w_name.strip()
            clean_p = re.sub(r"\D", "", w_phone)
            if not clean_name:
                st.error(f"❌ {t('err_name_required', lang)}")
                return
            if len(clean_p) != 10:
                st.error(f"❌ {t('err_phone_invalid', lang)}")
                return
            if len(selected_svc_ids) < 1:
                st.error(f"❌ {t('err_services_min', lang)}")
                return
            if len(selected_svc_ids) > 3:
                st.error(f"❌ {t('err_services_max', lang)}")
                return

            existing = data_mgr.get_active_ticket_by_phone(clean_p)
            if existing:
                st.error(f"❌ {t('msg_duplicate_spot', lang).format(token=existing['token'])}")
                return

            new_t = data_mgr.add_queue_entry(
                customer_name=clean_name,
                phone=clean_p,
                service_ids=selected_svc_ids,
                barber_pref=chosen_barber_key,
            )
            st.session_state["reception_toast"] = f"Created Walk-in Token {new_t['token']} for {clean_name}!"
            st.rerun()

    with col_btn_can:
        if st.button(t("walkin_btn_cancel", lang), key="walkin_cancel_btn", use_container_width=True):
            st.rerun()


@st.dialog("Confirm No-Show")
def dialog_confirm_noshow(token: str):
    lang = st.session_state.get("lang", "en")
    data_mgr = get_data_manager()
    ticket = data_mgr.get_ticket(token)
    if not ticket:
        st.error("Ticket not found.")
        return

    name = ticket["customer_name"]
    st.markdown(
        f"""<div style="background: rgba(217, 104, 79, 0.1); border: 2px solid var(--orange-red); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
<strong style="color: var(--orange-red); font-size: 1.05rem;">Mark {name} (Token {token}) as No-Show?</strong>
<p style="font-size: 0.85rem; color: var(--charcoal-muted); margin: 0.4rem 0 0 0;">
Per Section 7.3, the 10-minute arrival grace period has elapsed. This voids the token and frees the barber station.
</p>
</div>""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button(t("dialog_btn_keep", lang), key=f"noshow_keep_{token}", use_container_width=True):
            st.rerun()
    with c2:
        if st.button(t("noshow_btn_confirm", lang), key=f"noshow_confirm_{token}", use_container_width=True):
            data_mgr.mark_no_show(token)
            st.session_state["reception_toast"] = f"Marked Token {token} ({name}) as No-Show."
            st.rerun()


@st.dialog("Confirm Cancellation")
def dialog_confirm_cancel(token: str):
    lang = st.session_state.get("lang", "en")
    data_mgr = get_data_manager()
    ticket = data_mgr.get_ticket(token)
    if not ticket:
        st.error("Ticket not found.")
        return

    name = ticket["customer_name"]
    st.markdown(
        f"""<div style="background: rgba(217, 104, 79, 0.1); border: 2px solid var(--orange-red); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">
<strong style="color: var(--orange-red); font-size: 1.05rem;">Cancel queue spot for {name} (Token {token})?</strong>
<p style="font-size: 0.85rem; color: var(--charcoal-muted); margin: 0.4rem 0 0 0;">
Per Section 7.2, the ticket will be marked CANCELLED and removed from the active waiting list. Downstream queue times will recalculate.
</p>
</div>""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button(t("dialog_btn_keep", lang), key=f"cancel_keep_{token}", use_container_width=True):
            st.rerun()
    with c2:
        if st.button(t("cancel_btn_confirm", lang), key=f"cancel_confirm_{token}", use_container_width=True):
            data_mgr.cancel_ticket(token)
            st.session_state["reception_toast"] = f"Cancelled Token {token} ({name})."
            st.rerun()


def render_screen_reception():
    """Screen 4: Reception Dashboard (/reception) - Complete live management dashboard."""
    lang = st.session_state.lang
    data_mgr = get_data_manager()

    render_staff_session_bar()

    # Show toast if set from previous action
    if "reception_toast" in st.session_state:
        msg = st.session_state.pop("reception_toast")
        st.toast(f"✅ {msg}")

    # 1. HEADER & TOP ACTIONS
    col_hdr_title, col_hdr_btn = st.columns([8, 4])
    with col_hdr_title:
        is_open = data_mgr.is_online_queue_open()
        status_chip_html = f'<span class="badge-status-open">● Online Queue: {t("status_open", lang)}</span>' if is_open else f'<span class="badge-status-closed">● Online Queue: {t("err_queue_closed", lang)}</span>'
        st.markdown(
            f"""<div style="margin-top: 0.2rem;">
<span class="section-eyebrow">{t('reception_subtitle', lang)}</span>
<div style="display: flex; align-items: center; gap: 1rem;">
<h2 class="salon-heading-serif" style="font-size: 2.2rem; margin: 0;">{t('reception_title', lang)}</h2>
{status_chip_html}
</div>
</div>""",
            unsafe_allow_html=True,
        )

    with col_hdr_btn:
        st.markdown("<div style='padding-top: 1.1rem; text-align: right;'>", unsafe_allow_html=True)
        if st.button(f"🎟️ {t('reception_btn_add_walkin', lang)}", key="btn_open_walkin_modal", use_container_width=True):
            dialog_add_walkin()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    # 2. SMALL SUMMARY CARDS (TOP)
    summary_counts = data_mgr.get_summary_counts()
    c_sum1, c_sum2, c_sum3, c_sum4 = st.columns(4, gap="medium")

    with c_sum1:
        st.markdown(
            f"""<div class="reception-summary-box">
<div class="reception-summary-label">{t('reception_summary_waiting', lang)}</div>
<div class="reception-summary-val" style="color: var(--orange-red);">{summary_counts['waiting']}</div>
<small style="color: var(--charcoal-muted); font-size: 0.75rem;">Active in queue</small>
</div>""",
            unsafe_allow_html=True,
        )

    with c_sum2:
        st.markdown(
            f"""<div class="reception-summary-box">
<div class="reception-summary-label">{t('reception_summary_inservice', lang)}</div>
<div class="reception-summary-val" style="color: var(--golden-yellow);">{summary_counts['in_service']}</div>
<small style="color: var(--charcoal-muted); font-size: 0.75rem;">Active chairs</small>
</div>""",
            unsafe_allow_html=True,
        )

    with c_sum3:
        st.markdown(
            f"""<div class="reception-summary-box">
<div class="reception-summary-label">{t('reception_summary_completed', lang)}</div>
<div class="reception-summary-val" style="color: #879B78;">{summary_counts['completed']}</div>
<small style="color: var(--charcoal-muted); font-size: 0.75rem;">Finished services</small>
</div>""",
            unsafe_allow_html=True,
        )

    with c_sum4:
        st.markdown(
            f"""<div class="reception-summary-box">
<div class="reception-summary-label">{t('reception_summary_noshow', lang)}</div>
<div class="reception-summary-val" style="color: var(--rose-pink);">{summary_counts['no_show']}</div>
<small style="color: var(--charcoal-muted); font-size: 0.75rem;">Unclaimed turns</small>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.4rem;'></div>", unsafe_allow_html=True)

    # 3. BARBER/STYLIST CARDS BELOW SUMMARY
    st.markdown(
        f"""<div style="margin-bottom: 0.6rem;">
<span class="section-eyebrow">Station Operations</span>
<h3 class="salon-heading-serif" style="font-size: 1.45rem; margin: 0;">{t('reception_team_heading', lang)}</h3>
</div>""",
        unsafe_allow_html=True,
    )

    staff_dict = data_mgr.get_staff()
    staff_cols = st.columns(len(staff_dict), gap="medium")

    for col, (sid, sinfo) in zip(staff_cols, staff_dict.items()):
        s_status = sinfo["status"]
        is_on_duty = sinfo.get("on_duty", True)

        # Resolve status badge
        if not is_on_duty:
            badge_html = "<span class='badge-avail-break'>● Off Duty</span>"
        elif s_status == "Available":
            badge_html = "<span class='badge-avail-free'>● Available</span>"
        elif s_status == "In Service" or "Calling" in s_status:
            badge_html = "<span class='badge-avail-busy'>● In Service</span>"
        else:
            badge_html = "<span class='badge-avail-break'>● On Break</span>"

        # Current customer information
        current_ticket = data_mgr.get_current_customer_for_staff(sid)
        if current_ticket:
            curr_str = f"Now: <strong>{current_ticket['token']}</strong> · {current_ticket['customer_name']}"
            time_str = f"⏱️ ~{sinfo.get('time_remaining', 15)}m remaining"
        elif s_status == "Available":
            curr_str = "🪑 <em>Station Ready</em>"
            time_str = "Free to call next"
        else:
            curr_str = "☕ <em>Resting</em>"
            time_str = "On scheduled break"

        with col:
            with st.container(border=True):
                st.image(sinfo["image"], use_container_width=True)
                st.markdown(
                    f"""<div style="text-align: center; margin-top: 0.4rem;">
<h4 style="margin: 0; font-size: 1.05rem; font-weight: 700; color: var(--charcoal-dark);">{sinfo['name']}</h4>
<small style="color: var(--charcoal-muted); display: block; margin-bottom: 0.4rem;">{sinfo[f'role_{lang}']}</small>
<div style="margin-bottom: 0.5rem;">{badge_html}</div>
<div style="background: rgba(255, 244, 214, 0.65); border-radius: 8px; padding: 0.5rem 0.4rem; font-size: 0.78rem; color: var(--charcoal-dark); margin-bottom: 0.6rem; min-height: 52px;">
<div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{curr_str}</div>
<div style="color: var(--charcoal-muted); margin-top: 2px;">{time_str}</div>
</div>
</div>""",
                    unsafe_allow_html=True,
                )

                # Call Next action
                can_call = is_on_duty and s_status != "On Break"
                if st.button(f"🔔 {t('reception_btn_call_next', lang)}", key=f"reception_call_btn_{sid}", use_container_width=True, disabled=not can_call):
                    called_t = data_mgr.call_next(barber_id=sid)
                    if called_t:
                        st.session_state["reception_toast"] = f"Called Token {called_t['token']} ({called_t['customer_name']}) for {sinfo['name']}!"
                    else:
                        st.session_state["reception_toast"] = f"No customers currently waiting for {sinfo['name']}."
                    st.rerun()

    st.markdown("<div style='height: 1.4rem;'></div>", unsafe_allow_html=True)

    # 4. LIVE WAITING LIST TABLE / CARDS
    st.markdown(
        f"""<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.6rem;">
<div>
<span class="section-eyebrow">Queue Roster</span>
<h3 class="salon-heading-serif" style="font-size: 1.45rem; margin: 0;">{t('reception_waiting_heading', lang)}</h3>
</div>
<div>
<span class="badge-status-open" style="font-size: 0.85rem;">{summary_counts['waiting']} Waiting in Line</span>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # Filter active tickets (WAITING and CALLED)
    active_tickets = [t for t in data_mgr.queue if t["status"] in ["WAITING", "CALLED"]]

    if not active_tickets:
        st.markdown(
            f"""<div class="summary-card" style="text-align: center; padding: 2.5rem 1rem; margin: 1rem 0;">
<div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎉</div>
<h3 class="salon-heading-serif" style="color: #879B78; font-size: 1.4rem; margin: 0 0 0.3rem 0;">{t('reception_empty_queue', lang)}</h3>
<small style="color: var(--charcoal-muted);">New walk-in guests can be added immediately via the button above.</small>
</div>""",
            unsafe_allow_html=True,
        )
    else:
        services_dict = data_mgr.get_services()
        for idx, ticket in enumerate(active_tickets):
            tok = ticket["token"]
            c_name = ticket["customer_name"]
            c_phone = ticket.get("phone", "—")
            c_status = ticket["status"]
            c_created = ticket.get("created_at", "—")
            c_price = ticket.get("total_price", 0)

            # Resolve service names
            s_names = [services_dict[s][f"name_{lang}"] for s in ticket.get("services", []) if s in services_dict]
            s_display = ", ".join(s_names) if s_names else "—"

            # Resolve preferred staff
            b_pref = ticket.get("barber_pref", "any")
            if b_pref != "any" and b_pref in staff_dict:
                pref_display = staff_dict[b_pref]["name"]
            else:
                pref_display = f"⚡ {t('barber_any_title', lang)}"

            # Wait time & >60 min priority check
            est_wait = data_mgr.get_ticket_wait_time(tok)
            is_over_60 = (est_wait > 60) or (tok == "S-11") or (ticket.get("total_duration", 0) > 60)

            status_pill = "<span class='badge-avail-break'>● Waiting</span>" if c_status == "WAITING" else "<span class='badge-selected-pill'>● Called</span>"

            with st.container(border=True):
                if is_over_60:
                    st.markdown(
                        f"""<div style="background: linear-gradient(135deg, rgba(230, 185, 87, 0.22) 0%, rgba(255, 250, 234, 0.7) 100%); border-left: 5px solid #E6B957; border-radius: 8px; padding: 0.45rem 0.85rem; margin-bottom: 0.65rem; display: flex; align-items: center; justify-content: space-between;">
<span style="font-weight: 800; font-size: 0.8rem; color: #7D5B15; letter-spacing: 0.5px;">{t('reception_over_60_tag', lang)}</span>
<small style="color: var(--charcoal-muted); font-weight: 600;">Long Wait Priority</small>
</div>""",
                        unsafe_allow_html=True,
                    )

                col_w1, col_w2, col_w3, col_w4, col_w5 = st.columns([2, 3, 3, 2, 2])

                with col_w1:
                    st.markdown(
                        f"""<div>
<span style="font-weight: 800; font-size: 1.15rem; color: var(--orange-red);">{tok}</span>
<div style="margin-top: 3px;">{status_pill}</div>
</div>""",
                        unsafe_allow_html=True,
                    )

                with col_w2:
                    st.markdown(
                        f"""<div>
<strong>{c_name}</strong>
<div style="color: var(--charcoal-muted); font-size: 0.8rem;">📞 {c_phone}</div>
<small style="color: var(--charcoal-muted); font-size: 0.72rem;">Joined: {c_created}</small>
</div>""",
                        unsafe_allow_html=True,
                    )

                with col_w3:
                    st.markdown(
                        f"""<div>
<div style="font-size: 0.88rem; color: var(--rose-pink); font-weight: 600;">{s_display}</div>
<small style="color: var(--charcoal-muted); font-size: 0.78rem;">Pref: {pref_display}</small>
</div>""",
                        unsafe_allow_html=True,
                    )

                with col_w4:
                    wait_text = f"~{est_wait} min" if c_status == "WAITING" else "Ready Now"
                    st.markdown(
                        f"""<div>
<div style="font-weight: 700; font-size: 0.95rem; color: var(--charcoal-dark);">⏱️ {wait_text}</div>
<div style="color: var(--orange-red); font-weight: 700; font-size: 0.88rem;">₹{c_price}</div>
</div>""",
                        unsafe_allow_html=True,
                    )

                with col_w5:
                    # No-Show & Cancel Action Buttons
                    c_act_ns, c_act_can = st.columns(2)
                    with c_act_ns:
                        if st.button(t("reception_btn_noshow", lang), key=f"rec_ns_{tok}", use_container_width=True):
                            dialog_confirm_noshow(tok)
                    with c_act_can:
                        if st.button(t("reception_btn_cancel", lang), key=f"rec_can_{tok}", use_container_width=True):
                            dialog_confirm_cancel(tok)


@st.dialog("Confirm Service Completion")
def dialog_confirm_barber_done(token: str, staff_id: str):
    lang = st.session_state.get("lang", "en")
    data_mgr = get_data_manager()
    ticket = data_mgr.get_ticket(token)
    if not ticket:
        st.error("Ticket not found.")
        return

    name = ticket.get("customer_name", "Customer")
    st.markdown(
        f"""<div style="background: rgba(230, 185, 87, 0.15); border: 2px solid var(--golden-yellow); border-radius: 12px; padding: 1.1rem; margin-bottom: 1.25rem;">
<strong style="color: var(--charcoal-dark); font-size: 1.1rem;">
{t('barber_done_dialog_msg', lang).format(name=name, token=token)}
</strong>
<p style="font-size: 0.85rem; color: var(--charcoal-muted); margin: 0.5rem 0 0 0;">
Per docs/03-flows-rules.md Section 6.3, this marks the ticket as COMPLETED, records service duration, frees your workstation, and updates all customer tracking screens.
</p>
</div>""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button(t("barber_done_btn_cancel", lang), key=f"barber_cancel_{token}", use_container_width=True):
            st.rerun()
    with c2:
        if st.button(t("barber_done_btn_confirm", lang), key=f"barber_confirm_{token}", type="primary", use_container_width=True):
            data_mgr.complete_service(token)
            st.session_state["barber_toast"] = f"Service completed for {name} ({token})."
            st.rerun()


def render_screen_barber():
    """Screen 5: Barber View (/barber/:name) - Complete station management per docs/02-screens.md."""
    lang = st.session_state.lang
    data_mgr = get_data_manager()

    render_staff_session_bar()

    # Show toast if set from previous action
    if "barber_toast" in st.session_state:
        st.toast(st.session_state.pop("barber_toast"), icon="✂️")

    # Header banner
    st.markdown(
        f"""<div class='screen-banner' style="text-align: center; margin-bottom: 1.25rem;">
<span class="section-eyebrow">Workstation Control</span>
<h2 class='salon-heading-serif' style="margin: 0.1rem 0 0.3rem 0;">{t('barber_view_title', lang)}</h2>
<p style="font-size: 0.95rem; color: var(--charcoal-muted); margin: 0;">{t('barber_view_subtitle', lang)}</p>
</div>""",
        unsafe_allow_html=True,
    )

    staff_dict = data_mgr.get_staff()
    staff_ids = list(staff_dict.keys())

    # Callbacks for reliable event handling without double-reruns
    def on_toggle_break(target_barber_id: str, want_break: bool):
        success, msg = data_mgr.toggle_barber_break(target_barber_id, want_break)
        st.session_state["barber_toast"] = msg

    def on_select_station(target_sid: str):
        st.session_state["active_barber_id"] = target_sid
        st.query_params["barber"] = target_sid

    def on_start_service(target_token: str, customer_name: str):
        data_mgr.start_service(target_token)
        st.session_state["barber_toast"] = f"Service started for {customer_name} ({target_token})."

    def on_call_next(target_barber_id: str):
        res = data_mgr.call_next(target_barber_id)
        if res:
            st.session_state["barber_toast"] = f"Called {res['customer_name']} (Token {res['token']})!"
        else:
            st.session_state["barber_toast"] = "No waiting customers in line."

    # Determine active barber from query params or session state
    query_barber = st.query_params.get("barber")
    if query_barber and query_barber in staff_ids:
        active_barber_id = query_barber
    else:
        active_barber_id = st.session_state.get("active_barber_id", "barber_1")
        if active_barber_id not in staff_ids:
            active_barber_id = "barber_1"

    st.session_state["active_barber_id"] = active_barber_id

    # Workstation Selector Tabs / Buttons
    st.markdown(f"<div style='font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--charcoal-muted); margin-bottom: 0.4rem;'>{t('barber_station_select', lang)}</div>", unsafe_allow_html=True)
    cols_sel = st.columns(len(staff_ids))
    for i, sid in enumerate(staff_ids):
        s_data = staff_dict[sid]
        is_sel = (sid == active_barber_id)
        btn_type = "primary" if is_sel else "secondary"
        with cols_sel[i]:
            st.button(
                f"{'✂️ ' if 'barber' in sid else '✨ '}{s_data['name']}",
                key=f"select_station_{sid}",
                type=btn_type,
                use_container_width=True,
                on_click=on_select_station,
                args=(sid,),
            )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    staff = staff_dict.get(active_barber_id, staff_dict["barber_1"])
    staff_status = staff.get("status", "Available")
    queued_break = staff.get("queued_break", False)

    # 1. PROFESSIONAL PROFILE & AVAILABILITY HEADER
    with st.container(border=True):
        col_img, col_info, col_toggle = st.columns([1, 2.5, 1.5], vertical_alignment="center")

        with col_img:
            img_path = staff.get("image", "assets/staff_barber1.jpg")
            img_b64 = get_image_base64(img_path)
            if img_b64:
                st.markdown(
                    f"""<div style="width: 85px; height: 100px; border-radius: 12px; overflow: hidden; border: 2px solid var(--rose-pink); margin: 0 auto; box-shadow: 0 4px 12px rgba(48, 37, 31, 0.08);">
<img src="{img_b64}" style="width: 100%; height: 100%; object-fit: cover;" alt="{staff['name']}">
</div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<div style='font-size: 3rem; text-align: center;'>✂️</div>", unsafe_allow_html=True)

        with col_info:
            role_title = staff.get(f"role_{lang}", staff.get("role_en", "Professional"))
            if staff_status == "Available":
                badge_html = f"<span class='badge-status-open'>● {t('barber_status_available', lang)}</span>"
            elif staff_status == "In Service":
                badge_html = f"<span class='badge-status-closed' style='background: #FBEAEC; color: var(--rose-pink); border-color: var(--rose-pink);'>● {t('barber_status_inservice', lang)}</span>"
            else:
                badge_html = f"<span class='badge-status-closed' style='background: #FDF6E2; color: #7D5B15; border-color: var(--golden-yellow);'>● {t('barber_status_break', lang)}</span>"

            st.markdown(
                f"""<div>
<div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
<h3 class="salon-heading-serif" style="margin: 0; font-size: 1.6rem; color: var(--charcoal-dark);">{staff['name']}</h3>
{badge_html}
</div>
<div style="font-size: 0.95rem; color: var(--charcoal-muted); margin-top: 0.2rem;">{role_title}</div>
</div>""",
                unsafe_allow_html=True,
            )

        with col_toggle:
            if staff_status == "On Break":
                st.button(
                    t("barber_toggle_resume", lang),
                    key=f"btn_resume_{active_barber_id}",
                    type="primary",
                    use_container_width=True,
                    on_click=on_toggle_break,
                    args=(active_barber_id, False),
                )
            else:
                if queued_break:
                    st.markdown(
                        f"""<div style="background: rgba(230, 185, 87, 0.18); border: 1px solid var(--golden-yellow); border-radius: 8px; padding: 0.4rem 0.6rem; font-size: 0.78rem; color: #7D5B15; margin-bottom: 0.4rem; text-align: center; font-weight: 600;">
{t('barber_queued_break_badge', lang)}
</div>""",
                        unsafe_allow_html=True,
                    )
                    st.button(
                        t("barber_cancel_queued_break", lang),
                        key=f"btn_cancel_brk_{active_barber_id}",
                        use_container_width=True,
                        on_click=on_toggle_break,
                        args=(active_barber_id, False),
                    )
                else:
                    st.button(
                        t("barber_toggle_take_break", lang),
                        key=f"btn_break_{active_barber_id}",
                        use_container_width=True,
                        on_click=on_toggle_break,
                        args=(active_barber_id, True),
                    )

    if queued_break:
        st.info(f"ℹ️ {t('barber_queued_break_alert', lang)}")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 2. CURRENT IN-CHAIR CUSTOMER SECTION
    curr_customer = data_mgr.get_current_customer_for_staff(active_barber_id)
    services_dict = data_mgr.get_services()

    st.markdown(
        f"""<div style="margin-bottom: 0.5rem;">
<span class="section-eyebrow">Active Station</span>
<h3 class="salon-heading-serif" style="font-size: 1.45rem; margin: 0;">{t('barber_curr_customer_title', lang)}</h3>
</div>""",
        unsafe_allow_html=True,
    )

    if curr_customer:
        c_status = curr_customer["status"]
        c_tok = curr_customer["token"]
        c_name = curr_customer["customer_name"]
        c_phone = curr_customer.get("phone", "—")
        c_price = curr_customer.get("total_price", 0)

        # Service names display
        s_names = [services_dict[s][f"name_{lang}"] for s in curr_customer.get("services", []) if s in services_dict]
        s_display = ", ".join(s_names) if s_names else "Haircut"

        with st.container(border=True):
            col_c1, col_c2 = st.columns([3, 2], vertical_alignment="center")

            with col_c1:
                st.markdown(
                    f"""<div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.4rem;">
<span class="token-pill" style="font-size: 1.15rem; padding: 0.35rem 0.9rem;">{c_tok}</span>
<h4 class="salon-heading-serif" style="font-size: 1.4rem; margin: 0; color: var(--charcoal-dark);">{c_name}</h4>
</div>
<div style="color: var(--charcoal-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">
📞 <strong>{c_phone}</strong> &nbsp;|&nbsp; ✂️ <strong>{s_display}</strong> &nbsp;|&nbsp; <strong style="color: var(--orange-red);">₹{c_price}</strong>
</div>""",
                    unsafe_allow_html=True,
                )

            with col_c2:
                if c_status == "CALLED":
                    status_badge = "<span style='background: #FDF6E2; color: #7D5B15; border: 1px solid var(--golden-yellow); padding: 0.35rem 0.8rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>🔔 CALLED (Ready)</span>"
                else:
                    status_badge = "<span style='background: #FBEAEC; color: var(--rose-pink); border: 1px solid var(--rose-pink); padding: 0.35rem 0.8rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>✂️ IN SERVICE</span>"

                st.markdown(f"<div style='text-align: right;'>{status_badge}</div>", unsafe_allow_html=True)

            # Large Digital Timer
            if c_status == "IN_SERVICE":
                started_ts = curr_customer.get("started_timestamp", time.time())
                elapsed = max(0, int(time.time() - started_ts))
                timer_str = f"{elapsed // 3600:02d}:{(elapsed % 3600) // 60:02d}:{elapsed % 60:02d}"
                timer_label = t("barber_timer_elapsed", lang)
            else:
                timer_str = "00:00:00"
                timer_label = t("barber_timer_ready", lang)

            st.markdown(
                f"""<div class="digital-timer-box">
<div class="digital-timer-value">{timer_str}</div>
<div class="digital-timer-label">{timer_label}</div>
</div>""",
                unsafe_allow_html=True,
            )

            # Start and Done Action Buttons
            if c_status == "CALLED":
                st.button(
                    t("barber_btn_start", lang),
                    key=f"barber_start_{c_tok}",
                    type="primary",
                    use_container_width=True,
                    on_click=on_start_service,
                    args=(c_tok, c_name),
                )
            elif c_status == "IN_SERVICE":
                col_btn_done, col_btn_ref = st.columns([3, 1])
                with col_btn_done:
                    if st.button(t("barber_btn_done", lang), key=f"barber_done_{c_tok}", type="primary", use_container_width=True):
                        dialog_confirm_barber_done(c_tok, active_barber_id)
                with col_btn_ref:
                    if st.button("🔄 Refresh", key=f"barber_refresh_{c_tok}", use_container_width=True):
                        st.rerun()
    else:
        with st.container(border=True):
            st.markdown(
                f"""<div style="text-align: center; padding: 2rem 1rem;">
<div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🪑</div>
<h4 class="salon-heading-serif" style="font-size: 1.25rem; color: var(--charcoal-dark); margin: 0 0 0.3rem 0;">{t('barber_no_current_customer', lang)}</h4>
<p style="font-size: 0.9rem; color: var(--charcoal-muted); margin: 0 0 1rem 0;">Workstation is clean and prepared for the next client.</p>
</div>""",
                unsafe_allow_html=True,
            )
            if staff_status == "Available":
                st.button(
                    t("barber_btn_call_next", lang),
                    key=f"barber_call_next_empty_{active_barber_id}",
                    type="primary",
                    use_container_width=True,
                    on_click=on_call_next,
                    args=(active_barber_id,),
                )
            elif staff_status == "On Break":
                st.info(f"Workstation is currently On Break. Click '{t('barber_toggle_resume', lang)}' above when you are ready to resume.")

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # 3. NEXT CUSTOMER PREVIEW ("Next for You")
    st.markdown(
        f"""<div style="margin-bottom: 0.5rem;">
<span class="section-eyebrow">Upcoming Turn</span>
<h3 class="salon-heading-serif" style="font-size: 1.35rem; margin: 0;">{t('barber_next_preview_title', lang)}</h3>
</div>""",
        unsafe_allow_html=True,
    )

    next_cust = data_mgr.get_next_customer_for_staff(active_barber_id)
    if next_cust:
        n_tok = next_cust["token"]
        n_name = next_cust["customer_name"]
        n_pref = next_cust.get("barber_pref", "any")
        n_pref_text = "★ Specifically Requested You" if n_pref == active_barber_id else "👥 Any Barber (Fastest)"
        n_services = [services_dict[s][f"name_{lang}"] for s in next_cust.get("services", []) if s in services_dict]
        n_services_str = ", ".join(n_services) if n_services else "—"
        n_duration = next_cust.get("total_duration", 30)
        n_price = next_cust.get("total_price", 0)

        with st.container(border=True):
            col_n1, col_n2 = st.columns([3, 1], vertical_alignment="center")
            with col_n1:
                st.markdown(
                    f"""<div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.3rem;">
<span class="token-pill" style="font-size: 1rem; padding: 0.25rem 0.75rem;">{n_tok}</span>
<strong style="font-size: 1.15rem; color: var(--charcoal-dark);">{n_name}</strong>
<span style="font-size: 0.75rem; background: rgba(217, 104, 79, 0.1); color: var(--orange-red); padding: 0.2rem 0.55rem; border-radius: 12px; font-weight: 600;">{n_pref_text}</span>
</div>
<div style="font-size: 0.88rem; color: var(--charcoal-muted);">
✂️ {n_services_str} &nbsp;|&nbsp; ⏱️ ~{n_duration} min &nbsp;|&nbsp; <strong style="color: var(--orange-red);">₹{n_price}</strong>
</div>""",
                    unsafe_allow_html=True,
                )
            with col_n2:
                st.markdown(
                    f"""<div style="text-align: right;">
<span class="badge-status-open" style="font-size: 0.8rem;">1st in Line</span>
</div>""",
                    unsafe_allow_html=True,
                )
    else:
        with st.container(border=True):
            st.markdown(
                f"""<div style="text-align: center; padding: 1.25rem; color: var(--charcoal-muted); font-size: 0.9rem;">
{t('barber_no_next_customer', lang)}
</div>""",
                unsafe_allow_html=True,
            )


@st.fragment(run_every=5)
def render_tv_display_content(lang: str):
    """Fragment that automatically refreshes waiting lobby metrics and turns every 5 seconds."""
    data_mgr = get_data_manager()
    staff_dict = data_mgr.get_staff()
    services_dict = data_mgr.get_services()

    # 1. NEWLY CALLED TOKEN BANNER (Gold Flashing & Audio Chime)
    called_tickets = [t for t in data_mgr.queue if t.get("status") == "CALLED"]
    if called_tickets:
        # Web Audio API chime (harmonic sine bell chime with safe autoplay fallback)
        st.markdown(
            """<script>
            try {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (AudioCtx) {
                    const ctx = new AudioCtx();
                    const now = ctx.currentTime;
                    const osc1 = ctx.createOscillator();
                    const gain1 = ctx.createGain();
                    osc1.type = 'sine';
                    osc1.frequency.setValueAtTime(659.25, now);
                    gain1.gain.setValueAtTime(0.3, now);
                    gain1.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
                    osc1.connect(gain1);
                    gain1.connect(ctx.destination);
                    osc1.start(now);
                    osc1.stop(now + 1.2);

                    const osc2 = ctx.createOscillator();
                    const gain2 = ctx.createGain();
                    osc2.type = 'sine';
                    osc2.frequency.setValueAtTime(830.61, now + 0.2);
                    gain2.gain.setValueAtTime(0.35, now + 0.2);
                    gain2.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
                    osc2.connect(gain2);
                    gain2.connect(ctx.destination);
                    osc2.start(now + 0.2);
                    osc2.stop(now + 1.5);
                }
            } catch (err) {
                console.log("Audio alert playback gracefully deferred", err);
            }
            </script>""",
            unsafe_allow_html=True,
        )

        for c_tok in called_tickets:
            c_name = c_tok.get("customer_name", "Guest")
            c_token = c_tok.get("token")
            assigned_id = c_tok.get("assigned_barber") or "barber_1"
            assigned_name = staff_dict.get(assigned_id, {}).get("name", "Station")
            assigned_role = staff_dict.get(assigned_id, {}).get(f"role_{lang}", "")

            st.markdown(
                f"""<div class="tv-called-banner">
<div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; color: #664A10; margin-bottom: 0.25rem;">
{t('display_now_calling', lang)}
</div>
<div style="font-family: 'Playfair Display', Georgia, serif; font-size: 3.2rem; font-weight: 700; color: #30251F; line-height: 1.1; margin: 0.35rem 0;">
{c_token} · {c_name}
</div>
<div style="font-size: 1.2rem; font-weight: 700; color: #A83B25;">
{t('display_proceed_to', lang).format(station=assigned_name, staff=assigned_role)}
</div>
</div>""",
                unsafe_allow_html=True,
            )

    # 2. TOP ROW: TEAM CARDS / ACTIVE STATIONS
    st.markdown(
        f"""<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.75rem;">
<div>
<span class="section-eyebrow">Station Progress</span>
<h3 class="salon-heading-serif" style="font-size: 1.5rem; margin: 0;">{t('display_active_stations_heading', lang)}</h3>
</div>
<div style="color: var(--charcoal-muted); font-size: 0.85rem;">
4 On-Duty Workstations
</div>
</div>""",
        unsafe_allow_html=True,
    )

    t1, t2, t3, t4 = st.columns(4, gap="medium")
    for col, (sid, sinfo) in zip([t1, t2, t3, t4], staff_dict.items()):
        img_b64 = get_image_base64(sinfo.get("image", "assets/staff_barber1.jpg"))
        role_name = sinfo.get(f"role_{lang}", sinfo.get("role_en", "Stylist"))
        st_status = sinfo.get("status", "Available")
        curr_cust = data_mgr.get_current_customer_for_staff(sid)

        is_calling = curr_cust and curr_cust.get("status") == "CALLED"
        is_serving = curr_cust and curr_cust.get("status") == "IN_SERVICE"

        if is_calling:
            tok = curr_cust["token"]
            cust_name = curr_cust.get("customer_name", "")
            status_html = (
                f'<div style="text-align: center; background: #FDF6E2; border: 1.5px solid var(--golden-yellow); border-radius: 8px; padding: 0.2rem 0.5rem; width: 100%; box-sizing: border-box;">'
                f'<div style="font-weight: 800; color: #7D5B15; font-size: 0.95rem; font-family: \'Playfair Display\', Georgia, serif; line-height: 1.2;">🔔 {tok}</div>'
                f'<div style="color: var(--charcoal-dark); font-weight: 600; font-size: 0.78rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{cust_name}</div>'
                f'</div>'
            )
        elif is_serving:
            tok = curr_cust["token"]
            cust_name = curr_cust.get("customer_name", "")
            status_html = (
                f'<div style="text-align: center; width: 100%;">'
                f'<div class="tv-token-now" style="margin-top: 0; padding: 0.15rem 0.5rem; font-size: 1.05rem;">{tok}</div>'
                f'<div style="font-size: 0.78rem; color: var(--charcoal-muted); margin-top: 0.2rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{cust_name}</div>'
                f'</div>'
            )
        elif st_status == "Available":
            status_html = (
                f'<div style="text-align: center; width: 100%;">'
                f'<span class="badge-status-open" style="display: inline-block; font-size: 0.82rem; padding: 0.35rem 0.75rem;">● {t("display_station_free", lang)}</span>'
                f'</div>'
            )
        else:
            status_html = (
                f'<div style="text-align: center; width: 100%;">'
                f'<span class="badge-status-closed" style="display: inline-block; font-size: 0.82rem; padding: 0.35rem 0.75rem; background: #FDF6E2; color: #7D5B15; border-color: var(--golden-yellow);">● {t("display_station_break", lang)}</span>'
                f'</div>'
            )

        staff_name = sinfo.get("name", "Stylist")
        card_html = (
            f'<div class="tv-station-card-inner">'
            f'<div>'
            f'<div class="tv-station-img-frame"><img src="{img_b64}" alt="{staff_name}"></div>'
            f'<div class="tv-station-name">{staff_name}</div>'
            f'<div class="tv-station-role">{role_name}</div>'
            f'</div>'
            f'<div class="tv-station-status-box">{status_html}</div>'
            f'</div>'
        )

        with col:
            with st.container(border=True):
                st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)

    # 3. BOTTOM SECTION: UP NEXT (Next 5 Queue Tokens)
    st.markdown(
        f"""<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.75rem;">
<div>
<span class="section-eyebrow">Upcoming Turns</span>
<h3 class="salon-heading-serif" style="font-size: 1.5rem; margin: 0;">{t('display_upnext_heading', lang)}</h3>
</div>
<div style="color: var(--charcoal-muted); font-size: 0.85rem;">
FIFO Waiting Queue
</div>
</div>""",
        unsafe_allow_html=True,
    )

    waiting_tickets = [t for t in data_mgr.queue if t.get("status") == "WAITING"][:5]

    if waiting_tickets:
        for idx, ticket in enumerate(waiting_tickets, start=1):
            tok = ticket.get("token")
            c_name = ticket.get("customer_name")
            s_ids = ticket.get("services", [])
            s_names = [services_dict[s][f"name_{lang}"] for s in s_ids if s in services_dict]
            s_display = ", ".join(s_names) if s_names else "Service"
            b_pref = ticket.get("barber_pref", "any")
            pref_display = staff_dict[b_pref]["name"] if (b_pref != "any" and b_pref in staff_dict) else "Any Stylist"
            est_wait = data_mgr.get_ticket_wait_time(tok)

            with st.container(border=True):
                col_u1, col_u2, col_u3, col_u4 = st.columns([1.5, 3, 2, 1.5], vertical_alignment="center")
                with col_u1:
                    st.markdown(
                        f"""<div style="display: flex; align-items: center; gap: 0.6rem;">
<span style="font-size: 1.15rem; font-weight: 800; color: var(--rose-pink);">#{idx}</span>
<span class="tv-upnext-token">{tok}</span>
</div>""",
                        unsafe_allow_html=True,
                    )
                with col_u2:
                    st.markdown(
                        f"""<div>
<div style="font-weight: 700; font-size: 1.1rem; color: var(--charcoal-dark);">{c_name}</div>
<div style="color: var(--charcoal-muted); font-size: 0.85rem;">✂️ {s_display}</div>
</div>""",
                        unsafe_allow_html=True,
                    )
                with col_u3:
                    st.markdown(
                        f"""<div>
<span style="background: rgba(230, 185, 87, 0.15); color: #7D5B15; border: 1px solid var(--golden-yellow); padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
★ {pref_display}
</span>
</div>""",
                        unsafe_allow_html=True,
                    )
                with col_u4:
                    st.markdown(
                        f"""<div class="tv-upnext-time-wrapper" style="text-align: right;">
<div style="font-weight: 700; font-size: 1.05rem; color: var(--orange-red);">⏱️ ~{est_wait} min</div>
<div style="font-size: 0.75rem; color: var(--charcoal-muted); text-transform: uppercase; letter-spacing: 0.5px;">Estimated Wait</div>
</div>""",
                        unsafe_allow_html=True,
                    )
    else:
        with st.container(border=True):
            st.markdown(
                f"""<div style="text-align: center; padding: 2.5rem 1rem;">
<div style="font-size: 3rem; margin-bottom: 0.5rem;">🎉</div>
<h3 class="salon-heading-serif" style="color: #879B78; font-size: 1.5rem; margin: 0 0 0.4rem 0;">{t('display_empty_queue', lang)}</h3>
<p style="color: var(--charcoal-muted); font-size: 0.95rem; margin: 0;">Our artists are ready to welcome walk-in guests immediately.</p>
</div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

    # 4. THANK-YOU FOOTER
    st.markdown(
        f"""<div style="background: linear-gradient(135deg, rgba(255, 250, 234, 0.85) 0%, rgba(227, 154, 158, 0.2) 100%); border: 1px solid var(--card-border); border-radius: 14px; padding: 1.25rem 1.5rem; text-align: center;">
<div style="font-size: 0.95rem; color: var(--charcoal-dark); font-weight: 600; margin-bottom: 0.3rem;">
{t('display_footer_thanks', lang)}
</div>
<div style="font-size: 0.85rem; color: var(--charcoal-muted);">
{t('display_footer_hours', lang)} &nbsp;•&nbsp; SALt N' PEPPER Queue Management System
</div>
</div>""",
        unsafe_allow_html=True,
    )


def render_screen_display():
    """Screen 6: Waiting Area TV (/display) - Real-time unattended lobby display per docs/02-screens.md."""
    lang = st.session_state.lang
    data_mgr = get_data_manager()

    # Public Display Header
    col_h1, col_h2 = st.columns([3, 1], vertical_alignment="center")
    with col_h1:
        st.markdown(
            f"""<div style="margin-bottom: 0.5rem;">
<span class="section-eyebrow">Public Waiting Lobby</span>
<h2 class="salon-heading-serif" style="margin: 0.1rem 0 0.3rem 0; font-size: 2rem;">{t('display_view_title', lang)}</h2>
<p style="font-size: 0.95rem; color: var(--charcoal-muted); margin: 0;">{t('display_view_subtitle', lang)}</p>
</div>""",
            unsafe_allow_html=True,
        )
    with col_h2:
        is_open = data_mgr.is_online_queue_open()
        status_chip = f"<span class='badge-status-open' style='font-size: 0.85rem;'>● {t('status_open', lang)} · Closes 9 PM</span>" if is_open else f"<span class='badge-status-closed'>● {t('err_queue_closed', lang)}</span>"
        st.markdown(
            f"""<div class="tv-header-status-wrapper" style="text-align: right;">
{status_chip}
<div style="font-size: 0.8rem; color: var(--charcoal-muted); margin-top: 0.3rem;">Auto-updates live every 5s</div>
</div>""",
            unsafe_allow_html=True,
        )

    # Render fragment that auto-refreshes every 5 seconds
    render_tv_display_content(lang)


@st.dialog("Confirm Settings Update")
def dialog_confirm_save_settings(pending_services: Dict[str, Dict[str, Any]], pending_duty: Dict[str, bool]):
    lang = st.session_state.get("lang", "en")
    data_mgr = get_data_manager()

    st.markdown(
        f"""
        <div style="font-size: 1rem; color: var(--charcoal-dark); margin-bottom: 1.25rem; line-height: 1.5;">
            {t('admin_save_dialog_msg', lang)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_cancel, col_confirm = st.columns(2, gap="medium")
    with col_cancel:
        if st.button(t("admin_save_dialog_btn_cancel", lang), use_container_width=True, key="dlg_cancel_save"):
            st.rerun()

    with col_confirm:
        if st.button(t("admin_save_dialog_btn_confirm", lang), type="primary", use_container_width=True, key="dlg_confirm_save"):
            ok_s, msg_s = data_mgr.update_services(pending_services)
            ok_d, msg_d = data_mgr.update_staff_duty(pending_duty)
            if ok_s and ok_d:
                st.session_state.admin_save_success = True
                st.session_state.admin_save_error = None
            else:
                st.session_state.admin_save_success = False
                st.session_state.admin_save_error = msg_s if not ok_s else msg_d
            st.rerun()


def render_screen_admin():
    """Screen 7: Owner Settings (/admin) - Full service management, staff roster, online queue control and today's metrics."""
    lang = st.session_state.lang
    data_mgr = get_data_manager()

    render_staff_session_bar()

    # 1. SCREEN HEADER
    st.markdown(
        f"""
        <div class="screen-banner">
            <span class="section-eyebrow">Executive Management</span>
            <h2 class="salon-heading-serif" style="font-size: 2.2rem; margin: 0.15rem 0 0.35rem 0;">
                {t('admin_view_title', lang)}
            </h2>
            <p style="color: var(--charcoal-muted); font-size: 1rem; margin: 0;">
                {t('admin_view_subtitle', lang)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("admin_save_success"):
        st.success(f"✅ {t('admin_save_success', lang)}")
        st.session_state.admin_save_success = False
    elif st.session_state.get("admin_save_error"):
        st.error(f"❌ {st.session_state.admin_save_error}")
        st.session_state.admin_save_error = None

    # 2. TODAY'S SALON PERFORMANCE (METRIC CARDS)
    st.markdown(
        f"""
        <h3 class="salon-heading-serif" style="font-size: 1.4rem; color: var(--orange-red); margin: 1.5rem 0 0.8rem 0;">
            📊 {t('admin_stats_heading', lang)}
        </h3>
        """,
        unsafe_allow_html=True,
    )

    stats = data_mgr.get_today_statistics()
    m1, m2, m3, m4 = st.columns(4, gap="medium")

    with m1:
        st.markdown(
            f"""
            <div class="reception-summary-card">
                <div class="reception-summary-label">{t('admin_stat_served', lang)}</div>
                <div class="reception-summary-val" style="color: #879B78;">{stats['served']}</div>
                <small style="color: var(--charcoal-muted); font-size: 0.78rem;">Completed sessions</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div class="reception-summary-card">
                <div class="reception-summary-label">{t('admin_stat_avg_wait', lang)}</div>
                <div class="reception-summary-val" style="color: var(--orange-red);">{stats['avg_wait']} <span style="font-size: 1rem;">min</span></div>
                <small style="color: var(--charcoal-muted); font-size: 0.78rem;">Estimated turn turnaround</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="reception-summary-card">
                <div class="reception-summary-label">{t('admin_stat_noshows', lang)}</div>
                <div class="reception-summary-val" style="color: var(--rose-pink);">{stats['noshows']}</div>
                <small style="color: var(--charcoal-muted); font-size: 0.78rem;">Unclaimed spots today</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""
            <div class="reception-summary-card">
                <div class="reception-summary-label">{t('admin_stat_queue_active', lang)}</div>
                <div class="reception-summary-val" style="color: var(--golden-yellow);">{stats['waiting']}</div>
                <small style="color: var(--charcoal-muted); font-size: 0.78rem;">{stats['in_service']} currently in chair</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 3. ONLINE QUEUE ACCESS CONTROL
    st.markdown(
        f"""
        <h3 class="salon-heading-serif" style="font-size: 1.4rem; color: var(--orange-red); margin: 0 0 0.8rem 0;">
            🌐 {t('admin_queue_control_heading', lang)}
        </h3>
        """,
        unsafe_allow_html=True,
    )

    is_queue_open = data_mgr.is_online_queue_open()
    with st.container(border=True):
        col_q_info, col_q_toggle = st.columns([3, 1.2], vertical_alignment="center")
        with col_q_info:
            q_badge = f'<span class="badge-status-open" style="font-size: 0.9rem;">● {t("status_open", lang)}</span>' if is_queue_open else f'<span class="badge-status-closed" style="font-size: 0.9rem;">● {t("status_closed", lang)}</span>'
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.4rem;">
                    <strong style="font-size: 1.05rem;">{t('admin_queue_status_label', lang)}:</strong>
                    {q_badge}
                </div>
                <p style="color: var(--charcoal-muted); font-size: 0.88rem; margin: 0; line-height: 1.4;">
                    {t('admin_queue_open_desc', lang) if is_queue_open else t('admin_queue_closed_desc', lang)}
                </p>
                """,
                unsafe_allow_html=True,
            )
        with col_q_toggle:
            if is_queue_open:
                if st.button(t("admin_queue_toggle_close", lang), use_container_width=True, key="btn_close_queue"):
                    data_mgr.set_online_queue_status(False)
                    st.rerun()
            else:
                if st.button(t("admin_queue_toggle_open", lang), use_container_width=True, key="btn_open_queue", type="primary"):
                    data_mgr.set_online_queue_status(True)
                    st.rerun()

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 4. MANAGE SERVICES (STRICT ₹250 TO ₹1,200 RANGE)
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.8rem;">
            <h3 class="salon-heading-serif" style="font-size: 1.4rem; color: var(--orange-red); margin: 0;">
                ✂️ {t('admin_services_heading', lang)}
            </h3>
            <span style="font-size: 0.85rem; color: var(--charcoal-muted); font-weight: 600;">Approved range: ₹250 – ₹1,200 per service</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    services_data = data_mgr.get_services()
    service_items = list(services_data.items())

    # 2x2 Grid of services
    s_r1_c1, s_r1_c2 = st.columns(2, gap="large")
    s_r2_c1, s_r2_c2 = st.columns(2, gap="large")
    service_cols = [s_r1_c1, s_r1_c2, s_r2_c1, s_r2_c2]

    # Session state tracking for pending edits
    if "admin_pending_services" not in st.session_state:
        st.session_state.admin_pending_services = {}

    for col, (sid, sinfo) in zip(service_cols, service_items):
        with col:
            with st.container(border=True):
                # Service Header with Image thumbnail & active tag
                img_path = sinfo.get("image", "")
                img_b64 = get_image_base64(img_path)

                header_left, header_right = st.columns([3, 1], vertical_alignment="center")
                with header_left:
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                            <img src="{img_b64}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover; border: 1px solid var(--card-border);" alt="{sinfo.get('name_en', sid)}">
                            <div>
                                <h4 style="margin: 0; font-size: 1.05rem; color: var(--charcoal-dark); font-weight: 700;">{sinfo.get(f'name_{lang}', sid)}</h4>
                                <small style="color: var(--charcoal-muted); font-size: 0.78rem;">ID: <code>{sid}</code></small>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with header_right:
                    is_active_val = st.toggle(
                        t("admin_service_active", lang),
                        value=bool(sinfo.get("active", True)),
                        key=f"srv_active_{sid}",
                    )

                # Editable fields
                c_name_en, c_name_gu = st.columns(2, gap="small")
                with c_name_en:
                    name_en_val = st.text_input(
                        t("admin_service_name_en", lang),
                        value=sinfo.get("name_en", ""),
                        key=f"srv_name_en_{sid}",
                    )
                with c_name_gu:
                    name_gu_val = st.text_input(
                        t("admin_service_name_gu", lang),
                        value=sinfo.get("name_gu", ""),
                        key=f"srv_name_gu_{sid}",
                    )

                c_price, c_dur = st.columns(2, gap="small")
                with c_price:
                    price_val = st.number_input(
                        t("admin_service_price", lang),
                        min_value=250,
                        max_value=1200,
                        value=int(sinfo.get("price", 350)),
                        step=50,
                        key=f"srv_price_{sid}",
                        help="Approved salon range is ₹250 to ₹1,200 (TC-02).",
                    )
                with c_dur:
                    dur_val = st.number_input(
                        t("admin_service_duration", lang),
                        min_value=10,
                        max_value=180,
                        value=int(sinfo.get("duration", 30)),
                        step=5,
                        key=f"srv_dur_{sid}",
                    )

                st.session_state.admin_pending_services[sid] = {
                    "name_en": name_en_val.strip(),
                    "name_gu": name_gu_val.strip(),
                    "price": int(price_val),
                    "duration": int(dur_val),
                    "active": bool(is_active_val),
                }

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # 5. STAFF DUTY ROSTER
    st.markdown(
        f"""
        <h3 class="salon-heading-serif" style="font-size: 1.4rem; color: var(--orange-red); margin: 0 0 0.8rem 0;">
            👥 {t('admin_staff_heading', lang)}
        </h3>
        """,
        unsafe_allow_html=True,
    )

    staff_dict = data_mgr.get_staff()
    st_c1, st_c2, st_c3, st_c4 = st.columns(4, gap="medium")

    if "admin_pending_duty" not in st.session_state:
        st.session_state.admin_pending_duty = {}

    for col, (st_id, st_info) in zip([st_c1, st_c2, st_c3, st_c4], staff_dict.items()):
        img_b64 = get_image_base64(st_info["image"])
        role_name = st_info[f"role_{lang}"]
        st_status = st_info["status"]
        is_on_duty = st_info.get("on_duty", True)

        with col:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="width: 100%; height: 160px; overflow: hidden; border-radius: 8px; margin-bottom: 8px;">
                        <img src="{img_b64}" style="width: 100%; height: 100%; object-fit: cover;" alt="{st_info['name']}">
                    </div>
                    <div style="text-align: center; font-weight: 700; font-size: 1.05rem; margin-bottom: 2px;">{st_info['name']}</div>
                    <div style="text-align: center; color: var(--rose-pink); font-size: 0.82rem; font-weight: 600; height: 32px; display: flex; align-items: center; justify-content: center; margin-bottom: 6px;">{role_name}</div>
                    <div style="text-align: center; margin-bottom: 10px;">
                        <span class="badge-status-open" style="font-size: 0.75rem; padding: 2px 8px;">● {st_status}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                duty_toggle = st.toggle(
                    f"{t('admin_staff_duty_on', lang)}" if is_on_duty else f"{t('admin_staff_duty_off', lang)}",
                    value=bool(is_on_duty),
                    key=f"staff_duty_toggle_{st_id}",
                )
                st.session_state.admin_pending_duty[st_id] = bool(duty_toggle)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # 6. SAVE ALL CHANGES WITH CONFIRMATION
    st.markdown('<div class="btn-gold-cta" style="max-width: 400px; margin: 0 auto;">', unsafe_allow_html=True)
    if st.button(t("admin_btn_save_all", lang), type="primary", use_container_width=True, key="save_admin_settings_btn"):
        # Validate prices and durations before opening confirmation
        validation_error = None
        for sid, sdata in st.session_state.admin_pending_services.items():
            p = sdata.get("price", 0)
            if p < 250 or p > 1200:
                validation_error = f"Price for {sdata.get('name_en', sid)} must be strictly between ₹250 and ₹1,200 (TC-02)."
                break
            if sdata.get("duration", 0) <= 0:
                validation_error = f"Duration for {sdata.get('name_en', sid)} must be positive."
                break
            if not sdata.get("name_en") or not sdata.get("name_gu"):
                validation_error = f"Both English and Gujarati service names are required for {sid}."
                break

        if validation_error:
            st.error(f"❌ {validation_error}")
        else:
            dialog_confirm_save_settings(st.session_state.admin_pending_services, st.session_state.admin_pending_duty)
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# 10. MAIN APPLICATION DISPATCHER
# ==============================================================================

def main():
    """Main routing controller orchestrating the 7 screens."""
    render_top_bar()
    active_screen = render_navigation_sidebar()

    # Protect staff screens (Reception, Barber, Admin) with PIN authentication
    if active_screen in PROTECTED_SCREENS and not st.session_state.get("staff_authenticated", False):
        render_screen_staff_pin(active_screen)
        return

    if active_screen == "home":
        render_screen_home()
    elif active_screen == "join":
        render_screen_join()
    elif active_screen == "status":
        render_screen_status()
    elif active_screen == "reception":
        render_screen_reception()
    elif active_screen == "barber":
        render_screen_barber()
    elif active_screen == "display":
        render_screen_display()
    elif active_screen == "admin":
        render_screen_admin()
    else:
        render_screen_home()


if __name__ == "__main__":
    main()
