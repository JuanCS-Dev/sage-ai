"""
Browser Action Schema Tests - Week 1, Task 5
=============================================

Comprehensive test suite for browser action schema.

Test Coverage:
- All action types (8 total)
- Action validation
- ElementSelector validation
- Enum types
- Serialization (to_dict)
- Convenience functions
- Edge cases and error handling

Author: MAXIMUS AI
Date: November 10, 2025
"""

import pytest
from datetime import datetime
from sage.browser.actions import (
    # Enums
    ActionType,
    ScrollDirection,
    WaitCondition,
    KeyboardKey,
    # Data structures
    ElementSelector,
    Action,
    # Action types
    ClickAction,
    TypeAction,
    ScrollAction,
    NavigateAction,
    WaitAction,
    PressKeyAction,
    HoverAction,
    SelectAction,
    # Convenience functions
    click,
    type_text,
    scroll,
    navigate,
    wait,
    press_key,
    hover,
    select,
)


class TestEnums:
    """Test enum types."""

    def test_action_type_values(self):
        """Test ActionType enum values."""
        assert ActionType.CLICK.value == "click"
        assert ActionType.TYPE.value == "type"
        assert ActionType.SCROLL.value == "scroll"
        assert ActionType.NAVIGATE.value == "navigate"
        assert ActionType.WAIT.value == "wait"
        assert ActionType.PRESS_KEY.value == "press_key"
        assert ActionType.HOVER.value == "hover"
        assert ActionType.SELECT.value == "select"

    def test_scroll_direction_values(self):
        """Test ScrollDirection enum values."""
        assert ScrollDirection.UP.value == "up"
        assert ScrollDirection.DOWN.value == "down"
        assert ScrollDirection.LEFT.value == "left"
        assert ScrollDirection.RIGHT.value == "right"
        assert ScrollDirection.TOP.value == "top"
        assert ScrollDirection.BOTTOM.value == "bottom"

    def test_wait_condition_values(self):
        """Test WaitCondition enum values."""
        assert WaitCondition.ELEMENT_VISIBLE.value == "element_visible"
        assert WaitCondition.ELEMENT_HIDDEN.value == "element_hidden"
        assert WaitCondition.ELEMENT_EXISTS.value == "element_exists"
        assert WaitCondition.TIMEOUT.value == "timeout"
        assert WaitCondition.NETWORKIDLE.value == "networkidle"
        assert WaitCondition.LOAD.value == "load"

    def test_keyboard_key_values(self):
        """Test KeyboardKey enum values."""
        assert KeyboardKey.ENTER.value == "Enter"
        assert KeyboardKey.TAB.value == "Tab"
        assert KeyboardKey.ESCAPE.value == "Escape"
        assert KeyboardKey.ARROW_UP.value == "ArrowUp"


class TestElementSelector:
    """Test ElementSelector class."""

    def test_css_selector_default(self):
        """Test CSS selector (default type)."""
        selector = ElementSelector("#submit-button")
        assert selector.value == "#submit-button"
        assert selector.type == "css"

    def test_xpath_selector(self):
        """Test XPath selector."""
        selector = ElementSelector("//button[@id='submit']", type="xpath")
        assert selector.value == "//button[@id='submit']"
        assert selector.type == "xpath"

    def test_text_selector(self):
        """Test text content selector."""
        selector = ElementSelector("Click me", type="text")
        assert selector.value == "Click me"
        assert selector.type == "text"

    def test_aria_label_selector(self):
        """Test ARIA label selector."""
        selector = ElementSelector("Submit form", type="aria-label")
        assert selector.value == "Submit form"
        assert selector.type == "aria-label"

    def test_invalid_selector_type(self):
        """Test invalid selector type raises error."""
        with pytest.raises(ValueError, match="Invalid selector type"):
            ElementSelector("foo", type="invalid")

    def test_empty_selector_value(self):
        """Test empty selector value raises error."""
        with pytest.raises(ValueError, match="Selector value cannot be empty"):
            ElementSelector("")

    def test_whitespace_selector_value(self):
        """Test whitespace-only selector value raises error."""
        with pytest.raises(ValueError, match="Selector value cannot be empty"):
            ElementSelector("   ")

    def test_to_dict(self):
        """Test selector serialization to dict."""
        selector = ElementSelector("#button", type="css")
        data = selector.to_dict()
        assert data == {"value": "#button", "type": "css"}


class TestClickAction:
    """Test ClickAction class."""

    def test_basic_click(self):
        """Test basic click action."""
        selector = ElementSelector("#button")
        action = ClickAction(selector=selector)

        assert action.type == ActionType.CLICK
        assert action.selector == selector
        assert action.button == "left"
        assert action.click_count == 1
        assert action.modifiers == []

    def test_right_click(self):
        """Test right click."""
        selector = ElementSelector("#button")
        action = ClickAction(selector=selector, button="right")

        assert action.button == "right"

    def test_double_click(self):
        """Test double click."""
        selector = ElementSelector("#button")
        action = ClickAction(selector=selector, click_count=2)

        assert action.click_count == 2

    def test_click_with_modifiers(self):
        """Test click with keyboard modifiers."""
        selector = ElementSelector("#button")
        action = ClickAction(selector=selector, modifiers=["Control", "Shift"])

        assert action.modifiers == ["Control", "Shift"]

    def test_click_validation_no_selector(self):
        """Test click validation fails without selector."""
        action = ClickAction()
        with pytest.raises(ValueError, match="requires a selector"):
            action.validate()

    def test_click_validation_invalid_button(self):
        """Test click validation fails with invalid button."""
        selector = ElementSelector("#button")
        action = ClickAction(selector=selector, button="invalid")
        with pytest.raises(ValueError, match="Invalid button"):
            action.validate()

    def test_click_validation_invalid_count(self):
        """Test click validation fails with invalid count."""
        selector = ElementSelector("#button")
        action = ClickAction(selector=selector, click_count=0)
        with pytest.raises(ValueError, match="click_count must be >= 1"):
            action.validate()

    def test_click_validation_invalid_modifier(self):
        """Test click validation fails with invalid modifier."""
        selector = ElementSelector("#button")
        action = ClickAction(selector=selector, modifiers=["InvalidMod"])
        with pytest.raises(ValueError, match="Invalid modifier"):
            action.validate()

    def test_click_to_dict(self):
        """Test click action serialization."""
        selector = ElementSelector("#button")
        action = ClickAction(selector=selector, button="right", click_count=2)

        data = action.to_dict()
        assert data["type"] == "click"
        assert data["selector"]["value"] == "#button"
        assert data["button"] == "right"
        assert data["click_count"] == 2


class TestTypeAction:
    """Test TypeAction class."""

    def test_basic_type(self):
        """Test basic type action."""
        selector = ElementSelector("#input")
        action = TypeAction(selector=selector, text="Hello World")

        assert action.type == ActionType.TYPE
        assert action.selector == selector
        assert action.text == "Hello World"
        assert action.delay == 0
        assert action.clear_first is False

    def test_type_with_delay(self):
        """Test type with delay (human-like typing)."""
        selector = ElementSelector("#input")
        action = TypeAction(selector=selector, text="Hello", delay=50)

        assert action.delay == 50

    def test_type_with_clear(self):
        """Test type with clear_first option."""
        selector = ElementSelector("#input")
        action = TypeAction(selector=selector, text="Hello", clear_first=True)

        assert action.clear_first is True

    def test_type_validation_no_selector(self):
        """Test type validation fails without selector."""
        action = TypeAction(text="Hello")
        with pytest.raises(ValueError, match="requires a selector"):
            action.validate()

    def test_type_validation_invalid_text_type(self):
        """Test type validation fails with non-string text."""
        selector = ElementSelector("#input")
        action = TypeAction(selector=selector, text=123)  # Not a string
        with pytest.raises(ValueError, match="text must be a string"):
            action.validate()

    def test_type_validation_negative_delay(self):
        """Test type validation fails with negative delay."""
        selector = ElementSelector("#input")
        action = TypeAction(selector=selector, text="Hello", delay=-1)
        with pytest.raises(ValueError, match="delay must be >= 0"):
            action.validate()

    def test_type_to_dict(self):
        """Test type action serialization."""
        selector = ElementSelector("#input")
        action = TypeAction(selector=selector, text="Test", delay=50, clear_first=True)

        data = action.to_dict()
        assert data["type"] == "type"
        assert data["text"] == "Test"
        assert data["delay"] == 50
        assert data["clear_first"] is True


class TestScrollAction:
    """Test ScrollAction class."""

    def test_basic_scroll(self):
        """Test basic scroll action."""
        action = ScrollAction(direction=ScrollDirection.DOWN, amount=100)

        assert action.type == ActionType.SCROLL
        assert action.direction == ScrollDirection.DOWN
        assert action.amount == 100
        assert action.smooth is True

    def test_scroll_up(self):
        """Test scroll up."""
        action = ScrollAction(direction=ScrollDirection.UP, amount=200)
        assert action.direction == ScrollDirection.UP
        assert action.amount == 200

    def test_scroll_to_top(self):
        """Test scroll to top (no amount needed)."""
        action = ScrollAction(direction=ScrollDirection.TOP)
        assert action.direction == ScrollDirection.TOP

    def test_scroll_to_bottom(self):
        """Test scroll to bottom (no amount needed)."""
        action = ScrollAction(direction=ScrollDirection.BOTTOM)
        assert action.direction == ScrollDirection.BOTTOM

    def test_scroll_within_element(self):
        """Test scroll within specific element."""
        selector = ElementSelector("#container")
        action = ScrollAction(direction=ScrollDirection.DOWN, selector=selector)
        assert action.selector == selector

    def test_scroll_validation_invalid_direction(self):
        """Test scroll validation fails with invalid direction."""
        action = ScrollAction()
        action.direction = "invalid"  # Not a ScrollDirection
        with pytest.raises(ValueError, match="Invalid direction"):
            action.validate()

    def test_scroll_validation_invalid_amount(self):
        """Test scroll validation fails with invalid amount."""
        action = ScrollAction(direction=ScrollDirection.DOWN, amount=0)
        with pytest.raises(ValueError, match="amount must be > 0"):
            action.validate()

    def test_scroll_to_dict(self):
        """Test scroll action serialization."""
        action = ScrollAction(direction=ScrollDirection.UP, amount=300)
        data = action.to_dict()
        assert data["type"] == "scroll"
        assert data["direction"] == "up"
        assert data["amount"] == 300


class TestNavigateAction:
    """Test NavigateAction class."""

    def test_basic_navigate(self):
        """Test basic navigate action."""
        action = NavigateAction(url="https://example.com")

        assert action.type == ActionType.NAVIGATE
        assert action.url == "https://example.com"
        assert action.wait_until == "load"
        assert action.timeout == 30000

    def test_navigate_with_networkidle(self):
        """Test navigate with networkidle wait."""
        action = NavigateAction(url="https://example.com", wait_until="networkidle")
        assert action.wait_until == "networkidle"

    def test_navigate_with_timeout(self):
        """Test navigate with custom timeout."""
        action = NavigateAction(url="https://example.com", timeout=60000)
        assert action.timeout == 60000

    def test_navigate_validation_empty_url(self):
        """Test navigate validation fails with empty URL."""
        action = NavigateAction(url="")
        with pytest.raises(ValueError, match="url cannot be empty"):
            action.validate()

    def test_navigate_validation_invalid_scheme(self):
        """Test navigate validation fails with invalid URL scheme."""
        action = NavigateAction(url="ftp://example.com")
        with pytest.raises(ValueError, match="Invalid URL scheme"):
            action.validate()

    def test_navigate_validation_invalid_wait(self):
        """Test navigate validation fails with invalid wait_until."""
        action = NavigateAction(url="https://example.com", wait_until="invalid")
        with pytest.raises(ValueError, match="Invalid wait_until"):
            action.validate()

    def test_navigate_validation_invalid_timeout(self):
        """Test navigate validation fails with invalid timeout."""
        action = NavigateAction(url="https://example.com", timeout=0)
        with pytest.raises(ValueError, match="timeout must be > 0"):
            action.validate()

    def test_navigate_https_url(self):
        """Test navigate with HTTPS URL."""
        action = NavigateAction(url="https://secure.example.com")
        action.validate()  # Should not raise

    def test_navigate_http_url(self):
        """Test navigate with HTTP URL."""
        action = NavigateAction(url="http://example.com")
        action.validate()  # Should not raise

    def test_navigate_to_dict(self):
        """Test navigate action serialization."""
        action = NavigateAction(url="https://example.com", wait_until="networkidle")
        data = action.to_dict()
        assert data["type"] == "navigate"
        assert data["url"] == "https://example.com"
        assert data["wait_until"] == "networkidle"


class TestWaitAction:
    """Test WaitAction class."""

    def test_basic_wait_timeout(self):
        """Test basic timeout wait."""
        action = WaitAction(condition=WaitCondition.TIMEOUT, timeout=5000)

        assert action.type == ActionType.WAIT
        assert action.condition == WaitCondition.TIMEOUT
        assert action.timeout == 5000

    def test_wait_for_element_visible(self):
        """Test wait for element visible."""
        selector = ElementSelector("#element")
        action = WaitAction(condition=WaitCondition.ELEMENT_VISIBLE, selector=selector)

        assert action.condition == WaitCondition.ELEMENT_VISIBLE
        assert action.selector == selector

    def test_wait_for_networkidle(self):
        """Test wait for networkidle."""
        action = WaitAction(condition=WaitCondition.NETWORKIDLE)
        assert action.condition == WaitCondition.NETWORKIDLE

    def test_wait_validation_invalid_condition(self):
        """Test wait validation fails with invalid condition."""
        action = WaitAction()
        action.condition = "invalid"
        with pytest.raises(ValueError, match="Invalid condition"):
            action.validate()

    def test_wait_validation_element_condition_no_selector(self):
        """Test wait validation fails when element condition has no selector."""
        action = WaitAction(condition=WaitCondition.ELEMENT_VISIBLE)
        with pytest.raises(ValueError, match="requires a selector"):
            action.validate()

    def test_wait_validation_invalid_timeout(self):
        """Test wait validation fails with invalid timeout."""
        action = WaitAction(condition=WaitCondition.TIMEOUT, timeout=0)
        with pytest.raises(ValueError, match="timeout must be > 0"):
            action.validate()

    def test_wait_to_dict(self):
        """Test wait action serialization."""
        selector = ElementSelector("#element")
        action = WaitAction(condition=WaitCondition.ELEMENT_VISIBLE, selector=selector)
        data = action.to_dict()
        assert data["type"] == "wait"
        assert data["condition"] == "element_visible"


class TestPressKeyAction:
    """Test PressKeyAction class."""

    def test_basic_press_key(self):
        """Test basic press key action."""
        action = PressKeyAction(key="Enter")

        assert action.type == ActionType.PRESS_KEY
        assert action.key == "Enter"
        assert action.modifiers == []

    def test_press_key_with_modifier(self):
        """Test press key with modifier."""
        action = PressKeyAction(key="c", modifiers=["Control"])
        assert action.key == "c"
        assert action.modifiers == ["Control"]

    def test_press_key_validation_empty_key(self):
        """Test press key validation fails with empty key."""
        action = PressKeyAction(key="")
        with pytest.raises(ValueError, match="key cannot be empty"):
            action.validate()

    def test_press_key_validation_invalid_modifier(self):
        """Test press key validation fails with invalid modifier."""
        action = PressKeyAction(key="a", modifiers=["InvalidMod"])
        with pytest.raises(ValueError, match="Invalid modifier"):
            action.validate()

    def test_press_key_to_dict(self):
        """Test press key action serialization."""
        action = PressKeyAction(key="Tab")
        data = action.to_dict()
        assert data["type"] == "press_key"
        assert data["key"] == "Tab"


class TestHoverAction:
    """Test HoverAction class."""

    def test_basic_hover(self):
        """Test basic hover action."""
        selector = ElementSelector("#element")
        action = HoverAction(selector=selector)

        assert action.type == ActionType.HOVER
        assert action.selector == selector

    def test_hover_validation_no_selector(self):
        """Test hover validation fails without selector."""
        action = HoverAction()
        with pytest.raises(ValueError, match="requires a selector"):
            action.validate()

    def test_hover_to_dict(self):
        """Test hover action serialization."""
        selector = ElementSelector("#element")
        action = HoverAction(selector=selector)
        data = action.to_dict()
        assert data["type"] == "hover"
        assert data["selector"]["value"] == "#element"


class TestSelectAction:
    """Test SelectAction class."""

    def test_select_by_value(self):
        """Test select by value."""
        selector = ElementSelector("#dropdown")
        action = SelectAction(selector=selector, value="option1")

        assert action.type == ActionType.SELECT
        assert action.selector == selector
        assert action.value == "option1"
        assert action.label is None
        assert action.index is None

    def test_select_by_label(self):
        """Test select by label."""
        selector = ElementSelector("#dropdown")
        action = SelectAction(selector=selector, label="Option 1")

        assert action.label == "Option 1"
        assert action.value is None
        assert action.index is None

    def test_select_by_index(self):
        """Test select by index."""
        selector = ElementSelector("#dropdown")
        action = SelectAction(selector=selector, index=0)

        assert action.index == 0
        assert action.value is None
        assert action.label is None

    def test_select_validation_no_selector(self):
        """Test select validation fails without selector."""
        action = SelectAction(value="option1")
        with pytest.raises(ValueError, match="requires a selector"):
            action.validate()

    def test_select_validation_no_selection_method(self):
        """Test select validation fails without selection method."""
        selector = ElementSelector("#dropdown")
        action = SelectAction(selector=selector)
        with pytest.raises(ValueError, match="requires one of: value, label, or index"):
            action.validate()

    def test_select_validation_multiple_selection_methods(self):
        """Test select validation fails with multiple selection methods."""
        selector = ElementSelector("#dropdown")
        action = SelectAction(selector=selector, value="opt1", label="Option 1")
        with pytest.raises(ValueError, match="accepts only one of"):
            action.validate()

    def test_select_validation_negative_index(self):
        """Test select validation fails with negative index."""
        selector = ElementSelector("#dropdown")
        action = SelectAction(selector=selector, index=-1)
        with pytest.raises(ValueError, match="index must be >= 0"):
            action.validate()

    def test_select_to_dict(self):
        """Test select action serialization."""
        selector = ElementSelector("#dropdown")
        action = SelectAction(selector=selector, value="option1")
        data = action.to_dict()
        assert data["type"] == "select"
        assert data["value"] == "option1"


class TestConvenienceFunctions:
    """Test convenience functions for action creation."""

    def test_click_convenience(self):
        """Test click convenience function."""
        action = click("#button")
        assert isinstance(action, ClickAction)
        assert action.selector.value == "#button"
        assert action.selector.type == "css"

    def test_click_convenience_with_xpath(self):
        """Test click convenience with XPath."""
        action = click("//button[@id='submit']", selector_type="xpath")
        assert action.selector.type == "xpath"

    def test_type_text_convenience(self):
        """Test type_text convenience function."""
        action = type_text("#input", "Hello World")
        assert isinstance(action, TypeAction)
        assert action.text == "Hello World"

    def test_scroll_convenience(self):
        """Test scroll convenience function."""
        action = scroll(ScrollDirection.DOWN, 200)
        assert isinstance(action, ScrollAction)
        assert action.direction == ScrollDirection.DOWN
        assert action.amount == 200

    def test_navigate_convenience(self):
        """Test navigate convenience function."""
        action = navigate("https://example.com")
        assert isinstance(action, NavigateAction)
        assert action.url == "https://example.com"

    def test_wait_convenience(self):
        """Test wait convenience function."""
        action = wait(WaitCondition.TIMEOUT, 3000)
        assert isinstance(action, WaitAction)
        assert action.condition == WaitCondition.TIMEOUT
        assert action.timeout == 3000

    def test_press_key_convenience(self):
        """Test press_key convenience function."""
        action = press_key("Enter")
        assert isinstance(action, PressKeyAction)
        assert action.key == "Enter"

    def test_hover_convenience(self):
        """Test hover convenience function."""
        action = hover("#element")
        assert isinstance(action, HoverAction)
        assert action.selector.value == "#element"

    def test_select_convenience(self):
        """Test select convenience function."""
        action = select("#dropdown", value="option1")
        assert isinstance(action, SelectAction)
        assert action.selector.value == "#dropdown"


class TestActionMetadata:
    """Test action metadata and timestamps."""

    def test_action_has_timestamp(self):
        """Test that actions have timestamps."""
        action = NavigateAction(url="https://example.com")
        assert action.timestamp is not None
        assert isinstance(action.timestamp, datetime)

    def test_action_has_metadata_dict(self):
        """Test that actions have metadata dict."""
        action = NavigateAction(url="https://example.com")
        assert action.metadata == {}

    def test_action_with_custom_metadata(self):
        """Test action with custom metadata."""
        metadata = {"source": "planner", "step": 1}
        action = NavigateAction(url="https://example.com", metadata=metadata)
        assert action.metadata == metadata

    def test_timestamp_in_to_dict(self):
        """Test that timestamp is included in serialization."""
        action = NavigateAction(url="https://example.com")
        data = action.to_dict()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)  # ISO format


# Test configuration
pytest_plugins = ["pytest_asyncio"]


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v", "--tb=short"])
