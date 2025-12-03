"use client";

import { motion } from "framer-motion";

const FADE_UP_ANIMATION_VARIANTS = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 260, damping: 20, duration: 0.6 } },
};

export default function HowItWorks() {
  return (
    <motion.section
      initial="hidden"
      animate="show"
      viewport={{ once: true }}
      variants={{
        hidden: {},
        show: {
          transition: {
            staggerChildren: 0.1,
          },
        },
      }}
      className="w-full bg-background py-16 sm:py-20 lg:py-24 border-t border-subtle-border"
    >
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl mb-4">
            How NexSupply Works
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <motion.div variants={FADE_UP_ANIMATION_VARIANTS} className="glass-card border border-subtle-border rounded-2xl p-6 sm:p-8">
            <h3 className="text-xl font-bold mb-4">Step 1: Quick Scan</h3>
            <p className="text-muted-foreground">
              Start with a simple description, link, or photo. NexSupply runs a first pass landed cost and risk estimate.
            </p>
          </motion.div>
          <motion.div variants={FADE_UP_ANIMATION_VARIANTS} className="glass-card border border-subtle-border rounded-2xl p-6 sm:p-8">
            <h3 className="text-xl font-bold mb-4">Step 2: Conversational Deep Dive</h3>
            <p className="text-muted-foreground">
              If you want a more accurate quote, the NexSupply Copilot asks a few short questions about country, volume, and timeline, then refines the analysis.
            </p>
          </motion.div>
          <motion.div variants={FADE_UP_ANIMATION_VARIANTS} className="glass-card border border-subtle-border rounded-2xl p-6 sm:p-8">
            <h3 className="text-xl font-bold mb-4">Step 3: Get a Sourcing Quote</h3>
            <p className="text-muted-foreground">
              When you are serious, send the report to the NexSupply team. Our lead engine prioritizes real buyers and routes them to our sourcing network.
            </p>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
}