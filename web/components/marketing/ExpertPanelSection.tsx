'use client';

import Image from 'next/image';
import { urlFor } from '@/lib/sanity/image';
import { useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

type Expert = {
  name: string;
  role: string;
  bio: string;
  organizations?: string[];
  photo?: any;
};

type Props = {
  panel?: {
    title?: string;
    subtitle?: string;
    experts?: Expert[];
  };
};

export default function ExpertPanelSection({ panel }: Props) {
  const trackRef = useRef<HTMLDivElement>(null);

  if (!panel || !panel.experts || panel.experts.length === 0) return null;

  const { title, subtitle, experts } = panel;

  const scrollBy = (direction: 'left' | 'right') => {
    if (trackRef.current) {
      const card = trackRef.current.querySelector('article');
      if (card) {
        const cardWidth = card.offsetWidth;
        const scrollAmount = (cardWidth + 24) * (direction === 'left' ? -1 : 1); // card width + gap
        trackRef.current.scrollBy({
          left: scrollAmount,
          behavior: 'smooth',
        });
      }
    }
  };

  return (
    <section className="bg-white py-16 sm:py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 lg:gap-16">
          {/* Left column */}
          <div className="lg:col-span-1 mb-12 lg:mb-0">
            <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-neutral-900">
              {title ?? 'Global sourcing crafted by real operators'}
            </h2>
            {subtitle && (
              <p className="mt-4 text-base text-neutral-600 leading-relaxed">
                {subtitle}
              </p>
            )}
          </div>

          {/* Right: cards carousel */}
          <div className="lg:col-span-2 relative">
            <div
              ref={trackRef}
              className="flex overflow-x-auto snap-x snap-mandatory scrollbar-hide space-x-6 pb-4"
            >
              {experts.map((expert) => (
                <article
                  key={expert.name}
                  className="snap-start flex-shrink-0 w-[85vw] sm:w-[360px] bg-[#F9F4EC] rounded-3xl shadow-md overflow-hidden"
                >
                  <div className="relative h-64 sm:h-72 w-full">
                    {expert.photo && (
                      <Image
                        src={urlFor(expert.photo).width(460).height(520).url()}
                        alt={expert.name}
                        fill
                        className="object-cover"
                        sizes="(min-width: 640px) 360px, 85vw"
                      />
                    )}
                  </div>
                  <div className="p-6">
                    <h3 className="font-bold text-neutral-900 text-lg">{expert.name}</h3>
                    <p className="text-sm font-medium text-neutral-700 mt-1">{expert.role}</p>
                    <p className="text-sm text-neutral-600 mt-3 leading-relaxed">{expert.bio}</p>

                    {expert.organizations && expert.organizations.length > 0 && (
                      <div className="mt-4 flex flex-wrap gap-2">
                        {expert.organizations.map((org) => (
                          <span
                            key={org}
                            className="inline-block px-3 py-1 text-xs font-medium text-neutral-600 bg-white rounded-full border border-neutral-200"
                          >
                            {org}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </article>
              ))}
            </div>
            <div className="hidden sm:flex absolute -bottom-4 right-0 lg:-top-4 lg:bottom-auto items-center gap-2">
              <button
                type="button"
                aria-label="Previous expert"
                onClick={() => scrollBy('left')}
                className="w-10 h-10 rounded-full bg-white border border-neutral-200 flex items-center justify-center text-neutral-600 hover:bg-neutral-100 transition-colors disabled:opacity-50"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <button
                type="button"
                aria-label="Next expert"
                onClick={() => scrollBy('right')}
                className="w-10 h-10 rounded-full bg-white border border-neutral-200 flex items-center justify-center text-neutral-600 hover:bg-neutral-100 transition-colors disabled:opacity-50"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}