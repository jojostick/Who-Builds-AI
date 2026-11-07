"""Regenerate processed files and compare their SHA-256 hashes with the checked-in versions."""
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from analysis import export  # noqa: E402

OUTPUT = ROOT / "data" / "processed"
FILES = ["annual_concentration.csv", "country_year.csv", "model_country_weights.csv", "data_audit.json"]


def checksum(path):
    """Return a deterministic file digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    """Verify that exported outputs exactly reproduce the packaged results."""
    originals = {name: checksum(OUTPUT / name) for name in FILES}
    export()
    after = {name: checksum(OUTPUT / name) for name in FILES}
    failures = [name for name in FILES if originals[name] != after[name]]
    for name in FILES:
        print(f"{'PASS' if name not in failures else 'FAIL'}: {name}")
    if failures:
        raise SystemExit(f"Reproduction mismatch: {failures}")
    print("PASS: all four processed outputs exactly regenerate from the source CSV")


if __name__ == "__main__":
    main()
