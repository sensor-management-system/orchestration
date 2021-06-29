<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <v-card>
    <v-card-subtitle class="pb-0">
      <v-row no-gutters>
        <v-col>
          {{ value.updateDate | toUtcDate }}
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <slot name="menu" />
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-card-title class="pt-0">
      {{ updateName }}
    </v-card-title>
    <v-card-subtitle class="pb-1">
      <v-row
        no-gutters
      >
        <v-col>
          {{ value.contact.toString() }}
        </v-col>
        <v-col
          align-self="end"
          class="text-right"
        >
          <slot name="actions" />
          <v-btn
            icon
            @click.stop.prevent="toggleVisibility()"
          >
            <v-icon>{{ isVisible() ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-subtitle>
    <v-expand-transition>
      <div
        v-show="isVisible(value.id)"
      >
        <v-card-text
          class="grey lighten-5 text--primary pt-2"
        >
          <v-row dense>
            <v-col cols="12" md="4">
              <label>
                Version
              </label>
              {{ value.version }}
            </v-col>
            <v-col cols="12" md="4">
              <label>
                Repository
              </label>
              <!-- eslint-disable-next-line vue/no-v-html -->
              <span v-html="repositoryLink" />
            </v-col>
          </v-row>
          <label>Description</label>
          {{ value.description }}
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
/**
 * @file provides a component for a Software Update Action card
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { protocolsInUrl } from '@/utils/urlHelpers'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

/**
 * A class component for Software Update Action card
 * @extends Vue
 */
@Component({
  filters: {
    toUtcDate: dateToDateTimeString
  }
})
// @ts-ignore
export default class SoftwareUpdateActionCard extends Vue {
  private showDetails: boolean = false

  /**
   * a SoftwareUpdateAction
   */
  @Prop({
    default: () => new SoftwareUpdateAction(),
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: SoftwareUpdateAction

  /**
   * whether the card expansion is shown or not
   *
   * @return {boolean} whether the card expansion is shown or not
   */
  isVisible (): boolean {
    return this.showDetails
  }

  /**
   * toggles the shown state of the card expansion
   *
   */
  toggleVisibility (): void {
    this.showDetails = !this.showDetails
  }

  /**
   * returns an URL as an link
   *
   * All characters except 0-9, a-z, :, / and . are removed from the link to
   * prevent xss attacks. If the URL doesn't start with a known protocol, it
   * won't be wrapped.
   *
   * @return {string} the url wrapped in an HTML link element
   */
  get repositoryLink (): string {
    // eslint-disable-next-line no-useless-escape
    const url = this.value.repositoryUrl.replace(/[^a-zA-Z0-9:\/.-]/g, '')
    if (protocolsInUrl(['https', 'http', 'ftp', 'ftps', 'sftp', 'dav', 'davs'], url)) {
      return '<a href="' + url + '" target="_blank">' + url + '</a>'
    }
    return url
  }

  /**
   * returns the name of the update
   *
   * @returns {string} the update name
   */
  get updateName (): string {
    if (this.value.softwareTypeName.toLowerCase() === 'others') {
      return 'Device Software Update'
    }
    return this.value.softwareTypeName + ' Update'
  }
}
</script>
