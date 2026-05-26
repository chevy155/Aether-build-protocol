# MCP Skeleton

This directory contains a local-only MCP server skeleton for Aether Build Protocol.

## Purpose

The skeleton shows how an MCP client could safely discover Aether resources, tools, and prompts without granting unsafe authority.

## Current Status

- skeleton only
- local-only
- no real MCP dependency required yet
- no production server
- no external calls

## Safe Scope

The current skeleton supports local reads and local script execution for existing safe Aether workflows.

It also exposes deterministic local machine response generation so MCP-style clients receive the same safe response envelope shape used by the machine gateway.

It explicitly refuses:

- send_email
- call_webhook
- contact_supplier
- approve_fabrication
- approve_engineering
- certify_load_rating
- scan_network
- read_outside_repo

## Future Use

Future MCP support could connect agent clients to Aether manifests, schemas, and safe local tools while preserving human approval gates.

No real MCP deployment is provided in this repository yet.