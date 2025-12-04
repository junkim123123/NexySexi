import { defineConfig } from 'sanity';
import { structureTool } from 'sanity/structure';
import { visionTool } from '@sanity/vision';

// Import new schemas
import siteSettings from './sanity/schemas/siteSettings';
import homePage from './sanity/schemas/homePage';
import howItWorksPage from './sanity/schemas/howItWorksPage';
import useCasesPage from './sanity/schemas/useCasesPage';

// Keep reusable document types for future use
import testimonial from './sanity/schemas/testimonial';
import faq from './sanity/schemas/faq';
import useCase from './sanity/schemas/useCase';

export default defineConfig({
  name: 'default',
  title: 'NexSupply CMS',

  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || 'vqt42bhw',
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

