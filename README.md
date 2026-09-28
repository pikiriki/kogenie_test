# KOgenie Copy Studio

A simple browser interface for building an AI-assisted copywriting workflow.

## Current version

Version 2 — Usable Mini Copywriter

## What the app currently does

1. Accepts a product description.
2. Accepts an audience.
3. Accepts a campaign objective.
4. Accepts basic brand voice information.
5. Sends a structured campaign brief to an OpenAI model.
6. Receives a structured copy draft containing:
   - headline
   - body
   - CTA
7. Keeps the generated draft across Streamlit reruns.
8. Allows the human to edit the draft.
9. Converts those edits back into a structured working draft.
10. Handles ordinary generation failures with a user-friendly error.

## Current architecture

```text
Streamlit UI
    ↓
CampaignBrief
    ↓
generate_copy()
    ↓
OpenAI API
    ↓
CopyDraft
    ↓
Session State
    ↓
Human Editing
    ↓
Working CopyDraft