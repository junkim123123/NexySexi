/**
 * OnboardingSummaryCard Component
 * 
 * Displays the current onboarding state in a summary card format.
 * Shows all collected information with human-readable labels.
 */

'use client';

import { Card } from '@/components/ui/card';
import type { OnboardingState } from '@/lib/types/onboarding';
import { getChannelLabel, getMarketLabel, getVolumePlanLabel, getTimelinePlanLabel } from '@/lib/types/onboarding';

interface OnboardingSummaryCardProps {
  onboardingState: OnboardingState;
}

export function OnboardingSummaryCard({ onboardingState }: OnboardingSummaryCardProps) {
  const getChannelDisplay = () => {
    if (!onboardingState.sellingContext.mainChannel) {
      return <span className="text-muted-foreground">Not set yet</span>;
    }
    
    if (onboardingState.sellingContext.mainChannel === 'other') {
      const otherText = onboardingState.sellingContext.mainChannelOtherText;
      return otherText ? `Other (${otherText})` : 'Other';
    }
    
    return getChannelLabel(onboardingState.sellingContext.mainChannel);
  };

  const getMarketsDisplay = () => {
    const markets = onboardingState.sellingContext.targetMarkets;
    if (markets.length === 0) {
      return <span className="text-muted-foreground">Not set yet</span>;
    }

    const labels = markets.map(market => {
      if (market === 'other') {
        const otherText = onboardingState.sellingContext.targetMarketsOtherText;
        return otherText ? `Other (${otherText})` : 'Other';
      }
      return getMarketLabel(market);
    });

    return labels.join(', ');
  };

  const getVolumeDisplay = () => {
    if (!onboardingState.yearlyVolumePlan) {
      return <span className="text-muted-foreground">Not set yet</span>;
    }
    return getVolumePlanLabel(onboardingState.yearlyVolumePlan);
  };

  const getTimelineDisplay = () => {
    if (!onboardingState.timelinePlan) {
      return <span className="text-muted-foreground">Not set yet</span>;
    }
    return getTimelinePlanLabel(onboardingState.timelinePlan);
  };

  return (
    <div className="p-4 sm:p-6 space-y-4">
      <h2 className="text-lg font-semibold mb-4">Project Summary</h2>

      <Card className="p-4">
        <h3 className="text-sm font-semibold mb-3 text-foreground">Current Status</h3>
        <div className="space-y-2 text-sm text-muted-foreground">
          <p>• Collecting information</p>
          <p>• Waiting for analysis</p>
        </div>
      </Card>

      <Card className="p-4">
        <h3 className="text-sm font-semibold mb-3 text-foreground">Collected Information</h3>
        <div className="space-y-3 text-sm">
          <div>
            <div className="text-muted-foreground mb-1">Project</div>
            <div className="text-foreground font-medium">
              {onboardingState.projectName || <span className="text-muted-foreground">Not set yet</span>}
            </div>
          </div>

          <div>
            <div className="text-muted-foreground mb-1">Channel</div>
            <div className="text-foreground font-medium">{getChannelDisplay()}</div>
          </div>

          <div>
            <div className="text-muted-foreground mb-1">Markets</div>
            <div className="text-foreground font-medium">{getMarketsDisplay()}</div>
          </div>

          <div>
            <div className="text-muted-foreground mb-1">Volume plan</div>
            <div className="text-foreground font-medium">{getVolumeDisplay()}</div>
          </div>

          <div>
            <div className="text-muted-foreground mb-1">Timeline</div>
            <div className="text-foreground font-medium">{getTimelineDisplay()}</div>
          </div>
        </div>
      </Card>

      <Card className="p-4">
        <h3 className="text-sm font-semibold mb-3 text-foreground">Estimated DDP Range</h3>
        <p className="text-sm text-muted-foreground">
          Will be displayed after analysis is complete
        </p>
      </Card>
    </div>
  );
}

