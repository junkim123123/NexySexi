/**
 * Helper functions for working with onboarding state
 * 
 * Provides utilities to convert onboarding state to API-ready formats
 * and extract relevant context for AI analysis.
 */

import type { OnboardingState } from './types/onboarding';

/**
 * Convert OnboardingState to a format suitable for API requests
 * This extracts only the relevant fields for AI analysis
 */
export function getOnboardingContextForAnalysis(
  onboardingState: OnboardingState | null
): {
  projectName?: string;
  mainChannel?: string;
  mainChannelOtherText?: string;
  targetMarkets?: string[];
  targetMarketsOtherText?: string;
  yearlyVolumePlan?: string;
  timelinePlan?: string;
} | undefined {
  if (!onboardingState) {
    return undefined;
  }

  return {
    projectName: onboardingState.projectName,
    mainChannel: onboardingState.sellingContext.mainChannel,
    mainChannelOtherText: onboardingState.sellingContext.mainChannelOtherText,
    targetMarkets: onboardingState.sellingContext.targetMarkets,
    targetMarketsOtherText: onboardingState.sellingContext.targetMarketsOtherText,
    yearlyVolumePlan: onboardingState.yearlyVolumePlan,
    timelinePlan: onboardingState.timelinePlan,
  };
}

