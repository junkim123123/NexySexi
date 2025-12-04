import { defineConfig } from 'sanity';
import { structureTool } from 'sanity/structure';
import { visionTool } from '@sanity/vision';

// Import new schemas
import siteSettings from './schemas/siteSettings';
import homePage from './schemas/homePage';
import howItWorksPage from './schemas/howItWorksPage';
import useCasesPage from './schemas/useCasesPage';

// Keep reusable document types for future use
import testimonial from './schemas/testimonial';
import faq from './schemas/faq';
import useCase from './schemas/useCase';

export default defineConfig({
  name: 'default',
  title: 'NexSupply CMS',

  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || 'm4g1dr67',
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET || 'production',

  plugins: [structureTool(), visionTool()],

  schema: {
    types: [
      // Singleton pages
      siteSettings,
      homePage,
      howItWorksPage,
      useCasesPage,
      // Reusable documents
      testimonial,
      faq,
      useCase,
    ],
  },
});

