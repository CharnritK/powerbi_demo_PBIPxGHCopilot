# Testing Strategy

This repository uses lightweight tests to validate behavior that is practical for a local demo and realistic for enterprise-style development.

For measure validation, the strategy is:

- treat the CSV template as the reviewable source file for measure test cases
- infer candidate scenarios from the committed PBIP semantic model and report metadata
- preserve approved or human-reviewed rows during regeneration
- test the schema and merge behavior with unit tests instead of adding CI/CD complexity

Current unit-test coverage for this feature includes:

- template schema validation
- CSV parsing into typed validation rows
- rejection of invalid statuses
- duplicate `test_id` detection
- PBIP-driven scenario generation against the committed demo semantic model and report
- preservation of reviewed rows when generated content is merged

Human review remains mandatory for:

- expected values
- business-purpose wording
- executive-critical prioritization decisions
- any scenario that implies RLS semantics or finance-signoff requirements
