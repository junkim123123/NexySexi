/**
 * Helper functions for accessing category-specific questions.
 * 
 * During alpha, questions are stored in JSON files.
 * Eventually, these may be moved to a database or admin UI.
 */

import type { CategoryQuestionsConfig, CategoryQuestionsData, CategoryQuestion } from '../types/categoryQuestions';

// Lazy load the questions data
let questionsCache: CategoryQuestionsData | null = null;

function loadCategoryQuestions(): CategoryQuestionsData {
  if (questionsCache) {
    return questionsCache;
  }

  try {
    // Try to load the actual questions file, fall back to empty if not found
    const questionsModule = require('@/data/category-questions.json');
    questionsCache = questionsModule as CategoryQuestionsData;
  } catch (error) {
    // If the file doesn't exist yet, return empty structure
    console.warn('[CategoryQuestions] category-questions.json not found. Using empty questions. Create the file from category-questions.sample.json');
    questionsCache = { categories: [] };
  }

  return questionsCache;
}

/**
 * Get category-specific questions for a given category ID.
 * 
 * @param categoryId - The category identifier (e.g., "baby_teether")
 * @returns The questions configuration for the category, or undefined if not found
 */
export function getCategoryQuestions(categoryId: string): CategoryQuestionsConfig | undefined {
  const questions = loadCategoryQuestions();
  return questions.categories.find(cat => cat.categoryId === categoryId);
}

/**
 * Get high-priority questions for a category (importance === 'high').
 * 
 * @param categoryId - The category identifier
 * @returns Array of high-priority questions
 */
export function getHighPriorityQuestions(categoryId: string): CategoryQuestion[] {
  const config = getCategoryQuestions(categoryId);
  if (!config) return [];

  return config.questions.filter(q => q.importance === 'high');
}

/**
 * Get all questions for a category, sorted by importance (high -> medium -> low).
 * 
 * @param categoryId - The category identifier
 * @returns Array of questions sorted by importance
 */
export function getAllCategoryQuestions(categoryId: string): CategoryQuestion[] {
  const config = getCategoryQuestions(categoryId);
  if (!config) return [];

  const importanceOrder = { high: 0, medium: 1, low: 2 };
  return [...config.questions].sort((a, b) => {
    return importanceOrder[a.importance] - importanceOrder[b.importance];
  });
}

/**
 * Check if a category has any questions defined.
 * 
 * @param categoryId - The category identifier
 * @returns true if questions exist for this category
 */
export function hasCategoryQuestions(categoryId: string): boolean {
  const config = getCategoryQuestions(categoryId);
  return config !== undefined && config.questions.length > 0;
}

