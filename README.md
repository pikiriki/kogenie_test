# KOgenie Copy Studio

A simple browser interface for building an AI-assisted copywriting workflow.

## Current version

Version 6 — Evidence-Grounded Copywriting Engine

## What the app currently does

- Creates structured campaign briefs.
- Generates structured AI copy drafts.
- Lets humans edit and apply changes.
- Stores campaigns in SQLite.
- Reloads saved campaigns.
- Maintains draft version history.
- Records version provenance and notes.
- Stores reusable brand profiles.
- Stores claims, evidence, sources, and verification status.
- Sends only verified claims to the writer.
- Exports a complete campaign record as JSON.

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
```

## Version 6 — Evidence-Grounded Copywriting Engine

The application can now transform research into a structured
copywriting strategy and complete sales message.

Current pipeline:

ResearchDocument
→ ReaderProfile
→ DesireHypothesis
→ DesireIntensity
→ AwarenessHypothesis
→ MessageEntryPoint
→ SophisticationHypothesis
→ MechanismHypothesis
→ ObjectionMap
→ OfferStrategy
→ BigIdeaHypothesis
→ CreativeAngleSet
→ HeadlineCandidate
→ OpeningDraft
→ MechanismSectionDraft
→ ProofSectionDraft
→ ObjectionSectionDraft
→ OfferSectionDraft
→ CompleteSalesMessage
→ CopyStrategyCard

The system separates:

- research
- strategy
- writing
- proof boundaries
- offer boundaries
- final copy

Missing evidence and missing commercial terms are preserved
instead of silently invented.

## Current limitation

The system still relies on humans to enter research, claims, evidence,
and brand knowledge manually.

The next version begins adding tool-using AI research capabilities.
