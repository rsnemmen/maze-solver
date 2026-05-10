# CLAUDE.md

## Jupyter Notebook Inspection

When you need to read or inspect Jupyter notebooks (`.ipynb` files) in this project, **do not** read the `.ipynb` files directly. They are JSON and difficult to parse meaningfully.

Instead, follow this workflow:

1. First, check if a markdown version already exists (e.g., `notebook.md` for `notebook.ipynb`).
2. If no markdown version exists, convert the notebook to markdown using: `jupyter nbconvert --to markdown <notebook>.ipynb --ExtractOutputPreprocessor.enabled=False`.
3. If `jupyter nbconvert` is not available, try `jupytext --to md <notebook>.ipynb` as a fallback.
4. Read and inspect the resulting `.md` file.

### Notes

- The markdown conversion preserves cell outputs, markdown cells, and code cells in a readable format.
- Do **not** commit generated `.md` files unless explicitly asked to.
- When summarizing a notebook, reference cells by their order (e.g., "In cell 3…") so the user can locate them easily.
- If a notebook has been recently modified, regenerate the markdown version before reading it to ensure it's up to date.
