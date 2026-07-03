# Git Branch Workflow — Steps and Rules

## Basic Branch Structure

```
main (or master)       ← always stable, deployable code
  └── feature/xxx       ← new functionality
  └── fix/xxx           ← bug fix
  └── hotfix/xxx        ← urgent fix directly for production
```

## When to use fix/ vs feature/

**`fix/`** — when you're fixing something that already exists and isn't working correctly:
- Bug in existing logic
- Security patch
- Data/model error

Naming: `fix/decode-token-error-handling`, `fix/schedule-fk-reference`

**`feature/`** — when you're adding something that didn't exist before:
- New endpoint
- New table/model
- New role/permission logic

Naming: `feature/student-grades-endpoint`, `feature/role-based-permissions`

**`hotfix/`** — only if main is already deployed somewhere and there's a critical production issue

**`docs/`** — when adding or updating documentation:

Naming: `docs/git-workflow-guide`, `docs/readme-update`

## Steps for Working with a Branch

### 1. Always start from an up-to-date main

```bash
git checkout main
git pull origin main
```

### 2. Create a branch

```bash
git checkout -b fix/decode-token-error-handling
```

### 3. Work and commit in small logical chunks

```bash
git add managers/auth.py
git commit -m "fix: return None instead of tuple on token decode error"
```

Good practice for commit messages (conventional commits):
- `fix: ...` — bug fix
- `feat: ...` — new functionality
- `refactor: ...` — restructuring without changing behavior
- `docs: ...` — documentation
- `chore: ...` — configuration, dependencies, etc.

### 4. Push the branch

```bash
git push origin fix/decode-token-error-handling
```

### 5. Open a Pull Request

- Through the GitHub UI (you'll see a "Compare & pull request" button after pushing)
- Or with the `gh` CLI:

```bash
gh pr create --title "fix: token decode error handling" --body "..."
```

**A good PR description includes:**

```markdown
## What it does
Fixes a bug when decoding an expired/invalid JWT token, which previously
threw an error instead of returning a 401.

## Why
`decode_token` returned a tuple instead of None on exception, which broke
`filter_by(id=...)` in verify_token.

## How it was tested
- Tested with an expired token → now getting a clean 401
- Tested with an invalid token → same result
```

### 6. Merge

- For a personal project: you can merge directly once you're satisfied
- If working with others: wait for review before merging

```bash
git checkout main
git pull origin main
git branch -d fix/decode-token-error-handling   # delete local branch after merge
```

## One Important Rule

**One branch = one logical change.** Don't mix `fix/decode-token` with `feature/student-grades` in a single branch/PR — it makes review harder, and if something needs to be reverted, you end up reverting everything at once.

## Example of Prioritizing Branches in a Project

1. `fix/leaked-secrets` (rotation + `.gitignore`)
2. `fix/decode-token-error-handling`
3. `fix/register-race-condition`
4. `fix/schedule-teacher-fk`
5. `feature/role-based-registration`
