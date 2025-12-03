// A simple in-memory rate limiter.
// NOTE: This is not suitable for production use at scale, as it's not shared across server instances.
// However, it's a good starting point for V1.

type UsageEntry = {
  count: number;
  // Use a numeric date (e.g., 20231225) to easily check if the entry is from a previous day.
  date: number;
};

const usage = new Map<string, UsageEntry>();

const ANONYMOUS_LIMIT = 1;
const AUTHENTICATED_LIMIT = 10;

function getCurrentDateAsNumber(): number {
  const now = new Date();
  const year = now.getFullYear();
  const month = (now.getMonth() + 1).toString().padStart(2, '0');
  const day = now.getDate().toString().padStart(2, '0');
  return parseInt(`${year}${month}${day}`, 10);
}

export function checkUsage(identifier: string, isAuthenticated: boolean): { allowed: boolean; reason?: string } {
  const limit = isAuthenticated ? AUTHENTICATED_LIMIT : ANONYMOUS_LIMIT;
  const currentDate = getCurrentDateAsNumber();
  const entry = usage.get(identifier);

  if (!entry || entry.date !== currentDate) {
    // First request of the day for this identifier.
    usage.set(identifier, { count: 1, date: currentDate });
    return { allowed: true };
  }

  if (entry.count >= limit) {
    return {
      allowed: false,
      reason: isAuthenticated ? 'authenticated_daily_limit' : 'anonymous_daily_limit',
    };
  }

  // Increment and allow.
  entry.count++;
  usage.set(identifier, entry);
  return { allowed: true };
}