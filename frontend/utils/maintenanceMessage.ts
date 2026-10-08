/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import DOMPurify from 'dompurify'
import { marked } from 'marked'

export function renderMaintenanceMessage (markdown: string): string {
  // Sanitize after Markdown conversion. Keep formatting and links, but no
  // images, embedded content, styles, event handlers, or unsafe URL schemes.
  return DOMPurify.sanitize(marked(markdown), {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'del', 'a', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td'],
    ALLOWED_ATTR: ['href', 'title'],
    ALLOW_DATA_ATTR: false,
    ALLOW_ARIA_ATTR: false
  })
}
