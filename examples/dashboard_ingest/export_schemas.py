"""Export JSON Schemas a dashboard can use to validate incoming eval records.

Run it with `python export_schemas.py [output_dir]` (default: ./schemas). A
dashboard or ingest service can ship these schemas and validate uploads in any
language, not just Python.
"""

from __future__ import annotations

import sys
from pathlib import Path

from agent_eval_contract import export_json_schemas


def main() -> None:
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("schemas")
    exported = export_json_schemas(output_dir)
    print(f"wrote {len(exported)} schemas to {output_dir}")
    for name in exported:
        print(f"  {name}")


if __name__ == "__main__":
    main()
