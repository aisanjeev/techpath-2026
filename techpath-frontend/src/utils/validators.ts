/**
 * Form Validation Utilities
 */

export interface ValidationResult {
  valid: boolean;
  message?: string;
}

/**
 * Validates an email address
 */
export function validateEmail(email: string): ValidationResult {
  if (!email) {
    return { valid: false, message: 'Email is required' };
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return { valid: false, message: 'Please enter a valid email address' };
  }

  return { valid: true };
}

/**
 * Validates a required field
 */
export function validateRequired(value: string, fieldName = 'This field'): ValidationResult {
  if (!value || value.trim() === '') {
    return { valid: false, message: `${fieldName} is required` };
  }

  return { valid: true };
}

/**
 * Validates minimum length
 */
export function validateMinLength(
  value: string,
  minLength: number,
  fieldName = 'This field'
): ValidationResult {
  if (value.length < minLength) {
    return {
      valid: false,
      message: `${fieldName} must be at least ${minLength} characters`,
    };
  }

  return { valid: true };
}

/**
 * Validates maximum length
 */
export function validateMaxLength(
  value: string,
  maxLength: number,
  fieldName = 'This field'
): ValidationResult {
  if (value.length > maxLength) {
    return {
      valid: false,
      message: `${fieldName} must be less than ${maxLength} characters`,
    };
  }

  return { valid: true };
}

/**
 * Validates a phone number
 */
export function validatePhone(phone: string): ValidationResult {
  if (!phone) {
    return { valid: true }; // Phone is optional
  }

  // Basic phone validation - allows various formats
  const phoneRegex = /^[\d\s\-\+\(\)]{10,20}$/;
  if (!phoneRegex.test(phone)) {
    return { valid: false, message: 'Please enter a valid phone number' };
  }

  return { valid: true };
}

/**
 * Validates a URL
 */
export function validateUrl(url: string): ValidationResult {
  if (!url) {
    return { valid: true }; // URL is optional
  }

  try {
    new URL(url);
    return { valid: true };
  } catch {
    return { valid: false, message: 'Please enter a valid URL' };
  }
}

/**
 * Validates a password
 */
export function validatePassword(password: string): ValidationResult {
  if (!password) {
    return { valid: false, message: 'Password is required' };
  }

  if (password.length < 8) {
    return { valid: false, message: 'Password must be at least 8 characters' };
  }

  if (!/[A-Z]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one uppercase letter' };
  }

  if (!/[a-z]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one lowercase letter' };
  }

  if (!/[0-9]/.test(password)) {
    return { valid: false, message: 'Password must contain at least one number' };
  }

  return { valid: true };
}

/**
 * Validates password confirmation
 */
export function validatePasswordMatch(password: string, confirmPassword: string): ValidationResult {
  if (password !== confirmPassword) {
    return { valid: false, message: 'Passwords do not match' };
  }

  return { valid: true };
}

/**
 * Contact form validation
 */
export interface ContactFormData {
  name: string;
  email: string;
  company?: string;
  message: string;
  service?: string;
}

export function validateContactForm(data: ContactFormData): Record<string, string> {
  const errors: Record<string, string> = {};

  const nameResult = validateRequired(data.name, 'Name');
  if (!nameResult.valid) errors.name = nameResult.message!;

  const emailResult = validateEmail(data.email);
  if (!emailResult.valid) errors.email = emailResult.message!;

  const messageResult = validateRequired(data.message, 'Message');
  if (!messageResult.valid) errors.message = messageResult.message!;

  const messageLengthResult = validateMinLength(data.message, 10, 'Message');
  if (!messageLengthResult.valid) errors.message = messageLengthResult.message!;

  return errors;
}

/**
 * Newsletter subscription validation
 */
export function validateNewsletterSubscription(email: string): ValidationResult {
  return validateEmail(email);
}

