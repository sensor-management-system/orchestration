<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
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
  <div>
    <v-row>
      <v-col cols="12" md="6">
        <label>Manufacturer</label>
        {{ value.manufacturerName | orDefault }}
      </v-col>
      <v-col cols="12" md="6">
        <label>Model</label>
        {{ value.model | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <label>External system</label>
        {{ value.externalSystemName | orDefault }}
      </v-col>
      <v-col cols="12" md="6">
        <label>External system URL</label>
        {{ value.externalSystemUrl | orDefault }}
        <a v-if="value.externalSystemUrl.length > 0" :href="value.externalSystemUrl" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { ManufacturerModel } from '@/models/ManufacturerModel'

@Component({})
export default class ManufacturerModelBasicData extends Vue {
  @Prop({
    default: () => new ManufacturerModel(),
    type: ManufacturerModel
  })
  readonly value!: ManufacturerModel
}
</script>
