"use client";

import { useState } from "react";
import { Loader2 } from "lucide-react";

export default function LeadIntelInspector() {
  const [payload, setPayload] = useState({
    name: "Test User",
    workEmail: "test@example.com",
    company: "Test Co",
    useCase: "I need to source 5000 widgets from China.",
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRun = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("/api/sample-request/debug", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`Error: ${res.statusText}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <header>
          <h1 className="text-3xl font-bold text-gray-900">Lead Intelligence Inspector</h1>
          <p className="text-gray-500">v2.1 Engine Debug Console</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Column */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
              <h2 className="text-lg font-semibold mb-4">Input Payload</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Name</label>
                  <input
                    type="text"
                    value={payload.name}
                    onChange={(e) => setPayload({ ...payload, name: e.target.value })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Work Email</label>
                  <input
                    type="email"
                    value={payload.workEmail}
                    onChange={(e) => setPayload({ ...payload, workEmail: e.target.value })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Company</label>
                  <input
                    type="text"
                    value={payload.company}
                    onChange={(e) => setPayload({ ...payload, company: e.target.value })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Use Case</label>
                  <textarea
                    rows={6}
                    value={payload.useCase}
                    onChange={(e) => setPayload({ ...payload, useCase: e.target.value })}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                  />
                </div>
                <button
                  onClick={handleRun}
                  disabled={loading}
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? <Loader2 className="animate-spin h-5 w-5" /> : "Run Intelligence Engine"}
                </button>
                {error && <p className="text-red-600 text-sm">{error}</p>}
              </div>
            </div>
          </div>

          {/* Results Column */}
          <div className="lg:col-span-2 space-y-6">
            {result && (
              <>
                {/* High Level Routing Card */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">Routing Decision</h2>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-bold ${
                        result.routing.tier === "A"
                          ? "bg-purple-100 text-purple-800"
                          : result.routing.tier === "B"
                          ? "bg-blue-100 text-blue-800"
                          : result.routing.tier === "C"
                          ? "bg-green-100 text-green-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      Tier {result.routing.tier}
                    </span>
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="text-xs text-gray-500 uppercase">Score</div>
                      <div className="text-2xl font-bold text-gray-900">
                        {result.guardedAnalysis.qualification_engine.opportunity_score}
                      </div>
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="text-xs text-gray-500 uppercase">Queue</div>
                      <div className="text-lg font-medium text-gray-900 capitalize">
                        {result.routing.queue}
                      </div>
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="text-xs text-gray-500 uppercase">SLA</div>
                      <div className="text-lg font-medium text-gray-900">
                        {result.routing.slaHours < 1
                          ? `${Math.round(result.routing.slaHours * 60)} min`
                          : `${result.routing.slaHours} h`}
                      </div>
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="text-xs text-gray-500 uppercase">Email Type</div>
                      <div className="text-lg font-medium text-gray-900 capitalize">
                        {result.guardedAnalysis.lead_profile.email_type}
                      </div>
                    </div>
                  </div>
                  <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-100">
                    <div className="text-sm font-medium text-blue-900 mb-1">AI Reasoning Trace</div>
                    <p className="text-sm text-blue-800">
                      {result.guardedAnalysis.qualification_engine._reasoning_trace}
                    </p>
                  </div>
                </div>

                {/* Guarded Analysis Details */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                  <h2 className="text-lg font-semibold mb-4">Guarded Analysis (Final)</h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 mb-2">Scores Breakdown</h3>
                      <ul className="space-y-1 text-sm">
                        <li className="flex justify-between">
                          <span>Intent:</span>
                          <span className="font-mono">{result.guardedAnalysis.qualification_engine.intent_score_0_to_100}</span>
                        </li>
                        <li className="flex justify-between">
                          <span>Fit:</span>
                          <span className="font-mono">{result.guardedAnalysis.qualification_engine.fit_score_0_to_100}</span>
                        </li>
                        <li className="flex justify-between">
                          <span>Authority:</span>
                          <span className="font-mono">{result.guardedAnalysis.qualification_engine.authority_score_0_to_100}</span>
                        </li>
                        <li className="flex justify-between">
                          <span>Engagement:</span>
                          <span className="font-mono">{result.guardedAnalysis.qualification_engine.engagement_score_0_to_100}</span>
                        </li>
                        <li className="flex justify-between pt-2 border-t font-semibold">
                          <span>Tech Sophistication:</span>
                          <span className="font-mono">{result.guardedAnalysis.lead_profile.technical_sophistication_score}/10</span>
                        </li>
                      </ul>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 mb-2">Metadata</h3>
                      <ul className="space-y-1 text-sm">
                        <li>
                          <span className="text-gray-500">Role:</span> {result.guardedAnalysis.lead_profile.inferred_role}
                        </li>
                        <li>
                          <span className="text-gray-500">Persona:</span> {result.guardedAnalysis.lead_profile.buyer_persona_tag}
                        </li>
                        <li>
                          <span className="text-gray-500">Industry:</span> {result.guardedAnalysis.firmographics.industry_vertical}
                        </li>
                        <li>
                          <span className="text-gray-500">Urgency:</span> {result.guardedAnalysis.qualification_engine.urgency_signal}
                        </li>
                      </ul>
                    </div>
                  </div>
                  {result.guardedAnalysis.qualification_engine.intent_signals && (
                    <div className="mt-4">
                      <h3 className="text-sm font-medium text-gray-500 mb-2">Intent Signals</h3>
                      <div className="flex flex-wrap gap-2">
                        {result.guardedAnalysis.qualification_engine.intent_signals.high_intent_tags?.map((tag: string) => (
                          <span key={tag} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                            {tag}
                          </span>
                        ))}
                        {result.guardedAnalysis.qualification_engine.intent_signals.low_intent_tags?.map((tag: string) => (
                          <span key={tag} className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                      <p className="mt-2 text-sm text-gray-600 italic">
                        "{result.guardedAnalysis.qualification_engine.intent_signals.summary}"
                      </p>
                    </div>
                  )}
                </div>

                {/* Raw JSON Toggle */}
                <details className="bg-gray-50 p-4 rounded-xl border border-gray-200">
                  <summary className="cursor-pointer text-sm font-medium text-gray-700">View Raw AI Response</summary>
                  <pre className="mt-4 text-xs overflow-auto max-h-96 p-4 bg-gray-900 text-gray-100 rounded-lg">
                    {JSON.stringify(result.rawAnalysis, null, 2)}
                  </pre>
                </details>
              </>
            )}
            {!result && !loading && (
              <div className="h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-xl text-gray-400">
                Run the engine to see results
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}