# Devfolio Codex Plugin

This repository contains the Devfolio plugin for Codex. It lets Codex work with Devfolio through the Devfolio MCP server, including hackathon project submissions, profile side projects, active hackathon discovery, track/prize lookup, and upload URL generation.

## What It Includes

- A `devfolio` skill for preparing and safely managing project submissions through Devfolio MCP.
- A Codex plugin manifest at `plugins/devfolio/.codex-plugin/plugin.json`.
- A hosted MCP configuration at `plugins/devfolio/.mcp.json`.
- MCP workflow guidance for Devfolio project and submission tools.

## Install

Add the Devfolio plugin marketplace:

```bash
codex plugin marketplace add devfolioco/codex-plugin
```

Then open the Codex Plugins screen, choose Devfolio, and install the plugin.

For local development, clone this repository:

```bash
git clone git@github.com:devfolioco/codex-plugin.git
```

Then add the checkout as a local Codex plugin marketplace:

```bash
codex plugin marketplace add /path/to/codex-plugin
```

After installation, start a new Codex thread and invoke the plugin with:

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

Devfolio project publishing can make a project public immediately. The skill requires explicit confirmation before all create/update calls and before any `status: "publish"` action.

## Compatibility Notes

Keep future MCP and plugin changes additive where possible:

- Preserve the disconnected onboarding path so users without MCP auth understand that account-specific Devfolio MCP actions require OAuth authentication.
- Preserve existing tool names and argument meanings; add new optional fields or new tools before changing current flows.
- Use the OAuth-capable bare MCP URL for setup.
- Treat team support as an authorization-sensitive extension. Before create, update, or publish actions, the agent should read the current project/team state when available and ask for explicit confirmation.
- Keep draft-first behavior and explicit publish confirmation as stable safety guarantees.
