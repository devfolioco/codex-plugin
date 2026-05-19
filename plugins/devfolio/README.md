# Devfolio Codex Plugin

This plugin helps Codex work with Devfolio through the Devfolio MCP server. It supports hackathon project submissions, profile side projects, active hackathon discovery, track/prize lookup, and upload URL generation.

## Install

Add the Devfolio plugin marketplace:

```bash
codex plugin marketplace add devfolioco/codex-plugin
```

Then open the Codex Plugins screen, choose Devfolio, and install the plugin.

It bundles:

- A `devfolio` skill for preparing and safely managing project submissions through Devfolio MCP.
- `./.mcp.json` pointing Codex at the hosted Devfolio Streamable HTTP MCP server.
- MCP workflow guidance for Devfolio project and submission tools.

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

Connect Devfolio MCP with the bare MCP URL:

```bash
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp"
```

Codex should open the Devfolio OAuth flow during setup. If Codex says an MCP server named `devfolio` already exists, remove the existing entry and add it again:

```bash
codex mcp remove devfolio
codex mcp add devfolio \
  --url "https://mcp.devfolio.co/mcp"
```

For staging, internal testers can use the same shape with the Devrel endpoint:

```bash
codex mcp add devfolio \
  --url "https://mcp.devrel.in/mcp"
```

Legacy MCP URLs with `apiKey` query parameters are no longer valid for production. Remove the key from any existing Devfolio MCP config and reconnect with the bare MCP URL.

## Safety

Devfolio project publishing can make a project public immediately. The skill instructs Codex to require explicit confirmation before all create/update calls and before any `status: "publish"` action.

## Compatibility Notes

Future support for sign-in, teams, richer media, or organizer-specific workflows should be additive:

- Keep setup guidance clear when the MCP connection is missing or unauthenticated.
- Keep the hosted bare MCP URL as the public setup path.
- Add optional arguments or new tools before changing existing tool behavior.
- Read the current project/team state before mutating team-owned projects when the MCP server exposes that data.
- Preserve explicit confirmation before create, update, publish, transfer, invite, or other externally visible actions.
