# Feature Specification: Digital Marketing Seeding

**Feature Branch**: `[011-digital-marketing-seeding]`

**Created**: 2026-07-27

**Status**: Draft

**Input**: User description: "Program: Digital Marketing with Generative AI Assests: "D:\project\techpath\techpath-2026\syllabus\digital marketing with gen ai\assests" do one thing first write the meta data like assets type, also others meta dataand keep module wise, thene create records from curl, then next step update with assets data. this way, title description summary etc will be 100%. in previous you just trim from body."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Module Metadata (Priority: P1)

As an administrator, I want to explicitly generate 100% correct metadata (title, description, tags, asset type) for each module of the Digital Marketing program before uploading, so that the course content looks professional and accurate.

**Why this priority**: Correct metadata is crucial for the student experience. Relying on simple extraction leaves errors.
**Independent Test**: Can be tested by examining the generated `metadata.json` file in each module directory to ensure title, description, and tags accurately reflect the asset contents.

**Acceptance Scenarios**:
1. **Given** a directory of module assets, **When** the extraction process is run, **Then** a `metadata.json` is produced containing high-quality extracted attributes for each file.

---

### User Story 2 - Upload Course Assets (Priority: P2)

As an administrator, I want to upload the files and create database records utilizing the pre-generated metadata, so that the backend correctly mirrors the course structure.

**Why this priority**: Required to finalize the program seeding on the platform.
**Independent Test**: Can be tested by fetching the program assets via the API and verifying they match the metadata files exactly.

**Acceptance Scenarios**:
1. **Given** validated `metadata.json` files, **When** the seeding script runs, **Then** API records are created with the exact metadata, and files are uploaded as associated media.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST process the `D:\project\techpath\techpath-2026\syllabus\digital marketing with gen ai\assests` directory.
- **FR-002**: System MUST generate a `metadata.json` file in each module subdirectory containing `title`, `description`, `asset_type`, and `tags` for every file.
- **FR-003**: System MUST provide 100% accurate metadata extraction, avoiding crude truncation or regex trimming.
- **FR-004**: System MUST create asset records using a backend API (or cURL representation) authenticated with a Bearer token.
- **FR-005**: System MUST upload the physical files to blob storage and link them to the created asset records.

### Key Entities

- **Asset Metadata**: JSON structure mapping filenames to their title, description, tags, and type.
- **Module**: A collection of assets grouped together.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of files in the target directory have complete and accurate metadata generated.
- **SC-002**: 100% of the generated metadata records are successfully created in the database via the API without errors.
- **SC-003**: All physical assets are properly uploaded and associated with their respective metadata records.

## Assumptions

- The provided Bearer token has sufficient permissions to create assets and upload media.
- The Digital Marketing program ID already exists or will be correctly resolved during the upload process.
