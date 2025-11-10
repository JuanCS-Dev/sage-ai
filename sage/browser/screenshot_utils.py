"""
Screenshot Utilities - SAGE Browser Automation
================================================

Utilities for screenshot processing, optimization, and preparation
for vision model input (Claude 3.5 Sonnet).

Features:
- Base64 encoding for API transmission
- Image metadata extraction (size, format)
- Future: optimization, cropping, annotation

Author: MAXIMUS AI
Date: November 10, 2025
Version: 0.1.0 (Week 1 Task 4)
"""

import base64
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScreenshotMetadata:
    """Metadata for a captured screenshot."""

    size_bytes: int
    format: str
    width: Optional[int] = None
    height: Optional[int] = None
    timestamp: Optional[datetime] = None
    url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "size_bytes": self.size_bytes,
            "format": self.format,
            "width": self.width,
            "height": self.height,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "url": self.url,
        }


class ScreenshotProcessor:
    """
    Process and prepare screenshots for vision model analysis.

    Primary use case: Prepare screenshots for Claude 3.5 Sonnet vision API.

    Example:
        processor = ScreenshotProcessor()

        # Capture screenshot from browser
        screenshot_bytes = await browser.screenshot()

        # Encode for API
        base64_str = processor.encode_base64(screenshot_bytes)

        # Extract metadata
        metadata = processor.extract_metadata(screenshot_bytes)
        print(f"Screenshot size: {metadata.size_bytes} bytes")
    """

    def encode_base64(self, image_bytes: bytes) -> str:
        """
        Encode image bytes to base64 string for API transmission.

        Args:
            image_bytes: Raw image bytes (PNG format)

        Returns:
            Base64-encoded string

        Example:
            base64_str = processor.encode_base64(screenshot_bytes)
            # Use in Claude API: {"type": "image", "source": {"type": "base64", "data": base64_str}}
        """
        return base64.b64encode(image_bytes).decode('utf-8')

    def decode_base64(self, base64_str: str) -> bytes:
        """
        Decode base64 string back to image bytes.

        Args:
            base64_str: Base64-encoded string

        Returns:
            Raw image bytes
        """
        return base64.b64decode(base64_str)

    def extract_metadata(
        self,
        image_bytes: bytes,
        url: Optional[str] = None,
    ) -> ScreenshotMetadata:
        """
        Extract metadata from screenshot bytes.

        Args:
            image_bytes: Raw image bytes (PNG format)
            url: Optional URL of the page (if known)

        Returns:
            ScreenshotMetadata object

        Note:
            Width/height extraction requires PIL/Pillow (not installed by default).
            Falls back to None if PIL not available.
        """
        metadata = ScreenshotMetadata(
            size_bytes=len(image_bytes),
            format=self._detect_format(image_bytes),
            timestamp=datetime.now(),
            url=url,
        )

        # Try to extract dimensions using PIL (optional dependency)
        try:
            from PIL import Image
            import io

            image = Image.open(io.BytesIO(image_bytes))
            metadata.width = image.width
            metadata.height = image.height
        except ImportError:
            # PIL not installed - dimensions will be None
            pass
        except Exception:
            # Error reading image - dimensions will be None
            pass

        return metadata

    def _detect_format(self, image_bytes: bytes) -> str:
        """
        Detect image format from magic bytes.

        Args:
            image_bytes: Raw image bytes

        Returns:
            Format string ("PNG", "JPEG", "UNKNOWN")
        """
        if len(image_bytes) < 4:
            return "UNKNOWN"

        # Check PNG magic bytes
        if image_bytes[:4] == b'\x89PNG':
            return "PNG"

        # Check JPEG magic bytes
        if image_bytes[:2] == b'\xff\xd8':
            return "JPEG"

        return "UNKNOWN"

    def validate_screenshot(self, image_bytes: bytes) -> bool:
        """
        Validate that bytes represent a valid image.

        Args:
            image_bytes: Raw image bytes

        Returns:
            True if valid image, False otherwise
        """
        if not image_bytes or len(image_bytes) == 0:
            return False

        format_detected = self._detect_format(image_bytes)
        return format_detected in ("PNG", "JPEG")

    def prepare_for_vision_model(
        self,
        image_bytes: bytes,
        include_metadata: bool = False,
    ) -> Dict[str, Any]:
        """
        Prepare screenshot for vision model API (Claude 3.5 Sonnet).

        Args:
            image_bytes: Raw image bytes (PNG format)
            include_metadata: Include metadata in result

        Returns:
            Dictionary with base64 data and optional metadata

        Example:
            result = processor.prepare_for_vision_model(screenshot_bytes)

            # Use in Claude API:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "data": result["base64"]}},
                        {"type": "text", "text": "Analyze this UI..."}
                    ]
                }]
            )
        """
        base64_str = self.encode_base64(image_bytes)

        result = {
            "base64": base64_str,
            "format": self._detect_format(image_bytes),
        }

        if include_metadata:
            metadata = self.extract_metadata(image_bytes)
            result["metadata"] = metadata.to_dict()

        return result


# Convenience functions
def encode_screenshot_base64(image_bytes: bytes) -> str:
    """
    Convenience function to encode screenshot to base64.

    Args:
        image_bytes: Raw image bytes

    Returns:
        Base64-encoded string
    """
    processor = ScreenshotProcessor()
    return processor.encode_base64(image_bytes)


def prepare_screenshot_for_claude(image_bytes: bytes) -> Dict[str, Any]:
    """
    Convenience function to prepare screenshot for Claude vision API.

    Args:
        image_bytes: Raw image bytes (PNG format)

    Returns:
        Dictionary ready for Claude API

    Example:
        screenshot = await browser.screenshot()
        prepared = prepare_screenshot_for_claude(screenshot)

        # Use in Claude API
        response = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "data": prepared["base64"]}},
                    {"type": "text", "text": "What is on this page?"}
                ]
            }]
        )
    """
    processor = ScreenshotProcessor()
    return processor.prepare_for_vision_model(image_bytes)
