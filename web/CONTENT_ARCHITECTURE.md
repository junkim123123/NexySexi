# Content Architecture v1

## Repo Analysis

### Current Content Patterns

**Landing Page (`/`):**
- Hero headline and subheadline: Hard-coded in JSX (`web/app/(marketing)/page.tsx`)
- Featured Projects: 3 project cards hard-coded as JSX elements
- Process section: Text hard-coded in component
- AI App Intro: Text hard-coded in Card component

**Resources Page (`/resources`):**
- Guides array: Hard-coded JavaScript array in component
- FAQs array: Hard-coded JavaScript array in component
- About section: Text hard-coded in JSX

**Use Cases Page (`/use-cases`):**
- Use cases array: Hard-coded JavaScript array with icon references

**Images:**
- No `public/images` directory exists
- No image references found in current components
- Images would need to be added to `public/` or external CDN

**Summary:**
- All content is embedded directly in React components
- No separation between content and presentation
- No markdown or content files
- No content management system
- Adding/editing content requires modifying TypeScript/JSX files

---

## Proposed Content Architecture (v1)

### Decision: MDX-based Content System

**Why MDX:**
- Markdown is familiar to non-developers
- Frontmatter provides structured metadata
- Can be easily migrated to a CMS later
- Works well with Next.js static generation
- Supports rich content (markdown + React components if needed)

**Short-term Image Strategy:**
- Use `/public/images/` directory for now
- Images referenced via URLs: `/images/case-studies/example.jpg`
- Later migration path: Replace URLs with CDN (S3/Cloudinary) URLs
- Content files only contain URLs, not file paths

**Non-Developer Workflow (v1):**
1. Edit markdown files in `/content/` directory
2. Add images to `/public/images/` directory
3. Update image URLs in markdown frontmatter
4. Ask developer to commit/push (or use GitHub web UI)
5. Later: Can add a simple CMS admin interface

---

## Types & File Structure

### TypeScript Types

**Location:** `web/lib/types/content.ts`

**Key Types:**
- `CaseStudy`: Featured projects/case studies
- `ResourceArticle`: Blog posts, guides, resources
- `FAQ`: Frequently asked questions

All types include:
- `id`, `slug` for routing
- `title`, `summary`, `description/body` for content
- `heroImageUrl`, `thumbnailImageUrl` for images (URLs, not paths)
- `publishedAt`, `tags` for metadata
- Optional fields for flexibility

### File Structure

```
web/
├── content/                          # Content directory (new)
│   ├── case-studies/                 # Case study MDX files
│   │   ├── seasonal-marshmallows.mdx
│   │   ├── licensed-goods-7eleven.mdx
│   │   └── certified-toys.mdx
│   ├── resources/                    # Resource/article MDX files
│   │   ├── how-to-calculate-landed-cost.mdx
│   │   ├── beginners-guide-snacks.mdx
│   │   └── what-is-ddp.mdx
│   └── faqs/                         # FAQ MDX files
│       ├── what-does-nexsupply-do.mdx
│       ├── shipping-or-analysis.mdx
│       └── ...
├── public/
│   └── images/                       # Image assets (new)
│       ├── case-studies/
│       │   ├── seasonal-marshmallows-hero.jpg
│       │   └── ...
│       └── resources/
│           └── ...
└── lib/
    ├── types/
    │   └── content.ts                # Content type definitions
    └── content/                      # Content loaders (new)
        ├── case-studies.ts          # getAllCaseStudies(), getCaseStudyBySlug()
        └── resources.ts             # getAllResources(), getResourceBySlug(), getAllFAQs()
```

### MDX File Format

**Case Study Example:**
```mdx
---
id: seasonal-marshmallows
slug: seasonal-marshmallows-don-quijote
title: Seasonal Marshmallows (Don Quijote)
summary: Rapid-cycle sourcing & DDP delivery for time-sensitive seasonal treats
heroImageUrl: /images/case-studies/seasonal-marshmallows-hero.jpg
thumbnailImageUrl: /images/case-studies/seasonal-marshmallows-thumb.jpg
client: Don Quijote
tags: [seasonal, food, japan, costco]
publishedAt: 2024-01-15T00:00:00Z
featured: true
featuredOrder: 1
---

Rapid-cycle sourcing & DDP delivery for time-sensitive seasonal treats (Halloween, Christmas) for Japanese/Costco markets.
```

**Resource Article Example:**
```mdx
---
id: how-to-calculate-landed-cost
slug: how-to-calculate-landed-cost-correctly
title: How to calculate landed cost correctly
summary: Learn the components of landed cost and how to avoid hidden fees.
category: Guides
status: published
publishedAt: 2024-02-01T00:00:00Z
heroImageUrl: /images/resources/landed-cost-hero.jpg
tags: [costing, guides, import]
---

# How to Calculate Landed Cost Correctly

[Full article content in markdown...]
```

**FAQ Example:**
```mdx
---
id: what-does-nexsupply-do
question: What does NexSupply actually do?
category: General
order: 1
---

NexSupply provides instant landed-cost and risk analysis for products you want to import...
```

---

## Integration Plan

### Phase 1: Proof of Concept (Current Implementation)

**1. Featured Projects Section (`/` landing page)**
- Replace hard-coded 3 project cards with `getAllCaseStudies({ featured: true })`
- Render cards from content data
- Keep existing Card component styling

**2. Resources Page**
- Replace hard-coded guides array with `getAllResources({ category: 'Guides' })`
- Replace hard-coded FAQs array with `getAllFAQs()`
- Keep existing Card component styling

**3. Create Example Content Files**
- Add 3 case study MDX files matching current featured projects
- Add 3 resource MDX files (can be "coming soon" status)
- Add 6 FAQ MDX files

### Phase 2: Full Migration (Future)

- Migrate hero copy to content config (optional)
- Migrate process section to content
- Create individual case study detail pages (`/case-studies/[slug]`)
- Create individual resource article pages (`/resources/[slug]`)

### Implementation Details

**Helper Functions:**
- `getAllCaseStudies(options?)`: Load all or filtered case studies
- `getCaseStudyBySlug(slug)`: Load single case study
- `getAllResources(options?)`: Load all or filtered resources
- `getResourceBySlug(slug)`: Load single resource
- `getAllFAQs()`: Load all FAQs

**Key Features:**
- Tree-shakable (only load what's needed)
- Works with Next.js static generation
- Easy to replace with CMS API calls later
- Type-safe with TypeScript

---

## Founder Guide: How to Update Content Without Touching Code (v1)

### Step 1: Understand the Content Structure

Content lives in the `/content` directory:
- `/content/case-studies/` - Featured project case studies
- `/content/resources/` - Blog posts and guides
- `/content/faqs/` - Frequently asked questions

Each file is a `.mdx` file (Markdown with frontmatter).

### Step 2: Adding or Editing a Case Study

1. **Create or edit a file** in `/content/case-studies/`
   - Filename: `your-project-name.mdx`
   - Example: `seasonal-marshmallows.mdx`

2. **Add frontmatter** (metadata at the top between `---`):
   ```yaml
   ---
   id: unique-id
   slug: url-friendly-slug
   title: Your Project Title
   summary: Short description for cards
   featured: true
   featuredOrder: 1
   publishedAt: 2024-01-15T00:00:00Z
   heroImageUrl: /images/case-studies/your-image.jpg
   ---
   ```

3. **Write the description** below the frontmatter (markdown supported)

4. **Add images** to `/public/images/case-studies/` and reference them in `heroImageUrl`

### Step 3: Adding or Editing a Resource Article

1. **Create or edit a file** in `/content/resources/`
   - Filename: `your-article-slug.mdx`

2. **Add frontmatter**:
   ```yaml
   ---
   id: unique-id
   slug: url-friendly-slug
   title: Article Title
   summary: Short summary
   category: Guides
   status: published
   publishedAt: 2024-02-01T00:00:00Z
   ---
   ```

3. **Write the article body** in markdown below the frontmatter

### Step 4: Adding or Editing FAQs

1. **Create or edit a file** in `/content/faqs/`
   - Filename: `question-slug.mdx`

2. **Add frontmatter**:
   ```yaml
   ---
   id: unique-id
   question: What is your question?
   category: General
   order: 1
   ---
   ```

3. **Write the answer** in markdown below

### Step 5: Managing Images

**Short-term (v1):**
1. Add images to `/public/images/` directory
   - Case studies: `/public/images/case-studies/`
   - Resources: `/public/images/resources/`
2. Reference in frontmatter: `heroImageUrl: /images/case-studies/filename.jpg`
3. Use relative paths starting with `/images/`

**Future (v2+):**
- Upload to S3/Cloudinary
- Replace URLs in content files
- No code changes needed

### Step 6: Making Changes Live

**Option A: GitHub Web UI (Recommended for non-developers)**
1. Go to your GitHub repository
2. Navigate to `/content/` directory
3. Click "Add file" or edit existing files
4. Commit changes
5. Changes deploy automatically (if auto-deploy is set up)

**Option B: Ask Developer**
1. Edit files locally or send content to developer
2. Developer commits and pushes
3. Changes deploy

### Step 7: Testing Your Changes

1. After committing, wait for deployment (usually 2-5 minutes)
2. Visit your site:
   - Homepage: Featured projects should update
   - `/resources`: Resources and FAQs should update
3. If something looks wrong, check:
   - Frontmatter syntax (must be valid YAML)
   - Image paths (must start with `/images/`)
   - File names (must end with `.mdx`)

### Quick Reference

**File Locations:**
- Case studies: `web/content/case-studies/*.mdx`
- Resources: `web/content/resources/*.mdx`
- FAQs: `web/content/faqs/*.mdx`
- Images: `web/public/images/`

**Required Frontmatter Fields:**
- Case studies: `id`, `slug`, `title`, `summary`, `publishedAt`
- Resources: `id`, `slug`, `title`, `summary`, `category`, `status`, `publishedAt`
- FAQs: `id`, `question`

**Common Mistakes to Avoid:**
- Don't forget the `---` markers around frontmatter
- Don't use spaces in image filenames (use hyphens)
- Don't forget to set `featured: true` for homepage case studies
- Don't use `status: draft` if you want content to show (use `published`)

---

## Next Steps (Future Enhancements)

1. **Add MDX Support**: Install `@next/mdx` and `gray-matter` packages
2. **Create Admin UI**: Simple interface to edit content without touching files
3. **Image Upload**: Direct image upload to S3/Cloudinary from admin
4. **Content Preview**: Preview changes before publishing
5. **Version Control**: Track content changes over time

---

## Dependencies Required

Add to `package.json`:
```json
{
  "dependencies": {
    "gray-matter": "^4.0.3"
  }
}
```

Install with: `npm install gray-matter`

