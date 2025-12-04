/**
 * Onboarding Steps Configuration
 * 
 * This is the single source of truth for the Nexi onboarding conversation flow.
 * Each step defines:
 * - The message Nexi asks
 * - The type of answer expected
 * - Which UI component to render
 * 
 * To add a new step:
 * 1. Add a new StepId to web/lib/types/onboardingSteps.ts
 * 2. Add a new step object to this array
 * 3. Wire up the answer handling in the chat component
 * 4. Update the onboarding state type if needed
 */

import type { OnboardingStep } from '@/lib/types/onboardingSteps';

export const onboardingSteps: OnboardingStep[] = [
  {
    id: 'project_name',
    order: 1,
    nexMessage: 'Hi, I\'m Nexi! What would you like to call this project?',
    helperText: 'A simple name like "Japanese gummy test" or "US wholesale trial" is fine.',
    answerKind: 'short_text',
  },
  {
    id: 'main_channel',
    order: 2,
    nexMessage: 'What\'s the most important sales channel for this project?',
    helperText: 'Just pick the one channel you want to focus on right now.',
    answerKind: 'chips_single',
    usesChannelChips: true,
  },
  {
    id: 'target_markets',
    order: 3,
    nexMessage: 'Which markets are you primarily targeting for this product?',
    helperText: 'You can select multiple. You can change this later.',
    answerKind: 'chips_multi',
    usesMarketChips: true,
  },
  {
    id: 'yearly_volume',
    order: 4,
    nexMessage: 'Roughly how much volume are you thinking for the year?',
    helperText: 'It doesn\'t need to be exact. Just pick what feels right.',
    answerKind: 'chips_single',
  },
  {
    id: 'timeline',
    order: 5,
    nexMessage: 'When do you want to receive your first box?',
    helperText: 'I\'ll use this to calculate lead times.',
    answerKind: 'chips_single',
  },
];

/**
 * Helper to get step by ID
 */
export function getStepById(stepId: string): OnboardingStep | undefined {
  return onboardingSteps.find((step) => step.id === stepId);
}

/**
 * Helper to get step by order/index
 */
export function getStepByOrder(order: number): OnboardingStep | undefined {
  return onboardingSteps.find((step) => step.order === order);
}

/**
 * Get the next step after a given step ID
 */
export function getNextStep(currentStepId: string): OnboardingStep | null {
  const currentStep = getStepById(currentStepId);
  if (!currentStep) return null;
  
  const nextStep = getStepByOrder(currentStep.order + 1);
  return nextStep || null;
}

