from pathlib import Path
from dataclasses import dataclass

from secretshield.patterns import Pattern


@dataclass
class Finding:
    file_path: str
    line_number: int
    pattern_name: str
    severity: str
    matched_text: str


def scan_file(file_path: Path, patterns: list[Pattern]) -> list[Finding]:
    """Scan a single file line-by-line against all patterns."""
    findings = []

    try:
        lines = file_path.read_text(errors="ignore").splitlines()
    except (UnicodeDecodeError, PermissionError, OSError):
        return findings

    for line_number, line in enumerate(lines, start=1):
        for pattern in patterns:
            match = pattern.regex.search(line)
            if match:
                findings.append(
                    Finding(
                        file_path=str(file_path),
                        line_number=line_number,
                        pattern_name=pattern.name,
                        severity=pattern.severity,
                        matched_text=_redact(match.group()),
                    )
                )

    return findings


def _redact(matched: str) -> str:
    """Show only a safe prefix of a matched secret, never the full value."""
    if len(matched) <= 8:
        return "*" * len(matched)
    return matched[:4] + "*" * (len(matched) - 4)