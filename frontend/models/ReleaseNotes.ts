/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2025
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export interface ChangelogEntry {
  text: string,
  linkToMergeRequest: string|null
  linkToWiki: string|null
}

export interface Release {
  tag: string,
  date: string,
  notes: {
    added: ChangelogEntry[],
    changed: ChangelogEntry[],
    fixed: ChangelogEntry[]
  }
}
