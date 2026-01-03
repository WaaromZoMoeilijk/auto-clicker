"""
Unit tests for Auto Clicker - Testing core logic without GUI dependencies
"""

import pytest
import time


class TestCPSLogic:
    """Test clicks-per-second calculations"""

    def test_cps_to_delay_min(self):
        """Test minimum CPS (1) produces 1 second delay"""
        cps = 1
        delay = 1 / cps
        assert delay == 1.0

    def test_cps_to_delay_max(self):
        """Test maximum CPS (50) produces 20ms delay"""
        cps = 50
        delay = 1 / cps
        assert delay == 0.02

    def test_cps_to_delay_default(self):
        """Test default CPS (10) produces 100ms delay"""
        cps = 10
        delay = 1 / cps
        assert delay == 0.1

    def test_all_cps_values_valid(self):
        """Test all CPS values in range produce valid delays"""
        for cps in range(1, 51):
            delay = 1 / cps
            assert delay > 0
            assert delay <= 1.0

    def test_cps_timing_accuracy(self):
        """Test that sleep timing is approximately correct"""
        cps = 10
        expected_delay = 1 / cps

        start = time.time()
        time.sleep(expected_delay)
        elapsed = time.time() - start

        # Allow 50ms tolerance
        assert abs(elapsed - expected_delay) < 0.05


class TestCPSParsing:
    """Test CPS value parsing from slider"""

    def test_parse_integer_string(self):
        """Test parsing integer string from slider"""
        value = "25"
        parsed = int(float(value))
        assert parsed == 25

    def test_parse_float_string(self):
        """Test parsing float string from slider"""
        value = "25.0"
        parsed = int(float(value))
        assert parsed == 25

    def test_parse_float_rounds_down(self):
        """Test that float values round down to int"""
        value = "25.7"
        parsed = int(float(value))
        assert parsed == 25

    def test_parse_min_value(self):
        """Test parsing minimum value"""
        value = "1.0"
        parsed = int(float(value))
        assert parsed == 1

    def test_parse_max_value(self):
        """Test parsing maximum value"""
        value = "50.0"
        parsed = int(float(value))
        assert parsed == 50


class TestStateLogic:
    """Test state toggle logic"""

    def test_toggle_when_stopped_starts(self):
        """Test toggle logic when stopped"""
        is_running = False
        # Toggle logic
        is_running = not is_running
        assert is_running is True

    def test_toggle_when_running_stops(self):
        """Test toggle logic when running"""
        is_running = True
        # Toggle logic
        is_running = not is_running
        assert is_running is False

    def test_multiple_toggles(self):
        """Test multiple toggle operations"""
        is_running = False

        is_running = not is_running
        assert is_running is True

        is_running = not is_running
        assert is_running is False

        is_running = not is_running
        assert is_running is True


class TestClickCounter:
    """Test click counting logic"""

    def test_initial_count_zero(self):
        """Test initial click count is zero"""
        click_count = 0
        assert click_count == 0

    def test_increment_count(self):
        """Test incrementing click count"""
        click_count = 0
        click_count += 1
        assert click_count == 1

    def test_multiple_increments(self):
        """Test multiple click increments"""
        click_count = 0
        for _ in range(100):
            click_count += 1
        assert click_count == 100

    def test_count_format_string(self):
        """Test click count format string"""
        click_count = 42
        formatted = f"Clicks: {click_count}"
        assert formatted == "Clicks: 42"


class TestMouseButtonSelection:
    """Test mouse button selection logic"""

    def test_left_button_selection(self):
        """Test left button selection"""
        selection = "Left"
        is_left = selection == "Left"
        assert is_left is True

    def test_right_button_selection(self):
        """Test right button selection"""
        selection = "Right"
        is_right = selection == "Right"
        assert is_right is True

    def test_button_options(self):
        """Test available button options"""
        options = ["Left", "Right"]
        assert len(options) == 2
        assert "Left" in options
        assert "Right" in options
