import { defineType, defineField } from 'sanity';

export default defineType({
  name: 'featuredOn',
  title: 'Featured On',
  type: 'document',
  fields: [
    defineField({
      name: 'label',
      title: 'Label',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'companies',
      title: 'Companies',
      type: 'array',
      of: [{ type: 'string' }],
      validation: (Rule) => Rule.required().min(1),
    }),
  ],
  preview: {
    select: {
      title: 'label',
    },
  },
});

