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

/**
 * A mixin component for standard form validation rules
 * @extends Vue
 */
@Component
export class Rules extends Vue {
  /**
   * various rules for validating form inputs
   *
   * @property {function} required - triggers when value is empty
   * @property {function} validUrl - triggers when value does not start with http(s):// or ftp://
   */
  private rules: Object = {
    required: (v: any) => {
      switch (typeof v) {
        case 'string':
          return v.trim() !== '' || 'Required'
        case 'number':
          return true
      }
      return !!v || 'Required'
    },
    validUrl: (v: string) => v.match(/^https*:\/\//) !== null || v.match(/^ftp*:\/\//) !== null || 'URL not valid',
    numeric: (v: any) => !isNaN(parseInt(v)) || 'Number expected',
    numericOrEmpty: (v: any) => {
      if (v === '' || v === null || v === undefined) {
        return true
      }
      return !isNaN(parseInt(v)) || 'Expected to be numeric or empty'
    }
  }
}
