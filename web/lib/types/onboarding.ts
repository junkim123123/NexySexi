/**
 * Type definitions for onboarding selling context
 * 
 * These types define the structure for storing channel and market selections
 * during the chat onboarding flow.
 */

export type ChannelOption =
  | "amazon_fba"
  | "shopify_dtc"
  | "tiktok_shop"
  | "retail_wholesale"
  | "b2b_distributor"
  | "not_sure"
  | "other";

export type MarketOption =
  | "united_states"
  | "canada"
  | "mexico"
  | "europe"
  | "united_kingdom"
  | "japan"
  | "south_korea"
  | "taiwan"
  | "china_mainland"
  | "hong_kong"
  | "philippines"
  | "southeast_asia"
  | "middle_east_gulf"
  | "australia_new_zealand"
  | "latin_america"
  | "multiple"
  | "not_decided"
  | "other";

/**
 * Onboarding selling context
 * 
 * Stores the user's channel and market selections with support for "other" free text.
 * The "other" text is stored separately from the option enums for type safety.
 */
export interface OnboardingSellingContext {
  mainChannel?: ChannelOption;
  mainChannelOtherText?: string;
  targetMarkets: MarketOption[];
  targetMarketsOtherText?: string;
}

/**
 * Yearly volume plan options
 */
export type YearlyVolumePlan = "test" | "small_launch" | "steady" | "aggressive" | "not_sure";

/**
 * Timeline plan options
 */
export type TimelinePlan = "within_1_month" | "within_3_months" | "after_3_months" | "flexible";

/**
 * Complete onboarding state
 * 
 * Stores all answers collected during the onboarding conversation flow.
 */
export interface OnboardingState {
  projectName?: string;
  sellingContext: OnboardingSellingContext;
  yearlyVolumePlan?: YearlyVolumePlan;
  timelinePlan?: TimelinePlan;
}

/**
 * Helper functions for volume plan labels
 */
export function getVolumePlanLabel(plan: YearlyVolumePlan): string {
  const labels: Record<YearlyVolumePlan, string> = {
    test: "Test level (1-2 boxes)",
    small_launch: "Small launch (1 pallet or less)",
    steady: "Steady sales (1-3 pallets)",
    aggressive: "Aggressive expansion (3+ pallets)",
    not_sure: "Not sure yet",
  };
  return labels[plan];
}

/**
 * Helper functions for timeline plan labels
 */
export function getTimelinePlanLabel(plan: TimelinePlan): string {
  const labels: Record<TimelinePlan, string> = {
    within_1_month: "Within 1 month if possible",
    within_3_months: "Within 2-3 months",
    after_3_months: "After 3 months, no rush",
    flexible: "Timeline is flexible",
  };
  return labels[plan];
}

/**
 * Helper function to get human-readable label for channel option
 */
export function getChannelLabel(option: ChannelOption): string {
  const labels: Record<ChannelOption, string> = {
    amazon_fba: "Amazon FBA",
    shopify_dtc: "Shopify / DTC",
    tiktok_shop: "TikTok Shop",
    retail_wholesale: "Retail or wholesale",
    b2b_distributor: "B2B distributor or private label",
    not_sure: "Not sure yet",
    other: "Other",
  };
  return labels[option];
}

/**
 * Helper function to get human-readable label for market option
 */
export function getMarketLabel(option: MarketOption): string {
  const labels: Record<MarketOption, string> = {
    united_states: "United States",
    canada: "Canada",
    mexico: "Mexico",
    europe: "Europe (EU)",
    united_kingdom: "United Kingdom",
    japan: "Japan",
    south_korea: "South Korea",
    taiwan: "Taiwan",
    china_mainland: "China (Mainland)",
    hong_kong: "Hong Kong",
    philippines: "Philippines",
    southeast_asia: "Southeast Asia",
    middle_east_gulf: "Middle East and Gulf",
    australia_new_zealand: "Australia and New Zealand",
    latin_america: "Latin America",
    multiple: "Multiple markets",
    not_decided: "Not decided yet",
    other: "Other",
  };
  return labels[option];
}

