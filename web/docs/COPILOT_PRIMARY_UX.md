# Copilot Primary UX Implementation

## Overview

NexSupply has been redesigned to prioritize the **Conversational Copilot** as the primary user experience. The single-line analyzer is now a secondary, advanced option.

## Changes Summary

### 1. Landing Page Emphasis

**Location**: `web/app/(sections)/product-analyzer.tsx`

- **Main CTA**: Large, prominent "Describe Product with a Conversation" button that links to `/copilot`
- **Secondary Option**: Quick analyzer input is hidden by default and can be revealed via a small text link: "I already know exactly what I want - use quick input"
- **Visual Hierarchy**: Copilot button uses primary styling with gradient background; quick input is minimal and secondary

### 2. Conversation Entry Flow

**Location**: `web/app/copilot/page.tsx`

- **Direct Navigation**: Users clicking "Describe Product with a Conversation" are taken directly to `/copilot`
- **Header Clarification**: Copilot header now states "I'll ask 3-5 short questions about your product, then generate a comprehensive landed cost and risk report"
- **Quick Replies**: Initial welcome message includes category selection buttons and suggested questions

### 3. End of Flow Contract CTA

**Location**: `web/components/copilot/ContractCTACard.tsx`

After a successful analysis, a CTA card is automatically appended to the chat:

- **Title**: "Ready to turn this into a real sourcing project?"
- **Body**: Explains that NexSupply can handle factory search, negotiation, testing, QC, and logistics
- **Primary Button**: "Book a sourcing call" → Uses `NEXT_PUBLIC_BOOKING_URL`
- **Secondary Button**: "Request a full quote and contract" → Uses `NEXT_PUBLIC_CONTRACT_URL`

**Environment Variables**:
- `NEXT_PUBLIC_BOOKING_URL`: Required for primary button
- `NEXT_PUBLIC_CONTRACT_URL`: Optional - if missing, secondary button is hidden

### 4. Code Structure

#### New Components

- **`QuickAnalyzerInput`**: `web/components/analyzer/QuickAnalyzerInput.tsx`
  - Compact, secondary input component for quick analysis
  - Extracted from main analyzer for reuse

- **`ContractCTACard`**: `web/components/copilot/ContractCTACard.tsx`
  - CTA card displayed after analysis completion
  - Handles booking and contract URL buttons

#### Updated Components

- **`ProductAnalyzer`**: Restructured to emphasize Copilot entry
- **`CopilotPage`**: Updated header text and integrated CTA card display

## User Flow

### New User Journey

1. **Landing Page**
   - User sees prominent Copilot CTA button
   - Can optionally reveal quick input if needed

2. **Copilot Entry**
   - User clicks "Describe Product with a Conversation"
   - Redirected to `/copilot` page
   - Sees welcome message with quick reply options

3. **Analysis Flow**
   - User selects category or types product description
   - Receives triple-step response:
     - Summary message (2-4 lines)
     - Full analysis card
     - Follow-up question
   - After analysis: Contract CTA card appears

4. **Contract CTA**
   - User can book a call or request a quote
   - Actions are logged for analytics

### Returning User Journey

- Can still use quick input if preferred
- Copilot remains the primary, recommended flow

## Analytics Integration

All actions are logged:

- `copilot_viewed`: User visits copilot page
- `copilot_analysis_completed`: Analysis succeeds with hints/flags
- `cta_booking_click`: User clicks booking button
- `cta_contract_click`: User clicks contract button

Category usage is automatically logged via existing `logCategoryUsage()` function.

## Environment Variables

### Required

- `NEXT_PUBLIC_BOOKING_URL`: Calendar/booking page URL for sourcing calls

### Optional

- `NEXT_PUBLIC_CONTRACT_URL`: Quote/contract request page URL
  - If not set, the secondary button is automatically hidden

## Testing Checklist

- [ ] Anonymous user lands on page and sees Copilot CTA prominently
- [ ] Copilot CTA navigates to `/copilot` correctly
- [ ] Quick input is hidden by default
- [ ] Quick input can be revealed via link
- [ ] Analysis completes successfully in Copilot
- [ ] Contract CTA card appears after analysis
- [ ] Booking button works (if URL set)
- [ ] Contract button works (if URL set)
- [ ] Contract button hides when URL not set
- [ ] Usage limits still work correctly
- [ ] LimitReachedCard appears in chat when quota exceeded

## Migration Notes

- Existing quick analyzer functionality is preserved
- All backend APIs remain unchanged
- Analytics and logging continue to work as before
- Quick Scan UI is still available but de-emphasized

