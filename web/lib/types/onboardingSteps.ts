/**
 * Onboarding Step Model
 * 
 * Defines the structure for Nexi onboarding conversation steps.
 * Each step knows its question, answer type, and which UI component to render.
 */

export type AnswerKind =
  | "short_text"
  | "chips_single"
  | "chips_multi"
  | "number";

export type StepId =
  | "project_name"
  | "main_channel"
  | "target_markets"
  | "yearly_volume"
  | "timeline";

export interface OnboardingStep {
  id: StepId;
  order: number;
  nexMessage: string;
  helperText?: string;
  answerKind: AnswerKind;
  // Optional sub configs so steps know which component to use
  usesChannelChips?: boolean;
  usesMarketChips?: boolean;
  numberUnitLabel?: string;
}

