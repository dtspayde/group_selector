"""
Copyright (c) 2023 Damon Spayde. All rights reserved.

group_selector: An application for forming groups of a specified size from a list of students.
"""

from __future__ import annotations

from typing import Literal, Protocol, runtime_checkable

__all__ = ["Protocol", "runtime_checkable", "Literal"]


def __dir__() -> list[str]:
    return __all__
