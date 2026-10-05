# KOgenie Copy Studio

A simple browser interface for building an AI-assisted copywriting workflow.

## Current version

Version 11 — Outcome Evidence and Learning

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

## Version 8 — Review, Revision, and Human Approval

Version 8 adds a structured quality-control layer around generated copy.

The system now includes:

- copy-quality critique
- targeted copy revision
- claim-level evidence review
- evidence-grounded claim repair
- brand-voice review
- targeted brand-voice revision
- unified review reporting
- dependency-aware revision planning
- bounded revision orchestration
- cross-channel re-review
- human approval records

Approval lifecycle:

Draft
→ Automated checks passed
→ Awaiting human approval
→ Approved or rejected

Human approval applies to a specific stored copy snapshot.

If the copy changes, a new approval request is required.

Automated review passing does not automatically publish or approve copy.

## Version 9 — Campaign Memory and Strategic Novelty

Version 9 adds approved campaign memory and uses historical
campaign context to detect strategic repetition without
blindly copying past campaigns.

The system now supports:

- approved campaign memory
- persistent campaign memory storage
- semantic strategic repetition review
- evidence-grounded novelty guidance
- alternative strategy generation
- independent alternative-strategy evaluation
- explicit human strategy selection
- controlled application of the selected strategy
- downstream copy invalidation after strategy changes
- strategy-locked core copy regeneration
- regenerated multi-channel campaigns
- cross-channel consistency review and targeted repair
- fresh human approval after strategy change
- campaign-memory update only after approval

Core memory principle:

Past campaigns are historical context, not future commands.

Approved does not mean successful.

A new strategy must still pass evidence review,
copy review, brand review, channel review,
and fresh human approval before it becomes trusted memory.

## Version 10 — Visual Creative System

Version 10 extends campaign strategy into visual execution.

The system now supports:

- visual creative briefs
- separation of visual meaning from visual style
- structured visual generation specifications
- real image generation
- generated-image provenance
- automated visual review
- targeted one-pass visual repair
- immutable human visual approval
- SHA-256 visual identity
- approved visual snapshots
- persistent visual asset history
- exact duplicate detection
- semantic visual repetition review
- evidence-grounded visual novelty guidance

Visual architecture:

Campaign strategy
→ visual creative brief
→ visual style specification
→ visual generation specification
→ generated visual
→ automated visual review
→ bounded repair
→ visual repetition review
→ human approval
→ approved VisualAsset

Core principles:

1. Generated does not mean approved.
2. Automated review does not mean human approval.
3. Visual approval belongs to exact image bytes.
4. Editing an approved image creates a new unapproved artifact.
5. Visual novelty must not change product truth or evidence.
6. Different styling does not automatically mean a different visual idea.
7. Approved visual history does not prove campaign performance.

## Version 11 — Outcome Evidence and Learning

Version 11 connects approved campaign history to measured
outcomes without treating correlation as causation.

The system now supports:

- raw CampaignOutcome records
- deterministic campaign metrics
- outcome evidence snapshots
- conversion and attribution context
- explicit interpretation boundaries
- comparable previous-period baselines
- absolute and relative metric changes
- evidence-bounded AI performance analysis
- campaign-level creative/outcome provenance links
- repeated creative evidence ledgers
- supporting, contradicting, neutral, and incomparable observations
- bounded CreativeLearning
- controlled next-test planning

Core evidence ladder:

CampaignOutcome
→ CampaignMetrics
→ OutcomeEvidenceSnapshot
→ PerformanceContext
→ PerformanceComparison
→ PerformanceAnalysis
→ CreativeOutcomeLink
→ CreativeEvidenceLedger
→ CreativeLearning
→ NextTestPlan

Core rules:

1. Approval does not mean performance.
2. Attribution does not automatically mean causation.
3. A metric requires measurement context.
4. Performance change requires a valid baseline.
5. Historical association is not causal proof.
6. Contradicting evidence must remain visible.
7. Learning should produce testable hypotheses, not universal laws.
8. A test plan is not evidence that the treatment works.
9. Statistical thresholds must not be invented when no statistical design exists.

## Centralized configuration

KOgenie loads runtime configuration through `config.py`.

`AppConfig` is the single source of truth for:

- text model
- vision model
- image model
- vector store ID
- SQLite database path
- generated visual directory
- approved visual directory

Safe defaults live in `config.py`.

Environment-specific overrides live in `.env`.

Secrets such as `OPENAI_API_KEY` stay in the environment
and are never committed.

Use `.env.example` as the setup template.

Configuration is loaded once per process and treated
as immutable.

## Workflow checkpoints and recovery

Substantial workflows now create durable stage checkpoints.

A checkpoint records:

- workflow run ID
- completed stage
- artifact type
- artifact reference
- SHA-256 artifact fingerprint
- creation time
- validity state

Checkpoint artifacts are stored under the configured
workflow checkpoint directory.

Recovery rules:

1. A stage is reusable only after its checkpoint is saved.
2. Checkpoint artifacts are hash-validated before reuse.
3. Missing or corrupted checkpoints are not trusted.
4. Checkpoint creation is idempotent for identical outputs.
5. Existing checkpoints are never silently overwritten with
   different output.
6. Failed workflow runs remain failed.
7. Recovery starts a new workflow run.
8. The recovery run records which failed run and checkpoint
   it reused.
9. Recovery resumes after the last contiguous valid stage.

## Current limitation

The system still relies on humans to enter research, claims, evidence,
and brand knowledge manually.

The next version begins adding tool-using AI research capabilities.
