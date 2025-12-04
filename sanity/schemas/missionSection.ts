import { defineType, defineField } from 'sanity';

export default defineType({
  name: 'missionSection',
  title: 'Mission Section',
  type: 'document',
  fields: [
    defineField({
      name: 'leftCardTitle',
      title: 'Left Card Title',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'leftCardBody',
      title: 'Left Card Body',
      type: 'text',
      rows: 4,
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'leftCardFooter',
      title: 'Left Card Footer',
      type: 'text',
      rows: 2,
    }),
    defineField({
      name: 'rightCardTitle',
      title: 'Right Card Title',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'rightCardBody',
      title: 'Right Card Body',
      type: 'text',
      rows: 3,
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'rightCardCtaText',
      title: 'Right Card CTA Text',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'rightCardCtaLink',
      title: 'Right Card CTA Link',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
  ],
  preview: {
    select: {
      title: 'leftCardTitle',
    },
  },
});

