/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/**
 * @file provides a mixin component for standard form validation rules
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { Vue, Component } from 'nuxt-property-decorator'

import UploadConfig from '@/config/uploads'

/**
 * A mixin component for standard form validation rules for uploads
 * @extends Vue
 */
@Component
export class UploadRules extends Vue {
  /**
   * various rules for validating form inputs
   *
   */
  private uploadRules: Object = {
    maxSize: (f: File | null) => {
      const uploadSizeLimit = this.$store.state.files.uploadSizeLimit
      if (f !== null && f.size > uploadSizeLimit) {
        return 'File is too large'
      }
      return true
    },
    mimeTypeAllowed: (f: File | null) => {
      if (f === null) {
        return true
      }

      const mimeTypeIndex = UploadConfig.allowedMimeTypes.indexOf(f.type)
      if (mimeTypeIndex < 0) {
        if (f.type) {
          return '' + f.type + ' is not supported'
        }
        return 'Unsupported file type'
      }
      return true
    }
  }
}
