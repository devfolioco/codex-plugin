---
name: devfolio
description: "Work with Devfolio from Codex: prepare hackathon submissions, study MCP server capabilities, and safely use Devfolio project workflows."
---

# Devfolio

Use this skill when the user asks for Devfolio, `@devfolio`, Devfolio MCP, hackathon submissions, project drafts, sponsor tracks, Devfolio project JSON, side projects, or publishing projects.

## MCP Server Setup

This plugin declares one MCP server named `devfolio` in `./.mcp.json`. For normal users, prefer the hosted Devfolio MCP endpoint:

`https://mcp.devfolio.co/mcp`

Users connect with the bare MCP URL. Codex should open the Devfolio OAuth flow during setup.

For production, use:

```bash
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp"
```

For Devrel staging, internal testers can use:

```bash
codex mcp add devfolio \
  --url "https://mcp.devrel.in/mcp"
```

If Codex says an MCP server named `devfolio` already exists, tell the user to remove the existing entry and add it again:

```bash
codex mcp remove devfolio
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp"
```

Do not tell users to run `codex mcp login` unless Codex explicitly asks for it. For OAuth-enabled Streamable HTTP MCP servers, `codex mcp add ... --url ...` can start and complete the OAuth flow.

Legacy MCP URLs with `apiKey` query parameters are no longer valid for production. If a user has an existing Devfolio MCP config containing `apiKey`, tell them to remove that MCP entry and reconnect with the bare MCP URL. If a user pastes a real API-key MCP URL into chat, avoid echoing it back.

## First-Run and Disconnected Experience

When the user invokes `@devfolio` without a concrete task, asks what the plugin can do, asks setup/account questions, or when the MCP server is unreachable or returns an auth error, respond with a concise onboarding message instead of trying unrelated fallbacks.

Use this shape:

- Welcome them to Devfolio for Codex.
- Explain that without a connected Devfolio MCP server, Codex can explain setup and help prepare project copy from local context, but it cannot fetch account-specific submission rules, validate hackathon-specific requirements, create drafts, upload images, update projects, or publish.
- Explain that with a Devfolio MCP connection, Codex can view their active hackathons, fetch their current hackathon project, inspect tracks/prizes, fetch submission guides and custom field requirements, get signed upload URLs, create/update side projects, create/update hackathon project drafts, and publish only after explicit confirmation.
- Tell them to connect with `codex mcp add devfolio --url "https://mcp.devfolio.co/mcp"`.
- If they are testing Devrel staging, tell them to use `codex mcp add devfolio --url "https://mcp.devrel.in/mcp"`.
- If that command reports that `devfolio` already exists, tell them to run `codex mcp remove devfolio` and then re-run the `codex mcp add` command.
- Tell them to remove any old `apiKey` Devfolio MCP URL because production now uses OAuth with the bare MCP URL.
- Offer the next useful action, such as "Connect MCP and ask me to show your active hackathons" or "Share local project context and I can help prepare submission copy before connecting."

Do not claim the user is logged in unless an MCP resource/tool confirms it in the current session.

## MCP Tool Discovery

Do not maintain a static list of Devfolio MCP tools in responses. The MCP server exposes its current tools, resources, prompts, schemas, and descriptions dynamically, and those should be treated as the source of truth.

For project submission work, prioritize the submission guide tool exposed by the MCP server before assembling or validating any create/update payload. The returned guide is the source of truth for required fields, field names, custom questions, validation rules, minimum links, image requirements, cover/logo requirements, and publish readiness.

## Compatibility Rules

Keep future Devfolio MCP and plugin capabilities additive:

- Preserve clear setup guidance for users who have not connected MCP. Do not imply that account-specific Devfolio MCP tools can be used without a successful OAuth connection.
- Preserve existing tool names and argument meanings. Prefer optional arguments or new tools for new capabilities.
- Use OAuth-capable bare MCP URLs for setup.
- Treat team support as authorization-sensitive. When a tool exposes team or role data, read it before mutating a project and summarize the target team before confirmation.
- Preserve draft-first create/update flows and explicit publish confirmation.

## Safety Rules

Always ask for explicit confirmation before calling Devfolio MCP tools that create, update, publish, upload externally visible media, transfer ownership, invite collaborators, or otherwise mutate Devfolio account/project state.

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

2. Draft project copy from local context before using MCP tools.
   - Use concise, judge-readable language.
   - Mention sponsor APIs, SDKs, tracks, and prize names only when they are real project dependencies or appear in the hackathon guide.

3. Fetch the submission guide before assembling any create/update payload.
   - Use the Devfolio MCP submission guide tool with the exact flow, such as `create_hackathon_project`, `update_hackathon_project`, `create_side_project`, or `update_side_project`.
   - Treat the returned markdown guide as the source of truth for required fields, field names, custom question UUIDs, validation rules, minimum links, image requirements, cover image/logo requirements, and publish readiness.
   - Do not rely on a static local JSON template for Devfolio submission validity.

4. Use MCP draft flow when available.
   - Use the Devfolio MCP resources/tools to identify active hackathons if the hackathon slug is unknown.
   - Use the Devfolio MCP tracks/prizes tool if applying to tracks.
   - Use the Devfolio MCP upload flow for gallery images or image-type custom fields, upload bytes, then use the returned storage path.
   - Prefer draft status first. Publish only after explicit confirmation.

5. Publish safely.
   - Devfolio publishing may be irreversible or immediately public. Before the final publish action, summarize the exact project name, hackathon, repo URL, deployed URL, tracks, and whether the user is the team admin.
   - Ask for explicit confirmation unless the user has already given a direct publish instruction in the current turn.
   - Prefer browser-driven submission for Devfolio unless the hackathon has documented an API for project submission.
   - If using a hackathon-specific API, read the current draft first, use the user-configured MCP connection, and redact secrets in output.

## Output Style

When helping with a submission, lead with the project-ready fields or the validation issues. Keep marketing copy crisp; judges should be able to scan it quickly.

When reporting MCP support, lead with the exact transport/config, available tools, auth requirements, and safety boundaries. Keep open questions separate from confirmed facts.
