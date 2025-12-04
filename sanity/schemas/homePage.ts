import { defineType, defineField } from 'sanity';

export default defineType({
  name: 'homePage',
  title: 'Home Page',
  type: 'document',
  __experimental_actions: [
    // 'create',
    'update',
    // 'delete',
    'publish',
  ],
  fields: [
    // Hero Section
    defineField({
      name: 'heroTitle',
      title: 'Hero Title',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'heroSubtitle',
      title: 'Hero Subtitle',
      type: 'text',
      rows: 3,
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'heroCtaLabel',
      title: 'Hero CTA Label',
      type: 'string',
      initialValue: 'Get started',
    }),
    defineField({
      name: 'heroBadge',
      title: 'Hero Badge Text',
      type: 'string',
    }),
    defineField({
      name: 'heroImage',
      title: 'Hero Image',
      type: 'image',
      options: {
        hotspot: true,
      },
    }),

    // Highlight Cards
    defineField({
      name: 'highlights',
      title: 'Highlight Cards',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'title', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'body', type: 'text', rows: 3, validation: (Rule) => Rule.required() },
            { name: 'ctaLabel', type: 'string' },
            { name: 'ctaUrl', type: 'string' },
          ],
        },
      ],
    }),

    // Social Proof / Reviews
    defineField({
      name: 'reviewsTitle',
      title: 'Reviews Section Title',
      type: 'string',
    }),
    defineField({
      name: 'reviews',
      title: 'Reviews',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'headline', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'quote', type: 'text', rows: 3, validation: (Rule) => Rule.required() },
            { name: 'author', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'date', type: 'string' },
            { name: 'rating', type: 'number', initialValue: 5 },
          ],
        },
      ],
    }),
    defineField({
      name: 'ratingText',
      title: 'Rating Summary Text',
      type: 'string',
    }),

    // Benefit Cards
    defineField({
      name: 'benefitsTitle',
      title: 'Benefits Section Title',
      type: 'string',
    }),
    defineField({
      name: 'benefits',
      title: 'Benefit Cards',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'title', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'body', type: 'text', rows: 3, validation: (Rule) => Rule.required() },
          ],
        },
      ],
    }),

    // Trusted By
    defineField({
      name: 'trustedTitle',
      title: 'Trusted By Title',
      type: 'string',
    }),
    defineField({
      name: 'trustedLogos',
      title: 'Trusted By Logos',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'label', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'logo', type: 'image', options: { hotspot: true } },
            { name: 'textOnly', type: 'boolean', initialValue: true },
          ],
        },
      ],
    }),

    // Impact Block
    defineField({
      name: 'impactTitle',
      title: 'Impact Title',
      type: 'string',
    }),
    defineField({
      name: 'impactBody',
      title: 'Impact Body',
      type: 'text',
      rows: 4,
    }),
    defineField({
      name: 'impactStatLabel',
      title: 'Impact Stat Label',
      type: 'string',
    }),
    defineField({
      name: 'impactStatBody',
      title: 'Impact Stat Body',
      type: 'text',
      rows: 2,
    }),
    defineField({
      name: 'impactCtaLabel',
      title: 'Impact CTA Label',
      type: 'string',
    }),
    defineField({
      name: 'impactCtaUrl',
      title: 'Impact CTA URL',
      type: 'string',
    }),

    // Category List
    defineField({
      name: 'categoriesTitle',
      title: 'Categories Title',
      type: 'string',
    }),
    defineField({
      name: 'categories',
      title: 'Categories',
      type: 'array',
      of: [{ type: 'string' }],
    }),

    // FAQ Teaser
    defineField({
      name: 'faqTeaserTitle',
      title: 'FAQ Teaser Title',
      type: 'string',
    }),
    defineField({
      name: 'faqTeaserBody',
      title: 'FAQ Teaser Body',
      type: 'text',
      rows: 2,
    }),
    defineField({
      name: 'faqItems',
      title: 'FAQ Items',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'question', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'answer', type: 'text', rows: 3, validation: (Rule) => Rule.required() },
          ],
        },
      ],
    }),
  ],
  preview: {
    prepare() {
      return {
        title: 'Home Page',
      };
    },
  },
});

