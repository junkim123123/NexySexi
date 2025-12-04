// web/lib/content/resources.ts

import {
  ResourcePageConfig,
  ResourceHeroSection,
  StartHereSection,
  DeepDiveSection,
  FAQSection,
} from '@/lib/types/resources';

const resourceHeroSection: ResourceHeroSection = {
  title: 'Resources',
  subtitle: 'Guides and FAQs to help you run smarter imports.',
};

const startHereSection: StartHereSection = {
  title: 'Start here',
  cards: [
    {
      id: 'how-it-works',
      title: 'How it Works',
      description: 'Learn how NexSupply guides you through the sourcing process.',
      cta: {
        id: 'view-guide',
        label: 'View guide →',
        href: '/how-it-works',
      },
    },
    {
      id: 'faq-page',
      title: 'FAQ page',
      description: 'Common questions about NexSupply and importing.',
      cta: {
        id: 'view-faqs',
        label: 'View FAQs →',
        href: '/resources#faq',
      },
    },
  ],
};

const deepDiveSection: DeepDiveSection = {
  title: 'Deep dive examples (coming soon)',
  cards: [
    {
      id: 'article-1',
      title: 'Example article 1',
      description: 'A placeholder description for a future deep-dive article.',
      badge: 'Coming soon',
    },
    {
      id: 'article-2',
      title: 'Example article 2',
      description: 'A placeholder description for a future deep-dive article.',
      badge: 'Coming soon',
    },
    {
      id: 'article-3',
      title: 'Example article 3',
      description: 'A placeholder description for a future deep-dive article.',
      badge: 'Coming soon',
    },
  ],
};

const faqSection: FAQSection = {
  title: 'Frequently Asked Questions',
  items: [
    {
      id: 'what-does-nexsupply-do',
      question: 'What does NexSupply actually do?',
      answer:
        'NexSupply provides instant landed-cost and risk analysis for products you want to import. We estimate FOB price, freight, duties, and compliance risks so you can make informed sourcing decisions.',
    },
    {
      id: 'shipping-or-analysis',
      question: 'Do you handle shipping or only analysis?',
      answer:
        'We focus on analysis and sourcing consultation. Our team connects you with verified suppliers and can help coordinate logistics, but we are primarily a sourcing intelligence platform.',
    },
    {
      id: 'replacement-for-sourcing-agent',
      question: 'Is this a replacement for a sourcing agent?',
      answer:
        'NexSupply complements traditional sourcing agents by providing instant, data-driven estimates. For serious orders, our team works with you to find and vet suppliers, similar to a sourcing agent but with AI-powered analysis upfront.',
    },
    {
      id: 'how-accurate-are-numbers',
      question: 'How accurate are the numbers?',
      answer:
        'Our estimates are ‘80% accurate’ for directional planning. Actual costs may vary based on supplier negotiations, market conditions, and specific requirements. We recommend using our reports as a starting point for deeper research.',
    },
    {
      id: 'how-long-analysis-take',
      question: 'How long does an analysis take?',
      answer:
        'Most analyses are completed in under 2 minutes. For more detailed reports with conversational deep-dive, the process takes 5–10 minutes.',
    },
  ],
};

export const resourcePageConfig: ResourcePageConfig = {
  hero: resourceHeroSection,
  startHere: startHereSection,
  deepDive: deepDiveSection,
  faq: faqSection,
};