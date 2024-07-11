/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/**
 * @file provides a mixin component with helper functions to handle attachments
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { Vue, Component } from 'nuxt-property-decorator'
import { Attachment } from '@/models/Attachment'

import { removeTrailingSlash } from '@/utils/urlHelpers'

/**
 * A mixin component with helper functions to handle attachments
 * @extends Vue
 */
@Component
export class AttachmentsMixin extends Vue {
  /**
   * returns a filename from a full filepath
   *
   * @return {string} the filename
   */
  filename (attachment: Attachment): string {
    const UNKNOWN_FILENAME = 'unknown filename'

    if (attachment.url === '') {
      return UNKNOWN_FILENAME
    }
    const url = removeTrailingSlash(attachment.url)
    const paths = url.split('/')
    if (!paths.length) {
      return UNKNOWN_FILENAME
    }
    // @ts-ignore
    return paths.pop()
  }

  /**
   * returns a material design icon name based on the file type extension
   *
   * @return {string} a material design icon name
   */
  filetypeIcon (attachment: Attachment): string {
    let extension = ''
    const paths = this.filename(attachment).split('.')
    if (paths.length) {
      // @ts-ignore
      extension = paths.pop().toLowerCase()
    }
    switch (extension) {
      case 'png':
      case 'jpg':
      case 'jpeg':
      case 'gif':
      case 'svg':
      case 'webp':
        return 'mdi-image'
      case 'pdf':
        return 'mdi-file-pdf-box'
      case 'doc':
      case 'docx':
      case 'odt':
        return 'mdi-text-box'
      default:
        return 'mdi-paperclip'
    }
  }
}
