<!--
 SPDX-FileCopyrightText: 2020 - 2024

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div
    right
  >
    <v-card class="mb-2">
      <v-card-title>
        <ExtendedItemName :value="action.device" />
      </v-card-title>
      <v-card-subtitle>
        <tsm-linking-dates
          :from="action.beginDate"
          :to="action.endDate"
        />
      </v-card-subtitle>
      <v-container>
        <v-treeview
          v-model="model"
          :items="items"
          selectable
          dense
          @input="update"
        />
      </v-container>
    </v-card>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import TsmLinkingDates from '@/components/configurations/tsmLinking/TsmLinkingDates.vue'
import { DevicesPropertiesWithLinkingGetter, DevicesPropertiesWithoutLinkingGetter } from '@/store/tsmLinking'
import { generatePropertyTitle } from '@/utils/stringHelpers'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

@Component({
  components: {
    ExtendedItemName,
    TsmLinkingDates
  },
  computed: {
    ...mapGetters('tsmLinking', ['devicesPropertiesWithoutLinking', 'devicesPropertiesWithLinking'])
  }
})
export default class TsmLinkingMeasuredQuantitySelectItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private readonly action!: DeviceMountAction

  private model: string[] = []

  // vuex definition for typescript check
  devicesPropertiesWithLinking!: DevicesPropertiesWithLinkingGetter
  devicesPropertiesWithoutLinking!: DevicesPropertiesWithoutLinkingGetter

  get calcDevicesPropertiesWithoutLinking () {
    return this.devicesPropertiesWithoutLinking(this.action)
  }

  get calcDevicesPropertiesWithLinking () {
    return this.devicesPropertiesWithLinking(this.action)
  }

  get items () {
    const items = []

    if (this.calcDevicesPropertiesWithoutLinking.length > 0) {
      const itemWithoutLinking = {
        id: 'WithoutLinking-0',
        name: 'Measured quantities without linking',
        children: this.calcDevicesPropertiesWithoutLinking.map((el) => {
          return {
            id: el.id,
            name: generatePropertyTitle(el)
          }
        })
      }
      items.push(itemWithoutLinking)
    }

    if (this.calcDevicesPropertiesWithLinking.length > 0) {
      const itemWithLinking = {
        id: 'WithLinking-0',
        name: 'Measured quantities with linking',
        children: this.calcDevicesPropertiesWithLinking.map((el) => {
          return {
            id: el.id,
            name: generatePropertyTitle(el)
          }
        })
      }

      items.push(itemWithLinking)
    }

    return items
  }

  get selectedMeasuredQuantities () {
    return this.action.device.properties.filter((el) => {
      if (el.id === null) {
        return false
      }
      return this.model.includes(el.id)
    })
  }

  update () {
    this.$emit('input', this.selectedMeasuredQuantities)
  }
}
</script>
