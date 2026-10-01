# KOgenie Copy Studio

A simple browser interface for building an AI-assisted copywriting workflow.

## Current version

Version 7 — Cross-Channel Campaign Engine

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

## Version 7 — Cross-Channel Campaign Engine

The system can now adapt one evidence-grounded campaign strategy
across multiple channels without rebuilding the campaign from scratch.

Supported executions:

- Meta Feed
- Google Search
- Email
- Landing Page
- X

Version 7 also includes:

- channel specifications
- controlled Meta execution variants
- cross-channel campaign packaging
- semantic consistency review
- unsupported-claim detection
- CTA conflict detection
- targeted channel repair
- post-repair review

Core principle:

Strategy stays stable while execution changes by channel.

Passing channel drafts are preserved during repair.
Only channels identified by the consistency reviewer are rewritten.

## Current limitation

The system still relies on humans to enter research, claims, evidence,
and brand knowledge manually.

The next version begins adding tool-using AI research capabilities.
