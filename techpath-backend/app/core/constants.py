"""Application constants."""
from dataclasses import dataclass, field
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    TRAINER = "trainer"
    USER = "user"


class InquiryStatus(str, Enum):
    """Contact inquiry status enumeration."""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class BlogPostStatus(str, Enum):
    """Blog post status enumeration."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


# Pagination defaults
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# File upload limits
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
ALLOWED_DOCUMENT_TYPES = ["application/pdf", "application/msword"]


# ============================================
# Lecture assets
# ============================================


class AssetStorageKind(str, Enum):
    """Where an asset's payload physically lives.

    Derived from ``AssetType`` via the registry rather than stored on the row, so it
    cannot drift from the type.
    """

    INLINE_TEXT = "inline_text"  # -> lecture_assets.body
    FILE = "file"  # -> lecture_assets.media_file_id
    LINK = "link"  # -> lecture_assets.external_url
    STRUCTURED = "structured"  # -> lecture_assets.config_json
    BUNDLE = "bundle"  # -> lecture_assets.bundle_path + bundle_entry


class AssetType(str, Enum):
    """The kinds of reusable block a lecture module can be built from."""

    # inline text
    MARKDOWN = "markdown"
    NOTES = "notes"
    CHEAT_SHEET = "cheat_sheet"
    CODE_SNIPPET = "code_snippet"
    # uploaded file
    PDF = "pdf"
    PPT = "ppt"
    VIDEO = "video"
    NOTEBOOK = "notebook"
    ZIP = "zip"
    EXCEL = "excel"
    CSV = "csv"
    TERMINAL_RECORDING = "terminal_recording"
    # link
    EXTERNAL_URL = "external_url"
    GITHUB_REPO = "github_repo"
    YOUTUBE = "youtube"
    # structured
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    LAB = "lab"
    # bundle — not selectable yet, see ASSET_TYPES_ENABLED
    HTML_BUNDLE = "html_bundle"


@dataclass(frozen=True)
class AssetTypeRule:
    """How one asset type is stored, validated and labelled."""

    kind: AssetStorageKind
    label: str
    max_size_mb: int = 0
    allowed_content_types: list[str] = field(default_factory=list)
    allowed_extensions: list[str] = field(default_factory=list)


ASSET_TYPE_RULES: dict[AssetType, AssetTypeRule] = {
    AssetType.MARKDOWN: AssetTypeRule(AssetStorageKind.INLINE_TEXT, "Markdown"),
    AssetType.NOTES: AssetTypeRule(AssetStorageKind.INLINE_TEXT, "Notes"),
    AssetType.CHEAT_SHEET: AssetTypeRule(AssetStorageKind.INLINE_TEXT, "Cheat Sheet"),
    AssetType.CODE_SNIPPET: AssetTypeRule(AssetStorageKind.INLINE_TEXT, "Code Snippet"),
    AssetType.PDF: AssetTypeRule(
        AssetStorageKind.FILE, "PDF", 50, ["application/pdf"], [".pdf"]
    ),
    AssetType.PPT: AssetTypeRule(
        AssetStorageKind.FILE,
        "Presentation",
        100,
        [
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ],
        [".ppt", ".pptx"],
    ),
    AssetType.VIDEO: AssetTypeRule(
        AssetStorageKind.FILE,
        "Video",
        500,
        ["video/mp4", "video/webm", "video/quicktime", "video/x-matroska"],
        [".mp4", ".webm", ".mov", ".mkv"],
    ),
    AssetType.NOTEBOOK: AssetTypeRule(
        AssetStorageKind.FILE,
        "Notebook",
        25,
        ["application/x-ipynb+json", "application/json"],
        [".ipynb"],
    ),
    AssetType.ZIP: AssetTypeRule(
        AssetStorageKind.FILE,
        "Archive",
        100,
        ["application/zip", "application/x-zip-compressed"],
        [".zip"],
    ),
    AssetType.EXCEL: AssetTypeRule(
        AssetStorageKind.FILE,
        "Spreadsheet",
        25,
        [
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ],
        [".xls", ".xlsx"],
    ),
    AssetType.CSV: AssetTypeRule(
        AssetStorageKind.FILE, "CSV", 25, ["text/csv", "application/csv"], [".csv"]
    ),
    AssetType.TERMINAL_RECORDING: AssetTypeRule(
        AssetStorageKind.FILE,
        "Terminal Recording",
        25,
        ["application/json", "application/x-asciicast", "text/plain"],
        [".cast", ".json"],
    ),
    AssetType.EXTERNAL_URL: AssetTypeRule(AssetStorageKind.LINK, "External Link"),
    AssetType.GITHUB_REPO: AssetTypeRule(AssetStorageKind.LINK, "GitHub Repo"),
    AssetType.YOUTUBE: AssetTypeRule(AssetStorageKind.LINK, "YouTube"),
    AssetType.QUIZ: AssetTypeRule(AssetStorageKind.STRUCTURED, "Quiz"),
    AssetType.ASSIGNMENT: AssetTypeRule(AssetStorageKind.STRUCTURED, "Assignment"),
    AssetType.LAB: AssetTypeRule(AssetStorageKind.STRUCTURED, "Lab"),
    AssetType.HTML_BUNDLE: AssetTypeRule(
        AssetStorageKind.BUNDLE,
        "HTML Bundle",
        100,
        ["application/zip", "application/x-zip-compressed"],
        [".zip"],
    ),
}

# html_bundle is modelled but deliberately not offered: authored JS must be served from
# a dedicated origin before it can be rendered safely, and that origin does not exist
# yet. Everything else about the type is ready, so enabling it is a one-line change.
ASSET_TYPES_DISABLED: frozenset[AssetType] = frozenset({AssetType.HTML_BUNDLE})

ASSET_TYPES_ENABLED: tuple[AssetType, ...] = tuple(
    t for t in AssetType if t not in ASSET_TYPES_DISABLED
)


def asset_rule(asset_type: AssetType | str) -> AssetTypeRule:
    """Look up the rule for an asset type."""
    return ASSET_TYPE_RULES[AssetType(asset_type)]


class AssetStatus(str, Enum):
    """Publication state of a lecture asset or training entity."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class TrainingDeliveryMode(str, Enum):
    """How a training programme or batch is delivered."""

    ONLINE = "online"
    OFFLINE = "offline"
    HYBRID = "hybrid"


class SessionStatus(str, Enum):
    """Lifecycle of a live training session."""

    SCHEDULED = "scheduled"
    LIVE = "live"
    ENDED = "ended"
    CANCELLED = "cancelled"


class PollStatus(str, Enum):
    """Lifecycle of a live classroom poll."""

    OPEN = "open"
    CLOSED = "closed"


class BatchStatus(str, Enum):
    """Mirrored batch lifecycle, mapped from the external roster API."""

    UPCOMING = "upcoming"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Cache TTL (in seconds)
CACHE_TTL_SHORT = 60  # 1 minute
CACHE_TTL_MEDIUM = 300  # 5 minutes
CACHE_TTL_LONG = 3600  # 1 hour

# Rate limiting
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW_SECONDS = 60

