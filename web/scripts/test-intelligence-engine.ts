import { analyzeSampleRequest } from "../lib/ai/geminiClient";
import { applyLeadGuardrails } from "../lib/sample-request/guardrails";
import { deriveLeadRouting } from "../lib/sample-request/routing";
import { SampleRequestPayload } from "../lib/sample-request/schema";
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from .env.local
dotenv.config({ path: path.resolve(__dirname, '../.env.local') });

const testCases: { name: string; payload: SampleRequestPayload; expected: string }[] = [
  {
    name: "FBA 7 figure seller",
    payload: {
      name: "Emma Lee",
      workEmail: "emma.lee@acmecoffee.com",
      company: "Acme Coffee",
      useCase: "Already running FBA for 3 years. Currently seeing IPI score and inventory turns drop for 3 ASINs. Importing two 40HQ FCLs quarterly from China FOB. EBITDA under pressure due to Section 301 tariffs and landed cost."
    },
    expected: "Tier A, Score > 90, Business Email"
  },
  {
    name: "Serious DTC Brand Owner (Prosumer)",
    payload: {
      name: "Founder",
      workEmail: "founder@plantmilk.co",
      company: "Plant Milk Co",
      useCase: "Ahead of EU launch, need info on CE marking and CPSC testing costs. Tooling cost and contribution margin variation with MOQ. Comparing EXW vs FOB."
    },
    expected: "Tier B/A, Score ~80, Prosumer Email, High Intent"
  },
  {
    name: "High Intent Gmail Operator",
    payload: {
      name: "Daniel",
      workEmail: "daniel.ops.manager@gmail.com",
      company: "Daniel Ops",
      useCase: "Using two US 3PLs. Need FCL inventory strategy to improve inventory turns due to 3PL fee structure and stockout risk."
    },
    expected: "Tier B, Score > 70, Free Email but High Intent"
  },
  {
    name: "Emotional/Low Intent Gmail",
    payload: {
      name: "King Amazon",
      workEmail: "kingofamazon777@gmail.com",
      company: "King Amazon",
      useCase: "Want to turn my life around with Amazon and make passive income. What is selling well these days? Can you give me cheap price with no MOQ?"
    },
    expected: "Tier D, Score < 30, Free Email, Low Intent"
  },
  {
    name: "Disposable/Spam",
    payload: {
      name: "Best Deal",
      workEmail: "bestdeal@guerrillamail.com",
      company: "Best Deal",
      useCase: "send best price catalog"
    },
    expected: "Tier D, Score <= 25, Disposable Email"
  },
  {
    name: "Student Research",
    payload: {
      name: "MJ Kim",
      workEmail: "mjkim@wustl.edu",
      company: "Washington University",
      useCase: "Requesting survey for global sourcing and FBA research. No actual purchasing plan."
    },
    expected: "Tier C/D, Score < 40, Business Email, Low Intent"
  },
  {
    name: "Retail Chain Buyer",
    payload: {
      name: "Purchasing Director",
      workEmail: "purchasing.director@midwestgrocers.com",
      company: "Midwest Grocers",
      useCase: "Want to expand plan to OEM in specific category. Over 3 containers per month. Want risk diversification between China and Vietnam."
    },
    expected: "Tier A, Score > 90, Business Email"
  },
  {
    name: "Exploratory Brand (Gmail)",
    payload: {
      name: "Ashley",
      workEmail: "ashley.brand@gmail.com",
      company: "Ashley Brand",
      useCase: "Running two private label brands. Expanding SKUs next season, want rough idea of MOQ and tooling cost."
    },
    expected: "Tier C, Score ~50-60, Free Email, Moderate Intent"
  }
];

async function runTests() {
  console.log("Starting Intelligence Engine Test Suite...\n");

  for (const test of testCases) {
    console.log(`--- Test Case: ${test.name} ---`);
    console.log(`Payload: ${JSON.stringify(test.payload, null, 2)}`);
    console.log(`Expected: ${test.expected}`);

    try {
      const rawAnalysis = await analyzeSampleRequest(test.payload);
      const guardedAnalysis = applyLeadGuardrails(test.payload, rawAnalysis);
      const routing = deriveLeadRouting(guardedAnalysis);

      console.log("\nResult:");
      console.log(`  Tier: ${routing.tier}`);
      console.log(`  Score: ${guardedAnalysis.qualification_engine.opportunity_score}`);
      console.log(`  Intent Score: ${guardedAnalysis.qualification_engine.intent_score_0_to_100}`);
      console.log(`  Authority Score: ${guardedAnalysis.qualification_engine.authority_score_0_to_100}`);
      console.log(`  Email Type: ${guardedAnalysis.lead_profile.email_type}`);
      console.log(`  Reasoning: ${guardedAnalysis.qualification_engine._reasoning_trace}`);
      console.log("\n--------------------------------------------------\n");
    } catch (error) {
      console.error(`Error running test case ${test.name}:`, error);
    }
  }
}

runTests();