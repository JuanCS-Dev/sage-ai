"""
Screenshot Utilities Tests - Week 1, Task 4
============================================

Test suite for screenshot processing and vision model preparation utilities.

Test Coverage:
- Base64 encoding/decoding
- Metadata extraction
- Format detection
- Image validation
- Vision model preparation (Claude API format)

Author: MAXIMUS AI
Date: November 10, 2025
"""

import pytest
from datetime import datetime
from sage.browser.screenshot_utils import (
    ScreenshotProcessor,
    ScreenshotMetadata,
    encode_screenshot_base64,
    prepare_screenshot_for_claude,
)


class TestScreenshotMetadata:
    """Test ScreenshotMetadata dataclass."""

    def test_metadata_creation(self):
        """Test creating metadata object."""
        metadata = ScreenshotMetadata(
            size_bytes=1024,
            format="PNG",
            width=1920,
            height=1080,
            timestamp=datetime(2025, 11, 10, 12, 0, 0),
            url="https://example.com",
        )

        assert metadata.size_bytes == 1024
        assert metadata.format == "PNG"
        assert metadata.width == 1920
        assert metadata.height == 1080
        assert metadata.url == "https://example.com"

    def test_metadata_to_dict(self):
        """Test converting metadata to dictionary."""
        metadata = ScreenshotMetadata(
            size_bytes=2048,
            format="JPEG",
            width=1280,
            height=720,
        )

        data = metadata.to_dict()

        assert data["size_bytes"] == 2048
        assert data["format"] == "JPEG"
        assert data["width"] == 1280
        assert data["height"] == 720


class TestScreenshotProcessor:
    """Test suite for ScreenshotProcessor."""

    @pytest.fixture
    def processor(self):
        """Create processor instance."""
        return ScreenshotProcessor()

    @pytest.fixture
    def png_bytes(self):
        """Create sample PNG bytes (magic bytes only for testing)."""
        # PNG magic bytes + minimal data
        return b'\x89PNG\r\n\x1a\n' + b'\x00' * 100

    @pytest.fixture
    def jpeg_bytes(self):
        """Create sample JPEG bytes (magic bytes only for testing)."""
        # JPEG magic bytes + minimal data
        return b'\xff\xd8\xff\xe0' + b'\x00' * 100

    def test_encode_base64(self, processor, png_bytes):
        """Test base64 encoding."""
        encoded = processor.encode_base64(png_bytes)

        assert isinstance(encoded, str)
        assert len(encoded) > 0
        # Base64 should be longer than original (due to encoding overhead)
        assert len(encoded) > len(png_bytes) * 0.7  # Rough estimate

    def test_decode_base64(self, processor, png_bytes):
        """Test base64 decoding."""
        encoded = processor.encode_base64(png_bytes)
        decoded = processor.decode_base64(encoded)

        assert decoded == png_bytes

    def test_encode_decode_roundtrip(self, processor, png_bytes):
        """Test encode -> decode roundtrip."""
        encoded = processor.encode_base64(png_bytes)
        decoded = processor.decode_base64(encoded)

        assert decoded == png_bytes, "Roundtrip should preserve data"

    def test_detect_format_png(self, processor, png_bytes):
        """Test PNG format detection."""
        format_detected = processor._detect_format(png_bytes)
        assert format_detected == "PNG"

    def test_detect_format_jpeg(self, processor, jpeg_bytes):
        """Test JPEG format detection."""
        format_detected = processor._detect_format(jpeg_bytes)
        assert format_detected == "JPEG"

    def test_detect_format_unknown(self, processor):
        """Test unknown format detection."""
        unknown_bytes = b'UNKNOWN\x00\x00\x00'
        format_detected = processor._detect_format(unknown_bytes)
        assert format_detected == "UNKNOWN"

    def test_detect_format_too_short(self, processor):
        """Test format detection with insufficient bytes."""
        short_bytes = b'AB'
        format_detected = processor._detect_format(short_bytes)
        assert format_detected == "UNKNOWN"

    def test_extract_metadata(self, processor, png_bytes):
        """Test metadata extraction."""
        metadata = processor.extract_metadata(png_bytes, url="https://example.com")

        assert metadata.size_bytes == len(png_bytes)
        assert metadata.format == "PNG"
        assert metadata.url == "https://example.com"
        assert metadata.timestamp is not None
        assert isinstance(metadata.timestamp, datetime)

    def test_extract_metadata_no_url(self, processor, png_bytes):
        """Test metadata extraction without URL."""
        metadata = processor.extract_metadata(png_bytes)

        assert metadata.size_bytes == len(png_bytes)
        assert metadata.format == "PNG"
        assert metadata.url is None

    def test_validate_screenshot_valid_png(self, processor, png_bytes):
        """Test validation of valid PNG."""
        assert processor.validate_screenshot(png_bytes) is True

    def test_validate_screenshot_valid_jpeg(self, processor, jpeg_bytes):
        """Test validation of valid JPEG."""
        assert processor.validate_screenshot(jpeg_bytes) is True

    def test_validate_screenshot_invalid_empty(self, processor):
        """Test validation of empty bytes."""
        assert processor.validate_screenshot(b'') is False

    def test_validate_screenshot_invalid_format(self, processor):
        """Test validation of invalid format."""
        invalid_bytes = b'NOTANIMAGE\x00\x00'
        assert processor.validate_screenshot(invalid_bytes) is False

    def test_prepare_for_vision_model_basic(self, processor, png_bytes):
        """Test preparing screenshot for vision model."""
        result = processor.prepare_for_vision_model(png_bytes)

        assert "base64" in result
        assert "format" in result
        assert result["format"] == "PNG"
        assert isinstance(result["base64"], str)
        assert len(result["base64"]) > 0

    def test_prepare_for_vision_model_with_metadata(self, processor, png_bytes):
        """Test preparing screenshot with metadata."""
        result = processor.prepare_for_vision_model(png_bytes, include_metadata=True)

        assert "base64" in result
        assert "format" in result
        assert "metadata" in result
        assert result["metadata"]["size_bytes"] == len(png_bytes)
        assert result["metadata"]["format"] == "PNG"

    def test_prepare_for_vision_model_structure(self, processor, png_bytes):
        """Test that result structure is correct for Claude API."""
        result = processor.prepare_for_vision_model(png_bytes)

        # Should have base64 data ready for Claude API
        assert "base64" in result
        # Can be used directly in Claude API like:
        # {"type": "image", "source": {"type": "base64", "data": result["base64"]}}
        assert isinstance(result["base64"], str)


class TestConvenienceFunctions:
    """Test convenience functions."""

    @pytest.fixture
    def png_bytes(self):
        """Create sample PNG bytes."""
        return b'\x89PNG\r\n\x1a\n' + b'\x00' * 100

    def test_encode_screenshot_base64(self, png_bytes):
        """Test convenience function for base64 encoding."""
        encoded = encode_screenshot_base64(png_bytes)

        assert isinstance(encoded, str)
        assert len(encoded) > 0

    def test_prepare_screenshot_for_claude(self, png_bytes):
        """Test convenience function for Claude preparation."""
        result = prepare_screenshot_for_claude(png_bytes)

        assert "base64" in result
        assert "format" in result
        assert result["format"] == "PNG"

    def test_prepare_screenshot_for_claude_structure(self, png_bytes):
        """Test that Claude preparation has correct structure."""
        result = prepare_screenshot_for_claude(png_bytes)

        # Verify structure matches Claude API expectations
        assert isinstance(result, dict)
        assert isinstance(result["base64"], str)
        assert result["format"] in ("PNG", "JPEG")


# Test configuration
pytest_plugins = ["pytest_asyncio"]


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v", "--tb=short"])
