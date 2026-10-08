/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import { renderMaintenanceMessage } from '@/utils/maintenanceMessage'

describe('maintenance message sanitation', () => {
  it('preserves Markdown formatting and safe links', () => {
    const html = renderMaintenanceMessage('## Maintenance\n\n**Tomorrow**: [Details](https://example.org)')
    expect(html).toContain('<h2>Maintenance</h2>')
    expect(html).toContain('<strong>Tomorrow</strong>')
    expect(html).toContain('href="https://example.org"')
  })

  it.each([
    '<script>alert(1)</script>',
    '<img src=x onerror="alert(1)">',
    '<svg onload="alert(1)"></svg>',
    '<iframe src="https://example.org"></iframe>',
    '[Click](javascript:alert%281%29)',
    '<a href="jav&#x61;script:alert(1)" onclick="alert(1)">Click</a>',
    '<p style="background:url(https://example.org)">Text</p>'
  ])('removes unsafe content: %s', (markdown) => {
    const html = renderMaintenanceMessage(markdown)
    expect(html).not.toMatch(/<script|<img|<svg|<iframe|javascript:|onerror|onload|onclick|style=/i)
  })
})
