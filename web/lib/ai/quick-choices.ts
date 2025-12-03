import { ProductAnalysis } from '@/lib/product-analysis/schema';

/**
 * A map of field names to recommended quick-choice options.
 * This is used to render chips in the UI for the user to click.
 */
export const QUICK_CHOICES: Partial<Record<keyof ProductAnalysis, string[]>> = {
  import_country: [
    'United States',
    'European Union',
    'United Kingdom',
    'South Korea',
    'Other',
  ],
  sales_channel: [
    'Amazon FBA',
    'TikTok Shop',
    'Shopify (DTC)',
    'Wholesale / Retail',
    'Other',
  ],
  main_risk_concern: [
    'Duty / Tariffs',
    'Quality issues',
    'Shipping delays',
    'Compliance / Certifications',
    'Other',
  ],
  volume_plan: [
    'Test order (200–500 units)',
    'Standard (500–1,000 units)',
    'Growing (1,000–3,000 units)',
    'Aggressive (3,000+ units)',
  ],
};