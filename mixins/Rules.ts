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
    required: (v: string) => !!v || 'Required',
    validUrl: (v: string) => v.match(/^https*:\/\//) !== null || v.match(/^ftp*:\/\//) !== null || 'URL not valid'
  }
}
