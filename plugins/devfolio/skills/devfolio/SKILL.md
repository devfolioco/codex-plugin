---
name: devfolio
description: Work with Devfolio from Codex: prepare hackathon submissions, inspect Devfolio's multi-repo codebase, study MCP server capabilities, and safely use Devfolio project workflows.
---

# Devfolio

Use this skill when the user asks for Devfolio, `@devfolio`, Devfolio MCP, hackathon submissions, project drafts, sponsor tracks, Devfolio project JSON, publishing projects, or questions about the Devfolio multi-repo codebase.

## Workspace Setup

Devfolio repos should live under one parent directory. If `DEVFOLIO_WORKSPACE_PATH` is set, use that as the parent. Otherwise, infer it from nearby folders and tell the user what path you used.

Expected repo names include:

- `api-types` — shared TypeScript types for API request/response shapes
- `datalayer` or `projectx` — DB operations and Sequelize/Postgres models
- `devfolio-api` — public-facing Express/Node API server
- `devfolio-backend` — infrastructure, Docker, Hasura migrations, local dev setup
- `devfolio-frontend` — hacker-facing Devfolio app
- `devfolio-mcp-server` or `mcp-server` — Devfolio MCP server
- `organizer-dashboard` — legacy organizer dashboard
- `od` — organizer dashboard v2
- `source` — design system
- `skills` or `devfolio-agent-skills` — internal Devfolio agent skills

When answering a codebase question, stay in the current repo if it has the answer. Read sibling repos only when the answer crosses boundaries.

## Repo Navigation

For API route definitions, start in `devfolio-api/server/routers/<resource>.ts`.

For business logic behind an API route, follow `devfolio-api/server/controllers/<resource>.ts` to `devfolio-api/server/services/<resource>.ts`.

For persistence and DB models, inspect `projectx/src/models/<resource>.ts`, `projectx/src/controllers/<resource>.ts`, `datalayer`, and raw schema or migrations under `devfolio-backend`.

For hacker-facing flows such as applications, microsites, judging, and project pages, inspect `devfolio-frontend/pages/`, GraphQL queries, mutations, and hooks.

For legacy organizer behavior, inspect `organizer-dashboard/views/`, `organizer-dashboard/components/`, `organizer-dashboard/actions/`, `organizer-dashboard/queries/`, `organizer-dashboard/mutations/`, and `organizer-dashboard/api/`.

For shared types, inspect `api-types/types/` and `api-types/composed/`.

For design system components, inspect `source/src/components/<ComponentName>/`, `source/src/index.ts`, and `source/src/theme/index.ts`.

## MCP Server Setup

This plugin declares one MCP server named `devfolio` in `./.mcp.json`. For normal users, prefer the hosted Devfolio MCP endpoint:

`https://mcp.devfolio.co/mcp`

Most account-specific tools require the user's unique Devfolio MCP URL, which includes an `apiKey` query parameter. The user can get it from Devfolio:

1. Open Devfolio Account Settings.
2. Join Devfolio Beta if the MCP tab is not visible.
3. Open the MCP tab.
4. Generate or copy the unique MCP URL.
5. Run the Codex command shown there:

```bash
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp?apiKey=..."
```

If Codex says an MCP server named `devfolio` already exists, tell the user to remove the unauthenticated placeholder and add the Devfolio-provided URL:

```bash
codex mcp remove devfolio
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp?apiKey=..."
```

Treat the MCP URL like a password. Never hardcode, print, or repeat the key. If a user pastes a real MCP URL into chat, avoid echoing it back and recommend revoking it if it was exposed somewhere public.

For Devfolio engineers testing the server locally, run:


```bash
export DEVFOLIO_WORKSPACE_PATH="/Users/ashwinexe/Documents/GitHub/devfolio"
export DEVFOLIO_API_BASE_URL="<devfolio-api-base-url>"
plugins/devfolio/scripts/start-local-mcp.sh
```

The Devfolio MCP server also exposes legacy SSE at `http://localhost:3000/sse`, but Codex should prefer Streamable HTTP at `/mcp`.

The MCP connection requires a Devfolio MCP API key. The server accepts it as `x-api-key` or `apiKey` at the MCP edge and forwards it to `devfolio-api` as `x-mcp-api-key`. Never hardcode or print this key.

## First-Run and Disconnected Experience

When the user invokes `@devfolio` without a concrete task, asks what the plugin can do, asks setup/account questions, or when the MCP server is unreachable, missing an API key, or returns an auth error, respond with a concise onboarding message instead of trying unrelated fallbacks.

Use this shape:

- Welcome them to Devfolio for Codex.
- Explain that without a Devfolio MCP connection, Codex can still inspect public Devfolio hackathon pages, read local project repos, draft/validate submission JSON, prepare project copy, and explain setup.
- Explain that with a Devfolio MCP connection, Codex can view their active hackathons, fetch their current hackathon project, inspect tracks/prizes, fetch submission guides and custom field requirements, get signed upload URLs, create/update side projects, create/update hackathon project drafts, and publish only after explicit confirmation.
- Tell them to connect by opening Devfolio Account Settings, joining Devfolio Beta if needed, opening the MCP tab, generating/copying the unique MCP URL, and running the Codex command shown by Devfolio: `codex mcp add devfolio --url "https://mcp.devfolio.co/mcp?apiKey=..."`.
- If that command reports that `devfolio` already exists, tell them to run `codex mcp remove devfolio` and then re-run the Devfolio-provided `codex mcp add` command.
- Warn that the MCP URL is sensitive like a password and should be revoked if exposed.
- Offer the next useful action, such as "I can help draft a submission offline now, or you can connect MCP and ask me to show your active hackathons."

If the error says a local MCP server is not running, explain that local MCP is only for Devfolio engineering/development. For normal plugin use, the user should connect the hosted Devfolio MCP URL from Account Settings.

Do not claim the user is logged in unless an MCP resource/tool confirms it in the current session.

## MCP Tools

Read/setup tools:

- `getUserActiveHackathons` — list hackathons the signed-in user is currently participating in; call first when a hackathon slug is unknown.
- `getMyHackathonProject` — fetch the user's project for a hackathon, including drafts, team info, custom fields, and answers.
- `getHackathonTracksAndPrizes` — fetch tracks and nested prizes for a hackathon; use returned track UUIDs for applications.
- `getUserPublicProjects` — list/search public profile projects.
- `getProjectSubmissionGuide` — fetch required fields, custom field UUIDs, validation notes, and field guidance for create/update flows.
- `getSignedUploadUrl` — create a presigned S3 upload URL and storage path for project images.

Write tools:

- `createHackathonProject` — create a hackathon project. Defaults to `status: "draft"` unless `publish` is explicitly requested.
- `updateHackathonProject` — update a hackathon project. Requires `commitMessage`; can publish with `status: "publish"`.
- `createSideProject` — create a standalone profile project. Defaults to draft.
- `updateSideProject` — update a profile project. Requires `commitMessage`; can publish with `status: "publish"`.

Resources:

- `devfolio://user/profile`
- `devfolio://user/active-hackathons`

Prompts:

- `submit-hackathon-project`
- `update-hackathon-project`
- `create-side-project`
- `update-side-project`
- `devfolio-overview`

## MCP Workflow

When the user asks to build, review, or update Devfolio MCP support:

1. Locate the MCP server repo at `$DEVFOLIO_WORKSPACE_PATH/devfolio-mcp-server`, `$DEVFOLIO_WORKSPACE_PATH/mcp-server`, or a nearby MCP server directory.
2. Read its README, package manifest, server entrypoint, tool registration files, and auth/config docs before proposing plugin config.
3. Identify the MCP transport type: stdio, SSE, or streamable HTTP.
4. List the exposed MCP tools, their input schemas, side effects, required auth, and whether each tool is read-only or mutating.
5. Treat create, update, submit, publish, delete, transfer, invite, payout, and auth/session actions as confirmation-required unless the server docs say otherwise.
6. Do not hardcode secrets. Source tokens from documented environment variables or a user-approved session.
7. When packaging as a Codex plugin, prefer `.mcp.json` for MCP server configuration plus Devfolio workflow skills for multi-step behavior.

## Safety Rules

Always ask for explicit confirmation before calling:

- `createHackathonProject`
- `updateHackathonProject`
- `createSideProject`
- `updateSideProject`
- any tool call with `status: "publish"`

Before a publish action, summarize the project name, target hackathon or profile destination, repo/deployed links, screenshots, selected tracks, and whether the user is authorized to publish for the team.

For image uploads, screenshots in `pictures` must be real screenshots of the running project. Do not generate gallery screenshots with an AI image model. AI-generated images are only acceptable for branding visuals such as `favicon`, `cover_img`, or banners when the user explicitly wants that.

Devfolio project submissions usually need:

- Project name
- Tagline
- Problem it solves
- Challenges encountered
- Technologies used
- Links such as source repo, deployed app, docs, demo, deck, Figma, Play Store, or Drive
- Video demo, preferably a public YouTube/Vimeo-style URL
- Screenshots, where the first image is commonly used as the cover image

## Workflow

Use this workflow for project submission tasks:

1. Gather project facts from the repo before drafting copy.
   - Read `README*`, package manifests, docs, deployment config, screenshots, and existing pitch material.
   - Check whether the source repo is public or intended to be public.
   - Identify deployed URLs, demo videos, docs, deck links, and sponsor/track language.

2. Draft the submission in a structured JSON file when the user has not provided one.
   - Prefer `devfolio-submission.json` in the repo root.
   - Use concise, judge-readable language.
   - Mention sponsor APIs, SDKs, tracks, and prize names in `technologies`, `tracks`, or `submissionMetadata` when they are real project dependencies.

3. Validate before publishing.
   - If MCP is available, call `getProjectSubmissionGuide` before create/update so the draft matches the event's current rules.
   - Run `python3 plugins/devfolio/scripts/devfolio_submission.py validate devfolio-submission.json` when this plugin is in the repo marketplace.
   - Require a non-empty name, tagline, problem statement, and technologies.
   - Treat missing public repo, broken deployment, absent demo video, and missing screenshots as warnings unless the hackathon rules make them required.

4. Use MCP draft flow when available.
   - Call `getUserActiveHackathons` if the hackathon slug is unknown.
   - Call `getHackathonTracksAndPrizes` if applying to tracks.
   - Call `getSignedUploadUrl` for gallery images or image-type custom fields, upload bytes, then use the returned `filePath`.
   - Prefer draft status first. Publish only after explicit confirmation.

5. Publish safely.
   - Devfolio publishing may be irreversible or immediately public. Before the final publish action, summarize the exact project name, hackathon, repo URL, deployed URL, tracks, and whether the user is the team admin.
   - Ask for explicit confirmation unless the user has already given a direct publish instruction in the current turn.
   - Prefer browser-driven submission for Devfolio unless the hackathon has documented an API for project submission.
   - If using a hackathon-specific API, read the current draft first, never hardcode tokens, source auth from environment variables or the user-approved session, and redact secrets in output.

## Output Style

When helping with a submission, lead with the project-ready fields or the validation issues. Keep marketing copy crisp; judges should be able to scan it quickly.

When reporting MCP support, lead with the exact transport/config, available tools, auth requirements, and safety boundaries. Keep open questions separate from confirmed facts.
