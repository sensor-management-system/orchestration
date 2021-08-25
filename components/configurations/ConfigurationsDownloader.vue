<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
  <v-menu
    close-on-click
    close-on-content-click
    offset-x
    left
    z-index="999"
  >
    <template #activator="{ on }">
      <v-btn
        icon
        v-on="on"
      >
        <v-icon
          dense
        >
          mdi-file-download
        </v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item
        dense
        @click.prevent="exportCsv"
      >
        <v-list-item-content>
          <v-list-item-title>
            <v-icon
              left
            >
              mdi-table
            </v-icon>
            CSV
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { saveAs } from 'file-saver'

import { ConfigurationSearcher } from '@/services/sms/ConfigurationApi'

@Component
export default class ConfigurationsDownloader extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly lastActiveSearcher!: ConfigurationSearcher;

  exportCsv () { // TODO lastActiveSearcher ist nur noch in der ConfigurationsSearch
    this.lastActiveSearcher.findMatchingAsCsvBlob().then((blob) => {
      saveAs(blob, 'configurations.csv')
    }).catch((_err) => {
      this.$store.commit('snackbar/setError', 'CSV export failed')
    })
  }
}
</script>

<style scoped>

</style>
