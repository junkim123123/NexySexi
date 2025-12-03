"use client";

import { motion } from "framer-motion";

const FADE_UP_ANIMATION_VARIANTS = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 260, damping: 20, duration: 0.6 } },
};

export default function WhoIsThisFor() {
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
            Who Is This For?
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <motion.div variants={FADE_UP_ANIMATION_VARIANTS} className="glass-card border border-subtle-border rounded-2xl p-6 sm:p-8">
            <h3 className="text-xl font-bold mb-4">Amazon FBA and TikTok Shop sellers</h3>
            <p className="text-muted-foreground">
              You found a product on TikTok or Alibaba and want to know if it will still be profitable after freight, duty, and fees.
            </p>
          </motion.div>
          <motion.div variants={FADE_UP_ANIMATION_VARIANTS} className="glass-card border border-subtle-border rounded-2xl p-6 sm:p-8">
            <h3 className="text-xl font-bold mb-4">DTC and Shopify brands</h3>
            <p className="text-muted-foreground">
              You already have a brand and want better control over cost, quality, and compliance for your next production run.
            </p>
          </motion.div>
          <motion.div variants={FADE_UP_ANIMATION_VARIANTS} className="glass-card border border-subtle-border rounded-2xl p-6 sm:p-8">
            <h3 className="text-xl font-bold mb-4">Retail and distributors</h3>
            <p className="text-muted-foreground">
              You are considering container level purchases and want a clear landed cost model and supplier risk view before committing.
            </p>
          </motion.div>
        </div>
      </div>
    </motion.section>
  );
}