/**
 * MarketChips Component
 * 
 * Multi-select chip group for selecting target markets.
 * Includes an "Other" option that shows an inline text input when selected.
 * 
 * When "Other" is selected:
 * - "other" is added to the targetMarkets array
 * - targetMarketsOtherText stores the free text input
 */

'use client';

import { useState } from 'react';
import type { MarketOption } from '@/lib/types/onboarding';
import { getMarketLabel } from '@/lib/types/onboarding';

interface MarketChipsProps {
  selectedMarkets: MarketOption[];
  otherText?: string;
  onChange: (markets: MarketOption[], otherText?: string) => void;
  disabled?: boolean;
}

// Group markets by region for better visual organization
const MARKET_GROUPS = [
  {
    label: 'North America and Europe',
    options: ['united_states', 'canada', 'mexico', 'europe', 'united_kingdom'] as MarketOption[],
  },
  {
    label: 'Asia',
    options: [
      'japan',
      'south_korea',
      'taiwan',
      'china_mainland',
      'hong_kong',
      'philippines',
      'southeast_asia',
    ] as MarketOption[],
  },
  {
    label: 'Other regions',
    options: [
      'middle_east_gulf',
      'australia_new_zealand',
      'latin_america',
      'multiple',
      'not_decided',
      'other',
    ] as MarketOption[],
  },
];

export function MarketChips({
  selectedMarkets,
  otherText = '',
  onChange,
  disabled = false,
}: MarketChipsProps) {
  const [showOtherInput, setShowOtherInput] = useState(selectedMarkets.includes('other'));

  const handleChipClick = (option: MarketOption) => {
    if (disabled) return;

    const isSelected = selectedMarkets.includes(option);

    if (option === 'other') {
      if (isSelected) {
        // Unselecting "Other" - remove from array and clear text
        const newMarkets = selectedMarkets.filter((m) => m !== 'other');
        setShowOtherInput(false);
        onChange(newMarkets);
      } else {
        // Selecting "Other" - add to array and show input
        const newMarkets = [...selectedMarkets, 'other'];
        setShowOtherInput(true);
        onChange(newMarkets, otherText || '');
      }
    } else {
      // Toggle regular market option
      const newMarkets = isSelected
        ? selectedMarkets.filter((m) => m !== option)
        : [...selectedMarkets, option];
      
      // Keep other input state in sync
      const hasOther = newMarkets.includes('other');
      setShowOtherInput(hasOther);
      
      onChange(newMarkets, hasOther ? otherText : undefined);
    }
  };

  const handleOtherTextChange = (text: string) => {
    // Store the free text separately, only if "other" is in the selected markets
    if (selectedMarkets.includes('other')) {
      onChange(selectedMarkets, text);
    }
  };

  return (
    <div className="space-y-4">
      <p className="text-xs text-muted-foreground">You can select more than one</p>

      <div className="space-y-4">
        {MARKET_GROUPS.map((group) => (
          <div key={group.label} className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
              {group.label}
            </p>
            <div className="flex flex-wrap gap-2">
              {group.options.map((option) => {
                const isSelected = selectedMarkets.includes(option);
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
                    {getMarketLabel(option)}
                    {isOther && '...'}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Inline text input shown when "Other" is selected */}
      {showOtherInput && selectedMarkets.includes('other') && (
        <div className="mt-2">
          <input
            type="text"
            value={otherText || ''}
            onChange={(e) => handleOtherTextChange(e.target.value)}
            placeholder="Enter market, for example Brazil or South Africa"
            disabled={disabled}
            className="w-full px-4 py-2 rounded-lg bg-surface border border-subtle-border text-foreground placeholder-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            autoFocus
          />
        </div>
      )}
    </div>
  );
}

