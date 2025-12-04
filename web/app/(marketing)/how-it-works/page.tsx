// How It Works Page Structure (Rebuilt):
// 1) Hero with left text and right visual collage (chat → report → box)
// 2) Journey in three moves (3-card overview)
// 3) Step by step timeline (4 detailed steps)
// 4) Pricing and coverage band (two cards)
// 5) FAQ section
// 6) Final CTA banner
// 7) Footer (handled in layout)

import Link from 'next/link';
import { MessageSquare, FileText, Package, Upload, Brain, Users, Truck, TrendingUp } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Accordion, AccordionItem } from '@/components/ui/accordion';

export const revalidate = 60;

export default async function HowItWorksPage() {
  // Journey cards
  const journeyCards = [
    {
      title: 'Start with a chat',
      body: 'Tell us what you want to sell, where you want to sell it, and how big you want to go. We capture the key details in a shared project brief.',
      icon: MessageSquare,
    },
    {
      title: 'Get a cost and risk snapshot',
      body: 'Our tools turn that brief into a landed cost and risk view, so you see margins, duties, and red flags before you spend on inventory.',
      icon: TrendingUp,
    },
    {
      title: 'Run a pilot with NexSupply',
      body: 'When the numbers look right, we help you line up suppliers, QC and logistics for a first controlled shipment, not a blind leap.',
      icon: Package,
    },
  ];

  // Detailed steps
  const steps = [
    {
      stepNumber: '1',
      title: 'Describe your product',
      timeEstimate: '~10 minutes',
      body: 'Upload a product idea, photo or reference listing. In a short guided flow, we capture what matters for sourcing.',
      bullets: [
        'Product idea or reference listing',
        'Target market and main sales channel',
        'Rough volume and timing (test run or ongoing)',
      ],
      icon: Upload,
    },
    {
      stepNumber: '2',
      title: 'AI cost and risk check',
      timeEstimate: 'Within 24 hours',
      body: 'Our toolkit turns your brief into a first pass landed cost and risk picture so you can sanity check the project before you commit.',
      bullets: [
        'Estimated DDP per unit',
        'Simple breakdown of factory, freight, duty and extras',
        'Early flags for compliance or AD/CVD risk',
      ],
      icon: Brain,
    },
    {
      stepNumber: '3',
      title: 'Talk to NexSupply',
      timeEstimate: '30 minute call',
      body: 'If it looks promising, you can book a call with our sourcing team to go deeper.',
      bullets: [
        'Human specialist reviews your assumptions',
        'Together you stress test margin and risk scenarios',
        'You decide whether to move into supplier search',
      ],
      icon: Users,
    },
    {
      stepNumber: '4',
      title: 'Pilot run and beyond',
      timeEstimate: '1–2 week pilot',
      body: 'When you are ready to move, we help you run a controlled first order instead of jumping straight to a huge PO.',
      bullets: [
        'Shortlist and compare qualified factories',
        'Align on QC and logistics that match your risk level',
        'Turn lessons from the pilot into a repeatable playbook',
      ],
      icon: Truck,
    },
  ];

  // FAQ content
  const faqs = [
    {
      question: 'Do I have to be an experienced seller?',
      answer: 'No. Many of our early users are launching their first or second product. We focus on helping you understand landed cost and risk before you commit.',
    },
    {
      question: 'Can I use NexSupply if I already have suppliers?',
      answer: 'Yes. You can bring your own suppliers and use NexSupply only for cost and risk checks or to benchmark new options.',
    },
    {
      question: 'Do you handle shipping and customs?',
      answer: 'We help you plan freight and customs but we are not a customs broker or law firm. We can coordinate with your partners or recommend specialists.',
    },
    {
      question: 'How long does the whole process take?',
      answer: 'Most projects receive an initial analysis within one business day and a first pilot supplier plan within one to two weeks, depending on category.',
    },
  ];

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section aria-label="Hero" className="py-16 sm:py-20 bg-white">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            {/* Left: Text Content */}
            <div className="flex flex-col justify-center">
              <h1 className="text-4xl sm:text-5xl lg:text-[52px] font-semibold tracking-tight text-neutral-900 leading-tight mb-6">
                How NexSupply Works
              </h1>
              <p className="text-lg sm:text-xl text-neutral-700 font-medium mb-3 leading-relaxed">
                From first idea to your first test shipment, NexSupply keeps your project moving at every step of the sourcing process.
              </p>
              <p className="text-sm text-neutral-500 mb-4">
                Most projects get an initial snapshot within one business day.
              </p>
              <p className="text-base text-neutral-600 mb-8 leading-relaxed">
                Start with one chat. When the numbers work, scale at your own pace.
              </p>
              <div className="flex flex-row flex-wrap gap-3 sm:gap-4 items-center">
                <Link href="/chat">
                  <Button
                    variant="primary"
                    size="lg"
                    className="rounded-full px-8 py-3.5"
                  >
                    Get started
                  </Button>
                </Link>
                <Link
                  href="/#home-use-cases"
                  className="text-sm font-medium text-neutral-600 hover:text-neutral-900 transition-colors"
                >
                  See use cases
                </Link>
              </div>
            </div>

            {/* Right: Visual Collage */}
            <div className="relative">
              {/* Top Card - Project Chat */}
              <div className="relative z-10 bg-white rounded-3xl p-6 shadow-lg border border-neutral-200">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                  <span className="text-xs font-semibold text-neutral-500 uppercase tracking-wide">
                    Project chat
                  </span>
                </div>
                <div className="space-y-3">
                  <div className="bg-neutral-50 rounded-2xl p-4">
                    <p className="text-sm text-neutral-600">
                      "I want to import snack products to the US..."
                    </p>
                  </div>
                  <div className="bg-neutral-50 rounded-2xl p-4">
                    <p className="text-sm text-neutral-600">
                      "Target market: Amazon FBA, test run volume..."
                    </p>
                  </div>
                </div>
              </div>

              {/* Bottom Left Card - DDP Snapshot (overlapping) */}
              <div className="absolute -bottom-4 -left-4 z-20 bg-white rounded-2xl p-4 shadow-md border border-neutral-200 w-[200px]">
                <div className="flex items-center gap-2 mb-2">
                  <FileText className="h-4 w-4 text-neutral-600" />
                  <span className="text-xs font-semibold text-neutral-700">
                    DDP and risk snapshot
                  </span>
                </div>
                <div className="text-xs text-neutral-600 space-y-1">
                  <p>• Estimated: $2.10/unit</p>
                  <p>• Risk: Low</p>
                </div>
              </div>

              {/* Bottom Right Card - Pilot Order (overlapping) */}
              <div className="absolute -bottom-4 right-4 z-20 bg-white rounded-2xl p-4 shadow-md border border-neutral-200 w-[200px]">
                <div className="flex items-center gap-2 mb-2">
                  <Package className="h-4 w-4 text-neutral-600" />
                  <span className="text-xs font-semibold text-neutral-700">
                    Pilot order checklist
                  </span>
                </div>
                <div className="text-xs text-neutral-600 space-y-1">
                  <p>• QC plan ready</p>
                  <p>• Logistics aligned</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Journey in Three Moves */}
      <section aria-label="Journey overview" className="py-16 sm:py-20 bg-neutral-50">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-neutral-900 mb-12 text-center">
            Your sourcing journey in three moves
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
            {journeyCards.map((card, idx) => {
              const Icon = card.icon;
              return (
                <Card key={idx} className="bg-transparent border-neutral-200 shadow-sm">
                  <div className="flex items-start gap-4 mb-4">
                    <div className="flex-shrink-0">
                      <Icon className="h-6 w-6 text-neutral-600" />
                    </div>
                    <h3 className="text-xl font-semibold text-neutral-900">
                      {card.title}
                    </h3>
                  </div>
                  <p className="text-base text-neutral-600 leading-relaxed">
                    {card.body}
                  </p>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Step by Step Timeline */}
      <section aria-label="Detailed steps" className="py-16 sm:py-20 bg-white">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-neutral-900 mb-12 text-center">
            What happens in each step
          </h2>
          <div className="space-y-12 sm:space-y-16">
            {steps.map((step, index) => {
              const Icon = step.icon;
              return (
                <div key={step.stepNumber} className="flex gap-6">
                  {/* Left: Icon and Number */}
                  <div className="flex-shrink-0">
                    <div className="relative">
                      <div className="w-16 h-16 rounded-full bg-neutral-900 text-white flex items-center justify-center font-bold text-2xl">
                        {step.stepNumber}
                      </div>
                      <div className="absolute -bottom-2 -right-2 bg-neutral-100 rounded-full p-2">
                        <Icon className="h-5 w-5 text-neutral-900" />
                      </div>
                    </div>
                    {/* Vertical line (except last) */}
                    {index < steps.length - 1 && (
                      <div className="w-0.5 h-full bg-neutral-200 ml-8 mt-4" style={{ height: 'calc(100% + 3rem)' }}></div>
                    )}
                  </div>

                  {/* Right: Content */}
                  <div className="flex-1 pb-12">
                    <div className="flex items-center gap-3 mb-4">
                      <h3 className="text-2xl font-bold text-neutral-900">
                        {step.title}
                      </h3>
                      {step.timeEstimate && (
                        <span className="text-sm text-neutral-500">
                          {step.timeEstimate}
                        </span>
                      )}
                    </div>
                    <p className="text-lg text-neutral-600 mb-6 leading-relaxed">
                      {step.body}
                    </p>
                    {step.bullets && step.bullets.length > 0 && (
                      <ul className="space-y-3">
                        {step.bullets.map((bullet, i) => (
                          <li key={i} className="flex items-start gap-3">
                            <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2.5 flex-shrink-0" />
                            <span className="text-neutral-600 leading-relaxed">{bullet}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Pricing and Coverage Band */}
      <section aria-label="Pricing and coverage" className="py-16 sm:py-20 bg-neutral-50">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-neutral-900 mb-12 text-center">
            What you pay and where we work
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
            {/* Left Card */}
            <Card className="bg-transparent border-neutral-200 shadow-sm">
              <h3 className="text-2xl font-bold text-neutral-900 mb-6">Analysis and planning</h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2.5 flex-shrink-0" />
                  <span className="text-neutral-600 leading-relaxed font-semibold">
                    Simple flat fee per project during alpha
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2.5 flex-shrink-0" />
                  <span className="text-neutral-600 leading-relaxed">
                    Includes AI report and one review call
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2.5 flex-shrink-0" />
                  <span className="text-neutral-600 leading-relaxed">
                    No subscription or long term contract
                  </span>
                </li>
              </ul>
            </Card>

            {/* Right Card */}
            <Card className="bg-transparent border-neutral-200 shadow-sm">
              <h3 className="text-2xl font-bold text-neutral-900 mb-6">When orders go through NexSupply</h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2.5 flex-shrink-0" />
                  <span className="text-neutral-600 leading-relaxed font-semibold">
                    Transparent project based success fee with a clear cap
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2.5 flex-shrink-0" />
                  <span className="text-neutral-600 leading-relaxed">
                    Clear cap so your per unit margin stays protected
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2.5 flex-shrink-0" />
                  <span className="text-neutral-600 leading-relaxed">
                    Currently focused on imports into the US and selected EU markets
                  </span>
                </li>
              </ul>
            </Card>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section aria-label="Frequently asked questions" className="py-16 sm:py-20 bg-white">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-neutral-900 mb-12 text-center">
            More questions
          </h2>
          <Accordion>
            {faqs.map((faq, idx) => (
              <AccordionItem
                key={idx}
                question={faq.question}
                answer={faq.answer}
              />
            ))}
          </Accordion>
        </div>
      </section>

      {/* Final CTA Banner */}
      <section aria-label="Call to action" className="py-16 sm:py-20 bg-neutral-100">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-semibold text-neutral-900 mb-4">
            Ready to test your next import?
          </h2>
          <p className="text-lg text-neutral-600 mb-8 max-w-2xl mx-auto">
            Start with one product, one box and see how NexSupply fits your workflow.
          </p>
          <Link href="/chat">
            <Button
              variant="primary"
              size="lg"
              className="rounded-full px-8 py-3.5"
            >
              Get started
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
