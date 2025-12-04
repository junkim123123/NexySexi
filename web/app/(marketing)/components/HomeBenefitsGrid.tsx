import { CheckCircle } from 'lucide-react';

const benefits = [
  {
    title: 'Verified factory partners',
    body: 'We pre-screen suppliers and QC partners so you can focus on your product.',
  },
  {
    title: 'Anywhere, anytime support',
    body: 'Get async advice from trade experts in your time zone, without the costly retainers.',
  },
  {
    title: 'Landed-cost clarity',
    body: 'See duties, freight, and other extras in one estimate before you commit.',
  },
  {
    title: 'Smaller tests first',
    body: 'Start with small DDP runs to test the market before committing to big orders.',
  },
  {
    title: 'One inbox for your project',
    body: 'Keep quotes, compliance documents, and shipping updates in one place.',
  },
  {
    title: 'No long-term lock-in',
    body: 'Our project-based engagement comes with clear pricing and no surprises.',
  },
];

export default function HomeBenefitsGrid() {
  return (
    <section className="py-16 sm:py-20 bg-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-neutral-900 sm:text-4xl">
            Why importers work with NexSupply
          </h2>
        </div>
        <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {benefits.map((benefit) => (
            <div key={benefit.title} className="flex">
              <div className="flex-shrink-0">
                <CheckCircle className="h-6 w-6 text-green-500" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-neutral-900">
                  {benefit.title}
                </h3>
                <p className="mt-2 text-base text-neutral-600">
                  {benefit.body}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}