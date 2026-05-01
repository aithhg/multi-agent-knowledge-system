# BASES — Multi-Agent Knowledge Compounding Engine

A Claude Code-powered multi-agent system that transforms fragmented information into structured, reusable knowledge assets through a closed-loop pipeline.

## Core Architecture

| Agent | Role |
|-------|------|
| **Ingest Agent** | Standardize external content (URLs, videos, articles) into unified Markdown |
| **Digest Agent** | Generate summaries, extract concepts, update topic pages and index (parallel execution) |
| **Output Agent** | Retrieve from index, then generate contextual output (articles, reports, social posts) |
| **Inspect Agent** | Periodic structural audit — detect orphans, broken links, sync drift |

Supporting sub-agents: `planner`, `code-reviewer`, `tdd-guide`, `security-reviewer`.

## Key Design Principles

- **File-first**: All knowledge stored as plain Markdown files
- **Incremental**: Only process new content, never rebuild the entire library
- **Traceable**: Every conclusion can be traced back to its source

## Directory Structure

```
workspace/
├── raw/                  # Standardized ingestion layer
├── knowledge/
│   ├── index.md          # Master knowledge index
│   └── _template.md
├── outputs/              # Automated daily reports & outputs
├── scripts/              # Sync & health-check automation
└── logs/
```

## Proof of Operation

- Running continuously for 20+ days
- 40+ raw materials ingested
- Daily automated Web3+AI intelligence reports
- Incremental sync pipeline to Obsidian (modification-time based)
