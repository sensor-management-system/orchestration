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
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    bottom
    offset-y
    nudge-top="30"
  >
    <template #activator="{ on }">
      <v-text-field
        v-model="search"
        outlined
        :append-icon="menu? 'mdi-chevron-up': 'mdi-chevron-down'"
        v-on="on"
      >
        <template #prepend-inner>
          <template v-for="(item, index) in selectedItems">
            <v-chip
              :key="index"
              class="mr-1"
              close
              @click:close="removeItem(item)"
            >
              {{ item.shortName }}
            </v-chip>
          </template>
        </template>
      </v-text-field>
    </template>
    <v-card>
      <template v-for="(item, index) in filteredItems">
        <v-row :key="index" no-gutters>
          <v-col cols="12">
            <DevicesListItem
              :key="item.id"
              :hide-header="true"
              :device="item"
              target="_blank"
              class="no-boxshadow"
            >
              <template #additional-actions>
                <v-checkbox class="d-inline-block ml-2 pa-0 my-0" :value="isSelected(item)" hide-details @click.stop.prevent="toggleItem(item)" />
              </template>
            </DevicesListItem>
          </v-col>
        </v-row>
        <v-divider
          v-if="index < filteredItems.length - 1"
          :key="`divider-${index}`"
        />
      </template>
    </v-card>
  </v-menu>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Device, IDevice } from '@/models/Device'
import { TsmLinking } from '@/models/TsmLinking'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'

@Component({
  components: {
    DevicesListItem,
    ProgressIndicator
  }
})
export default class TsmLinkingDeviceSelect extends Vue {
  @Prop({
    required: true,
    type: Array
  })
    linkings!: TsmLinking[]

  @Prop({
    required: true,
    type: Array
  })
    value!: Device[]

  @Prop({
    required: true,
    type: Array
  })
    devices!: Device[]

  private isLoading: boolean = false
  private menu = false
  private search = ''
  private selectedItems: Device[] = []
  private searchFields = [
    'shortName',
    'manufacturerName',
    'serialNumber',
    'description',
    'model',
    'inventoryNumber'
  ]

  get filteredItems () {
    return this.devices.filter((device: Device) => {
      return this.searchFields.some((searchField) => {
        const property = device[searchField as keyof IDevice]
        if (typeof property === 'string') {
          return property.toLowerCase().includes(this.search.toLowerCase())
        }
        return false
      })
    })
  }

  toggleItem (item: Device) {
    const index = this.selectedItems.findIndex((device: Device) => {
      return device.id === item.id
    })
    if (index === -1) {
      this.selectedItems.push(item)
    } else {
      this.selectedItems.splice(index, 1)
    }
  }

  removeItem (item: Device) {
    const index = this.selectedItems.findIndex((device: Device) => {
      return device.id === item.id
    })
    if (index !== -1) {
      this.selectedItems.splice(index, 1)
    }
  }

  isSelected (item: Device) {
    return this.selectedItems.findIndex((device: Device) => {
      return device.id === item.id
    }) !== -1
  }

  @Watch('search')
  onSearchChanged (val: String) {
    if (val) {
      this.menu = true
    }
  }

  @Watch('selectedItems', {
    immediate: true,
    deep: true
  })
  onSelectedItemsChanged () {
    this.$emit('input', this.selectedItems)
  }
}
</script>

<style scoped>
.no-boxshadow {
  box-shadow: none !important;
}
</style>
