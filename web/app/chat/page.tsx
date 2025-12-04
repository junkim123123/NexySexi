/**
 * NexSupply Chat-First Interface - Config-Driven Onboarding
 * 
 * This chat interface uses a configuration-driven approach where conversation
 * steps are defined in onboardingSteps.ts. The UI renders questions and collects
 * answers based on the step configuration.
 * 
 * Layout Structure:
 * - Top Header: NexSupply logo, project name, progress indicator
 * - Main Chat Area: Scrollable message timeline (Nexi bubbles on left, user bubbles on right)
 * - Right Side Panel: Current project snapshot with collected answers
 * - Bottom Input Area: Dynamic input based on current step (text, chips, etc.)
 */

'use client';

import { useState, useRef, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { Send, Camera } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { onboardingSteps, getStepById, getNextStep } from './onboardingSteps';
import type { OnboardingStep } from '@/lib/types/onboardingSteps';
import type { OnboardingState } from '@/lib/types/onboarding';
import { ChannelChips } from '@/components/chat/ChannelChips';
import { MarketChips } from '@/components/chat/MarketChips';
import { GenericChipGroup } from '@/components/chat/GenericChipGroup';
import type { ChannelOption, YearlyVolumePlan, TimelinePlan } from '@/lib/types/onboarding';
import { getChannelLabel, getMarketLabel } from '@/lib/types/onboarding';
import { OnboardingSummaryCard } from '@/components/chat/OnboardingSummaryCard';
import { saveOnboardingState, loadOnboardingState } from '@/lib/onboardingStorage';

type ChatMessage = {
  id: string;
  role: 'assistant' | 'user';
  content: string | ReactNode;
};

// Chip options for yearly volume and timeline steps
const YEARLY_VOLUME_OPTIONS = [
  { value: 'test', label: 'Test level (1-2 boxes)' },
  { value: 'small_launch', label: 'Small launch (1 pallet or less)' },
  { value: 'steady', label: 'Steady sales (1-3 pallets)' },
  { value: 'aggressive', label: 'Aggressive expansion (3+ pallets)' },
  { value: 'not_sure', label: 'Not sure yet' },
];

const TIMELINE_OPTIONS = [
  { value: 'within_1_month', label: 'Within 1 month if possible' },
  { value: 'within_3_months', label: 'Within 2-3 months' },
  { value: 'after_3_months', label: 'After 3 months, no rush' },
  { value: 'flexible', label: 'Timeline is flexible' },
];

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentStepId, setCurrentStepId] = useState<string | null>(null);
  const [input, setInput] = useState('');
  const [onboardingState, setOnboardingState] = useState<OnboardingState>({
    sellingContext: {
      targetMarkets: [],
    },
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load saved state from localStorage on mount
  useEffect(() => {
    if (isInitialized) return;

    const savedState = loadOnboardingState();
    if (savedState) {
      setOnboardingState(savedState);
      
      // Reconstruct messages from saved state
      const reconstructedMessages: ChatMessage[] = [];
      let nextStepId: string | null = null;
      
      // Check each step to see if it's completed
      for (const step of onboardingSteps) {
        let isStepComplete = false;
        let userAnswer = '';

        if (step.id === 'project_name') {
          isStepComplete = !!savedState.projectName;
          userAnswer = savedState.projectName || '';
        } else if (step.id === 'main_channel') {
          isStepComplete = !!savedState.sellingContext.mainChannel;
          if (isStepComplete) {
            if (savedState.sellingContext.mainChannel === 'other' && savedState.sellingContext.mainChannelOtherText) {
              userAnswer = `Other (${savedState.sellingContext.mainChannelOtherText})`;
            } else {
              userAnswer = getChannelLabel(savedState.sellingContext.mainChannel!);
            }
          }
        } else if (step.id === 'target_markets') {
          isStepComplete = savedState.sellingContext.targetMarkets.length > 0;
          if (isStepComplete) {
            userAnswer = savedState.sellingContext.targetMarkets
              .map(m => m === 'other' && savedState.sellingContext.targetMarketsOtherText
                ? `Other (${savedState.sellingContext.targetMarketsOtherText})`
                : getMarketLabel(m))
              .join(', ');
          }
        } else if (step.id === 'yearly_volume') {
          isStepComplete = !!savedState.yearlyVolumePlan;
          if (isStepComplete) {
            userAnswer = YEARLY_VOLUME_OPTIONS.find(opt => opt.value === savedState.yearlyVolumePlan)?.label || '';
          }
        } else if (step.id === 'timeline') {
          isStepComplete = !!savedState.timelinePlan;
          if (isStepComplete) {
            userAnswer = TIMELINE_OPTIONS.find(opt => opt.value === savedState.timelinePlan)?.label || '';
          }
        }

        if (isStepComplete) {
          // Add Nexi's question
          reconstructedMessages.push({
            id: `assistant-${step.id}-restored`,
            role: 'assistant',
            content: step.nexMessage,
          });
          // Add user's answer
          reconstructedMessages.push({
            id: `user-${step.id}-restored`,
            role: 'user',
            content: userAnswer,
          });
        } else {
          // This is the first incomplete step - set it as current
          nextStepId = step.id;
          reconstructedMessages.push({
            id: `assistant-${step.id}-restored`,
            role: 'assistant',
            content: step.nexMessage,
          });
          break;
        }
      }

      // If all steps are complete, show completion message with CTA
      if (nextStepId === null) {
        reconstructedMessages.push({
          id: 'complete-restored',
          role: 'assistant',
          content: (
            <div className="space-y-4">
              <div>
                <p className="mb-2">All done! 🎉</p>
                <p>We've collected all the information. You can now start analyzing your project.</p>
              </div>
              <Button
                onClick={() => router.push('/analyze/chat')}
                className="w-full sm:w-auto"
              >
                Start analysis for this project
              </Button>
            </div>
          ),
        });
      }

      setCurrentStepId(nextStepId);
      setMessages(reconstructedMessages);
    } else {
      // No saved state - initialize with first step
      if (onboardingSteps.length > 0) {
        const firstStep = onboardingSteps[0];
        setCurrentStepId(firstStep.id);
        setMessages([{
          id: 'welcome',
          role: 'assistant',
          content: firstStep.nexMessage,
        }]);
      }
    }

    setIsInitialized(true);
  }, [isInitialized]);

  // Save state to localStorage whenever it changes
  useEffect(() => {
    if (!isInitialized) return;
    saveOnboardingState(onboardingState);
  }, [onboardingState, isInitialized]);

  // Auto-scroll to bottom when messages change or current step changes
  useEffect(() => {
    // Small delay to ensure DOM is updated
    const timeoutId = setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
    return () => clearTimeout(timeoutId);
  }, [messages, currentStepId]);

  // Get current step from config
  const currentStep: OnboardingStep | undefined = currentStepId ? getStepById(currentStepId) : undefined;

  // Compute progress indicators
  const totalSteps = onboardingSteps.length;
  const currentStepIndex = currentStep ? onboardingSteps.findIndex(s => s.id === currentStep.id) : -1;

  /**
   * Helper to check if the current step is complete and ready to proceed
   */
  const isCurrentStepComplete = (step: OnboardingStep | undefined, state: OnboardingState, input: string): boolean => {
    if (!step) return false;

    if (step.answerKind === 'short_text') {
      return input.trim().length > 0;
    } else if (step.answerKind === 'chips_single') {
      if (step.usesChannelChips) {
        // For channel chips, also check if "other" has text when selected
        if (state.sellingContext.mainChannel === 'other') {
          return !!state.sellingContext.mainChannelOtherText?.trim();
        }
        return !!state.sellingContext.mainChannel;
      } else if (step.id === 'yearly_volume') {
        return !!state.yearlyVolumePlan;
      } else if (step.id === 'timeline') {
        return !!state.timelinePlan;
      }
    } else if (step.answerKind === 'chips_multi') {
      if (step.usesMarketChips) {
        // For market chips, check if "other" has text when selected
        if (state.sellingContext.targetMarkets.includes('other')) {
          return state.sellingContext.targetMarkets.length > 0 && !!state.sellingContext.targetMarketsOtherText?.trim();
        }
        return state.sellingContext.targetMarkets.length > 0;
      }
    }

    return false;
  };

  /**
   * Get the label for the Next button based on current step
   */
  const getNextButtonLabel = (step: OnboardingStep | undefined): string => {
    if (!step) return 'Continue';
    
    const isLastStep = currentStepIndex >= 0 && currentStepIndex === totalSteps - 1;
    return isLastStep ? 'Complete' : 'Continue';
  };

  /**
   * Handles moving to the next step in the conversation.
   * This is the main "Next" logic that validates, saves answers, and advances the flow.
   */
  const handleNext = () => {
    if (!currentStep) return;

    let canProceed = false;
    let answerValue: any = null;

    // Validate based on answer kind
    if (currentStep.answerKind === 'short_text') {
      canProceed = input.trim().length > 0;
      answerValue = input.trim();
    } else if (currentStep.answerKind === 'chips_single') {
      if (currentStep.usesChannelChips) {
        // For channel chips, also check if "other" has text when selected
        if (onboardingState.sellingContext.mainChannel === 'other') {
          canProceed = !!onboardingState.sellingContext.mainChannelOtherText?.trim();
        } else {
          canProceed = !!onboardingState.sellingContext.mainChannel;
        }
        answerValue = onboardingState.sellingContext.mainChannel;
      } else if (currentStep.id === 'yearly_volume') {
        canProceed = !!onboardingState.yearlyVolumePlan;
        answerValue = onboardingState.yearlyVolumePlan;
      } else if (currentStep.id === 'timeline') {
        canProceed = !!onboardingState.timelinePlan;
        answerValue = onboardingState.timelinePlan;
      }
    } else if (currentStep.answerKind === 'chips_multi') {
      // For market chips, check if "other" has text when selected
      if (onboardingState.sellingContext.targetMarkets.includes('other')) {
        canProceed = onboardingState.sellingContext.targetMarkets.length > 0 && 
                     !!onboardingState.sellingContext.targetMarketsOtherText?.trim();
      } else {
        canProceed = onboardingState.sellingContext.targetMarkets.length > 0;
      }
      answerValue = onboardingState.sellingContext.targetMarkets;
    }

    if (!canProceed) return;

    // Save answer to state
    if (currentStep.id === 'project_name') {
      setOnboardingState(prev => ({ ...prev, projectName: answerValue }));
    } else if (currentStep.id === 'main_channel') {
      // Channel is already saved via ChannelChips onChange
    } else if (currentStep.id === 'target_markets') {
      // Markets are already saved via MarketChips onChange
    } else if (currentStep.id === 'yearly_volume') {
      setOnboardingState(prev => ({ ...prev, yearlyVolumePlan: answerValue as YearlyVolumePlan }));
    } else if (currentStep.id === 'timeline') {
      setOnboardingState(prev => ({ ...prev, timelinePlan: answerValue as TimelinePlan }));
    }

    // Add user message to chat
    let userMessageContent = '';
    if (currentStep.answerKind === 'short_text') {
      userMessageContent = answerValue;
    } else if (currentStep.usesChannelChips) {
      userMessageContent = onboardingState.sellingContext.mainChannel === 'other' && onboardingState.sellingContext.mainChannelOtherText
        ? `Other (${onboardingState.sellingContext.mainChannelOtherText})`
        : answerValue || '';
    } else if (currentStep.usesMarketChips) {
      userMessageContent = answerValue.join(', ');
    } else if (currentStep.id === 'yearly_volume') {
      userMessageContent = YEARLY_VOLUME_OPTIONS.find(opt => opt.value === answerValue)?.label || '';
    } else if (currentStep.id === 'timeline') {
      userMessageContent = TIMELINE_OPTIONS.find(opt => opt.value === answerValue)?.label || '';
    }

    setMessages(prev => [...prev, {
      id: `user-${currentStep.id}-${Date.now()}`,
      role: 'user',
      content: userMessageContent,
    }]);

    // Clear input
    setInput('');

    // Advance to next step
    // This is where the conversation flow advances based on the config
    const nextStep = getNextStep(currentStep.id);
    if (nextStep) {
      setCurrentStepId(nextStep.id);
      // Add Nexi's next question message
      setMessages(prev => [...prev, {
        id: `assistant-${nextStep.id}-${Date.now()}`,
        role: 'assistant',
        content: nextStep.nexMessage,
      }]);
    } else {
      // Conversation complete - all steps from config are done
      setCurrentStepId(null);
      setMessages(prev => [...prev, {
        id: 'complete',
        role: 'assistant',
        content: (
          <div className="space-y-4">
            <div>
              <p className="mb-2">All done! 🎉</p>
              <p>We've collected all the information. You can now start analyzing your project.</p>
            </div>
            <Button
              onClick={() => router.push('/analyze/chat')}
              className="w-full sm:w-auto"
            >
              Start analysis for this project
            </Button>
          </div>
        ),
      }]);
    }
  };

  // Render input component based on current step
  const renderStepInput = () => {
    if (!currentStep) return null;

    if (currentStep.answerKind === 'short_text') {
      return (
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your answer..."
            className="flex-1 h-12 px-4 rounded-lg bg-surface border border-subtle-border text-foreground placeholder-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey && isCurrentStepComplete(currentStep, onboardingState, input)) {
                e.preventDefault();
                handleNext();
              }
            }}
          />
          <Button
            onClick={handleNext}
            disabled={!isCurrentStepComplete(currentStep, onboardingState, input)}
            className="h-12 px-6"
          >
            {getNextButtonLabel(currentStep)}
          </Button>
        </div>
      );
    }

    if (currentStep.usesChannelChips) {
      return (
        <div className="space-y-3">
          <ChannelChips
            value={onboardingState.sellingContext.mainChannel}
            otherText={onboardingState.sellingContext.mainChannelOtherText}
            onChange={(channel, otherText) => {
              setOnboardingState(prev => ({
                ...prev,
                sellingContext: {
                  ...prev.sellingContext,
                  mainChannel: channel,
                  mainChannelOtherText: otherText,
                },
              }));
            }}
          />
          <Button
            onClick={handleNext}
            disabled={!isCurrentStepComplete(currentStep, onboardingState, input)}
            className="w-full sm:w-auto"
          >
            {getNextButtonLabel(currentStep)}
          </Button>
        </div>
      );
    }

    if (currentStep.usesMarketChips) {
      return (
        <div className="space-y-3">
          <MarketChips
            selectedMarkets={onboardingState.sellingContext.targetMarkets}
            otherText={onboardingState.sellingContext.targetMarketsOtherText}
            onChange={(markets, otherText) => {
              setOnboardingState(prev => ({
                ...prev,
                sellingContext: {
                  ...prev.sellingContext,
                  targetMarkets: markets,
                  targetMarketsOtherText: otherText,
                },
              }));
            }}
          />
          <Button
            onClick={handleNext}
            disabled={!isCurrentStepComplete(currentStep, onboardingState, input)}
            className="w-full sm:w-auto"
          >
            {getNextButtonLabel(currentStep)}
          </Button>
        </div>
      );
    }

    if (currentStep.id === 'yearly_volume') {
      return (
        <div className="space-y-3">
          <GenericChipGroup
            options={YEARLY_VOLUME_OPTIONS}
            value={onboardingState.yearlyVolumePlan}
            onChange={(value) => {
              setOnboardingState(prev => ({
                ...prev,
                yearlyVolumePlan: value as YearlyVolumePlan,
              }));
            }}
          />
          <Button
            onClick={handleNext}
            disabled={!isCurrentStepComplete(currentStep, onboardingState, input)}
            className="w-full sm:w-auto"
          >
            {getNextButtonLabel(currentStep)}
          </Button>
        </div>
      );
    }

    if (currentStep.id === 'timeline') {
      return (
        <div className="space-y-3">
          <GenericChipGroup
            options={TIMELINE_OPTIONS}
            value={onboardingState.timelinePlan}
            onChange={(value) => {
              setOnboardingState(prev => ({
                ...prev,
                timelinePlan: value as TimelinePlan,
              }));
            }}
          />
          <Button
            onClick={handleNext}
            disabled={!isCurrentStepComplete(currentStep, onboardingState, input)}
            className="w-full sm:w-auto"
          >
            {getNextButtonLabel(currentStep)}
          </Button>
        </div>
      );
    }

    return null;
  };

  const progress = currentStep ? `${currentStep.order} / ${onboardingSteps.length}` : 'Complete';

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <header className="border-b border-subtle-border px-4 sm:px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold">NexSupply</h1>
          <div className="hidden sm:flex items-center gap-2 text-sm text-muted-foreground">
            <span>•</span>
            <span>{onboardingState.projectName || 'Untitled project'}</span>
            <span>•</span>
            <span>Collecting info ({progress})</span>
          </div>
        </div>
        <div className="text-xs text-muted-foreground">
          Chatting with Nexi
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Main Chat Area */}
        <main className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
            {/* Step Progress Indicator */}
            {currentStepIndex >= 0 ? (
              <div className="text-xs text-muted-foreground mb-2">
                Step {currentStepIndex + 1} of {totalSteps}
              </div>
            ) : currentStepIndex === -1 && !currentStep ? (
              <div className="text-xs text-muted-foreground mb-2">
                Onboarding complete
              </div>
            ) : null}

            {messages.map((message, index) => {
              // Find the step that corresponds to this assistant message
              const stepForMessage = message.role === 'assistant' && message.id.startsWith('assistant-')
                ? getStepById(message.id.split('-')[1])
                : null;

              return (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] sm:max-w-lg rounded-lg px-4 py-3 ${
                      message.role === 'user'
                        ? 'bg-primary text-black'
                        : 'bg-surface border border-subtle-border text-foreground'
                    }`}
                  >
                    {typeof message.content === 'string' ? (
                      <p className="whitespace-pre-wrap break-words text-sm leading-relaxed">
                        {message.content}
                      </p>
                    ) : (
                      <div className="text-sm leading-relaxed">
                        {message.content}
                      </div>
                    )}
                    {/* Show helper text for assistant messages */}
                    {stepForMessage && stepForMessage.helperText && (
                      <p className="text-xs text-muted-foreground mt-2">{stepForMessage.helperText}</p>
                    )}
                  </div>
                </div>
              );
            })}

            {/* Current step input */}
            {currentStep && (
              <div className="flex justify-start">
                <div className="max-w-[85%] sm:max-w-lg w-full">
                  {renderStepInput()}
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </main>

        {/* Right Side Summary Panel */}
        <aside className="hidden lg:block w-80 border-l border-subtle-border overflow-y-auto">
          <OnboardingSummaryCard onboardingState={onboardingState} />
        </aside>
      </div>
    </div>
  );
}
