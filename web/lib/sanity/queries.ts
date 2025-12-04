/**
 * Sanity GROQ queries for marketing content
 */

// Homepage Hero Section
export const HERO_QUERY = `*[_type == "homepageHero"][0]{
  _id,
  headline,
  subheadline,
  primaryCtaText,
  primaryCtaLink,
  secondaryCtaText,
  secondaryCtaLink,
  heroImage,
  badgeText
}`;

// Services/Features Section
export const SERVICES_QUERY = `*[_type == "serviceCard"] | order(order asc){
  _id,
  title,
  description,
  linkText,
  linkUrl,
  order
}`;

// Testimonials/Reviews Section
export const TESTIMONIALS_QUERY = `*[_type == "testimonial"] | order(order asc){
  _id,
  title,
  quote,
  author,
  role,
  company,
  rating,
  order
}`;

// Benefits Section
export const BENEFITS_QUERY = `*[_type == "benefitCard"] | order(order asc){
  _id,
  title,
  description,
  order
}`;

// FAQ Section
export const FAQ_QUERY = `*[_type == "faq"] | order(order asc){
  _id,
  question,
  answer,
  order
}`;

// Use Cases
export const USE_CASES_QUERY = `*[_type == "useCase"] | order(order asc){
  _id,
  title,
  description,
  details[],
  icon,
  order
}`;

// Mission Section
export const MISSION_QUERY = `*[_type == "missionSection"][0]{
  _id,
  leftCardTitle,
  leftCardBody,
  leftCardFooter,
  rightCardTitle,
  rightCardBody,
  rightCardCtaText,
  rightCardCtaLink
}`;

// Featured On Section
export const FEATURED_ON_QUERY = `*[_type == "featuredOn"][0]{
  _id,
  label,
  companies[]
}`;

// Category Links Section
export const CATEGORY_LINKS_QUERY = `*[_type == "categoryLink"] | order(order asc){
  _id,
  title,
  link,
  order
}`;


