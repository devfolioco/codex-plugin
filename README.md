# Devfolio Codex Plugin

This repository contains the Devfolio plugin for Codex. It lets Codex work with Devfolio from local repositories and the Devfolio MCP server, including hackathon project submissions, profile side projects, active hackathon discovery, track/prize lookup, upload URL generation, and Devfolio codebase navigation.

## What It Includes

- A `devfolio` skill for drafting, validating, and safely publishing project submissions.
- A Codex plugin manifest at `plugins/devfolio/.codex-plugin/plugin.json`.
- A hosted MCP configuration at `plugins/devfolio/.mcp.json`.
- Devfolio multi-repo navigation guidance for engineering workflows.
- MCP workflow guidance for the tools exposed by `devfolioco/devfolio-mcp-server`.
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

## Devfolio Workspace

For Devfolio codebase work, keep Devfolio repos under one parent directory and point Codex at it:

```bash
export DEVFOLIO_WORKSPACE_PATH="/path/to/devfolio"
```

The plugin expects repos such as `devfolio-agent-skills`, `devfolio-mcp-server`, `devfolio-api`, `devfolio-backend`, `devfolio-frontend`, `api-types`, `projectx`, and `organizer-dashboard` to live under that parent.

For Devfolio engineers testing the MCP server locally:

```bash
export DEVFOLIO_WORKSPACE_PATH="/path/to/devfolio"
export DEVFOLIO_API_BASE_URL="<devfolio-api-base-url>"
plugins/devfolio/scripts/start-local-mcp.sh
```

The hosted and local servers require a Devfolio MCP API key at connection time. The MCP edge accepts `x-api-key` or `apiKey` and forwards it to Devfolio API as `x-mcp-api-key`.

## Current MCP Tools

- `getUserActiveHackathons`
- `getMyHackathonProject`
- `getHackathonTracksAndPrizes`
- `getUserPublicProjects`
- `getProjectSubmissionGuide`
- `getSignedUploadUrl`
- `createHackathonProject`
- `updateHackathonProject`
- `createSideProject`
- `updateSideProject`

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
