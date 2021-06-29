/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
    validUrl: (v: string) => v.match(/^https*:\/\//) !== null || v.match(/^ftp*:\/\//) !== null || 'URL not valid',
    numericRequired: (v: number | null | undefined) => !!v || v === 0 || v === 0.0 || 'Required'
  }
}
