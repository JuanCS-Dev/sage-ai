"""
SAGE Browser Automation Module
================================

Provides browser automation capabilities for SAGE 3.0 "Heroic" upgrade.

Components:
- VisionModelInterface: Abstract interface for pluggable vision models
- ClaudeVisionModel: Claude 3.5 Sonnet implementation
- BrowserController: Playwright-based browser control
- BrowserAgent: High-level agent for autonomous browser automation

Architecture:
- Vision model: Claude 3.5 Sonnet (pluggable via Strategy pattern)
- Browser driver: Playwright (Chromium)
- Planning: Hybrid ReWOO + ReAct
- Memory: Session-based state persistence

Target: 65%+ WebVoyager benchmark by Week 8

Author: MAXIMUS AI
Date: November 10, 2025
Version: 0.1.0 (Week 1 - Foundation)
"""

__version__ = "0.1.0"
__author__ = "MAXIMUS AI"

# Core browser controller interface and implementations
from .browser_controller import (
    BrowserController,
    BrowserConfig,
    BrowserType,
    BrowserControllerError,
    BrowserLaunchError,
    BrowserNotLaunchedError,
    NavigationError,
    ScreenshotError,
    ScriptExecutionError,
)

from .playwright_controller import PlaywrightBrowserController

# Screenshot utilities
from .screenshot_utils import (
    ScreenshotProcessor,
    ScreenshotMetadata,
    encode_screenshot_base64,
    prepare_screenshot_for_claude,
)

# Action schema
from .actions import (
    # Enums
    ActionType,
    ScrollDirection,
    WaitCondition,
    KeyboardKey,
    # Core classes
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

__all__ = [
    # Core classes
    "BrowserController",
    "BrowserConfig",
    "BrowserType",
    "PlaywrightBrowserController",
    # Screenshot utilities
    "ScreenshotProcessor",
    "ScreenshotMetadata",
    "encode_screenshot_base64",
    "prepare_screenshot_for_claude",
    # Action schema - Enums
    "ActionType",
    "ScrollDirection",
    "WaitCondition",
    "KeyboardKey",
    # Action schema - Classes
    "ElementSelector",
    "Action",
    "ClickAction",
    "TypeAction",
    "ScrollAction",
    "NavigateAction",
    "WaitAction",
    "PressKeyAction",
    "HoverAction",
    "SelectAction",
    # Action schema - Convenience functions
    "click",
    "type_text",
    "scroll",
    "navigate",
    "wait",
    "press_key",
    "hover",
    "select",
    # Exceptions
    "BrowserControllerError",
    "BrowserLaunchError",
    "BrowserNotLaunchedError",
    "NavigationError",
    "ScreenshotError",
    "ScriptExecutionError",
]
