# Devfolio Codex Plugin

This plugin helps Codex work with Devfolio from local repositories and the Devfolio MCP server. It supports hackathon project submissions, profile side projects, active hackathon discovery, track/prize lookup, upload URL generation, and Devfolio codebase navigation.

It bundles:

- A `devfolio` skill for drafting, validating, and safely publishing project submissions.
- `./.mcp.json` pointing Codex at the hosted Devfolio Streamable HTTP MCP server.
- Devfolio multi-repo navigation guidance adapted from the internal `devfolioco/skills` repository.
- MCP workflow guidance for the tools exposed by `devfolioco/devfolio-mcp-server`.
- A small `devfolio_submission.py` helper for generating a submission template, validating required fields, and printing a summary.

## Devfolio Workspace

For codebase or MCP work, keep Devfolio repos under one parent directory and point Codex at it:

```bash
export DEVFOLIO_WORKSPACE_PATH="/Users/ashwinexe/Documents/GitHub/devfolio"
```

The plugin expects repos such as `devfolio-agent-skills`, `devfolio-mcp-server`, `devfolio-api`, `devfolio-backend`, `devfolio-frontend`, `api-types`, `projectx`, and `organizer-dashboard` to live under that parent.

## MCP Server

The plugin declares this MCP server:

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

Most account-specific tools require the user's unique Devfolio MCP URL. In Devfolio, open Account Settings, join Devfolio Beta if needed, open the MCP tab, generate an MCP URL, then run the Codex command shown there:

```bash
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp?apiKey=..."
```

If Codex says an MCP server named `devfolio` already exists, remove the unauthenticated placeholder first, then run the command again:

```bash
codex mcp remove devfolio
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp?apiKey=..."
```

Treat this URL like a password. Anyone with it can act on the user's Devfolio account. Revoke it in Devfolio if it is exposed.

For Devfolio engineers testing the MCP server locally, run:

```bash
export DEVFOLIO_WORKSPACE_PATH="/Users/ashwinexe/Documents/GitHub/devfolio"
export DEVFOLIO_API_BASE_URL="<devfolio-api-base-url>"
plugins/devfolio/scripts/start-local-mcp.sh
```

The hosted and local servers require a Devfolio MCP API key at connection time. The MCP edge accepts `x-api-key` or `apiKey` and forwards it to Devfolio API as `x-mcp-api-key`.

Current MCP tools include:

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

## Local Usage

Generate a starter submission:

```bash
python3 plugins/devfolio/scripts/devfolio_submission.py template > devfolio-submission.json
```

Validate it:

```bash
python3 plugins/devfolio/scripts/devfolio_submission.py validate devfolio-submission.json
```

## Safety

Devfolio project publishing can make a project public immediately. The skill instructs Codex to require explicit confirmation before all create/update calls and before any `status: "publish"` action.
