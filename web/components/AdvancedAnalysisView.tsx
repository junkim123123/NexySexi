/**
 * AdvancedAnalysisView
 * 
 * A detailed view component for professional users (like Ethan) who need
 * deeper insights into the analysis methodology, assumptions, and data quality.
 * 
 * This component displays:
 * - Estimate confidence score and explanation
 * - Assumptions made during analysis
 * - Missing information that could improve accuracy
 * - Detailed regulation reasoning
 * - Testing cost breakdown
 * - Initial order cost breakdown
 */

'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { ProductAnalysis } from '@/lib/product-analysis/schema';
import { Card } from '@/components/ui/card';
import { ChevronDown, ChevronUp, AlertCircle, Info, CheckCircle2, XCircle } from 'lucide-react';

interface AdvancedAnalysisViewProps {
  analysis: ProductAnalysis;
}

/**
 * Get color for confidence score
 */
function getConfidenceColor(score: number): string {
  if (score >= 80) return 'text-green-600 dark:text-green-400';
  if (score >= 60) return 'text-yellow-600 dark:text-yellow-400';
  return 'text-red-600 dark:text-red-400';
}

/**
 * Get background color for confidence score
 */
function getConfidenceBgColor(score: number): string {
  if (score >= 80) return 'bg-green-500/10 border-green-500/20';
  if (score >= 60) return 'bg-yellow-500/10 border-yellow-500/20';
  return 'bg-red-500/10 border-red-500/20';
}

/**
 * Get confidence level label
 */
function getConfidenceLevel(score: number): string {
  if (score >= 80) return 'High';
  if (score >= 60) return 'Medium';
  return 'Low';
}

export function AdvancedAnalysisView({ analysis }: AdvancedAnalysisViewProps) {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev => {
      const next = new Set(prev);
      if (next.has(sectionId)) {
        next.delete(sectionId);
      } else {
        next.add(sectionId);
      }
      return next;
    });
  };

  const hasAdvancedData = 
    analysis.estimate_confidence !== undefined ||
    (analysis.assumptions && analysis.assumptions.length > 0) ||
    (analysis.missing_info && analysis.missing_info.length > 0) ||
    (analysis.regulation_reasoning && analysis.regulation_reasoning.length > 0) ||
    (analysis.testing_cost_estimate && analysis.testing_cost_estimate.length > 0) ||
    analysis.initial_order_cost;

  if (!hasAdvancedData) {
    return (
      <Card className="border-subtle-border">
        <div className="p-6 text-center">
          <Info className="h-8 w-8 mx-auto mb-3 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            No additional analysis details available for this product.
          </p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Estimate Confidence */}
      {analysis.estimate_confidence !== undefined && (
        <Card className={`border ${getConfidenceBgColor(analysis.estimate_confidence)}`}>
          <div className="p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${getConfidenceBgColor(analysis.estimate_confidence)}`}>
                  <Info className={`h-5 w-5 ${getConfidenceColor(analysis.estimate_confidence)}`} />
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-1">Analysis Confidence</h3>
                  <p className="text-sm text-muted-foreground">
                    How reliable is this estimate?
                  </p>
                </div>
              </div>
              <div className="text-right">
                <div className={`text-3xl font-bold ${getConfidenceColor(analysis.estimate_confidence)}`}>
                  {analysis.estimate_confidence}%
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  {getConfidenceLevel(analysis.estimate_confidence)} Confidence
                </div>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-subtle-border">
              <p className="text-sm text-foreground leading-relaxed">
                This confidence score reflects the quality and completeness of the input data, 
                category knowledge, and market conditions used in the analysis. Higher scores 
                indicate more reliable estimates based on established patterns and verified data.
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* Assumptions Made */}
      {analysis.assumptions && analysis.assumptions.length > 0 && (
        <Card>
          <button
            onClick={() => toggleSection('assumptions')}
            className="w-full p-6 flex items-center justify-between hover:bg-surface/50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-primary/10">
                <Info className="h-5 w-5 text-primary" />
              </div>
              <div className="text-left">
                <h3 className="text-lg font-semibold">Assumptions Made</h3>
                <p className="text-sm text-muted-foreground">
                  {analysis.assumptions.length} assumption{analysis.assumptions.length !== 1 ? 's' : ''} used in this analysis
                </p>
              </div>
            </div>
            {expandedSections.has('assumptions') ? (
              <ChevronUp className="h-5 w-5 text-muted-foreground" />
            ) : (
              <ChevronDown className="h-5 w-5 text-muted-foreground" />
            )}
          </button>
          <AnimatePresence>
            {expandedSections.has('assumptions') && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="px-6 pb-6 border-t border-subtle-border">
                  <ul className="mt-4 space-y-3">
                    {analysis.assumptions.map((assumption, index) => (
                      <li key={index} className="flex items-start gap-3">
                        <div className="mt-1 shrink-0">
                          <div className="w-2 h-2 rounded-full bg-primary/60" />
                        </div>
                        <p className="text-sm text-foreground leading-relaxed flex-1">{assumption}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </Card>
      )}

      {/* Missing Information */}
      {analysis.missing_info && analysis.missing_info.length > 0 && (
        <Card>
          <button
            onClick={() => toggleSection('missing_info')}
            className="w-full p-6 flex items-center justify-between hover:bg-surface/50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-yellow-500/10">
                <AlertCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
              </div>
              <div className="text-left">
                <h3 className="text-lg font-semibold">Missing Information</h3>
                <p className="text-sm text-muted-foreground">
                  {analysis.missing_info.length} piece{analysis.missing_info.length !== 1 ? 's' : ''} of information that could improve accuracy
                </p>
              </div>
            </div>
            {expandedSections.has('missing_info') ? (
              <ChevronUp className="h-5 w-5 text-muted-foreground" />
            ) : (
              <ChevronDown className="h-5 w-5 text-muted-foreground" />
            )}
          </button>
          <AnimatePresence>
            {expandedSections.has('missing_info') && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="px-6 pb-6 border-t border-subtle-border">
              <div className="mt-4 p-4 bg-yellow-500/5 border border-yellow-500/20 rounded-lg mb-4">
                <p className="text-sm text-foreground">
                  Providing this information would help us generate a more accurate analysis. 
                  You can update your product description or answer follow-up questions to improve the estimate.
                </p>
              </div>
              <ul className="space-y-3">
                {analysis.missing_info.map((info, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <XCircle className="h-4 w-4 text-yellow-600 dark:text-yellow-400 mt-0.5 shrink-0" />
                    <p className="text-sm text-foreground leading-relaxed flex-1">{info}</p>
                  </li>
                ))}
              </ul>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </Card>
      )}

      {/* Regulation Reasoning */}
      {analysis.regulation_reasoning && analysis.regulation_reasoning.length > 0 && (
        <Card>
          <button
            onClick={() => toggleSection('regulation_reasoning')}
            className="w-full p-6 flex items-center justify-between hover:bg-surface/50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-blue-500/10">
                <CheckCircle2 className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="text-left">
                <h3 className="text-lg font-semibold">Regulation Analysis</h3>
                <p className="text-sm text-muted-foreground">
                  Detailed reasoning for {analysis.regulation_reasoning.length} regulation{analysis.regulation_reasoning.length !== 1 ? 's' : ''}
                </p>
              </div>
            </div>
            {expandedSections.has('regulation_reasoning') ? (
              <ChevronUp className="h-5 w-5 text-muted-foreground" />
            ) : (
              <ChevronDown className="h-5 w-5 text-muted-foreground" />
            )}
          </button>
          <AnimatePresence>
            {expandedSections.has('regulation_reasoning') && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="px-6 pb-6 border-t border-subtle-border">
              <div className="mt-4 space-y-4">
                {analysis.regulation_reasoning.map((item, index) => (
                  <div key={index} className="p-4 bg-surface border border-subtle-border rounded-lg">
                    <h4 className="font-semibold text-sm mb-2 text-foreground">{item.regulation}</h4>
                    <p className="text-sm text-muted-foreground leading-relaxed">{item.reason}</p>
                  </div>
                ))}
              </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </Card>
      )}

      {/* Testing Cost Estimate */}
      {analysis.testing_cost_estimate && analysis.testing_cost_estimate.length > 0 && (
        <Card>
          <button
            onClick={() => toggleSection('testing_cost')}
            className="w-full p-6 flex items-center justify-between hover:bg-surface/50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-purple-500/10">
                <CheckCircle2 className="h-5 w-5 text-purple-600 dark:text-purple-400" />
              </div>
              <div className="text-left">
                <h3 className="text-lg font-semibold">Testing Cost Breakdown</h3>
                <p className="text-sm text-muted-foreground">
                  {analysis.testing_cost_estimate.length} required test{analysis.testing_cost_estimate.length !== 1 ? 's' : ''}
                </p>
              </div>
            </div>
            {expandedSections.has('testing_cost') ? (
              <ChevronUp className="h-5 w-5 text-muted-foreground" />
            ) : (
              <ChevronDown className="h-5 w-5 text-muted-foreground" />
            )}
          </button>
          <AnimatePresence>
            {expandedSections.has('testing_cost') && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="px-6 pb-6 border-t border-subtle-border">
              <div className="mt-4 space-y-3">
                {analysis.testing_cost_estimate.map((test, index) => {
                  const avgCost = (test.low + test.high) / 2;
                  return (
                    <div key={index} className="p-4 bg-surface border border-subtle-border rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-semibold text-sm text-foreground">{test.test}</h4>
                        <div className="text-right">
                          <div className="text-sm font-semibold text-foreground">
                            ${test.low.toLocaleString()} - ${test.high.toLocaleString()}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            Avg: ${avgCost.toLocaleString()}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
                <div className="mt-4 pt-4 border-t border-subtle-border">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-semibold text-foreground">Total Estimated Testing Cost</span>
                    <span className="text-lg font-bold text-primary">
                      ${analysis.testing_cost_estimate.reduce((sum, t) => sum + t.low, 0).toLocaleString()} - 
                      ${analysis.testing_cost_estimate.reduce((sum, t) => sum + t.high, 0).toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </Card>
      )}

      {/* Initial Order Cost */}
      {analysis.initial_order_cost && (
        <Card>
          <button
            onClick={() => toggleSection('initial_order_cost')}
            className="w-full p-6 flex items-center justify-between hover:bg-surface/50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-green-500/10">
                <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div className="text-left">
                <h3 className="text-lg font-semibold">Initial Order Cost Breakdown</h3>
                <p className="text-sm text-muted-foreground">
                  Detailed breakdown of capital required for first production run
                </p>
              </div>
            </div>
            {expandedSections.has('initial_order_cost') ? (
              <ChevronUp className="h-5 w-5 text-muted-foreground" />
            ) : (
              <ChevronDown className="h-5 w-5 text-muted-foreground" />
            )}
          </button>
          <AnimatePresence>
            {expandedSections.has('initial_order_cost') && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden"
              >
                <div className="px-6 pb-6 border-t border-subtle-border">
              <div className="mt-4 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-surface border border-subtle-border rounded-lg">
                    <p className="text-xs text-muted-foreground mb-1">Unit Cost (Landed)</p>
                    <p className="text-lg font-semibold text-foreground">
                      ${analysis.initial_order_cost.unitCost.toFixed(2)}
                    </p>
                  </div>
                  <div className="p-4 bg-surface border border-subtle-border rounded-lg">
                    <p className="text-xs text-muted-foreground mb-1">Minimum Order Quantity</p>
                    <p className="text-lg font-semibold text-foreground">
                      {analysis.initial_order_cost.moq.toLocaleString()} units
                    </p>
                  </div>
                </div>
                <div className="p-4 bg-surface border border-subtle-border rounded-lg">
                  <div className="flex justify-between items-center mb-2">
                    <p className="text-sm text-muted-foreground">Product Cost (MOQ)</p>
                    <p className="text-sm font-semibold text-foreground">
                      ${analysis.initial_order_cost.minimumOrderCost.toLocaleString()}
                    </p>
                  </div>
                  <div className="flex justify-between items-center mb-2">
                    <p className="text-sm text-muted-foreground">Testing Costs</p>
                    <p className="text-sm font-semibold text-foreground">
                      ${analysis.initial_order_cost.testingCostTotal.toLocaleString()}
                    </p>
                  </div>
                  <div className="border-t border-subtle-border mt-3 pt-3">
                    <div className="flex justify-between items-center">
                      <p className="text-base font-bold text-foreground">Total Initial Outlay</p>
                      <p className="text-xl font-bold text-primary">
                        ${analysis.initial_order_cost.totalInitialCost.toLocaleString()}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="p-4 bg-blue-500/5 border border-blue-500/20 rounded-lg">
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    <strong>Note:</strong> This estimate assumes a standard MOQ of {analysis.initial_order_cost.moq} units. 
                    Actual MOQ may vary by supplier. Testing costs are one-time expenses for initial compliance certification.
                  </p>
                </div>
              </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </Card>
      )}
    </div>
  );
}

