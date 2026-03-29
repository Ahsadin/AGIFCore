# Model Manifest

## Purpose

Freeze the exact allowed model mapping for each build-machine role.

If a role's primary model is unavailable and no allowed fallback exists, the task stops.

## Role To Model Map

| Role | Primary Model | Allowed Fallback | Downgrade Rule |
| --- | --- | --- | --- |
| Program Governor | `gpt-5.4` | none | stop if unavailable |
| Constitution Keeper | `gpt-5.4-mini` | `gpt-5.4` | governor approval required |
| Source Cartographer | `gpt-5.4-mini` | `gpt-5.4` | governor approval required |
| Source Cartographer Helpers | `gpt-5.4-nano` | `gpt-5.4-mini` | allowed for utility-only work |
| Architecture & Contract Lead | `gpt-5.4` | none | stop if unavailable |
| Build Pod Leads | `gpt-5.3-codex` | none | stop if unavailable |
| Test & Replay Lead | `gpt-5.4-mini` | `gpt-5.4` | governor approval required |
| Anti-Shortcut Auditor | `gpt-5.4-mini` | `gpt-5.4` | governor approval required |
| Auditor Helpers | `gpt-5.4-nano` | `gpt-5.4-mini` | allowed for utility-only work |
| Merge Arbiter | `gpt-5.3-codex` | none | stop if unavailable |
| Validation Agent | `gpt-5.4` | none | stop if unavailable |
| Release & Evidence Lead | `gpt-5.4-mini` | `gpt-5.4` | governor approval required |
| Release Helpers | `gpt-5.4-nano` | `gpt-5.4-mini` | allowed for utility-only work |

## Hard Rules

- No role may improvise a downgrade.
- No role may use an unlisted model.
- Utility helpers may not do high-judgment approval work.
- Critical roles should pin a dated snapshot in the task card when the active build environment supports it.
