# Coding Standards

- Prefer typed Python functions and small module boundaries.
- Return plain Python data from reusable services; format with pandas only at the edges.
- Keep secrets out of code and committed config.
- Use compatibility wrappers only to preserve existing entrypoints; new code should target canonical modules.
- Update docs and tests when changing public behavior or semantic-model rules.
