"""
Browser Controller Interface - SAGE Browser Automation
========================================================

Abstract interface for browser control, following Strategy pattern.
Allows pluggable browser implementations (Playwright, Selenium, etc.)

Architecture Decision:
- Interface-based design (like VisionModelInterface from Task 1)
- Async-first (SAGE's architecture is async)
- Context manager support (proper resource cleanup)
- Error handling built-in

Author: MAXIMUS AI
Date: November 10, 2025
Version: 0.1.0 (Week 1 Task 3)
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from enum import Enum
import logging


class BrowserType(Enum):
    """Supported browser types."""
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class BrowserConfig:
    """Configuration for browser launch."""

    def __init__(
        self,
        headless: bool = True,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        timeout: int = 30000,  # 30 seconds default
        user_agent: Optional[str] = None,
        extra_args: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize browser configuration.

        Args:
            headless: Run browser in headless mode (no GUI)
            viewport_width: Browser viewport width in pixels
            viewport_height: Browser viewport height in pixels
            timeout: Default timeout for operations in milliseconds
            user_agent: Custom user agent string (None = default)
            extra_args: Additional browser-specific arguments
        """
        self.headless = headless
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.timeout = timeout
        self.user_agent = user_agent
        self.extra_args = extra_args or {}


class BrowserController(ABC):
    """
    Abstract base class for browser control.

    Provides high-level interface for browser automation, abstracting
    the underlying browser driver (Playwright, Selenium, etc.)

    Usage:
        async with PlaywrightBrowserController(config) as controller:
            await controller.navigate("https://example.com")
            screenshot = await controller.screenshot()
            # ... use controller
        # Automatically closed on context exit
    """

    def __init__(self, config: Optional[BrowserConfig] = None):
        """
        Initialize browser controller.

        Args:
            config: Browser configuration (uses defaults if None)
        """
        self.config = config or BrowserConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self._is_launched = False

    @abstractmethod
    async def launch(self) -> None:
        """
        Launch the browser instance.

        Raises:
            BrowserLaunchError: If browser fails to launch
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Close the browser instance and cleanup resources.

        Should be idempotent (safe to call multiple times).
        """
        pass

    @abstractmethod
    async def navigate(self, url: str, wait_until: str = "networkidle") -> None:
        """
        Navigate to a URL.

        Args:
            url: URL to navigate to
            wait_until: Wait condition ("load", "domcontentloaded", "networkidle")

        Raises:
            NavigationError: If navigation fails
            BrowserNotLaunchedError: If browser not launched
        """
        pass

    @abstractmethod
    async def screenshot(self, full_page: bool = False) -> bytes:
        """
        Capture screenshot as bytes.

        Args:
            full_page: Capture full page (scrolling) vs viewport only

        Returns:
            Screenshot as PNG bytes (for vision model input)

        Raises:
            ScreenshotError: If screenshot capture fails
            BrowserNotLaunchedError: If browser not launched
        """
        pass

    @abstractmethod
    async def get_url(self) -> str:
        """
        Get current page URL.

        Returns:
            Current URL as string

        Raises:
            BrowserNotLaunchedError: If browser not launched
        """
        pass

    @abstractmethod
    async def get_title(self) -> str:
        """
        Get current page title.

        Returns:
            Page title as string

        Raises:
            BrowserNotLaunchedError: If browser not launched
        """
        pass

    @abstractmethod
    async def execute_script(self, script: str) -> Any:
        """
        Execute JavaScript in page context.

        Args:
            script: JavaScript code to execute

        Returns:
            Result of script execution

        Raises:
            ScriptExecutionError: If script fails
            BrowserNotLaunchedError: If browser not launched
        """
        pass

    @property
    def is_launched(self) -> bool:
        """Check if browser is launched."""
        return self._is_launched

    # Context manager support
    async def __aenter__(self):
        """Async context manager entry."""
        await self.launch()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
        return False  # Don't suppress exceptions


# Custom exceptions
class BrowserControllerError(Exception):
    """Base exception for browser controller errors."""
    pass


class BrowserLaunchError(BrowserControllerError):
    """Browser failed to launch."""
    pass


class BrowserNotLaunchedError(BrowserControllerError):
    """Operation attempted on non-launched browser."""
    pass


class NavigationError(BrowserControllerError):
    """Navigation failed."""
    pass


class ScreenshotError(BrowserControllerError):
    """Screenshot capture failed."""
    pass


class ScriptExecutionError(BrowserControllerError):
    """JavaScript execution failed."""
    pass
