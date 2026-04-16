import { z } from "zod";

export const plannerSchema = z.object({
  exam: z.string().trim().min(2, "Exam name is required"),
  state: z.string().trim().min(2, "State is required"),
  hoursPerDay: z.number().min(1).max(16)
});

export const chatSchema = z.object({
  message: z.string().trim().min(1, "Message is required").max(4000),
  context: z
    .object({
      exam: z.string().trim().min(2).optional(),
      language: z.string().trim().min(2).optional()
    })
    .partial()
    .optional()
});

export type PlannerInput = z.infer<typeof plannerSchema>;
export type ChatInput = z.infer<typeof chatSchema>;
