/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { ReleaseNotesSerializer } from '@/serializers/custom/ReleaseNotesSerializer'

describe('ReleaseNotesSerializer', () => {
  describe('version regex', () => {
    it('should match version lines correctly', () => {
      const testData = [
        { line: '## 1.0.0 - 2020-01-01', expectedVersion: '1.0.0', expectedDate: '2020-01-01' },
        { line: '## 222.222.222 - 2222-02-22', expectedVersion: '222.222.222', expectedDate: '2222-02-22' }
      ]
      for (const test of testData) {
        const parsed = ReleaseNotesSerializer.getVersionRegex().exec(test.line)
        expect(parsed![1]).toEqual(test.expectedVersion)
        expect(parsed![2]).toEqual(test.expectedDate)
      }
    })

    it('should not match unreleased versions', () => {
      const testData = [
        { line: '## 1.0.0 (Unreleased)' }
      ]
      for (const test of testData) {
        const parsed = ReleaseNotesSerializer.getVersionRegex().exec(test.line)
        expect(parsed).toBeNull()
      }
    })
  })

  describe('section regex', () => {
    it('should match section lines correctly', () => {
      const testData = [
        { line: 'Added:', expectedSection: 'Added' },
        { line: 'Fixed:', expectedSection: 'Fixed' },
        { line: 'Changed:', expectedSection: 'Changed' }
      ]
      for (const test of testData) {
        const parsed = ReleaseNotesSerializer.getSectionRegex().exec(test.line)
        expect(parsed![1]).toEqual(test.expectedSection)
      }
    })
  })

  describe('merge request regex', () => {
    it('should match MR strings correctly', () => {
      const testData = [
        {
          line: 'Lorem ipsum dolor sit amet ([Merge Request](https://mr.com))',
          expectedMRString: '([Merge Request](https://mr.com))',
          expectedMRLink: 'https://mr.com'
        },
        {
          line: 'Lorem ipsum ([Merge Request](https://mr.com)) dolor sit amet ([Wiki](https://wiki.com))',
          expectedMRString: '([Merge Request](https://mr.com))',
          expectedMRLink: 'https://mr.com'
        }
      ]
      for (const test of testData) {
        const parsed = ReleaseNotesSerializer.getMrRegex().exec(test.line)
        expect(parsed![0]).toEqual(test.expectedMRString)
        expect(parsed![1]).toEqual(test.expectedMRLink)
      }
    })
  })

  describe('wiki regex', () => {
    it('should match Wiki strings correctly', () => {
      const testData = [
        {
          line: 'Lorem ipsum dolor sit amet ([Wiki](https://wiki.com))',
          expectedWikiString: '([Wiki](https://wiki.com))',
          expectedWikiLink: 'https://wiki.com'
        },
        {
          line: 'Lorem ipsum ([Wiki](https://wiki.com)) dolor sit amet ([Merge Request](https://mr.com))',
          expectedWikiString: '([Wiki](https://wiki.com))',
          expectedWikiLink: 'https://wiki.com'
        }
      ]
      for (const test of testData) {
        const parsed = ReleaseNotesSerializer.getWikiRegex().exec(test.line)
        expect(parsed![0]).toEqual(test.expectedWikiString)
        expect(parsed![1]).toEqual(test.expectedWikiLink)
      }
    })
  })

  it('should parse a changelog correctly', () => {
    const testData = [
      {
        rawText: '\n' +
          '## 1.0.1 - 2001-01-01  \n' +
          'Fixed:  \n' +
          '- Fixed an issue where the "Log Out" button would log you back in instead. ([Merge Request](https://example.com)) \n' +
          '- Fixed a bug that caused our Terms of Service to be written in pirate slang.  \n' +
          '\n' +
          'Added:  \n' +
          '- Added an AI assistant that only speaks in Morse code. ([Wiki](https://wiki.com))  \n' +
          '\n' +
          'Changed:  \n' +
          '- Changed all buttons to be slightly off-center just to annoy perfectionists. ([Merge Request](https://example.com)) ([Wiki](https://wiki.com)) \n' +
          '- Changed all device pictures to random cat images.  \n\n' +
          '## 1.0.0 - 2000-01-01  \n' +
          'Added:  \n' +
          ' - SMS now sends SMS when a registered device explodes.',
        expectedReleaseNotes: [
          {
            tag: '1.0.1',
            date: '2001-01-01',
            notes: {
              fixed: [
                {
                  text: 'Fixed an issue where the "Log Out" button would log you back in instead.',
                  linkToMergeRequest: 'https://example.com',
                  linkToWiki: null
                },
                {
                  text: 'Fixed a bug that caused our Terms of Service to be written in pirate slang.',
                  linkToMergeRequest: null,
                  linkToWiki: null
                }
              ],
              changed: [
                {
                  text: 'Changed all buttons to be slightly off-center just to annoy perfectionists.',
                  linkToMergeRequest: 'https://example.com',
                  linkToWiki: 'https://wiki.com'
                },
                {
                  text: 'Changed all device pictures to random cat images.',
                  linkToMergeRequest: null,
                  linkToWiki: null
                }
              ],
              added: [
                {
                  text: 'Added an AI assistant that only speaks in Morse code.',
                  linkToMergeRequest: null,
                  linkToWiki: 'https://wiki.com'
                }
              ]
            }
          },
          {
            tag: '1.0.0',
            date: '2000-01-01',
            notes: {
              fixed: [],
              changed: [],
              added: [
                {
                  text: 'SMS now sends SMS when a registered device explodes.',
                  linkToMergeRequest: null,
                  linkToWiki: null
                }
              ]
            }
          }
        ]
      }
    ]
    for (const test of testData) {
      const parsed = new ReleaseNotesSerializer().convertChangelogTextToModel(test.rawText)
      expect(parsed).toEqual(test.expectedReleaseNotes)
    }
  })
})
