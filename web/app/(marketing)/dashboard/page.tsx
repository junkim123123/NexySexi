import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { ArrowRight } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div className="bg-white min-h-screen">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-neutral-900 mb-4">
            NexSupply Project Dashboard
          </h1>
          <p className="text-lg text-neutral-600 mb-8">
            Coming soon. Your projects and analyses will appear here.
          </p>
          <Card className="p-12 bg-neutral-50 border-neutral-200">
            <p className="text-neutral-600 mb-6">
              This dashboard will show:
            </p>
            <ul className="text-left max-w-md mx-auto space-y-3 text-neutral-600 mb-8">
              <li className="flex items-start gap-3">
                <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2 flex-shrink-0" />
                <span>Your saved product analyses</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2 flex-shrink-0" />
                <span>Active sourcing projects</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2 flex-shrink-0" />
                <span>Supplier quotes and communications</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-1.5 h-1.5 rounded-full bg-neutral-900 mt-2 flex-shrink-0" />
                <span>Order tracking and logistics</span>
              </li>
            </ul>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/chat"
                className="inline-flex items-center justify-center rounded-full bg-neutral-900 px-8 py-3.5 text-base font-semibold text-white hover:bg-neutral-800 transition-colors"
              >
                Start a new project
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                href="/"
                className="inline-flex items-center justify-center rounded-full border border-neutral-300 px-8 py-3.5 text-base font-semibold text-neutral-900 hover:bg-neutral-50 transition-colors"
              >
                Back to home
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

