<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
