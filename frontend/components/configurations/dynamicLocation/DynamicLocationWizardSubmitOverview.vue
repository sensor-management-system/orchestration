<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <div>
    <dynamic-location-action-data v-if="newDynamicLocationAction" :value="newDynamicLocationAction" :devices="availableDevices" />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { mapGetters } from 'vuex'
import DynamicLocationActionData from '@/components/configurations/dynamicLocation/DynamicLocationActionData.vue'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { ActiveDevicesWithPropertiesForDateGetter } from '@/store/configurations'

@Component({
  components: { DynamicLocationActionData },
  filters: { dateToDateTimeStringHHMM },
  computed: {
    ...mapGetters('configurations', ['activeDevicesWithPropertiesForDate'])
  }
})
export default class DynamicLocationWizardSubmitOverview extends Vue {
  @Prop({
    required: true,
    type: Object
  })
    newDynamicLocationAction!: DynamicLocationAction

  activeDevicesWithPropertiesForDate!: ActiveDevicesWithPropertiesForDateGetter

  // vuex definition for typescript check
  get availableDevices () {
    return this.activeDevicesWithPropertiesForDate(this.newDynamicLocationAction.beginDate, this.newDynamicLocationAction.endDate)
  }
}
</script>

<style scoped>
.table-border-left {
  border-left: 1px solid #dddddd;
}
</style>
