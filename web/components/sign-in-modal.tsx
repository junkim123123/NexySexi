'use client';

import { useState } from 'react';
import { signIn } from 'next-auth/react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';

interface SignInModalProps {
  open: boolean;
  onClose: () => void;
}

export default function SignInModal({ open, onClose }: SignInModalProps) {
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
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md text-center">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold">Sign In to Continue</DialogTitle>
          <DialogDescription className="text-muted-foreground">
            NexSupply is in early alpha. Anonymous users are limited to 1 free analysis per day. Sign in for more.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4 py-4">
          {showGoogleSignIn && (
            <Button onClick={() => signIn('google')} className="w-full" size="lg">
              Continue with Google
            </Button>
          )}
          {showEmailSignIn && (
            <Button onClick={() => signIn('email')} className="w-full" size="lg" variant={showGoogleSignIn ? "outline" : "default"}>
              Continue with Email
            </Button>
          )}
          {!showGoogleSignIn && !showEmailSignIn && (
            <p className="text-sm text-muted-foreground">
              Authentication is not configured. Please contact support.
            </p>
          )}
        </div>
        <DialogFooter className="flex-col sm:flex-col sm:space-x-0">
          <div className="mt-4 pt-4 border-t border-subtle-border w-full">
            {!showAdminMode ? (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowAdminMode(true)}
                className="text-xs text-muted-foreground hover:text-foreground w-full"
              >
                Admin Mode
              </Button>
            ) : (
              <form onSubmit={handleAdminLogin} className="space-y-2 w-full">
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
          <Button variant="ghost" onClick={onClose} className="mt-2 w-full">
            Maybe later
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}