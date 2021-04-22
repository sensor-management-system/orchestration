/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */

/**
 * @file provides a mixin component with helper functions to handle attachments
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { Vue, Component } from 'nuxt-property-decorator'
import { Attachment } from '@/models/Attachment'

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
    const paths = attachment.url.split('/')
    if (!paths.length) {
      return UNKNOWN_FILENAME
    }
    // @ts-ignore
    return paths.pop()
  }

  /**
   * returns the timestamp of the upload date
   *
   * @TODO this must be implemented when the file API is ready
   * @return {string} a readable timestamp
   */
  uploadedDateTime (_attachment: Attachment): string {
    return '2020-06-17 16:35 (TODO)'
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
