<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
  <mount-action-date-form
    :value="mountAction"
    :begin-date-rules="beginDateRules"
    :end-date-rules="endDateRules"
    :end-required="selectedNodeEndDate !== null"
    @input="update"
  />
</template>

<script lang="ts">
import { Component, Vue, Prop, PropSync } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { MountAction } from '@/models/MountAction'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

import MountActionDateForm from '@/components/configurations/MountActionDateForm.vue'

@Component({
  components: {
    MountActionDateForm
  },
  filters: { dateToDateTimeStringHHMM }
})
export default class MountWizardDateSelect extends Vue {
  @PropSync('selectedDate', {
    required: true,
    type: Object
  })
    syncedSelectedDate!: DateTime

  @PropSync('selectedEndDate', {
    default: null,
    required: false,
    type: Object
  })
    syncedSelectedEndDate!: DateTime | null

  @Prop({
    default: null,
    required: false,
    type: Object
  })
  readonly selectedNodeBeginDate!: DateTime

  @Prop({
    default: null,
    required: false,
    type: Object
  })
  readonly selectedNodeEndDate!: DateTime | null

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly beginDateRules!: ((value: DateTime | null) => string | boolean)[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly endDateRules!: ((value: DateTime | null) => string | boolean)[]

  get mountAction (): MountAction {
    return MountAction.createFromObject({
      id: '',
      parentPlatform: null,
      beginContact: new Contact(), // we don't need a real contact here
      beginDate: this.syncedSelectedDate,
      endContact: null,
      endDate: this.syncedSelectedEndDate || null,
      beginDescription: '',
      endDescription: '',
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0
    })
  }

  update (mountAction: MountAction) {
    this.syncedSelectedDate = mountAction.beginDate
    this.syncedSelectedEndDate = mountAction.endDate
  }
}
</script>

<style scoped>
</style>
