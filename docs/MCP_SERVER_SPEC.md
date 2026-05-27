# MCP Server Spec

## Purpose

The MCP skeleton describes how Aether could expose local resources and safe tools to MCP clients.

## Current Status

The current implementation is a skeleton and stub only.

- no required MCP dependency yet
- no production server
- no external connectivity
- used by the v0.2.8 bounded local MCP-drive proof as a local discovery and refusal surface only
- not a live external MCP integration

## Safe Tool Surface

- read local manifests
- read local schema and error indexes
- run local Build Packet validation
- run local industrial-hook simulation
- run local company integration simulation

## Forbidden Surface

- send email
- call webhook
- contact supplier
- approve fabrication
- approve engineering
- certify load rating
- scan network
- read outside the repo

## Future Direction

Future MCP support can remain safe if the permission manifest and human approval gates stay first-class.