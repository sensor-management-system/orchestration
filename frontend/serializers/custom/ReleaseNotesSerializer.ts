/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2025
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { ChangelogEntry, Release } from '@/models/ReleaseNotes'

type SectionKey = 'added' | 'fixed' | 'changed'

export class ReleaseNotesSerializer {
  // regex to match a new version entry
  // ywe use <MAJOR>.<MINOR>.<PATCH> - <YYYY>-<MM>-<DD>
  public static getVersionRegex () {
    return /## (\d+\.\d+\.\d+) - (\d{4}-\d{2}-\d{2})/g
  }

  // regex to match a new section within a version entry,
  // we use 'Added', 'Fixed' and 'Changed'
  public static getSectionRegex () {
    return /(Added|Fixed|Changed):/g
  }

  // regex to match a release note entry within a section,
  // we start every line with a dash
  public static getNoteEntryRegex () {
    return /^\s*-\s.*$/g
  }

  // regex to match a link to a Merge Request
  // we use '([Merge Request](<LINK>))'
  public static getMrRegex () {
    return /\(\[(?:\w*\sRequest|MR\d+)]\((.*?)\)\)/
  }

  // regex to match a link to the Wiki
  // we use '([Wiki](<LINK>))',
  public static getWikiRegex () {
    return /\(\[Wiki]\((.*?)\)\)/
  }

  convertChangelogTextToModel (rawText: string | null): Release[] {
    if (!rawText) {
      return []
    }
    const lines = rawText.split('\n')

    const changelog = []
    let currentVersion: Release | null = null
    let currentSection: SectionKey | null = null

    for (const line of lines) {
      if (!line.trim()) {
        continue
      }

      const versionMatch = ReleaseNotesSerializer.getVersionRegex().exec(line)
      if (versionMatch) {
        if (currentVersion) {
          changelog.push(currentVersion)
        }
        currentVersion = {
          tag: versionMatch[1],
          date: versionMatch[2],
          notes: {
            added: [],
            fixed: [],
            changed: []
          }
        }
        continue
      }

      const sectionMatch = ReleaseNotesSerializer.getSectionRegex().exec(line)
      if (sectionMatch && currentVersion) {
        const sectionKey = sectionMatch[1].toLowerCase()
        if (['added', 'fixed', 'changed'].includes(sectionKey)) {
          currentSection = sectionKey as SectionKey
        }
        continue
      }

      const noteEntryMatch = ReleaseNotesSerializer.getNoteEntryRegex().exec(line)
      if (noteEntryMatch && currentSection && currentVersion) {
        const text = line.trimStart().substring(2).trim()
        const mrMatch = text.match(ReleaseNotesSerializer.getMrRegex())
        const wikiMatch = text.match(ReleaseNotesSerializer.getWikiRegex())
        const entry: ChangelogEntry = {
          text: text.replace(ReleaseNotesSerializer.getMrRegex(), '').replace(ReleaseNotesSerializer.getWikiRegex(), '').trim(),
          linkToMergeRequest: mrMatch ? mrMatch[1] : null,
          linkToWiki: wikiMatch ? wikiMatch[1] : null
        }
        currentVersion.notes[currentSection].push(entry)
      }
    }

    if (currentVersion) {
      changelog.push(currentVersion)
    }

    return changelog
  }
}
