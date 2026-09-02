# bightsplice

`bightsplice` reconstructs Python projects that have been split across multiple
file packs. It inventories each source tree, detects collisions, analyzes Python
modules, and prepares for syntax-preserving merges and import reconciliation.

This repository is an initial implementation scaffold.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Example

```bash
bightsplice pack-a pack-b --destination merged-project
```

The current implementation performs inventory and merge planning. The next
implementation stages will add LibCST-backed module merging and Rope-backed
import reconciliation.
