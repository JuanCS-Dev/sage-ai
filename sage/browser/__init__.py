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

# Imports will be added as components are implemented
__all__ = []
