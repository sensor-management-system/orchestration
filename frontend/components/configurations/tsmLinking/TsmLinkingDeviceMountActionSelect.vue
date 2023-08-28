<!--
 Web client of the Sensor Management System software developed within the
 Helmholtz DataHub Initiative by GFZ and UFZ.

 Copyright (C) 2020 - 2023
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
    <tsm-linking-device-select
      v-model="selectedDevices"
      :linkings="linkings"
      :devices="devices"
    />
    <div v-if="treeViewItems.length>0" class="overline">
      Select mounting date ranges
    </div>
    <v-treeview
      v-model="selectedDateRanges"
      dense
      :items="treeViewItems"
      selectable
      @input="updateStoreSelectedDeviceMountActions"
    >
      <template #label="{item, leaf}">
        <div v-if="leaf">
          {{ item.name }}
        </div>
        <div v-else>
          <ExtendedItemName :value="item.item" />
        </div>
      </template>
    </v-treeview>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import TsmLinkingDeviceSelect from '@/components/configurations/tsmLinking/TsmLinkingDeviceSelect.vue'
import { TsmLinking } from '@/models/TsmLinking'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import BaseMountList from '@/components/shared/BaseMountList.vue'
import {
  TsmDeviceMountPropertyCombination,
  TsmDeviceMountPropertyCombinationList
} from '@/utils/configurationInterfaces'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

@Component({
  components: {
    ExtendedItemName,
    BaseMountList,
    TsmLinkingDeviceSelect
  }
})
export default class TsmLinkingDeviceMountActionSelect extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  private value!: TsmDeviceMountPropertyCombinationList

  @Prop({
    required: true,
    type: Array
  })
  private linkings!: TsmLinking[]

  @Prop({
    required: true,
    type: Array
  })
  private devices!: Device[]

  @Prop({
    required: true,
    type: Array
  })
  private deviceMountActions!: DeviceMountAction[]

  private selectedDevices: Device[] = []

  private selectedDateRanges: string[] = []

  getActionsForDeviceAsChildren (device: Device) {
    const filteredActions = this.deviceMountActions.filter((el) => {
      return el.device.id === device.id
    })

    return filteredActions.map((el) => {
      const tmpName = `from: ${this.$root.$options.filters!.toUtcDateTimeStringHHMM(el.beginDate)} to: ${this.$root.$options.filters!.toUtcDateTimeStringHHMM(el.endDate)}`
      return {
        id: el.id,
        name: tmpName
      }
    })
  }

  get treeViewItems () {
    const items = []
    for (const device of this.selectedDevices) {
      const tmpName = `${device.shortName} (${device.serialNumber ? device.serialNumber : 'no serial number'})`
      const tmpObject = {
        id: `device-${device.id}`,
        name: tmpName,
        item: device,
        children: this.getActionsForDeviceAsChildren(device)
      }
      items.push(tmpObject)
    }
    return items
  }

  get selectedDeviceMountActions () {
    return this.deviceMountActions.filter((el) => {
      return this.selectedDateRanges.includes(el.id)
    })
  }

  updateStoreSelectedDeviceMountActions () {
    const selectedDeviceMountActionsWithMeasuredQuantityArray: TsmDeviceMountPropertyCombinationList = this.value.slice()

    const pipe = (...fns: ((arg: any) => any)[]) => (x: any) =>
      fns.reduce((v, f) => f(v), x)

    const result = pipe(this.setResultToEmptyArrayIfNothingIsSelected, this.addNewSelectionsToResult, this.removeNotSelectedEntriesFromResult)(selectedDeviceMountActionsWithMeasuredQuantityArray)

    this.$emit('input', result)
  }

  private setResultToEmptyArrayIfNothingIsSelected (selectedDeviceMountActionsWithMeasuredQuantityArray: Array<TsmDeviceMountPropertyCombination>) {
    if (this.selectedDeviceMountActions.length === 0) {
      selectedDeviceMountActionsWithMeasuredQuantityArray = []
    }
    return selectedDeviceMountActionsWithMeasuredQuantityArray
  }

  private addNewSelectionsToResult (selectedDeviceMountActionsWithMeasuredQuantityArray: Array<TsmDeviceMountPropertyCombination>) {
    const copySelectedDeviceMountActionsWithMeasuredQuantityArray = selectedDeviceMountActionsWithMeasuredQuantityArray.slice()

    for (const deviceMountAction of this.selectedDeviceMountActions) {
      const found = copySelectedDeviceMountActionsWithMeasuredQuantityArray.find(el => el.action.id === deviceMountAction.id)

      if (!found) { // do not override the measuredQuantities array
        copySelectedDeviceMountActionsWithMeasuredQuantityArray.push({
          action: deviceMountAction,
          measuredQuantities: []
        })
      }
    }

    return copySelectedDeviceMountActionsWithMeasuredQuantityArray
  }

  private removeNotSelectedEntriesFromResult (selectedDeviceMountActionsWithMeasuredQuantityArray: Array<TsmDeviceMountPropertyCombination>) {
    return selectedDeviceMountActionsWithMeasuredQuantityArray.filter((el) => {
      return this.selectedDeviceMountActions.some(action => action.id === el.action.id)
    })
  }
}
</script>

<style scoped>

</style>
