import { defineType, defineField } from 'sanity';

export default defineType({
  name: 'howItWorksPage',
  title: 'How It Works Page',
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
      name: 'steps',
      title: 'Steps',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            { name: 'stepNumber', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'title', type: 'string', validation: (Rule) => Rule.required() },
            { name: 'body', type: 'text', rows: 3, validation: (Rule) => Rule.required() },
            {
              name: 'bullets',
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
      name: 'ctaLines',
      title: 'CTA Lines',
      type: 'array',
      of: [{ type: 'string' }],
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
        title: 'How It Works Page',
      };
    },
  },
});

