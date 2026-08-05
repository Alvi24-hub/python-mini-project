"""
Safe serialization and deserialization module.
Prevents Remote Code Execution (RCE) vulnerabilities by replacing unsafe pickle/YAML loading with safe JSON/literal parsing.
"""

import ast
import json
from typing import Any

class SafeSerializer:
    """
    Secure deserialization helper enforcing safe data parsing.
    """

    @staticmethod
    def safe_load_json(data: str) -> Any:
        """Safely parse JSON data, rejecting non-string or malformed inputs."""
        if not isinstance(data, str):
            raise ValueError("Input data must be a string")
        return json.loads(data)

    @staticmethod
    def safe_load_literal(data: str) -> Any:
        """Safely parse Python literal structures (dicts, lists, strings, numbers, bools, None)."""
        if not isinstance(data, str):
            raise ValueError("Input data must be a string")
        return ast.literal_eval(data)
