<!--
 Web client of the Sensor Management System software developed within the
 Helmholtz DataHub Initiative by GFZ and UFZ.

 Copyright (C) 2020 - 2024
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
