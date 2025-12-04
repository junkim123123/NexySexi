export interface ProductIntake {
  // Project/Context
  projectName?: string;               // Onboarding projectName
  mainChannel?: string;              // e.g. "amazon_fba"
  destinationMarket?: string;        // e.g. "united_kingdom", "united_states"
  sourceCountry?: string;            // e.g. "south_korea", "china_mainland"

  // Product Description
  productName?: string;              // User's name for the product (q1 or separate field)
  category?: string;                 // "snacks", "toys", "not_sure" etc.
  oneLineDescription?: string;       // "one-line description + target retail price"
  productStage?: string;             // "existing", "testing", "new_idea" etc.

  // Trade Terms / Strategy
  tradeTerm?: string;                // "EXW" | "FOB" | "CIF" | "DDP" | "not_sure"
  speedVsCost?: string;              // "speed" | "balanced" | "cost"
  monthlyVolume?: number;            // Monthly volume from q10
  riskTolerance?: string;           // "low_risk", "balanced", "lowest_cost"

  // Other
  specialRequirements?: string;      // Certifications, packaging requirements, etc. (free text)
}