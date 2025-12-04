'use client';

import { useState, useRef } from 'react';
import { Loader2, ArrowRight, Camera } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface QuickAnalyzerInputProps {
  onSubmit: (input: string, image?: File) => Promise<void>;
  placeholder?: string;
  isLoading?: boolean;
  presets?: string[];
  onPresetClick?: (preset: string) => void;
}

/**
 * QuickAnalyzerInput
 * 
 * A compact, secondary input component for quick product analysis.
 * Designed to be less prominent than the main Copilot CTA.
 */
export function QuickAnalyzerInput({
  onSubmit,
  placeholder = "e.g. 'Noise-cancelling headphones' or AliExpress URL...",
  isLoading = false,
  presets = [],
  onPresetClick,
}: QuickAnalyzerInputProps) {
  const [input, setInput] = useState('');
  const [productImage, setProductImage] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() && !productImage) return;
    await onSubmit(input.trim(), productImage || undefined);
    setInput('');
    setProductImage(null);
  };

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setProductImage(file);
  };

  return (
    <div className="space-y-3">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={placeholder}
            className="w-full h-12 pl-12 pr-28 rounded-full bg-surface border border-subtle-border text-foreground placeholder-muted-foreground/50 focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
            disabled={isLoading}
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="absolute left-2 top-1/2 -translate-y-1/2 aspect-square h-8 w-8 flex items-center justify-center rounded-full bg-surface hover:bg-white/10 transition-colors text-muted-foreground"
          >
            <Camera className="h-4 w-4" />
          </button>
          <input
            type="file"
            ref={fileInputRef}
            accept="image/*"
            capture="environment"
            onChange={handleImageChange}
            className="hidden"
          />
          {productImage && (
            <div className="absolute left-12 top-1/2 -translate-y-1/2 text-xs text-muted-foreground bg-surface px-2 py-1 rounded-md border border-subtle-border">
              {productImage.name}
            </div>
          )}
          <Button
            type="submit"
            disabled={isLoading || !input.trim()}
            size="sm"
            variant="outline"
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full min-w-[80px] h-8 text-xs"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <>
                Analyze <ArrowRight className="ml-1 h-3 w-3" />
              </>
            )}
          </Button>
        </div>
      </form>

      {presets.length > 0 && (
        <div className="flex items-center justify-center gap-2 flex-wrap">
          {presets.map((preset) => (
            <Button
              key={preset}
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => {
                setInput(preset);
                onPresetClick?.(preset);
              }}
              className="text-xs h-7"
            >
              {preset}
            </Button>
          ))}
        </div>
      )}
    </div>
  );
}

