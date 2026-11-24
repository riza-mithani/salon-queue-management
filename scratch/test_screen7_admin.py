import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import SalonDataManager

def test_screen7_backend():
    print("Testing Screen 7 DataManager operations...")
    dm = SalonDataManager()

    # 1. Test Today's Statistics
    stats = dm.get_today_statistics()
    print("Stats:", stats)
    assert "served" in stats
    assert "avg_wait" in stats
    assert "noshows" in stats
    assert "waiting" in stats
    assert "in_service" in stats
    print("✓ get_today_statistics passed.")

    # 2. Test Online Queue Toggle
    initial_status = dm.is_online_queue_open()
    dm.set_online_queue_status(not initial_status)
    assert dm.is_online_queue_open() == (not initial_status)
    dm.set_online_queue_status(initial_status)
    assert dm.is_online_queue_open() == initial_status
    print("✓ set_online_queue_status passed.")

    # 3. Test Service Price Range Enforcement (TC-02)
    # Valid update
    valid_services = {
        "haircut": {
            "name_en": "Precision Haircut",
            "name_gu": "હેરકટ",
            "price": 400,
            "duration": 35,
            "active": True
        }
    }
    ok, msg = dm.update_services(valid_services)
    assert ok, f"Expected success but got: {msg}"
    assert dm.get_services()["haircut"]["price"] == 400
    print("✓ Valid service price update passed.")

    # Invalid update (below 250)
    low_services = {
        "haircut": {
            "name_en": "Cheap Haircut",
            "name_gu": "સસ્તું હેરકટ",
            "price": 200,
            "duration": 30,
            "active": True
        }
    }
    ok, msg = dm.update_services(low_services)
    assert not ok, "Expected price < 250 to be rejected"
    assert "250" in msg
    print("✓ Low price validation rejected (TC-02).")

    # Invalid update (above 1200)
    high_services = {
        "haircut": {
            "name_en": "Luxury Haircut",
            "name_gu": "લક્ઝરી હેરકટ",
            "price": 1500,
            "duration": 30,
            "active": True
        }
    }
    ok, msg = dm.update_services(high_services)
    assert not ok, "Expected price > 1200 to be rejected"
    assert "1,200" in msg or "1200" in msg
    print("✓ High price validation rejected (TC-02).")

    # 4. Test Staff Duty Update
    duty_update = {
        "barber_1": True,
        "stylist_1": False
    }
    ok, msg = dm.update_staff_duty(duty_update)
    assert ok, f"Expected duty update to succeed: {msg}"
    assert dm.get_staff()["stylist_1"]["on_duty"] is False
    print("✓ Staff duty update passed.")

    print("\nALL SCREEN 7 BACKEND TESTS PASSED!")

if __name__ == "__main__":
    test_screen7_backend()
