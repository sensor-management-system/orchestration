<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
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
      <v-pagination v-model="pageNumber" :length="totalPages" />
      <template v-for="(item, index) in paginatedItems">
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
                <v-checkbox v-if="canModifyEntity(item)" class="d-inline-block ml-2 pa-0 my-0" :input-value="isSelected(item)" hide-details @click.stop.prevent="toggleItem(item)" />
                <v-tooltip v-else top>
                  <template #activator="{ on }">
                    <v-btn icon v-on="on" @click.stop>
                      <v-icon color="warning">
                        mdi-alert
                      </v-icon>
                    </v-btn>
                  </template>
                  <span>No permission to add TSM Linking for <em>{{ item.shortName }}</em>.</span>
                </v-tooltip>
              </template>
            </DevicesListItem>
          </v-col>
        </v-row>
        <v-divider
          v-if="index < paginatedItems.length - 1"
          :key="`divider-${index}`"
        />
      </template>
    </v-card>
  </v-menu>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'

import { Device, IDevice } from '@/models/Device'
import { TsmLinking } from '@/models/TsmLinking'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'
import { CanModifyEntityGetter } from '@/store/permissions'

@Component({
  components: {
    DevicesListItem
  },
  computed: mapGetters('permissions', ['canModifyEntity'])
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

  private pageSize = 10
  private pageNumber = 1

  // vuex definition for typescript check
  canModifyEntity!: CanModifyEntityGetter

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

  get paginatedItems () {
    const start = (this.pageNumber - 1) * this.pageSize
    const end = start + this.pageSize
    return this.filteredItems.slice(start, end)
  }

  get totalPages () {
    return Math.ceil(this.filteredItems.length / this.pageSize)
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
    const isSelected = this.selectedItems.findIndex((device: Device) => {
      return device.id === item.id
    }) !== -1
    return isSelected
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
