/**
 * Client-side storage utilities for onboarding state
 * 
 * Persists onboarding state to localStorage so it survives page reloads
 * and can be reused by other parts of the app.
 */

import type { OnboardingState } from './types/onboarding';

const ONBOARDING_STORAGE_KEY = 'nexsupply_onboarding_state_v1';

/**
 * Save onboarding state to localStorage
 */
export const saveOnboardingState = (state: OnboardingState): void => {
  try {
    const serialized = JSON.stringify(state);
    localStorage.setItem(ONBOARDING_STORAGE_KEY, serialized);
  } catch (error) {
    console.error('[OnboardingStorage] Failed to save state:', error);
  }
};

/**
 * Load onboarding state from localStorage
 * 
 * @returns The saved onboarding state, or null if not found or invalid
 */
export const loadOnboardingState = (): OnboardingState | null => {
  try {
    const serialized = localStorage.getItem(ONBOARDING_STORAGE_KEY);
    if (!serialized) {
      return null;
    }

    const state = JSON.parse(serialized) as OnboardingState;
    
    // Basic validation: ensure required structure exists
    if (!state || typeof state !== 'object') {
      return null;
    }

    // Ensure sellingContext exists with at least targetMarkets array
    if (!state.sellingContext || !Array.isArray(state.sellingContext.targetMarkets)) {
      return {
        ...state,
        sellingContext: {
          targetMarkets: [],
          ...state.sellingContext,
        },
      };
    }

    return state;
  } catch (error) {
    console.error('[OnboardingStorage] Failed to load state:', error);
    return null;
  }
};

/**
 * Clear onboarding state from localStorage
 */
export const clearOnboardingState = (): void => {
  try {
    localStorage.removeItem(ONBOARDING_STORAGE_KEY);
  } catch (error) {
    console.error('[OnboardingStorage] Failed to clear state:', error);
  }
};

