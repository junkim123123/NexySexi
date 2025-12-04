'use client';

// Note: next-sanity/studio requires Next.js 15+
// For Next.js 14, we'll use a different approach
// This is a placeholder - will implement alternative solution

export default function StudioPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Sanity Studio</h1>
        <p className="text-neutral-600 mb-4">
          Sanity Studio requires Next.js 15+. 
        </p>
        <p className="text-sm text-neutral-500">
          Please access Sanity Studio at: <br />
          <a 
            href="https://www.sanity.io/manage" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            https://www.sanity.io/manage
          </a>
        </p>
        <p className="text-xs text-neutral-400 mt-4">
          Or run: npx sanity dev (from project root)
        </p>
      </div>
    </div>
  );
}
