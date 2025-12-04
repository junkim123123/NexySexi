/**
 * Case Studies Content Loader
 * 
 * This module loads case study content from MDX files.
 * In v1, we use file-based MDX. Later, this can be replaced with
 * a CMS API call without changing the interface.
 */

import { CaseStudy } from '@/lib/types/content';
import fs from 'fs';
import path from 'path';
// @ts-ignore - gray-matter types may not be available
import matter from 'gray-matter';

const CASE_STUDIES_DIR = path.join(process.cwd(), 'content', 'case-studies');

/**
 * Get all case studies, optionally filtered by featured status
 */
export function getAllCaseStudies(options?: { featured?: boolean }): CaseStudy[] {
  try {
    if (!fs.existsSync(CASE_STUDIES_DIR)) {
      return [];
    }

    const fileNames = fs.readdirSync(CASE_STUDIES_DIR);
    const mdxFiles = fileNames.filter((name) => name.endsWith('.mdx'));

    const caseStudies: CaseStudy[] = mdxFiles
      .map((fileName) => {
        const filePath = path.join(CASE_STUDIES_DIR, fileName);
        const fileContents = fs.readFileSync(filePath, 'utf8');
        const { data, content } = matter(fileContents);

        const slug = fileName.replace(/\.mdx$/, '');

        return {
          id: data.id || slug,
          slug: data.slug || slug,
          title: data.title || '',
          summary: data.summary || '',
          description: content.trim(),
          heroImageUrl: data.heroImageUrl,
          thumbnailImageUrl: data.thumbnailImageUrl,
          client: data.client,
          tags: data.tags || [],
          publishedAt: data.publishedAt || new Date().toISOString(),
          featured: data.featured ?? false,
          featuredOrder: data.featuredOrder ?? 999,
        } as CaseStudy;
      })
      .filter((cs) => {
        // Filter by featured if requested
        if (options?.featured !== undefined) {
          return cs.featured === options.featured;
        }
        return true;
      })
      .sort((a, b) => {
        // Sort featured by order, then by published date
        if (a.featured && b.featured) {
          return (a.featuredOrder || 999) - (b.featuredOrder || 999);
        }
        return new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime();
      });

    return caseStudies;
  } catch (error) {
    console.error('[getAllCaseStudies] Error loading case studies:', error);
    return [];
  }
}

/**
 * Get a single case study by slug
 */
export function getCaseStudyBySlug(slug: string): CaseStudy | null {
  try {
    const filePath = path.join(CASE_STUDIES_DIR, `${slug}.mdx`);
    
    if (!fs.existsSync(filePath)) {
      return null;
    }

    const fileContents = fs.readFileSync(filePath, 'utf8');
    const { data, content } = matter(fileContents);

    return {
      id: data.id || slug,
      slug: data.slug || slug,
      title: data.title || '',
      summary: data.summary || '',
      description: content.trim(),
      heroImageUrl: data.heroImageUrl,
      thumbnailImageUrl: data.thumbnailImageUrl,
      client: data.client,
      tags: data.tags || [],
      publishedAt: data.publishedAt || new Date().toISOString(),
      featured: data.featured ?? false,
      featuredOrder: data.featuredOrder ?? 999,
    } as CaseStudy;
  } catch (error) {
    console.error('[getCaseStudyBySlug] Error loading case study:', error);
    return null;
  }
}

