# Content Architecture v1 - Implementation Summary

## Repo Analysis

### Current Content Patterns

**Landing Page (`/`):**
- Hero headline and subheadline: Hard-coded in JSX (`web/app/(marketing)/page.tsx`)
- Featured Projects: 3 project cards hard-coded as JSX elements (lines 78-106)
- Process section: Text hard-coded in component (lines 112-136)
- AI App Intro: Text hard-coded in Card component (lines 42-62)

**Resources Page (`/resources`):**
- Guides array: Hard-coded JavaScript array in component (lines 6-27)
- FAQs array: Hard-coded JavaScript array in component (lines 29-55)
- About section: Text hard-coded in JSX (lines 108-125)

**Use Cases Page (`/use-cases`):**
- Use cases array: Hard-coded JavaScript array with icon references (lines 6-55)

**Images:**
- No `public/images` directory exists
- No image references found in current components
- Images would need to be added to `public/` or external CDN

**Summary:**
- ✅ All content is embedded directly in React components
- ✅ No separation between content and presentation
- ✅ No markdown or content files
- ✅ No content management system
- ✅ Adding/editing content requires modifying TypeScript/JSX files

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
├── content/                          # Content directory (NEW)
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
│       └── ... (6 total)
├── public/
│   └── images/                       # Image assets (NEW - to be created)
│       ├── case-studies/
│       └── resources/
└── lib/
    ├── types/
    │   └── content.ts                # Content type definitions (NEW)
    └── content/                      # Content loaders (NEW)
        ├── case-studies.ts          # getAllCaseStudies(), getCaseStudyBySlug()
        └── resources.ts             # getAllResources(), getResourceBySlug(), getAllFAQs()
```

### Helper Functions

**Location:** `web/lib/content/`

**Functions:**
- `getAllCaseStudies(options?)`: Load all or filtered case studies
- `getCaseStudyBySlug(slug)`: Load single case study
- `getAllResources(options?)`: Load all or filtered resources
- `getResourceBySlug(slug)`: Load single resource
- `getAllFAQs()`: Load all FAQs

**Key Features:**
- ✅ Tree-shakable (only load what's needed)
- ✅ Works with Next.js static generation
- ✅ Easy to replace with CMS API calls later
- ✅ Type-safe with TypeScript
- ✅ Graceful error handling (returns empty array if directory doesn't exist)

---

## Integration Plan

### Phase 1: Proof of Concept (Ready to Implement)

**1. Featured Projects Section (`/` landing page)**
- ✅ Content files created: 3 case study MDX files
- ✅ Loader function ready: `getAllCaseStudies({ featured: true })`
- 🔄 **Next step:** Update `web/app/(marketing)/page.tsx` to use content loader
- Replace hard-coded cards (lines 78-106) with dynamic rendering

**2. Resources Page**
- ✅ Content files created: 3 resource MDX files + 6 FAQ MDX files
- ✅ Loader functions ready: `getAllResources()`, `getAllFAQs()`
- 🔄 **Next step:** Update `web/app/(marketing)/resources/page.tsx` to use content loaders
- Replace hard-coded arrays (lines 6-27, 29-55) with dynamic rendering

**3. Image Directory Structure**
- 🔄 **Next step:** Create `/public/images/` directory structure
- Add placeholder images or actual images as needed

### Implementation Example

**Before (Hard-coded):**
```tsx
<Card>
  <h3>Seasonal Marshmallows (Don Quijote)</h3>
  <p>Rapid-cycle sourcing & DDP delivery...</p>
</Card>
```

**After (Content-driven):**
```tsx
import { getAllCaseStudies } from '@/lib/content/case-studies';

export default function HomePage() {
  const featuredProjects = getAllCaseStudies({ featured: true });
  
  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
      {featuredProjects.map((project) => (
        <Card key={project.id}>
          <h3>{project.title}</h3>
          <p>{project.summary}</p>
        </Card>
      ))}
    </div>
  );
}
```

### Phase 2: Full Migration (Future)

- Migrate hero copy to content config (optional)
- Migrate process section to content
- Create individual case study detail pages (`/case-studies/[slug]`)
- Create individual resource article pages (`/resources/[slug]`)
- Add image upload interface
- Add admin CMS UI

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
- ❌ Don't forget the `---` markers around frontmatter
- ❌ Don't use spaces in image filenames (use hyphens)
- ❌ Don't forget to set `featured: true` for homepage case studies
- ❌ Don't use `status: draft` if you want content to show (use `published`)

---

## Files Created

### Type Definitions
- ✅ `web/lib/types/content.ts` - TypeScript types for all content

### Content Loaders
- ✅ `web/lib/content/case-studies.ts` - Case study loading functions
- ✅ `web/lib/content/resources.ts` - Resource and FAQ loading functions

### Example Content Files
- ✅ `web/content/case-studies/seasonal-marshmallows.mdx`
- ✅ `web/content/case-studies/licensed-goods-7eleven.mdx`
- ✅ `web/content/case-studies/certified-toys.mdx`
- ✅ `web/content/resources/how-to-calculate-landed-cost.mdx`
- ✅ `web/content/resources/beginners-guide-snacks.mdx`
- ✅ `web/content/resources/what-is-ddp.mdx`
- ✅ `web/content/faqs/*.mdx` (6 FAQ files)

### Documentation
- ✅ `web/CONTENT_ARCHITECTURE.md` - Full architecture documentation
- ✅ `web/CONTENT_ARCHITECTURE_SUMMARY.md` - This summary file

### Dependencies
- ✅ `gray-matter` installed for parsing MDX frontmatter

---

## Next Steps

1. **Create image directories:**
   ```bash
   mkdir -p public/images/case-studies
   mkdir -p public/images/resources
   ```

2. **Update landing page** (`web/app/(marketing)/page.tsx`):
   - Import `getAllCaseStudies` from `@/lib/content/case-studies`
   - Replace hard-coded Featured Projects section with dynamic rendering
   - Convert to server component or add API route if needed

3. **Update resources page** (`web/app/(marketing)/resources/page.tsx`):
   - Import `getAllResources` and `getAllFAQs` from `@/lib/content/resources`
   - Replace hard-coded arrays with dynamic rendering

4. **Test the integration:**
   - Verify case studies appear on homepage
   - Verify resources and FAQs appear on resources page
   - Test adding a new case study file

5. **Future enhancements:**
   - Add MDX rendering for rich content
   - Create detail pages for individual case studies/resources
   - Add admin UI for content management
   - Migrate images to CDN

---

## Migration Path to CMS

When ready to move to a headless CMS:

1. **Keep the same TypeScript types** - they're CMS-agnostic
2. **Replace loader functions** - instead of reading files, make API calls:
   ```ts
   // Before: fs.readFileSync(...)
   // After: await fetch('https://cms.nexsupply.com/api/case-studies')
   ```
3. **Update image URLs** - replace `/images/` paths with CDN URLs
4. **No component changes needed** - components still use the same types

The architecture is designed to be CMS-ready from day one.

