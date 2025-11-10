"""
Browser Action Schema - SAGE Browser Automation
================================================

Defines the action schema for browser automation tasks.
Actions represent atomic operations the browser agent can perform.

Action Types:
- CLICK: Click on an element
- TYPE: Type text into an input field
- SCROLL: Scroll the page
- NAVIGATE: Navigate to a URL
- WAIT: Wait for element or timeout
- PRESS_KEY: Press keyboard key (Enter, Tab, Escape, etc.)
- HOVER: Hover over an element
- SELECT: Select option from dropdown

Author: MAXIMUS AI
Date: November 10, 2025
Version: 0.1.0 (Week 1 Task 5)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime


class ActionType(Enum):
    """Enumeration of browser action types."""

    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    NAVIGATE = "navigate"
    WAIT = "wait"
    PRESS_KEY = "press_key"
    HOVER = "hover"
    SELECT = "select"


class ScrollDirection(Enum):
    """Scroll direction options."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"      # Scroll to top of page
    BOTTOM = "bottom"  # Scroll to bottom of page


class WaitCondition(Enum):
    """Wait condition types."""

    ELEMENT_VISIBLE = "element_visible"
    ELEMENT_HIDDEN = "element_hidden"
    ELEMENT_EXISTS = "element_exists"
    TIMEOUT = "timeout"
    NETWORKIDLE = "networkidle"
    LOAD = "load"


class KeyboardKey(Enum):
    """Common keyboard keys."""

    ENTER = "Enter"
    TAB = "Tab"
    ESCAPE = "Escape"
    BACKSPACE = "Backspace"
    DELETE = "Delete"
    ARROW_UP = "ArrowUp"
    ARROW_DOWN = "ArrowDown"
    ARROW_LEFT = "ArrowLeft"
    ARROW_RIGHT = "ArrowRight"
    HOME = "Home"
    END = "End"
    PAGE_UP = "PageUp"
    PAGE_DOWN = "PageDown"


@dataclass
class ElementSelector:
    """
    Selector for targeting elements in the browser.

    Supports multiple selector strategies:
    - CSS selector (default)
    - XPath
    - Text content matching
    - ARIA label matching
    """

    value: str
    type: str = "css"  # css, xpath, text, aria-label

    def __post_init__(self):
        """Validate selector after initialization."""
        valid_types = ["css", "xpath", "text", "aria-label"]
        if self.type not in valid_types:
            raise ValueError(f"Invalid selector type: {self.type}. Must be one of {valid_types}")

        if not self.value or not self.value.strip():
            raise ValueError("Selector value cannot be empty")

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary representation."""
        return {
            "value": self.value,
            "type": self.type,
        }


@dataclass
class Action:
    """
    Base class for browser actions.

    All actions share common fields:
    - type: ActionType enum
    - timestamp: When action was created
    - metadata: Optional metadata for tracking
    """

    type: ActionType = field(init=False)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary representation."""
        return {
            "type": self.type.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    def validate(self) -> bool:
        """
        Validate action parameters.

        Returns:
            True if valid, raises ValueError if invalid
        """
        if not isinstance(self.type, ActionType):
            raise ValueError(f"Invalid action type: {self.type}")
        return True


@dataclass
class ClickAction(Action):
    """
    Click action - Click on an element.

    Parameters:
    - selector: ElementSelector for target element
    - button: Mouse button (left, right, middle)
    - click_count: Number of clicks (1=single, 2=double)
    - modifiers: Keyboard modifiers (Alt, Control, Meta, Shift)
    """

    selector: ElementSelector = None
    button: str = "left"  # left, right, middle
    click_count: int = 1
    modifiers: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Set action type."""
        self.type = ActionType.CLICK

    def validate(self) -> bool:
        """Validate click action parameters."""
        super().validate()

        if self.selector is None:
            raise ValueError("ClickAction requires a selector")

        valid_buttons = ["left", "right", "middle"]
        if self.button not in valid_buttons:
            raise ValueError(f"Invalid button: {self.button}. Must be one of {valid_buttons}")

        if self.click_count < 1:
            raise ValueError("click_count must be >= 1")

        valid_modifiers = ["Alt", "Control", "Meta", "Shift"]
        for mod in self.modifiers:
            if mod not in valid_modifiers:
                raise ValueError(f"Invalid modifier: {mod}. Must be one of {valid_modifiers}")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base = super().to_dict()
        base.update({
            "selector": self.selector.to_dict() if self.selector else None,
            "button": self.button,
            "click_count": self.click_count,
            "modifiers": self.modifiers,
        })
        return base


@dataclass
class TypeAction(Action):
    """
    Type action - Type text into an input field.

    Parameters:
    - selector: ElementSelector for target input field
    - text: Text to type
    - delay: Delay between keystrokes in milliseconds (for human-like typing)
    - clear_first: Clear existing text before typing
    """

    selector: ElementSelector = None
    text: str = ""
    delay: int = 0  # milliseconds between keystrokes
    clear_first: bool = False

    def __post_init__(self):
        """Set action type."""
        self.type = ActionType.TYPE

    def validate(self) -> bool:
        """Validate type action parameters."""
        super().validate()

        if self.selector is None:
            raise ValueError("TypeAction requires a selector")

        if not isinstance(self.text, str):
            raise ValueError("text must be a string")

        if self.delay < 0:
            raise ValueError("delay must be >= 0")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base = super().to_dict()
        base.update({
            "selector": self.selector.to_dict() if self.selector else None,
            "text": self.text,
            "delay": self.delay,
            "clear_first": self.clear_first,
        })
        return base


@dataclass
class ScrollAction(Action):
    """
    Scroll action - Scroll the page or an element.

    Parameters:
    - direction: ScrollDirection enum
    - amount: Scroll amount in pixels (for UP/DOWN/LEFT/RIGHT)
    - selector: Optional selector to scroll within element
    - smooth: Use smooth scrolling animation
    """

    direction: ScrollDirection = ScrollDirection.DOWN
    amount: int = 100  # pixels
    selector: Optional[ElementSelector] = None
    smooth: bool = True

    def __post_init__(self):
        """Set action type."""
        self.type = ActionType.SCROLL

    def validate(self) -> bool:
        """Validate scroll action parameters."""
        super().validate()

        if not isinstance(self.direction, ScrollDirection):
            raise ValueError(f"Invalid direction: {self.direction}")

        # TOP/BOTTOM don't need amount
        if self.direction in [ScrollDirection.TOP, ScrollDirection.BOTTOM]:
            pass
        elif self.amount <= 0:
            raise ValueError("amount must be > 0 for directional scrolls")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base = super().to_dict()
        base.update({
            "direction": self.direction.value,
            "amount": self.amount,
            "selector": self.selector.to_dict() if self.selector else None,
            "smooth": self.smooth,
        })
        return base


@dataclass
class NavigateAction(Action):
    """
    Navigate action - Navigate to a URL.

    Parameters:
    - url: Target URL
    - wait_until: Wait condition (load, networkidle, domcontentloaded)
    - timeout: Timeout in milliseconds
    """

    url: str = ""
    wait_until: str = "load"  # load, networkidle, domcontentloaded
    timeout: int = 30000  # 30 seconds default

    def __post_init__(self):
        """Set action type."""
        self.type = ActionType.NAVIGATE

    def validate(self) -> bool:
        """Validate navigate action parameters."""
        super().validate()

        if not self.url or not self.url.strip():
            raise ValueError("url cannot be empty")

        # Basic URL validation
        if not self.url.startswith(("http://", "https://", "file://", "about:")):
            raise ValueError(f"Invalid URL scheme: {self.url}")

        valid_wait = ["load", "networkidle", "domcontentloaded"]
        if self.wait_until not in valid_wait:
            raise ValueError(f"Invalid wait_until: {self.wait_until}. Must be one of {valid_wait}")

        if self.timeout <= 0:
            raise ValueError("timeout must be > 0")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base = super().to_dict()
        base.update({
            "url": self.url,
            "wait_until": self.wait_until,
            "timeout": self.timeout,
        })
        return base


@dataclass
class WaitAction(Action):
    """
    Wait action - Wait for a condition or timeout.

    Parameters:
    - condition: WaitCondition enum
    - selector: Element selector (for element conditions)
    - timeout: Timeout in milliseconds
    """

    condition: WaitCondition = WaitCondition.TIMEOUT
    selector: Optional[ElementSelector] = None
    timeout: int = 5000  # 5 seconds default

    def __post_init__(self):
        """Set action type."""
        self.type = ActionType.WAIT

    def validate(self) -> bool:
        """Validate wait action parameters."""
        super().validate()

        if not isinstance(self.condition, WaitCondition):
            raise ValueError(f"Invalid condition: {self.condition}")

        # Element conditions require selector
        element_conditions = [
            WaitCondition.ELEMENT_VISIBLE,
            WaitCondition.ELEMENT_HIDDEN,
            WaitCondition.ELEMENT_EXISTS,
        ]
        if self.condition in element_conditions and self.selector is None:
            raise ValueError(f"Condition {self.condition.value} requires a selector")

        if self.timeout <= 0:
            raise ValueError("timeout must be > 0")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base = super().to_dict()
        base.update({
            "condition": self.condition.value,
            "selector": self.selector.to_dict() if self.selector else None,
            "timeout": self.timeout,
        })
        return base


@dataclass
class PressKeyAction(Action):
    """
    Press key action - Press a keyboard key.

    Parameters:
    - key: KeyboardKey enum or string
    - modifiers: Keyboard modifiers (Alt, Control, Meta, Shift)
    """

    key: str = ""
    modifiers: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Set action type."""
        self.type = ActionType.PRESS_KEY

    def validate(self) -> bool:
        """Validate press key action parameters."""
        super().validate()

        if not self.key or not self.key.strip():
            raise ValueError("key cannot be empty")

        valid_modifiers = ["Alt", "Control", "Meta", "Shift"]
        for mod in self.modifiers:
            if mod not in valid_modifiers:
                raise ValueError(f"Invalid modifier: {mod}. Must be one of {valid_modifiers}")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base = super().to_dict()
        base.update({
            "key": self.key,
            "modifiers": self.modifiers,
        })
        return base


@dataclass
class HoverAction(Action):
    """
    Hover action - Hover mouse over an element.

    Parameters:
    - selector: ElementSelector for target element
    """

    selector: ElementSelector = None

    def __post_init__(self):
        """Set action type."""
        self.type = ActionType.HOVER

    def validate(self) -> bool:
        """Validate hover action parameters."""
        super().validate()

        if self.selector is None:
            raise ValueError("HoverAction requires a selector")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base = super().to_dict()
        base.update({
            "selector": self.selector.to_dict() if self.selector else None,
        })
        return base


@dataclass
class SelectAction(Action):
    """
    Select action - Select option from dropdown.

    Parameters:
    - selector: ElementSelector for dropdown element
    - value: Value to select (value attribute)
    - label: Label to select (visible text)
    - index: Index to select (0-based)

    Note: Exactly one of (value, label, index) must be provided.
    """

    selector: ElementSelector = None
    value: Optional[str] = None
    label: Optional[str] = None
    index: Optional[int] = None

    def __post_init__(self):
        """Set action type."""
        self.type = ActionType.SELECT

    def validate(self) -> bool:
        """Validate select action parameters."""
        super().validate()

        if self.selector is None:
            raise ValueError("SelectAction requires a selector")

        # Exactly one of (value, label, index) must be provided
        provided = sum([
            self.value is not None,
            self.label is not None,
            self.index is not None,
        ])

        if provided == 0:
            raise ValueError("SelectAction requires one of: value, label, or index")

        if provided > 1:
            raise ValueError("SelectAction accepts only one of: value, label, or index")

        if self.index is not None and self.index < 0:
            raise ValueError("index must be >= 0")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base = super().to_dict()
        base.update({
            "selector": self.selector.to_dict() if self.selector else None,
            "value": self.value,
            "label": self.label,
            "index": self.index,
        })
        return base


# Convenience functions for creating actions
def click(selector: str, selector_type: str = "css", **kwargs) -> ClickAction:
    """Create a click action."""
    return ClickAction(selector=ElementSelector(selector, selector_type), **kwargs)


def type_text(selector: str, text: str, selector_type: str = "css", **kwargs) -> TypeAction:
    """Create a type action."""
    return TypeAction(selector=ElementSelector(selector, selector_type), text=text, **kwargs)


def scroll(direction: ScrollDirection, amount: int = 100, **kwargs) -> ScrollAction:
    """Create a scroll action."""
    return ScrollAction(direction=direction, amount=amount, **kwargs)


def navigate(url: str, **kwargs) -> NavigateAction:
    """Create a navigate action."""
    return NavigateAction(url=url, **kwargs)


def wait(condition: WaitCondition, timeout: int = 5000, **kwargs) -> WaitAction:
    """Create a wait action."""
    return WaitAction(condition=condition, timeout=timeout, **kwargs)


def press_key(key: str, **kwargs) -> PressKeyAction:
    """Create a press key action."""
    return PressKeyAction(key=key, **kwargs)


def hover(selector: str, selector_type: str = "css", **kwargs) -> HoverAction:
    """Create a hover action."""
    return HoverAction(selector=ElementSelector(selector, selector_type), **kwargs)


def select(selector: str, selector_type: str = "css", **kwargs) -> SelectAction:
    """Create a select action."""
    return SelectAction(selector=ElementSelector(selector, selector_type), **kwargs)
