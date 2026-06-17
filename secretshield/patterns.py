import re
import yaml
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Pattern:
    name: str
    regex: re.Pattern
    severity: str


def load_patterns(yaml_path: Path) -> list[Pattern]:
    """Load and compile regex patterns from a YAML rules file."""
    data = yaml.safe_load(yaml_path.read_text())
    return [
        Pattern(
            name=p["name"],
            regex=re.compile(p["regex"]),
            severity=p["severity"],
        )
        for p in data["patterns"]
    ]