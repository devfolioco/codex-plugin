# Devfolio Codex Plugin

This plugin helps Codex work with Devfolio through the Devfolio MCP server. It supports hackathon project submissions, profile side projects, active hackathon discovery, track/prize lookup, and upload URL generation.

It bundles:

- A `devfolio` skill for drafting, validating, and safely publishing project submissions.
- `./.mcp.json` pointing Codex at the hosted Devfolio Streamable HTTP MCP server.
- MCP workflow guidance for Devfolio project and submission tools.
- A small `devfolio_submission.py` helper for generating a submission template, validating required fields, and printing a summary.

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

The hosted server requires a Devfolio MCP API key at connection time. The MCP edge accepts `x-api-key` or `apiKey` and forwards it to Devfolio API as `x-mcp-api-key`.

Current MCP tools include:

- `getMyHackathonProject`
- `getHackathonTracksAndPrizes`
- `getUserPublicProjects`
- `getProjectSubmissionGuide`
- `getSignedUploadUrl`
- `createHackathonProject`
- `updateHackathonProject`
- `createSideProject`
- `updateSideProject`

Current MCP resources include:

- `devfolio://user/profile`
- `devfolio://user/active-hackathons`

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

## Compatibility Notes

Future support for sign-in, teams, richer media, or organizer-specific workflows should be additive:

- Keep local drafting and validation usable without an MCP connection.
- Keep the hosted MCP URL as the normal public setup path.
- Add optional arguments or new tools before changing existing tool behavior.
- Read the current project/team state before mutating team-owned projects when the MCP server exposes that data.
- Preserve explicit confirmation before create, update, publish, transfer, invite, or other externally visible actions.
