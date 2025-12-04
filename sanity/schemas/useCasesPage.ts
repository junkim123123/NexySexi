import { defineType, defineField } from 'sanity';

export default defineType({
  name: 'useCasesPage',
  title: 'Use Cases Page',
  type: 'document',
  __experimental_actions: [
    // 'create',
    'update',
    // 'delete',
    'publish',
  ],
  fields: [
    defineField({
      name: 'title',
      title: 'Page Title',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'subtitle',
      title: 'Subtitle',
      type: 'text',
      rows: 2,
    }),
    defineField({
      name: 'useCases',
      title: 'Use Cases',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'label', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'description', type: 'text', rows: 2, validation: (Rule) => Rule.required() },
            { name: 'keyFeaturesTitle', type: 'string', initialValue: 'Key features:' },
            {
              name: 'keyFeatures',
              type: 'array',
              of: [{ type: 'string' }],
            },
          ],
        },
      ],
    }),
    defineField({
      name: 'ctaTitle',
      title: 'CTA Title',
      type: 'string',
    }),
    defineField({
      name: 'ctaBody',
      title: 'CTA Body',
      type: 'text',
      rows: 2,
    }),
    defineField({
      name: 'ctaButtonLabel',
      title: 'CTA Button Label',
      type: 'string',
    }),
    defineField({
      name: 'ctaButtonUrl',
      title: 'CTA Button URL',
      type: 'string',
    }),
  ],
  preview: {
    prepare() {
      return {
        title: 'Use Cases Page',
      };
    },
  },
});

