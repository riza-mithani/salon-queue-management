import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from streamlit.testing.v1 import AppTest

def test_screen7_ui():
    print("Testing Screen 7 UI with Streamlit AppTest...")
    at = AppTest.from_file(r"d:\salon-queue\app.py", default_timeout=30)
    at.run()
    assert not at.exception, f"Exception on startup: {at.exception}"

    # Navigate to admin
    at.session_state.active_screen = "admin"
    at.run()
    assert not at.exception, f"Exception on admin screen: {at.exception}"

    # Verify elements present
    # 1. Title / Header
    markdown_texts = [m.value for m in at.markdown]
    has_admin_title = any("Owner Dashboard & Settings" in m for m in markdown_texts)
    assert has_admin_title, "Admin title not found in markdown"
    print("✓ Admin view title found.")

    # 2. Performance stats
    has_stats_heading = any("Today's Salon Performance" in m for m in markdown_texts)
    assert has_stats_heading, "Stats heading not found in markdown"
    print("✓ Stats heading found.")

    # 3. Online Queue Control
    has_queue_ctrl = any("Online Queue Access Control" in m for m in markdown_texts)
    assert has_queue_ctrl, "Queue control heading not found"
    print("✓ Queue access control found.")

    # 4. Service Management
    has_srv_heading = any("Manage Salon Services" in m for m in markdown_texts)
    assert has_srv_heading, "Services heading not found"
    print("✓ Manage services heading found.")

    # 5. Buttons
    btn_labels = [b.label for b in at.button]
    print("Found buttons:", btn_labels)
    has_save_btn = any("Save All Changes" in b for b in btn_labels)
    assert has_save_btn, "Save All Changes button not found"
    print("✓ Save All Changes button found.")

    print("\nALL SCREEN 7 APPTEST UI CHECKS PASSED!")

if __name__ == "__main__":
    test_screen7_ui()
