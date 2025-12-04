/**
 * Type definitions for category-specific questions.
 * These types match the structure in web/data/category-questions.json
 */

export type QuestionType = 'multiple_choice' | 'text' | 'number' | 'yes_no';

export interface CategoryQuestion {
  /** Unique identifier for the question */
  id: string;

  /** The question text */
  question: string;

  /** Type of question */
  type: QuestionType;

  /** Options for multiple choice questions */
  options?: string[];

  /** Importance level for determining when to ask */
  importance: 'high' | 'medium' | 'low';

  /** Help text or explanation */
  helpText?: string;

  /** Whether this question is required */
  required?: boolean;
}

export interface CategoryQuestionsConfig {
  /** Category ID this question set belongs to */
  categoryId: string;

  /** Human-readable category label */
  categoryLabel: string;

  /** Array of questions for this category */
  questions: CategoryQuestion[];
}

export interface CategoryQuestionsData {
  categories: CategoryQuestionsConfig[];
}

