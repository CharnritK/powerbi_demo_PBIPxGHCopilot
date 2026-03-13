# Star Schema Guidelines

- Keep a clear fact/dimension split.
- Use surrogate keys for relationships.
- Hide technical keys from report consumers when possible.
- Keep date handling centralized through `Dim Date`.
- Treat security tables as optional extensions, not default report surfaces.
