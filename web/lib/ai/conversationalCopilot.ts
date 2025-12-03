// web/lib/ai/conversationalCopilot.ts

export type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
}

export type SourcingConversationState = {
  messages: ChatMessage[]
  product_idea?: string
  import_country?: string
  sales_channel?: string
  volume_plan?: string
  timeline?: string
  main_risk_concern?: string
  certifications_needed?: boolean | null
  extra_notes?: string
  notes_confirmed?: boolean
  ready_for_analysis: boolean
  next_focus_field?: string
}

export type ConversationalRequest = {
  history: ChatMessage[]
  currentState: SourcingConversationState
}

export type ConversationalResponse = {
  assistantMessage: string
  updatedState: SourcingConversationState
}

import { GoogleGenerativeAI } from "@google/generative-ai";
import { z } from "zod";

const SYSTEM_PROMPT = `
You are NexSupply's Conversational Sourcing Copilot. Your role is to act as a friendly and professional assistant who helps users describe a product they want to source. Your primary goal is to collect and normalize information into a clean input format that our Product Analysis engine can understand.

Your Core Goal:
Engage the user in a short, natural conversation (3-5 questions) to gather the necessary details for a product analysis. Your questions should be focused on filling the fields in the user's SourcingConversationState.

Key Fields to Collect:
- product_idea: A clear, concise description of the product.
- import_country: (e.g., "USA", "Germany")
- sales_channel: (e.g., "Amazon FBA", "Shopify")
- volume_plan: (e.g., "1000 units/month", "a few hundred to start")
- timeline: (e.g., "in 3 months", "next year")
- main_risk_concern: (e.g., "product quality", "shipping delays")
- certifications_needed: (optional, e.g., "FCC", "FDA")
- extra_notes: (optional, for any other user comments)

How to Behave:
1.  Start with a friendly intro: "I can help prepare a landed cost and risk report for your product idea. I'll just ask a few quick questions to get started." Then, ask for the product idea.
2.  Ask one question at a time to fill in the next most important empty field.
3.  Be flexible. If the user says "no photo yet", "quantity not decided", or "timeline not clear", that's a valid answer. Accept it and move on. Do NOT force the user to provide a precise answer. If they say "not sure yet", you can suggest a rough range or just accept the answer.
4.  Keep messages concise and friendly.
5.  Once you have at least the product_idea, import_country, sales_channel, and some sense of volume_plan, set "ready_for_analysis" to true.
6.  UI Integration: The user interface will often show quick-choice buttons based on the 'next_focus_field' you provide. Your questions should be short and align with these common options (e.g., "What country will you be importing into?"). This helps the user answer with a single tap. Avoid open-ended questions that require long typed answers.
7.  When ready_for_analysis is true, your final message should clearly state that you have enough information and what the next step is, for example: "Great, I have enough information to generate the Landed Cost + Risk Report."

Output Format:
You must always return a strictly valid JSON object. Do not include markdown or any other text outside the JSON structure. The JSON should have 'assistant_message', 'filled_fields', 'next_focus_field', 'state_updates', and 'ready_for_analysis'.

Example Output:
{
  "assistant_message": "Thanks! What country will you be importing into?",
  "filled_fields": ["product_idea"],
  "next_focus_field": "import_country",
  "state_updates": {
    "product_idea": "custom-printed coffee mugs"
  },
  "ready_for_analysis": false
}
`;

const AiResponseSchema = z.object({
  assistant_message: z.string(),
  filled_fields: z.array(z.string()).optional(),
  next_focus_field: z.string().optional(),
  state_updates: z.object({
    product_idea: z.string().optional(),
    import_country: z.string().optional(),
    sales_channel: z.enum(['amazon_fba', 'tiktok_shop', 'shopify', 'wholesale', 'other']).optional(),
    volume_plan: z.string().optional(),
    timeline: z.string().optional(),
    main_risk_concern: z.enum(['duty', 'quality', 'delay', 'compliance', 'other']).optional().nullable(),
    certifications_needed: z.string().optional(),
    extra_notes: z.string().optional(),
  }),
  ready_for_analysis: z.boolean(),
});

async function getApiKey(): Promise<string> {
  if (typeof process === 'undefined' || !process.env.GEMINI_API_KEY) {
    throw new Error("GEMINI_API_KEY is not configured.");
  }
  return process.env.GEMINI_API_KEY;
}

export async function handleAiChat(
  history: ChatMessage[],
  currentState: SourcingConversationState
): Promise<ConversationalResponse> {
  try {
    const apiKey = await getApiKey();
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: "gemini-2.5-pro",
      generationConfig: {
        responseMimeType: "application/json",
      },
      systemInstruction: SYSTEM_PROMPT,
    });

    const context = {
      history,
      currentState,
    };

    const result = await model.generateContent(JSON.stringify(context));
    const text = result.response.text();
    const parsed = JSON.parse(text);

    const validation = AiResponseSchema.safeParse(parsed);

    if (!validation.success) {
      console.error("Invalid AI response schema:", validation.error);
      throw new Error("Invalid AI response schema");
    }

    const { assistant_message, state_updates, ready_for_analysis, next_focus_field } = validation.data;

    const updatedState: SourcingConversationState = {
      ...currentState,
      ...state_updates,
      messages: [...history, { role: 'assistant', content: assistant_message }],
      ready_for_analysis: ready_for_analysis,
      next_focus_field: next_focus_field,
    };

    return {
      assistantMessage: assistant_message,
      updatedState: updatedState,
    };

  } catch (error) {
    console.error("[handleAiChat] Error processing chat", error);
    const updatedState: SourcingConversationState = {
        ...currentState,
        messages: [...history, { role: 'assistant', content: "Sorry, I had trouble understanding that. Could you please rephrase?" }],
        ready_for_analysis: false,
    };
    return {
      assistantMessage: "Sorry, I had trouble understanding that. Could you please rephrase?",
      updatedState,
    };
  }
}
export function buildAnalyzerInputFromConversation(
  state: SourcingConversationState
): { input: string } {
  const {
    product_idea,
    import_country,
    sales_channel,
    volume_plan,
    timeline,
    main_risk_concern,
    certifications_needed,
    extra_notes,
  } = state;

  if (product_idea && !import_country && !sales_channel && !volume_plan) {
    return { input: product_idea };
  }

  const parts = [
    `Product idea: ${product_idea || 'Not specified'}`,
    import_country ? `Importing to: ${import_country}` : '',
    sales_channel ? `Sales channel: ${sales_channel}` : '',
    volume_plan ? `Volume plan: ${volume_plan}` : '',
    timeline ? `Timeline: ${timeline}` : '',
    main_risk_concern ? `Main risk concern: ${main_risk_concern}` : '',
    certifications_needed ? `Certifications needed: ${certifications_needed}` : '',
    extra_notes ? `Extra notes: ${extra_notes}` : '',
  ];

  const inputText = parts.filter(Boolean).join('. ');

  return {
    input: inputText || 'No product description provided.',
  };
}