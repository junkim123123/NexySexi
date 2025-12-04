/**
 * ProductAnalysisCard
 * 
 * A reusable, presentational component for displaying product analysis results.
 * Can be rendered in both chat and non-chat contexts.
 * 
 * This is now the primary way to display analysis results in NexSupply.
 * Previously embedded in Quick Scan, now extracted for reuse in chat-first UX.
 */

'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import type { ProductAnalysis } from '@/lib/product-analysis/schema';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CategoryKnowledgeCards } from '@/components/category-knowledge-cards';
import { AdvancedAnalysisView } from '@/components/AdvancedAnalysisView';
import { ChevronDown, ChevronUp, BarChart3 } from 'lucide-react';

interface ProductAnalysisCardProps {
  analysis: ProductAnalysis;
  className?: string;
}

/**
 * Get color for risk score
 */
function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600 dark:text-green-400';
  if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
  return 'text-red-600 dark:text-red-400';
}

/**
 * Get color for risk level
 */
function getRiskColor(risk: string): string {
  if (risk === 'Low') return 'text-green-600 dark:text-green-400';
  if (risk === 'Medium') return 'text-yellow-600 dark:text-yellow-400';
  return 'text-red-600 dark:text-red-400';
}

export function ProductAnalysisCard({ analysis, className = '' }: ProductAnalysisCardProps) {
  const [showAdvanced, setShowAdvanced] = useState(false);
  const riskLevel = analysis.risk_assessment.overall_score >= 80 ? 'Low' : 
                    analysis.risk_assessment.overall_score >= 60 ? 'Medium' : 'High';

  const hasAdvancedData = 
    analysis.estimate_confidence !== undefined ||
    (analysis.assumptions && analysis.assumptions.length > 0) ||
    (analysis.missing_info && analysis.missing_info.length > 0) ||
    (analysis.regulation_reasoning && analysis.regulation_reasoning.length > 0) ||
    (analysis.testing_cost_estimate && analysis.testing_cost_estimate.length > 0) ||
    analysis.initial_order_cost;

  return (
    <div className={`space-y-6 ${className}`}>
      <Card>
        {/* Key Metrics Header - Most Important Info First */}
        <div className="mb-6 pb-6 border-b border-subtle-border">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div className="flex-1">
              <h3 className="card-title mb-2">{analysis.product_name}</h3>
              <p className="card-subtitle mb-4">Est. HTS Code: {analysis.hts_code}</p>
              <div className="flex flex-wrap gap-4">
                <div>
                  <p className="text-xs text-muted-foreground mb-1">Total Landed Cost</p>
                  <p className="text-2xl sm:text-3xl font-bold text-primary">{analysis.landed_cost_breakdown.landed_cost}</p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground mb-1">Overall Risk</p>
                  <div className="flex items-baseline gap-2">
                    <p className={`text-xl sm:text-2xl font-bold ${getRiskColor(riskLevel)}`}>
                      {riskLevel}
                    </p>
                    <span className={`text-sm font-semibold ${getScoreColor(analysis.risk_assessment.overall_score)}`}>
                      ({analysis.risk_assessment.overall_score}/100)
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Landed Cost Breakdown */}
        <div className="mb-6 pb-6 border-b border-subtle-border">
          <h4 className="text-lg font-semibold mb-4">Cost Breakdown</h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-muted-foreground mb-1">FOB Price</p>
              <p className="text-lg font-semibold">{analysis.landed_cost_breakdown.fob_price}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Freight</p>
              <p className="text-lg font-semibold">{analysis.landed_cost_breakdown.freight_cost}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Duty ({analysis.landed_cost_breakdown.duty_rate})</p>
              <p className="text-lg font-semibold">{analysis.landed_cost_breakdown.duty_cost}</p>
            </div>
            <div className="col-span-2 sm:col-span-1">
              <p className="text-xs text-muted-foreground mb-1">Total</p>
              <p className="text-lg font-bold text-primary">{analysis.landed_cost_breakdown.landed_cost}</p>
            </div>
          </div>
        </div>

        {/* Risk Assessment */}
        <div className="mb-6 pb-6 border-b border-subtle-border">
          <h4 className="text-lg font-semibold mb-4">Risk Assessment</h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
            <div>
              <p className="text-xs text-muted-foreground mb-1">Compliance Risk</p>
              <p className={`text-base font-semibold ${getRiskColor(analysis.risk_assessment.compliance_risk)}`}>
                {analysis.risk_assessment.compliance_risk}
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Supplier Risk</p>
              <p className={`text-base font-semibold ${getRiskColor(analysis.risk_assessment.supplier_risk)}`}>
                {analysis.risk_assessment.supplier_risk}
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Logistics Risk</p>
              <p className={`text-base font-semibold ${getRiskColor(analysis.risk_assessment.logistics_risk)}`}>
                {analysis.risk_assessment.logistics_risk}
              </p>
            </div>
          </div>
          <div>
            <p className="text-xs text-muted-foreground mb-2">Risk Summary</p>
            <p className="text-sm text-foreground leading-relaxed">{analysis.risk_assessment.summary}</p>
          </div>
        </div>

        {/* Recommendation */}
        <div>
          <h4 className="text-lg font-semibold mb-2">Recommendation</h4>
          <p className="text-sm text-foreground leading-relaxed">{analysis.recommendation}</p>
        </div>

        {/* Advanced View Toggle */}
        {hasAdvancedData && (
          <div className="mt-6 pt-6 border-t border-subtle-border">
            <Button
              variant="outline"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="w-full sm:w-auto"
            >
              <BarChart3 className="h-4 w-4 mr-2" />
              {showAdvanced ? 'Hide' : 'Show'} Advanced Analysis
              {showAdvanced ? (
                <ChevronUp className="h-4 w-4 ml-2" />
              ) : (
                <ChevronDown className="h-4 w-4 ml-2" />
              )}
            </Button>
          </div>
        )}
      </Card>

      {/* Advanced Analysis View */}
      {hasAdvancedData && (
        <motion.div
          initial={false}
          animate={{ height: showAdvanced ? 'auto' : 0, opacity: showAdvanced ? 1 : 0 }}
          transition={{ duration: 0.2 }}
          className="overflow-hidden"
        >
          {showAdvanced && <AdvancedAnalysisView analysis={analysis} />}
        </motion.div>
      )}

      {/* Category Knowledge Cards (compliance hints, factory vetting, etc.) */}
      <CategoryKnowledgeCards analysis={analysis} />
    </div>
  );
}

