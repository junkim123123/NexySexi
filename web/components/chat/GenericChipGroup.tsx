/**
 * GenericChipGroup Component
 * 
 * A reusable chip group for single-select options like yearly volume and timeline.
 * Used when we don't need the specialized ChannelChips or MarketChips components.
 */

'use client';

interface ChipOption {
  value: string;
  label: string;
}

interface GenericChipGroupProps {
  options: ChipOption[];
  value?: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function GenericChipGroup({ options, value, onChange, disabled = false }: GenericChipGroupProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((option) => {
        const isSelected = value === option.value;
        return (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            disabled={disabled}
            className={`px-4 py-2 rounded-lg border text-sm font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed ${
              isSelected
                ? 'border-primary bg-primary/10 text-foreground'
                : 'border-subtle-border bg-surface hover:border-primary/50 hover:bg-surface/80 text-foreground'
            }`}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}

