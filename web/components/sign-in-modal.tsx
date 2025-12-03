'use client';

import { useState } from 'react';
import { signIn } from 'next-auth/react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface SignInModalProps {
  onClose: () => void;
}

export default function SignInModal({ onClose }: SignInModalProps) {
  const [showAdminMode, setShowAdminMode] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const showGoogleSignIn = process.env.NEXT_PUBLIC_GOOGLE_ENABLED !== 'false';
  const showEmailSignIn = process.env.NEXT_PUBLIC_EMAIL_ENABLED !== 'false';

  const handleAdminLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const result = await signIn('credentials', {
        password: adminPassword,
        redirect: false,
      });
      if (result?.ok) {
        onClose();
      } else {
        alert('Invalid password');
      }
    } catch (error) {
      alert('Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center">
      <Card className="p-8 max-w-md w-full text-center">
        <h3 className="card-title mb-4">Sign In to Continue</h3>
        <p className="helper-text mb-6">
          NexSupply is in early alpha. To protect our servers, anonymous users can only run 1 free analysis per day. Sign in to continue.
        </p>
        <div className="space-y-4">
          {showGoogleSignIn && (
            <Button onClick={() => signIn('google')} className="w-full" size="lg">
              Continue with Google
            </Button>
          )}
          {showEmailSignIn && (
            <Button onClick={() => signIn('email')} className="w-full" size="lg" variant={showGoogleSignIn ? "outline" : "primary"}>
              Continue with Email
            </Button>
          )}
          {!showGoogleSignIn && !showEmailSignIn && (
            <p className="text-sm text-muted-foreground">
              Authentication is not configured. Please contact support.
            </p>
          )}
        </div>

        {/* Admin Mode - 작게 추가 */}
        <div className="mt-4 pt-4 border-t border-subtle-border">
          {!showAdminMode ? (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowAdminMode(true)}
              className="text-xs text-muted-foreground hover:text-foreground"
            >
              Admin Mode
            </Button>
          ) : (
            <form onSubmit={handleAdminLogin} className="space-y-2">
              <input
                type="password"
                placeholder="Admin password"
                value={adminPassword}
                onChange={(e) => setAdminPassword(e.target.value)}
                className="w-full px-3 py-2 text-sm rounded-lg bg-surface border border-subtle-border text-foreground placeholder-muted-foreground focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                autoFocus
              />
              <div className="flex gap-2 justify-center">
                <Button
                  type="submit"
                  size="sm"
                  disabled={isLoading}
                  className="text-xs"
                >
                  {isLoading ? 'Logging in...' : 'Login'}
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setShowAdminMode(false);
                    setAdminPassword('');
                  }}
                  className="text-xs"
                >
                  Cancel
                </Button>
              </div>
            </form>
          )}
        </div>

        <Button variant="ghost" onClick={onClose} className="mt-4">
          Maybe later
        </Button>
      </Card>
    </div>
  );
}