/**
 * Application configuration settings.
 */

export const config = {
  /**
   * API base URL - defaults to localhost:8000 for development
   */
  API_BASE_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  
  /**
   * Environment
   */
  NODE_ENV: process.env.NODE_ENV || "development",
  
  /**
   * Whether we're in development mode
   */
  isDevelopment: process.env.NODE_ENV === "development",
  
  /**
   * Whether we're in production mode
   */
  isProduction: process.env.NODE_ENV === "production",
} as const;

// Export commonly used values for convenience
export const { API_BASE_URL } = config;
