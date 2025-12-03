import { z } from 'zod';

/**
 * @fileoverview Zod schemas for validating API inputs.
 * @description This file contains the Zod schemas used to validate the
 * structure and types of incoming API requests.
 */

// Schema for the sample request form submission
export const sampleRequestSchema = z.object({
  name: z.string().min(2, { message: "Name must be at least 2 characters." }).trim(),
  workEmail: z.string().email({ message: "Please enter a valid email address." }),
  company: z.string().trim().optional(),
  useCase: z.string().min(10, { message: "Please describe your use case in at least 10 characters." }).trim(),
});

// Type alias for the validated data
export type SampleRequestData = z.infer<typeof sampleRequestSchema>;