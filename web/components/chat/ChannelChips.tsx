/**
 * ChannelChips Component
 * 
 * Single-select chip group for selecting the main selling channel.
 * Includes an "Other" option that shows an inline text input when selected.
 * 
 * When "Other" is selected:
 * - mainChannel is set to "other"
 * - mainChannelOtherText stores the free text input
 */

'use client';

import { useState } from 'react';
import type { ChannelOption } from '@/lib/types/onboarding';
import { getChannelLabel } from '@/lib/types/onboarding';

interface ChannelChipsProps {
  value?: ChannelOption;
  otherText?: string;
  onChange: (channel: ChannelOption, otherText?: string) => void;
  disabled?: boolean;
}

const CHANNEL_OPTIONS: ChannelOption[] = [
  'amazon_fba',
  'shopify_dtc',
  'tiktok_shop',
  'retail_wholesale',
  'b2b_distributor',
  'not_sure',
  'other',
];

export function ChannelChips({ value, otherText = '', onChange, disabled = false }: ChannelChipsProps) {
  const [showOtherInput, setShowOtherInput] = useState(value === 'other');

  const handleChipClick = (option: ChannelOption) => {
    if (disabled) return;

    if (option === 'other') {
      // Show input when "Other" is selected
      setShowOtherInput(true);
      onChange('other', otherText || '');
    } else {
      // Clear other input when switching to predefined option
      setShowOtherInput(false);
      onChange(option);
    }
  };

  const handleOtherTextChange = (text: string) => {
    // Store the free text separately from the option enum
    onChange('other', text);
  };

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        {CHANNEL_OPTIONS.map((option) => {
          const isSelected = value === option;
          const isOther = option === 'other';

          return (
            <button
              key={option}
              type="button"
              onClick={() => handleChipClick(option)}
              disabled={disabled}
              className={`px-4 py-2 rounded-lg border text-sm font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed ${
                isSelected
                  ? 'border-primary bg-primary/10 text-foreground'
                  : 'border-subtle-border bg-surface hover:border-primary/50 hover:bg-surface/80 text-foreground'
              }`}
            >
              {getChannelLabel(option)}
              {isOther && '...'}
            </button>
          );
        })}
      </div>

      {/* Inline text input shown when "Other" is selected */}
      {showOtherInput && value === 'other' && (
        <div className="mt-2">
          <input
            type="text"
            value={otherText || ''}
            onChange={(e) => handleOtherTextChange(e.target.value)}
            placeholder="Enter your main channel, for example Walmart marketplace or Faire"
            disabled={disabled}
            className="w-full px-4 py-2 rounded-lg bg-surface border border-subtle-border text-foreground placeholder-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            autoFocus
          />
        </div>
      )}
    </div>
  );
}

