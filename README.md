# Devfolio Codex Plugin

This repository contains the Devfolio plugin for Codex. It lets Codex work with Devfolio through the Devfolio MCP server, including hackathon project submissions, profile side projects, active hackathon discovery, track/prize lookup, and upload URL generation.

## What It Includes

- A `devfolio` skill for drafting, validating, and safely publishing project submissions.
- A Codex plugin manifest at `plugins/devfolio/.codex-plugin/plugin.json`.
- A hosted MCP configuration at `plugins/devfolio/.mcp.json`.
- MCP workflow guidance for Devfolio project and submission tools.
- A small `devfolio_submission.py` helper for generating a submission template, validating required fields, and printing a summary.

## Install Locally

Clone this repository:

```bash
git clone git@github.com:devfolioco/devfolio-codex-plugin.git
```

Add this repository as a local Codex plugin marketplace in `~/.codex/config.toml`:

```toml
[marketplaces.local-devfolio-plugins]
source_type = "local"
source = "/path/to/devfolio-codex-plugin"
```

Enable the plugin:

```toml
[plugins."devfolio@local-devfolio-plugins"]
enabled = true
```

Restart Codex, then invoke the plugin with:

```text
@devfolio show my active hackathons
```

## MCP Setup

The plugin declares the hosted Devfolio MCP endpoint:

```json
{
  "mcpServers": {
    "devfolio": {
      "type": "http",
      "url": "https://mcp.devfolio.co/mcp"
    }
  }
}
```

Most account-specific tools require each user to add their own Devfolio MCP URL. In Devfolio, open Account Settings, join Devfolio Beta if needed, open the MCP tab, generate an MCP URL, then run:

```bash
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp?apiKey=..."
```

If Codex says an MCP server named `devfolio` already exists, remove the existing entry and add the new one:

```bash
codex mcp remove devfolio
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp?apiKey=..."
```

Treat the MCP URL like a password. Anyone with it may be able to act on the user's Devfolio account. Revoke it in Devfolio if it is exposed.

The hosted server requires a Devfolio MCP API key at connection time. The MCP edge accepts `x-api-key` or `apiKey` and forwards it to Devfolio API as `x-mcp-api-key`.

## Current MCP Tools

- `getMyHackathonProject`
- `getHackathonTracksAndPrizes`
- `getUserPublicProjects`
- `getProjectSubmissionGuide`
- `getSignedUploadUrl`
- `createHackathonProject`
- `updateHackathonProject`
- `createSideProject`
- `updateSideProject`

## Current MCP Resources

- `devfolio://user/profile`
- `devfolio://user/active-hackathons`

## Local Submission Helper

Generate a starter submission:

```bash
python3 plugins/devfolio/scripts/devfolio_submission.py template > devfolio-submission.json
```

Validate it:

```bash
python3 plugins/devfolio/scripts/devfolio_submission.py validate devfolio-submission.json
```

## Safety

Devfolio project publishing can make a project public immediately. The skill requires explicit confirmation before all create/update calls and before any `status: "publish"` action.

## Compatibility Notes

Keep future MCP and plugin changes additive where possible:

- Preserve the unauthenticated onboarding path so users without MCP auth can still draft and validate submissions locally.
- Preserve existing tool names and argument meanings; add new optional fields or new tools before changing current flows.
- Keep sign-in outside the plugin package. Users should connect their own Devfolio MCP URL rather than committing account tokens or shared credentials.
- Treat team support as an authorization-sensitive extension. Before create, update, or publish actions, the agent should read the current project/team state when available and ask for explicit confirmation.
- Keep draft-first behavior and explicit publish confirmation as stable safety guarantees.
