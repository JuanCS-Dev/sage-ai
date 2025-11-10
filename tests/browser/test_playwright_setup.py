"""
Test Playwright Setup - Week 1, Task 2
========================================

Validates that Playwright is correctly installed and configured.

Test Coverage:
- Playwright import
- Browser launch (Chromium headless)
- Page navigation
- Screenshot capture
- Browser cleanup

Author: MAXIMUS AI
Date: November 10, 2025
"""

import pytest
from playwright.sync_api import sync_playwright, Browser, Page


class TestPlaywrightSetup:
    """Test suite for Playwright installation and basic functionality."""

    def test_playwright_import(self):
        """Test that Playwright can be imported successfully."""
        from playwright.sync_api import sync_playwright
        assert sync_playwright is not None, "Playwright import failed"

    def test_browser_launch_headless(self):
        """Test launching Chromium in headless mode."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            assert browser is not None, "Browser launch failed"
            assert browser.is_connected(), "Browser not connected"
            browser.close()

    def test_page_navigation(self):
        """Test basic page navigation."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to example.com (simple, fast test page)
            response = page.goto("https://example.com", wait_until="networkidle")

            assert response is not None, "Navigation failed"
            assert response.ok, f"Navigation returned error: {response.status}"
            assert "example" in page.title().lower(), f"Unexpected title: {page.title()}"

            browser.close()

    def test_screenshot_capture(self):
        """Test screenshot capture functionality."""
        import tempfile
        import os

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com", wait_until="networkidle")

            # Create temporary file for screenshot
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                screenshot_path = tmp.name

            try:
                # Capture screenshot
                page.screenshot(path=screenshot_path)

                # Verify screenshot file exists and has content
                assert os.path.exists(screenshot_path), "Screenshot file not created"
                assert os.path.getsize(screenshot_path) > 0, "Screenshot file is empty"

            finally:
                # Cleanup
                if os.path.exists(screenshot_path):
                    os.unlink(screenshot_path)
                browser.close()

    def test_screenshot_as_bytes(self):
        """Test screenshot capture as bytes (for vision model input)."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com", wait_until="networkidle")

            # Capture screenshot as bytes
            screenshot_bytes = page.screenshot()

            assert screenshot_bytes is not None, "Screenshot bytes are None"
            assert len(screenshot_bytes) > 0, "Screenshot bytes are empty"
            assert screenshot_bytes[:4] == b'\x89PNG', "Screenshot is not a valid PNG"

            browser.close()

    def test_browser_context_isolation(self):
        """Test browser context isolation (for sandbox security)."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # Create two isolated contexts
            context1 = browser.new_context()
            context2 = browser.new_context()

            page1 = context1.new_page()
            page2 = context2.new_page()

            # Navigate both pages
            page1.goto("https://example.com")
            page2.goto("https://example.org")

            # Verify isolation (different pages)
            assert page1.url != page2.url, "Contexts are not isolated"

            # Cleanup
            context1.close()
            context2.close()
            browser.close()

    def test_viewport_configuration(self):
        """Test custom viewport configuration (for UI element detection)."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # Create context with specific viewport
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            page = context.new_page()

            # Verify viewport size
            viewport_size = page.viewport_size
            assert viewport_size["width"] == 1920, f"Viewport width incorrect: {viewport_size['width']}"
            assert viewport_size["height"] == 1080, f"Viewport height incorrect: {viewport_size['height']}"

            context.close()
            browser.close()

    @pytest.mark.asyncio
    async def test_async_playwright(self):
        """Test async Playwright API (for SAGE's async architecture)."""
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto("https://example.com", wait_until="networkidle")
            title = await page.title()

            assert "example" in title.lower(), f"Unexpected title: {title}"

            await browser.close()


# Test configuration
pytest_plugins = ["pytest_asyncio"]


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v", "--tb=short"])
