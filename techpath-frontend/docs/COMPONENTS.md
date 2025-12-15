# Component Documentation

## Overview

TechPath uses a component-based architecture with Astro components for static content and React islands for interactivity.

## Component Categories

### Layouts (`src/layouts/`)

Base page layouts that wrap content.

| Component | Description | Props |
|-----------|-------------|-------|
| `MainLayout` | Default page layout | `title`, `description`, `image` |
| `BlogLayout` | Blog post layout | `title`, `pubDate`, `author`, `tags` |
| `DocumentationLayout` | Docs layout with sidebar | `title`, `section` |

### Shared Components (`src/components/shared/`)

Global components used across the site.

| Component | Description |
|-----------|-------------|
| `Header` | Site header with navigation |
| `Footer` | Site footer with links |
| `Navigation` | Main navigation menu |
| `Breadcrumb` | Page breadcrumb navigation |
| `CTA` | Call-to-action section |
| `SearchBar` | Search input component |

### Section Components (`src/components/sections/`)

Reusable page sections.

| Component | Description | Props |
|-----------|-------------|-------|
| `HeroSection` | Hero banner | N/A |
| `FeaturesGrid` | Features display | `features` |
| `ServiceShowcase` | Services grid | `services` |
| `Testimonials` | Client testimonials | `testimonials` |
| `StatCounter` | Statistics display | `stats` |
| `FAQSection` | FAQ accordion | `faqs` |
| `PricingTable` | Pricing plans | `plans` |
| `ContactForm` | Contact form | N/A |

### UI Components (`src/components/ui/`)

Base UI building blocks.

| Component | Description | Variants |
|-----------|-------------|----------|
| `Button` | Action button | `primary`, `secondary`, `outline`, `ghost` |
| `Card` | Content card | N/A |
| `Badge` | Status badge | `default`, `primary`, `success`, `warning`, `error` |
| `Tag` | Content tag | N/A |
| `Alert` | Alert message | `info`, `success`, `warning`, `error` |
| `Modal` | Dialog modal | `sm`, `md`, `lg`, `xl` |
| `Tabs` | Tabbed content | N/A |
| `Accordion` | Collapsible content | N/A |

### Form Components (`src/components/forms/`)

Form input elements.

| Component | Description |
|-----------|-------------|
| `Input` | Text input |
| `TextArea` | Multi-line text input |
| `Select` | Dropdown select |
| `Checkbox` | Checkbox input |
| `RadioGroup` | Radio button group |
| `FormError` | Error message display |

## Usage Examples

### Button Component

```astro
---
import Button from '@components/ui/Button.astro';
---

<Button variant="primary" size="lg" href="/contact">
  Get Started
</Button>
```

### Card Component

```astro
---
import Card from '@components/ui/Card.astro';
---

<Card
  title="AI Solutions"
  description="Transform your business with AI"
  href="/services/ai-consulting"
  tags={["AI", "ML"]}
/>
```

### Form Input

```astro
---
import Input from '@components/forms/Input.astro';
---

<Input
  id="email"
  name="email"
  type="email"
  label="Email Address"
  placeholder="you@company.com"
  required
/>
```

## Styling

All components use Tailwind CSS. Custom styles are defined in:
- `src/styles/globals.css` - Global styles and component classes

## Best Practices

1. **Keep components focused** - Each component should do one thing well
2. **Use TypeScript** - Define Props interfaces for type safety
3. **Responsive design** - Use Tailwind's responsive utilities
4. **Accessibility** - Include proper ARIA attributes
5. **Performance** - Minimize client-side JavaScript

