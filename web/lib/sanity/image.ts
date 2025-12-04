import { createImageUrlBuilder } from '@sanity/image-url';
import type { SanityImageSource } from '@sanity/image-url';
import { sanityClient } from './client';

// Image URL builder
const builder = createImageUrlBuilder(sanityClient);

export function urlFor(source: SanityImageSource) {
  if (!source) {
    return {
      width: () => ({ height: () => ({ url: () => '' }) }),
      height: () => ({ width: () => ({ url: () => '' }) }),
      url: () => '',
    };
  }
  return builder.image(source);
}

