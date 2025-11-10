"""
Browser Controller Tests - Week 1, Task 3
==========================================

Comprehensive test suite for BrowserController interface and
PlaywrightBrowserController implementation.

Test Coverage:
- Browser launch and close
- Navigation
- Screenshot capture
- URL and title retrieval
- Script execution
- Error handling
- Context manager behavior
- Configuration options

Author: MAXIMUS AI
Date: November 10, 2025
"""

import pytest
from sage.browser.browser_controller import (
    BrowserController,
    BrowserConfig,
    BrowserType,
    BrowserLaunchError,
    BrowserNotLaunchedError,
    NavigationError,
    ScreenshotError,
    ScriptExecutionError,
)
from sage.browser.playwright_controller import PlaywrightBrowserController


class TestBrowserConfig:
    """Test BrowserConfig class."""

    def test_default_config(self):
        """Test default configuration values."""
        config = BrowserConfig()

        assert config.headless is True, "Default should be headless"
        assert config.viewport_width == 1920, "Default viewport width"
        assert config.viewport_height == 1080, "Default viewport height"
        assert config.timeout == 30000, "Default timeout 30s"
        assert config.user_agent is None, "Default user agent is None"
        assert config.extra_args == {}, "Default extra args empty"

    def test_custom_config(self):
        """Test custom configuration values."""
        config = BrowserConfig(
            headless=False,
            viewport_width=1280,
            viewport_height=720,
            timeout=60000,
            user_agent="Custom UA",
            extra_args={"arg1": "value1"},
        )

        assert config.headless is False
        assert config.viewport_width == 1280
        assert config.viewport_height == 720
        assert config.timeout == 60000
        assert config.user_agent == "Custom UA"
        assert config.extra_args == {"arg1": "value1"}


class TestPlaywrightBrowserController:
    """Test suite for PlaywrightBrowserController."""

    @pytest.mark.asyncio
    async def test_launch_and_close(self):
        """Test browser launch and close."""
        controller = PlaywrightBrowserController()

        # Should not be launched initially
        assert not controller.is_launched, "Browser should not be launched initially"

        # Launch
        await controller.launch()
        assert controller.is_launched, "Browser should be launched"

        # Close
        await controller.close()
        assert not controller.is_launched, "Browser should be closed"

    @pytest.mark.asyncio
    async def test_launch_idempotent(self):
        """Test that launch is idempotent (can be called multiple times)."""
        controller = PlaywrightBrowserController()

        await controller.launch()
        assert controller.is_launched

        # Launch again - should be no-op
        await controller.launch()
        assert controller.is_launched

        await controller.close()

    @pytest.mark.asyncio
    async def test_close_idempotent(self):
        """Test that close is idempotent (can be called multiple times)."""
        controller = PlaywrightBrowserController()

        await controller.launch()
        await controller.close()
        assert not controller.is_launched

        # Close again - should be no-op
        await controller.close()
        assert not controller.is_launched

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test context manager (async with) behavior."""
        async with PlaywrightBrowserController() as controller:
            assert controller.is_launched, "Browser should be launched in context"

        # After context exit, should be closed
        assert not controller.is_launched, "Browser should be closed after context"

    @pytest.mark.asyncio
    async def test_navigate(self):
        """Test navigation to URL."""
        async with PlaywrightBrowserController() as controller:
            # Navigate to example.com
            await controller.navigate("https://example.com")

            # Check URL
            url = await controller.get_url()
            assert "example.com" in url, f"URL should contain example.com, got: {url}"

    @pytest.mark.asyncio
    async def test_navigate_not_launched(self):
        """Test that navigate raises error if browser not launched."""
        controller = PlaywrightBrowserController()

        with pytest.raises(BrowserNotLaunchedError):
            await controller.navigate("https://example.com")

    @pytest.mark.asyncio
    async def test_get_title(self):
        """Test getting page title."""
        async with PlaywrightBrowserController() as controller:
            await controller.navigate("https://example.com")

            title = await controller.get_title()
            assert "example" in title.lower(), f"Title should contain 'example', got: {title}"

    @pytest.mark.asyncio
    async def test_get_title_not_launched(self):
        """Test that get_title raises error if browser not launched."""
        controller = PlaywrightBrowserController()

        with pytest.raises(BrowserNotLaunchedError):
            await controller.get_title()

    @pytest.mark.asyncio
    async def test_screenshot_viewport(self):
        """Test screenshot capture (viewport only)."""
        async with PlaywrightBrowserController() as controller:
            await controller.navigate("https://example.com")

            screenshot = await controller.screenshot(full_page=False)

            assert screenshot is not None, "Screenshot should not be None"
            assert len(screenshot) > 0, "Screenshot should have content"
            assert screenshot[:4] == b'\x89PNG', "Screenshot should be PNG"

    @pytest.mark.asyncio
    async def test_screenshot_full_page(self):
        """Test screenshot capture (full page)."""
        async with PlaywrightBrowserController() as controller:
            await controller.navigate("https://example.com")

            screenshot = await controller.screenshot(full_page=True)

            assert screenshot is not None, "Screenshot should not be None"
            assert len(screenshot) > 0, "Screenshot should have content"
            assert screenshot[:4] == b'\x89PNG', "Screenshot should be PNG"

    @pytest.mark.asyncio
    async def test_screenshot_not_launched(self):
        """Test that screenshot raises error if browser not launched."""
        controller = PlaywrightBrowserController()

        with pytest.raises(BrowserNotLaunchedError):
            await controller.screenshot()

    @pytest.mark.asyncio
    async def test_execute_script(self):
        """Test JavaScript execution."""
        async with PlaywrightBrowserController() as controller:
            await controller.navigate("https://example.com")

            # Execute simple script
            result = await controller.execute_script("1 + 1")
            assert result == 2, f"Script should return 2, got: {result}"

            # Execute script that accesses DOM
            title = await controller.execute_script("document.title")
            assert "example" in title.lower(), f"Script should return title with 'example', got: {title}"

    @pytest.mark.asyncio
    async def test_execute_script_not_launched(self):
        """Test that execute_script raises error if browser not launched."""
        controller = PlaywrightBrowserController()

        with pytest.raises(BrowserNotLaunchedError):
            await controller.execute_script("1 + 1")

    @pytest.mark.asyncio
    async def test_custom_config(self):
        """Test browser with custom configuration."""
        config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            timeout=60000,
        )

        async with PlaywrightBrowserController(config) as controller:
            await controller.navigate("https://example.com")

            # Verify viewport size via JavaScript
            width = await controller.execute_script("window.innerWidth")
            height = await controller.execute_script("window.innerHeight")

            assert width == 1280, f"Viewport width should be 1280, got: {width}"
            assert height == 720, f"Viewport height should be 720, got: {height}"

    @pytest.mark.asyncio
    async def test_invalid_url_navigation(self):
        """Test navigation to invalid URL."""
        async with PlaywrightBrowserController() as controller:
            with pytest.raises(NavigationError):
                await controller.navigate("https://this-domain-does-not-exist-12345.com")

    @pytest.mark.asyncio
    async def test_browser_type_chromium(self):
        """Test launching Chromium browser."""
        controller = PlaywrightBrowserController(
            browser_type=BrowserType.CHROMIUM
        )

        async with controller:
            await controller.navigate("https://example.com")
            title = await controller.get_title()
            assert "example" in title.lower()

    @pytest.mark.asyncio
    async def test_get_url(self):
        """Test getting current URL."""
        async with PlaywrightBrowserController() as controller:
            await controller.navigate("https://example.com")

            url = await controller.get_url()
            assert url.startswith("https://"), f"URL should start with https://, got: {url}"
            assert "example.com" in url, f"URL should contain example.com, got: {url}"

    @pytest.mark.asyncio
    async def test_get_url_not_launched(self):
        """Test that get_url raises error if browser not launched."""
        controller = PlaywrightBrowserController()

        with pytest.raises(BrowserNotLaunchedError):
            await controller.get_url()

    @pytest.mark.asyncio
    async def test_multiple_navigations(self):
        """Test multiple sequential navigations."""
        async with PlaywrightBrowserController() as controller:
            # First navigation
            await controller.navigate("https://example.com")
            url1 = await controller.get_url()
            assert "example.com" in url1

            # Second navigation
            await controller.navigate("https://example.org")
            url2 = await controller.get_url()
            assert "example.org" in url2
            assert url1 != url2, "URLs should be different after navigation"


class TestBrowserControllerInterface:
    """Test that BrowserController is properly abstract."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that BrowserController cannot be instantiated directly."""
        with pytest.raises(TypeError):
            # Should fail because abstract methods not implemented
            BrowserController()


# Test configuration
pytest_plugins = ["pytest_asyncio"]


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v", "--tb=short"])
