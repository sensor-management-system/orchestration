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
  <div>
    <v-row>
      <v-col cols="12">
        <label>Visibility / Permissions</label>
        <VisibilityChip
          v-model="value.visibility"
        />
        <PermissionGroupChips
          :value="[value.permissionGroup]"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Label</label>
        {{ value.label }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Status</label>
        {{ value.status | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <label>Start date</label>
        <span v-if="value.startDate">
          {{ value.startDate | dateToDateTimeString | orDefault }}
          <span class="text-caption text--secondary">(UTC)</span>
        </span>
      </v-col>
      <v-col cols="12" md="3">
        <label>End date</label>
        <span v-if="value.endDate">
          {{ value.endDate | dateToDateTimeString | orDefault }}
          <span class="text-caption text--secondary">(UTC)</span>
        </span>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'

import { dateToDateTimeString } from '@/utils/dateHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'
import VisibilityChip from '@/components/VisibilityChip.vue'
import PermissionGroupChips from '@/components/PermissionGroupChips.vue'

@Component({
  components: {
    PermissionGroupChips,
    VisibilityChip,
    DateTimePicker
  },
  filters: {
    dateToDateTimeString
  }
})
export default class ConfigurationsBasicDataForm extends Vue {
  @Prop({ default: false, type: Boolean }) readonly readonly!: boolean
  @Prop({
    default: () => new Configuration(),
    required: true,
    type: Configuration
  })
  readonly value!: Configuration

  async mounted () {
    await this.$store.dispatch('configurations/loadConfigurationsStates')
  }

  get configurationStates () { return this.$store.state.configurations.configurationStates }
  // @ts-ignore
  update (key: string, value: any) {
    // @ts-ignore
    if (typeof this.value[key] !== 'undefined') {
      const newObj = Configuration.createFromObject(this.value)
      // @ts-ignore
      newObj[key] = value
      this.$emit('input', newObj)
    }
  }

  public validateForm (): boolean {
    return (this.$refs.basicDataForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>
