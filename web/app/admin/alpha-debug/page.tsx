'use client';

import { useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

type UsageData = {
  count: number;
  limit: number;
};

type EventData = {
  type: string;
  timestamp: string;
  metadata?: Record<string, any>;
};

type EventsResponse = {
  events: EventData[];
};

// A simple time-ago function for human-readable timestamps.
function timeAgo(timestamp: string): string {
  const now = new Date();
  const past = new Date(timestamp);
  const seconds = Math.floor((now.getTime() - past.getTime()) / 1000);

  let interval = seconds / 31536000;
  if (interval > 1) return Math.floor(interval) + " years ago";
  interval = seconds / 2592000;
  if (interval > 1) return Math.floor(interval) + " months ago";
  interval = seconds / 86400;
  if (interval > 1) return Math.floor(interval) + " days ago";
  interval = seconds / 3600;
  if (interval > 1) return Math.floor(interval) + " hours ago";
  interval = seconds / 60;
  if (interval > 1) return Math.floor(interval) + " minutes ago";
  return Math.floor(seconds) + " seconds ago";
}

export default function AlphaDebugPage() {
  const { data: session, status } = useSession();
  const [usage, setUsage] = useState<UsageData | null>(null);
  const [events, setEvents] = useState<EventData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (status === 'authenticated') {
      const fetchData = async () => {
        try {
          const [usageRes, eventsRes] = await Promise.all([
            fetch('/api/usage/me'),
            fetch('/api/events/me'),
          ]);
          const usageData: UsageData = await usageRes.json();
          const eventsData: EventsResponse = await eventsRes.json();
          setUsage(usageData);
          setEvents(eventsData.events.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()));
        } catch (error) {
          console.error("Failed to fetch debug data", error);
        } finally {
          setLoading(false);
        }
      };
      fetchData();
    }
  }, [status]);

  if (status === 'loading' || loading) {
    return <div>Loading...</div>;
  }

  if (status === 'unauthenticated') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <Card>
          <CardHeader>
            <CardTitle>Sign In Required</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Please sign in to view this page.</p>
            <Button onClick={() => window.location.href = '/api/auth/signin'} className="mt-4">
              Sign In
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Alpha Debug</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>User Info</CardTitle>
          </CardHeader>
          <CardContent>
            <p><strong>Signed in as:</strong> {session?.user?.email || 'anonymous'}</p>
            {usage && (
              <p><strong>Today’s analyses:</strong> {usage.count} / {usage.limit}</p>
            )}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Recent Events</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {events.map((event, index) => (
                <li key={index} className="text-sm">
                  <strong>{event.type}</strong> - <span className="text-gray-500">{timeAgo(event.timestamp)}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}