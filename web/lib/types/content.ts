/**
 * Content types for marketing content (case studies, blog posts, resources)
 * These types are designed to be future-proof and work with both file-based
 * and eventual CMS-based content.
 */

export interface CaseStudy {
  /** Unique identifier (e.g., "seasonal-marshmallows") */
  id: string;
  /** URL-friendly slug (e.g., "seasonal-marshmallows-don-quijote") */
  slug: string;
  /** Display title */
  title: string;
  /** Short summary for cards/previews */
  summary: string;
  /** Full description/body content (markdown supported) */
  description: string;
  /** Hero image URL (public URL or CDN) */
  heroImageUrl?: string;
  /** Thumbnail image URL for cards */
  thumbnailImageUrl?: string;
  /** Client/partner name */
  client?: string;
  /** Tags for filtering/categorization */
  tags?: string[];
  /** Publication date (ISO string) */
  publishedAt: string;
  /** Whether to feature on homepage */
  featured?: boolean;
  /** Order for featured display (lower = first) */
  featuredOrder?: number;
}

export interface ResourceArticle {
  /** Unique identifier */
  id: string;
  /** URL-friendly slug */
  slug: string;
  /** Display title */
  title: string;
  /** Short summary for cards */
  summary: string;
  /** Full article content (markdown supported) */
  body: string;
  /** Category (e.g., "Guides", "FAQs", "Case Studies") */
  category: string;
  /** Hero image URL */
  heroImageUrl?: string;
  /** Thumbnail image URL */
  thumbnailImageUrl?: string;
  /** Tags */
  tags?: string[];
  /** Publication date (ISO string) */
  publishedAt: string;
  /** Status (e.g., "published", "draft", "coming-soon") */
  status?: 'published' | 'draft' | 'coming-soon';
  /** Author name (optional) */
  author?: string;
}

export interface FAQ {
  /** Unique identifier */
  id: string;
  /** Question text */
  question: string;
  /** Answer text (markdown supported) */
  answer: string;
  /** Category for grouping */
  category?: string;
  /** Order for display */
  order?: number;
}

/**
 * Content metadata for frontmatter in MDX files
 */
export interface ContentFrontmatter {
  title: string;
  summary?: string;
  publishedAt: string;
  heroImageUrl?: string;
  thumbnailImageUrl?: string;
  tags?: string[];
  [key: string]: unknown; // Allow additional fields
}

