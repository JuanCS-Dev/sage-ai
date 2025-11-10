"""
Playwright Browser Controller - Concrete Implementation
=======================================================

Playwright-based implementation of BrowserController interface.

Features:
- Async-first architecture
- Context manager support
- Automatic resource cleanup
- Error handling with custom exceptions
- Logging for debugging

Author: MAXIMUS AI
Date: November 10, 2025
Version: 0.1.0 (Week 1 Task 3)
"""

from typing import Optional, Any
import logging

from playwright.async_api import async_playwright, Browser, Page, Error as PlaywrightError

from .browser_controller import (
    BrowserController,
    BrowserConfig,
    BrowserType,
    BrowserLaunchError,
    BrowserNotLaunchedError,
    NavigationError,
    ScreenshotError,
    ScriptExecutionError,
)


class PlaywrightBrowserController(BrowserController):
    """
    Playwright-based browser controller implementation.

    Uses Playwright's async API for browser automation.
    Supports Chromium, Firefox, and WebKit browsers.

    Example:
        config = BrowserConfig(headless=True, viewport_width=1920)
        async with PlaywrightBrowserController(config) as controller:
            await controller.navigate("https://example.com")
            screenshot = await controller.screenshot()
            print(f"Captured screenshot: {len(screenshot)} bytes")
    """

    def __init__(
        self,
        config: Optional[BrowserConfig] = None,
        browser_type: BrowserType = BrowserType.CHROMIUM,
    ):
        """
        Initialize Playwright browser controller.

        Args:
            config: Browser configuration
            browser_type: Type of browser to use (Chromium, Firefox, WebKit)
        """
        super().__init__(config)
        self.browser_type = browser_type
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context = None
        self._page: Optional[Page] = None
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{browser_type.value}")

    async def launch(self) -> None:
        """
        Launch Playwright browser.

        Raises:
            BrowserLaunchError: If browser fails to launch
        """
        if self._is_launched:
            self.logger.warning("Browser already launched, skipping")
            return

        try:
            self.logger.info(f"Launching {self.browser_type.value} browser (headless={self.config.headless})")

            # Start Playwright
            self._playwright = await async_playwright().start()

            # Select browser type
            if self.browser_type == BrowserType.CHROMIUM:
                browser_type_obj = self._playwright.chromium
            elif self.browser_type == BrowserType.FIREFOX:
                browser_type_obj = self._playwright.firefox
            elif self.browser_type == BrowserType.WEBKIT:
                browser_type_obj = self._playwright.webkit
            else:
                raise BrowserLaunchError(f"Unsupported browser type: {self.browser_type}")

            # Launch browser
            self._browser = await browser_type_obj.launch(
                headless=self.config.headless,
                **self.config.extra_args,
            )

            # Create context with viewport
            self._context = await self._browser.new_context(
                viewport={
                    "width": self.config.viewport_width,
                    "height": self.config.viewport_height,
                },
                user_agent=self.config.user_agent,
            )

            # Set default timeout
            self._context.set_default_timeout(self.config.timeout)

            # Create page
            self._page = await self._context.new_page()

            self._is_launched = True
            self.logger.info("Browser launched successfully")

        except PlaywrightError as e:
            self.logger.error(f"Playwright error during launch: {e}")
            raise BrowserLaunchError(f"Failed to launch browser: {e}") from e
        except Exception as e:
            self.logger.error(f"Unexpected error during launch: {e}")
            raise BrowserLaunchError(f"Unexpected error launching browser: {e}") from e

    async def close(self) -> None:
        """
        Close browser and cleanup resources.

        Idempotent - safe to call multiple times.
        """
        if not self._is_launched:
            self.logger.debug("Browser not launched, nothing to close")
            return

        try:
            self.logger.info("Closing browser")

            # Close page
            if self._page:
                await self._page.close()
                self._page = None

            # Close context
            if self._context:
                await self._context.close()
                self._context = None

            # Close browser
            if self._browser:
                await self._browser.close()
                self._browser = None

            # Stop Playwright
            if self._playwright:
                await self._playwright.stop()
                self._playwright = None

            self._is_launched = False
            self.logger.info("Browser closed successfully")

        except Exception as e:
            self.logger.error(f"Error during browser close: {e}")
            # Don't raise - cleanup should always succeed

    async def navigate(self, url: str, wait_until: str = "networkidle") -> None:
        """
        Navigate to URL.

        Args:
            url: URL to navigate to
            wait_until: Wait condition ("load", "domcontentloaded", "networkidle")

        Raises:
            NavigationError: If navigation fails
            BrowserNotLaunchedError: If browser not launched
        """
        self._check_launched()

        try:
            self.logger.info(f"Navigating to: {url} (wait_until={wait_until})")

            response = await self._page.goto(url, wait_until=wait_until)

            if response and not response.ok:
                raise NavigationError(
                    f"Navigation returned error status: {response.status} - {response.status_text}"
                )

            self.logger.info(f"Navigation successful: {url}")

        except PlaywrightError as e:
            self.logger.error(f"Playwright error during navigation: {e}")
            raise NavigationError(f"Failed to navigate to {url}: {e}") from e
        except NavigationError:
            raise  # Re-raise our own exception
        except Exception as e:
            self.logger.error(f"Unexpected error during navigation: {e}")
            raise NavigationError(f"Unexpected error navigating to {url}: {e}") from e

    async def screenshot(self, full_page: bool = False) -> bytes:
        """
        Capture screenshot as PNG bytes.

        Args:
            full_page: Capture full page (with scrolling) vs viewport only

        Returns:
            Screenshot as PNG bytes

        Raises:
            ScreenshotError: If screenshot fails
            BrowserNotLaunchedError: If browser not launched
        """
        self._check_launched()

        try:
            self.logger.debug(f"Capturing screenshot (full_page={full_page})")

            screenshot_bytes = await self._page.screenshot(full_page=full_page)

            self.logger.info(f"Screenshot captured: {len(screenshot_bytes)} bytes")
            return screenshot_bytes

        except PlaywrightError as e:
            self.logger.error(f"Playwright error during screenshot: {e}")
            raise ScreenshotError(f"Failed to capture screenshot: {e}") from e
        except Exception as e:
            self.logger.error(f"Unexpected error during screenshot: {e}")
            raise ScreenshotError(f"Unexpected error capturing screenshot: {e}") from e

    async def get_url(self) -> str:
        """
        Get current page URL.

        Returns:
            Current URL as string

        Raises:
            BrowserNotLaunchedError: If browser not launched
        """
        self._check_launched()
        return self._page.url

    async def get_title(self) -> str:
        """
        Get current page title.

        Returns:
            Page title as string

        Raises:
            BrowserNotLaunchedError: If browser not launched
        """
        self._check_launched()
        return await self._page.title()

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
        self._check_launched()

        try:
            self.logger.debug(f"Executing script: {script[:100]}...")

            result = await self._page.evaluate(script)

            self.logger.debug(f"Script executed successfully: {result}")
            return result

        except PlaywrightError as e:
            self.logger.error(f"Playwright error during script execution: {e}")
            raise ScriptExecutionError(f"Failed to execute script: {e}") from e
        except Exception as e:
            self.logger.error(f"Unexpected error during script execution: {e}")
            raise ScriptExecutionError(f"Unexpected error executing script: {e}") from e

    def _check_launched(self) -> None:
        """
        Check if browser is launched.

        Raises:
            BrowserNotLaunchedError: If browser not launched
        """
        if not self._is_launched or not self._page:
            raise BrowserNotLaunchedError(
                "Browser not launched. Call launch() or use context manager."
            )
