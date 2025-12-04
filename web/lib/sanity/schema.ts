/**
 * Sanity Schema definitions for TypeScript types
 * These match the actual Sanity schema documents
 */

export interface HomepageHero {
  _id: string;
  headline: string;
  subheadline: string;
  primaryCtaText: string;
  primaryCtaLink: string;
  secondaryCtaText?: string;
  secondaryCtaLink?: string;
  heroImage?: {
    asset: {
      _ref: string;
      _type: 'reference';
    };
  };
  badgeText?: string;
}

export interface ServiceCard {
  _id: string;
  title: string;
  description: string;
  linkText: string;
  linkUrl: string;
  order: number;
}

export interface Testimonial {
  _id: string;
  title: string;
  quote: string;
  author: string;
  role?: string;
  company?: string;
  rating?: number;
  order: number;
}

export interface BenefitCard {
  _id: string;
  title: string;
  description: string;
  order: number;
}

export interface FAQ {
  _id: string;
  question: string;
  answer: string;
  order: number;
}

export interface UseCase {
  _id: string;
  title: string;
  description: string;
  details: string[];
  icon?: string;
  order: number;
}

export interface MissionSection {
  _id: string;
  leftCardTitle: string;
  leftCardBody: string;
  leftCardFooter?: string;
  rightCardTitle: string;
  rightCardBody: string;
  rightCardCtaText: string;
  rightCardCtaLink: string;
}

export interface FeaturedOn {
  _id: string;
  label: string;
  companies: string[];
}

export interface CategoryLink {
  _id: string;
  title: string;
  link: string;
  order: number;
}

