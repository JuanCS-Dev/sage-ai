"""
SAGE - TRUE AI Personal Assistant with Consciousness
====================================================

A wise personal assistant that combines:
- AI assistants capabilities (organization, memory)
- Real-life PA capabilities (execution, action)
- Consciousness via Max AI (ethics, safety, validation)
- High performance (monitoring, optimization)

Author: MAXIMUS AI
Version: 2.0.0
Date: November 10, 2025
"""

__version__ = "2.0.0"
__author__ = "MAXIMUS AI"
__email__ = "contact@maximus-ai.com"
__license__ = "MIT"

from sage.core.secretary_agent import SecretaryAgent, Note, Task
from sage.core.secretary_executor import SecretaryExecutor, ExecutableTask, RoadmapStep
from sage.core.sage import Sage, ConsciousnessLevel, SafetyTier

__all__ = [
    "SecretaryAgent",
    "SecretaryExecutor",
    "Sage",
    "Note",
    "Task",
    "ExecutableTask",
    "RoadmapStep",
    "ConsciousnessLevel",
    "SafetyTier",
]
