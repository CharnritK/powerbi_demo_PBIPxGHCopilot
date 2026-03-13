# Documentation Guide

This folder is split into authoritative documentation and reference material.

Authoritative documentation:

- [`architecture/`](./architecture): repo shape, system context, integration boundaries, decisions, migration summary
- [`conventions/`](./conventions): naming, coding, folder, and notebook standards
- [`domain/`](./domain): business context, glossary, KPI meaning
- [`data-model/`](./data-model): semantic model rules, assumptions, and source-to-model mapping
- [`operations/`](./operations): local setup, auth prerequisites, troubleshooting, runbooks
- [`external-repos/`](./external-repos): upstream and downstream contracts
- [`ai/`](./ai): AI agent context, guardrails, and playbooks

Reference-only documentation:

- [`presentation/`](./presentation): speaker materials, session packaging, slide assets, presenter notes
- [`../references/`](../references): tooling notes, dependency reference, known limitations

If you are new to the repo, read in this order:

1. [`architecture/repo-architecture.md`](./architecture/repo-architecture.md)
2. [`operations/local-setup.md`](./operations/local-setup.md)
3. [`data-model/semantic-model-overview.md`](./data-model/semantic-model-overview.md)
4. [`external-repos/data-engineering-repo-contract.md`](./external-repos/data-engineering-repo-contract.md)
5. [`ai/agent-context.md`](./ai/agent-context.md)
