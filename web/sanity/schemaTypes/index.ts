import { type SchemaTypeDefinition } from 'sanity'

// Import schemas from the root sanity folder
import siteSettings from '../../../sanity/schemas/siteSettings'
import homePage from '../../../sanity/schemas/homePage'
import howItWorksPage from '../../../sanity/schemas/howItWorksPage'
import useCasesPage from '../../../sanity/schemas/useCasesPage'
import testimonial from '../../../sanity/schemas/testimonial'
import faq from '../../../sanity/schemas/faq'
import useCase from '../../../sanity/schemas/useCase'

export const schema: { types: SchemaTypeDefinition[] } = {
  types: [
    siteSettings,
    homePage,
    howItWorksPage,
    useCasesPage,
    testimonial,
    faq,
    useCase,
  ],
}
