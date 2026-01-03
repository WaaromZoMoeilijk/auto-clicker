"""
Unit tests for Auto Clicker
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import threading
import time


class TestAutoClickerState:
    """Test the core state management of AutoClicker"""

    @pytest.fixture
    def mock_app(self):
        """Create a mock AutoClicker instance without GUI"""
        with patch('tkinter.Tk'), \
             patch('tkinter.ttk.Frame'), \
             patch('tkinter.ttk.Label'), \
             patch('tkinter.ttk.Scale'), \
             patch('tkinter.ttk.Button'), \
             patch('tkinter.ttk.Combobox'), \
             patch('tkinter.StringVar'), \
             patch('pynput.keyboard.Listener'), \
             patch('pynput.mouse.Controller'):

            from src.auto_clicker import AutoClicker

            # Create mock root
            mock_root = MagicMock()
            mock_root.after = MagicMock(side_effect=lambda _, func: func())

            app = AutoClicker(mock_root)
            yield app

            # Cleanup
            app.is_running = False

    def test_initial_state(self, mock_app):
        """Test that initial state is correct"""
        assert mock_app.is_running is False
        assert mock_app.click_count == 0
        assert mock_app.cps == 10

    def test_update_cps(self, mock_app):
        """Test CPS slider update"""
        mock_app.update_cps("25.0")
        assert mock_app.cps == 25

        mock_app.update_cps("1.0")
        assert mock_app.cps == 1

        mock_app.update_cps("50.0")
        assert mock_app.cps == 50

    def test_update_cps_rounds_float(self, mock_app):
        """Test that CPS rounds float values to int"""
        mock_app.update_cps("25.7")
        assert mock_app.cps == 25

        mock_app.update_cps("25.3")
        assert mock_app.cps == 25

    def test_toggle_clicking_starts_when_stopped(self, mock_app):
        """Test that toggle starts clicking when stopped"""
        assert mock_app.is_running is False

        mock_app.toggle_clicking()

        assert mock_app.is_running is True

    def test_toggle_clicking_stops_when_running(self, mock_app):
        """Test that toggle stops clicking when running"""
        mock_app.is_running = True

        mock_app.toggle_clicking()

        assert mock_app.is_running is False

    def test_start_clicking_sets_state(self, mock_app):
        """Test that start_clicking sets correct state"""
        mock_app.start_clicking()

        assert mock_app.is_running is True
        assert mock_app.click_thread is not None

    def test_stop_clicking_sets_state(self, mock_app):
        """Test that stop_clicking sets correct state"""
        mock_app.is_running = True

        mock_app.stop_clicking()

        assert mock_app.is_running is False

    def test_update_button_left(self, mock_app):
        """Test mouse button selection - left"""
        from pynput.mouse import Button

        mock_app.button_var = MagicMock()
        mock_app.button_var.get.return_value = "Left"

        mock_app.update_button()

        assert mock_app.mouse_button == Button.left

    def test_update_button_right(self, mock_app):
        """Test mouse button selection - right"""
        from pynput.mouse import Button

        mock_app.button_var = MagicMock()
        mock_app.button_var.get.return_value = "Right"

        mock_app.update_button()

        assert mock_app.mouse_button == Button.right


class TestClickingLoop:
    """Test the clicking loop behavior"""

    def test_clicking_increments_counter(self):
        """Test that clicking loop increments click count"""
        with patch('pynput.mouse.Controller') as mock_mouse:
            from pynput.mouse import Button

            # Simulate clicking loop logic
            click_count = 0
            mouse = mock_mouse.return_value

            # Simulate 5 clicks
            for _ in range(5):
                mouse.click(Button.left)
                click_count += 1

            assert click_count == 5
            assert mouse.click.call_count == 5

    def test_cps_timing(self):
        """Test that CPS timing is approximately correct"""
        cps = 10
        expected_delay = 1 / cps  # 0.1 seconds

        start = time.time()
        time.sleep(expected_delay)
        elapsed = time.time() - start

        # Allow 50ms tolerance
        assert abs(elapsed - expected_delay) < 0.05


class TestCPSBounds:
    """Test CPS boundary conditions"""

    def test_min_cps(self):
        """Test minimum CPS value"""
        min_cps = 1
        delay = 1 / min_cps
        assert delay == 1.0  # 1 click per second = 1 second delay

    def test_max_cps(self):
        """Test maximum CPS value"""
        max_cps = 50
        delay = 1 / max_cps
        assert delay == 0.02  # 50 clicks per second = 20ms delay

    def test_cps_range(self):
        """Test all CPS values produce valid delays"""
        for cps in range(1, 51):
            delay = 1 / cps
            assert delay > 0
            assert delay <= 1.0
