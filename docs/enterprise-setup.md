# Enterprise Setup

This repo does not create real separate repositories. Instead, it presents a believable enterprise layout inside one repo so an audience can quickly understand team boundaries.

## Why this structure exists

- `bi-repo` shows what a BI developer team typically owns
- `data-engineer-repo` shows what an upstream data platform or engineering team might own
- `shared` shows the integration contract between those teams

## What is intentionally simplified

- no CI/CD
- no real orchestration
- no production infrastructure
- no secrets, tenant IDs, or connection strings

Everything here is optimized for demo readability.
