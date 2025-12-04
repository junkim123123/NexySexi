/**
 * NexSupply AI Report v2 - Unified schema for Quick Snapshot and Full Report
 */

export type NexSupplyAIReportV2 = {
  meta: {
    version: "2.0";
    generatedAt: string; // ISO datetime
    currency: "USD";
    targetMarket: string; // e.g. "US Amazon FBA"
    confidenceLevel: "low" | "medium" | "high";
    overallSummary: string; // One or two sentence summary
  };

  productSummary: {
    title: string;
    shortDescription: string;
    category: string;
    exampleUseCases: string[];
  };

  costOverview: {
    ddpPerUnitRange: { low: number; high: number };
    ddpPerShipmentRange?: { low: number; high: number };
    mainCostDrivers: string[]; // Max 5
    keyAssumptions: string[]; // Max 6, specs, incoterm, volume assumptions
  };

  costBreakdown: {
    fobPerUnitRange?: { low: number; high: number };
    freightPerUnitRange?: { low: number; high: number };
    dutyPerUnitRange?: { low: number; high: number };
    extraPerUnitRange?: { low: number; high: number };
    notes?: string;
  };

  volumeScenarios?: {
    scenarioName: string; // e.g. "One box pilot"
    units: number | null;
    ddpPerUnitEstimate?: number | null;
    totalDdpEstimate?: number | null;
    comment?: string;
  }[];

  leadTimePlan?: {
    estimatedLeadTimeWeeksRange?: { low: number; high: number };
    criticalMilestones: string[]; // e.g. "Sample approval", "Carton test", "First shipment"
  };

  riskAnalysis: {
    overallRiskLevel: "low" | "medium" | "high";
    complianceRisks: string[];
    logisticsRisks: string[];
    commercialRisks: string[];
    otherRisks?: string[];
    mustCheckBeforeOrder: string[]; // Checklist before ordering
  };

  channelNotes?: {
    amazonFBA?: string[];
    dtcShopify?: string[];
    retailWholesale?: string[];
  };

  dataQuality: {
    priceDataSource: "public_ecommerce" | "reference_transactions" | "internal_assumption" | "mixed";
    freightDataSource: "csv_table" | "market_average" | "rough_assumption";
    dutyDataSource: "hts_lookup" | "benchmark_rate" | "rough_assumption";
    overallReliability: "rough" | "directional" | "good";
    caveats: string[];
  };

  recommendedNextSteps: {
    priority: "high" | "medium" | "low";
    label: string;
    detail: string;
  }[];
};

