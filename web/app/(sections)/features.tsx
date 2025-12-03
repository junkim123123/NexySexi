"use client";

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, ShieldCheck, Factory, Route, CheckCircle2 } from 'lucide-react';
import type { LucideProps } from 'lucide-react';

// --- Data Structure ---
const FEATURES = [
  {
    id: "multi_channel",
    icon: BarChart3,
    label: "Multi-Channel Analysis",
    title: "Unified Cost & Risk Visibility",
    description: "Aggregate data from all your suppliers and logistics partners into a single, real-time dashboard.",
    bullets: [
      "Real-time landed cost calculation",
      "Supplier risk score aggregation",
      "SKU-level profitability tracking",
    ],
  },
  {
    id: "compliance",
    icon: ShieldCheck,
    label: "Automated Compliance",
    title: "Navigate Global Trade with Confidence",
    description: "Automate customs, tax, and regulatory checks to prevent costly delays and fines at the border.",
    bullets: [
      "Automated HTS code classification",
      "Real-time duty & tax calculation",
      "Denied party screening",
    ],
  },
  {
    id: "supplier_verification",
    icon: Factory,
    label: "Supplier Verification",
    title: "Onboard Partners You Can Trust",
    description: "Vet new suppliers against our proprietary database of ethical, financial, and operational risk factors.",
    bullets: [
      "Ethical sourcing & labor compliance checks",
      "Production capacity verification",
      "Financial health & credit risk analysis",
    ],
  },
  {
    id: "logistics",
    icon: Route,
    label: "Optimized Logistics",
    title: "Find the Smartest Route to Market",
    description: "Our AI engine analyzes millions of data points to recommend the optimal carrier, route, and mode of transport.",
    bullets: [
      "Carrier performance & cost benchmarking",
      "Route optimization to avoid delays",
      "Carbon footprint calculation per lane",
    ],
  },
];

// Custom hook for reduced motion
const usePrefersReducedMotion = () => {
  const [reduceMotion, setReduceMotion] = useState(false);
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReduceMotion(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => setReduceMotion(event.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);
  return reduceMotion;
};

export default function Features() {
  const reduceMotion = usePrefersReducedMotion();

  const containerVariants = {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: reduceMotion ? 0 : 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: 'spring',
        stiffness: 260,
        damping: 20,
        duration: 0.6,
      },
    },
  };

  return (
    <section className="relative w-full bg-background border-t border-subtle-border py-16 sm:py-20 lg:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Intro Row */}
        <div className="mb-12 text-left">
          <p className="text-sm font-semibold text-primary uppercase tracking-widest">
            Product Features
          </p>
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Everything you need to de-risk your supply chain.
          </h2>
          <p className="mt-4 max-w-2xl text-lg text-muted-foreground">
            NexSupply provides a unified platform to manage complexity, ensure compliance, and optimize every step from factory to final destination.
          </p>
        </div>

        {/* Features Grid */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8"
        >
          {FEATURES.map((feature) => (
            <motion.div
              key={feature.id}
              variants={itemVariants}
              className="glass-card relative h-full overflow-hidden rounded-2xl border border-subtle-border p-5 sm:p-6 transition-all duration-300 hover:border-highlight-border hover:scale-[1.02] hover:shadow-[0_0_20px_-5px_theme(colors.primary.DEFAULT)]"
            >
              <div className="flex items-start gap-4">
                <feature.icon className="h-7 w-7 text-primary flex-shrink-0" />
                <div className="flex-grow">
                  <p className="text-badge text-primary">{feature.label}</p>
                  <h3 className="mt-1 text-lg font-semibold text-foreground">
                    {feature.title}
                  </h3>
                  <p className="mt-2 text-sm text-muted-foreground">
                    {feature.description}
                  </p>
                  <ul className="mt-4 space-y-2">
                    {feature.bullets.map((bullet, i) => (
                      <li key={i} className="flex items-start text-sm text-muted-foreground">
                        <CheckCircle2 className="h-4 w-4 mr-2.5 mt-0.5 flex-shrink-0 text-primary/70" />
                        <span>{bullet}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}