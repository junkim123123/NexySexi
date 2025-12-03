"use client";

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Loader2, CheckCircle, AlertTriangle } from 'lucide-react';

type FormStatus = 'idle' | 'loading' | 'success' | 'error';

export default function SampleRequest() {
  const [status, setStatus] = useState<FormStatus>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [analysisPreview, setAnalysisPreview] = useState('');

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus('loading');
    setErrorMessage('');
    setAnalysisPreview('');

    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());

    try {
      const response = await fetch('/api/sample-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong.');
      }

      if (data.analysisPreview) {
        setAnalysisPreview(data.analysisPreview);
      }
      setStatus('success');
    } catch (error) {
      setStatus('error');
      setErrorMessage(error instanceof Error ? error.message : 'An unknown error occurred.');
    }
  };

  return (
    <section id="sample-request" className="relative w-full bg-background py-16 sm:py-20 lg:py-24">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ type: 'spring', stiffness: 260, damping: 20, duration: 0.6 }}
          className="glass-card border border-subtle-border rounded-2xl p-6 sm:p-8 text-center"
        >
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Request a Sample Report
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            See for yourself. We'll send a sample DDP and supplier risk report directly to your inbox.
          </p>

          {status === 'success' ? (
            <div className="mt-8 flex flex-col items-center text-center text-success">
              <CheckCircle className="h-12 w-12" />
              <h3 className="mt-4 text-2xl font-semibold">Request Received!</h3>
              <p className="mt-2">Thank you. We'll be in touch shortly.</p>
              {analysisPreview && (
                <p className="mt-4 text-sm text-muted-foreground border-t border-subtle-border pt-4">
                  <strong>AI First Impression:</strong> {analysisPreview}
                </p>
              )}
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="mt-8 space-y-4 text-left">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-muted-foreground">Name</label>
                  <input type="text" id="name" name="name" required className="mt-1 block w-full rounded-md bg-surface border-subtle-border px-3 py-2 text-foreground placeholder-muted-foreground/50 focus:border-primary focus:ring-primary sm:text-sm" />
                </div>
                <div>
                  <label htmlFor="workEmail" className="block text-sm font-medium text-muted-foreground">Work Email</label>
                  <input type="email" id="workEmail" name="workEmail" required className="mt-1 block w-full rounded-md bg-surface border-subtle-border px-3 py-2 text-foreground placeholder-muted-foreground/50 focus:border-primary focus:ring-primary sm:text-sm" />
                </div>
              </div>
              <div>
                <label htmlFor="company" className="block text-sm font-medium text-muted-foreground">Company</label>
                <input type="text" id="company" name="company" required className="mt-1 block w-full rounded-md bg-surface border-subtle-border px-3 py-2 text-foreground placeholder-muted-foreground/50 focus:border-primary focus:ring-primary sm:text-sm" />
              </div>
              <div>
                <label htmlFor="useCase" className="block text-sm font-medium text-muted-foreground">Use Case</label>
                <textarea id="useCase" name="useCase" rows={3} required className="mt-1 block w-full rounded-md bg-surface border-subtle-border px-3 py-2 text-foreground placeholder-muted-foreground/50 focus:border-primary focus:ring-primary sm:text-sm"></textarea>
              </div>
              
              <button
                type="submit"
                disabled={status === 'loading'}
                className="group relative w-full inline-flex items-center justify-center rounded-xl bg-primary px-8 py-3 text-base font-bold text-black transition-all duration-300 hover:bg-primary/90 disabled:bg-primary/50"
              >
                {status === 'loading' && <Loader2 className="mr-2 h-5 w-5 animate-spin" />}
                Send Request
              </button>
              
              {status === 'error' && (
                <div className="mt-4 flex items-center justify-center text-sm text-destructive">
                  <AlertTriangle className="h-4 w-4 mr-2" />
                  <span>{errorMessage}</span>
                </div>
              )}
            </form>
          )}
        </motion.div>
      </div>
    </section>
  );
}