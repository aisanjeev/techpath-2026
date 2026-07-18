# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Implement a Live Questions (Q&A) feature for students in virtual classrooms. Students can submit questions which are stored in PostgreSQL (`training_session_questions`) and broadcasted via WebSockets (`Classroom Broadcaster`). Trainers can toggle if questions are public, students can upvote public questions, and trainers can mark them as answered.

## Technical Context

**Language/Version**: Python 3.11, TypeScript (Next.js/Astro)

**Primary Dependencies**: FastAPI, SQLAlchemy 2.0, Zustand, React

**Storage**: PostgreSQL

**Testing**: pytest (backend)

**Target Platform**: Web Browsers (Trainer Admin & Student Portal)

**Project Type**: Monorepo (FastAPI backend + Next.js admin + Astro frontend)

**Performance Goals**: Real-time message delivery under 500ms via WebSockets.

**Constraints**: Must integrate smoothly into existing live streaming UI without blocking video.

**Scale/Scope**: Dozens of students per class, hundreds of questions per session.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
### Source Code (repository root)

```text
techpath-backend/
├── app/
│   ├── api/v1/endpoints/
│   ├── models/
│   ├── schemas/
│   ├── crud/
│   └── services/classroom/
└── tests/

techpath-admin/
├── src/
│   ├── components/training/
│   ├── services/
│   └── store/

techpath-frontend/
├── src/
│   ├── components/
│   └── utils/
```

**Structure Decision**: The feature spans all three tiers (backend for API/WebSockets, admin for trainer UI, frontend for student UI), adhering to the monorepo structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*(No violations found. The architecture properly separates API/DB from the React/Next.js/Astro frontends.)*
