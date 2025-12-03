'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { logEvent } from '@/lib/analytics/telemetry';
import type { ProductAnalysis } from '@/lib/product-analysis/schema';

interface ProductAnalysisFeedbackProps {
  analysis: ProductAnalysis;
  mode: 'quick_scan' | 'conversational';
  source?: string;
}

export function ProductAnalysisFeedback({ analysis, mode, source }: ProductAnalysisFeedbackProps) {
  const [feedbackSent, setFeedbackSent] = useState(false);

  const handleFeedback = async (rating: 'up' | 'down') => {
    // Immediately disable buttons
    setFeedbackSent(true);

    const payload = {
      rating,
      mode,
      productSummary: analysis.product_name,
      leadSource: source,
    };

    // Fire and forget API call (non-blocking)
    fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).catch(error => {
      // Silently fail - don't bother the user
      console.error('Failed to send feedback:', error);
    });

    // Log event to telemetry (also fire-and-forget)
    logEvent('analysis_feedback', { rating, mode });
  };

  return (
    <div className="space-y-3 mt-4">
      {/* Alpha Disclaimer */}
      <div className="p-3 bg-surface/20 border border-subtle-border/30 rounded-lg text-xs text-muted-foreground/80">
        <p className="leading-relaxed">
          <strong className="text-foreground/60 font-medium">NexSupply is in early alpha.</strong> These estimates are directional only and not legal or tax advice. Always double-check critical numbers with your freight forwarder or customs broker.
        </p>
      </div>

      {/* Feedback Row */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-2 sm:gap-3">
        {feedbackSent ? (
          <p className="text-xs text-muted-foreground/70">Thanks for your feedback!</p>
        ) : (
          <>
            <p className="text-xs text-muted-foreground/70">Was this analysis helpful?</p>
            <div className="flex gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleFeedback('up')}
                aria-label="Helpful"
                className="h-7 px-2.5 text-xs"
              >
                👍 Yes
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleFeedback('down')}
                aria-label="Not helpful"
                className="h-7 px-2.5 text-xs"
              >
                👎 Not really
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}