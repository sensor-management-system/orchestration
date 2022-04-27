<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
  <v-form
    ref="mountForm"
    @submit.prevent
  >
    <v-row>
      <v-col
        cols="12"
        md="3"
      >
        <v-text-field
          :value="mountAction.offsetX"
          label="Offset (x)"
          type="number"
          readonly
        />
      </v-col>
      <v-col
        cols="12"
        md="3"
      >
        <v-text-field
          v-model.number="mountAction.offsetY"
          label="Offset (y)"
          type="number"
          readonly
        />
      </v-col>
      <v-col
        cols="12"
        md="3"
      >
        <v-text-field
          :value="mountAction.offsetZ"
          label="Offset (z)"
          type="number"
          readonly
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          :value="mountAction.contact"
          label="Contact"
          readonly
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="12">
        <v-textarea
          :value="mountAction.description"
          label="Description"
          rows="3"
          readonly
        />
      </v-col>
    </v-row>
  </v-form>
</template>
<script lang="ts">

import { Component, Prop, Vue, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'

@Component
export default class ConfigurationsPlatformDeviceMountData extends mixins(Rules) {
  @Prop({
    required:true,
    type: Object
  })
  private mountAction!:DeviceMountAction|PlatformMountAction
}
</script>

<style scoped>
</style>
