<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-list>
      <v-list-item-group
        :value="value"
        :value-comparator="compareEntities"
        multiple
        color="primary"
        @change="change"
      >
        <template v-for="(item, i) in items">
          <v-list-item
            :key="itemKey(item, i)"
            :value="item"
            active-class="primary--text text--accent-4"
            :disabled="!isAvailable(item) || !canModifyEntity(item)"
          >
            <template #default="{ active }">
              <v-list-item-content>
                <v-list-item-title>
                  <extended-item-name
                    :value="item"
                  />
                </v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                <v-checkbox
                  v-if="isAvailable(item) && canModifyEntity(item)"
                  :input-value="active"
                  color="deep-purple accent-4"
                />
                <v-tooltip
                  v-else
                  top
                >
                  <template #activator="{ on }">
                    <v-btn icon v-on="on" @click.stop>
                      <v-icon color="warning">
                        mdi-alert
                      </v-icon>
                    </v-btn>
                  </template>
                  <span v-if="!isAvailable(item)">{{ availabilityReason(getAvailability(item)) }}</span>
                  <span v-else-if="!canModifyEntity(item)">No permission to mount <em>{{ item.shortName }}</em>.</span>
                </v-tooltip>
              </v-list-item-action>
            </template>
          </v-list-item>
        </template>
      </v-list-item-group>
    </v-list>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'

import { mapGetters } from 'vuex'

import { CanModifyEntityGetter } from '@/store/permissions'

import { Availability } from '@/models/Availability'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'
import { dateToString } from '@/utils/dateHelper'
import { Configuration } from '@/models/Configuration'

import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

@Component({
  components: {
    ExtendedItemName
  },
  computed: mapGetters('permissions', ['canModifyEntity'])
})
export default class BaseMountList extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  private value!: [Platform | Device]

  @Prop({
    required: true,
    type: Array
  })
  private items!: [Platform | Device]

  @Prop({
    type: Array
  })
  private availabilities!: Availability[]

  @Prop({
    default: false,
    type: Boolean
  })
  private keepValuesThatAreNotInItems!: boolean

  private availabilitiesWithConfigs: Availability[] = this.availabilities

  // vuex definition for typescript check
  canModifyEntity!: CanModifyEntityGetter

  async fetch () {
    this.availabilitiesWithConfigs = await Promise.all(this.availabilities.map(async (availability) => {
      if (availability.configurationID) {
        const copy = Availability.createFromObject(availability)
        const config = await this.findConfiguration(availability.configurationID)
        copy.configuration = config
        return copy
      }
      return availability
    }))
  }

  async created () {
  }

  itemKey (item: Platform | Device, i: number): string {
    if (item.id) {
      return `item-id-${item.id}`
    }
    return `item-index-${i}`
  }

  change (entities: [Platform | Device]) {
    const result: [Platform | Device] = [...entities]

    if (this.keepValuesThatAreNotInItems) {
      this.value.forEach((x: Platform | Device) => {
        if (this.items.findIndex(i => i.id === x.id) < 0) {
          if (entities.findIndex(e => e.id === x.id) < 0) {
            // Ok, here we are in this case that the new selection does not
            // contain an entry that is in the value - and the entry is not
            // covered by the items nor the entities list.
            // For those cases we want to stay with those values.
            result.push(x)
          }
        }
      })
      // You may wonder why this is needed? In some cases this is the default
      // behaviour, but in some it wasn't.
      // The problem was on adding the pagination to the mount wizzard.
      // After switching to another page, there was an emty entities entry
      // (while we actually wanted the values to stay in the selection).
      // So, this is the workaround here.
    }

    this.$emit('selectEntity', result)
  }

  getAvailability (entity: Platform | Device): Availability | undefined {
    const availability = this.availabilities.find(availability => availability.id === entity.id)

    if (availability && !availability.available) {
      return this.availabilitiesWithConfigs.find(availabilityWithConfig => availabilityWithConfig.id === entity.id)
    }
    return availability
  }

  isAvailable (entity: Platform | Device): boolean {
    return this.getAvailability(entity)?.available || false
  }

  compareEntities (a: Platform | Device, b: Platform | Device) {
    return a.id === b.id
  }

  async findConfiguration (id: string): Promise<Configuration> {
    return await this.$api.configurations.findById(id)
  }

  availabilityReason (availability?: Availability): string {
    if (!availability) {
      return 'Not available'
    }

    let configString = availability.configurationID

    if (availability.configuration) {
      configString = availability.configuration.label
    }

    let endString = ''
    if (!availability.endDate?.isValid) {
      endString = 'indefinitely'
    } else {
      endString = `until ${dateToString(availability.endDate as DateTime)}`
    }

    let beginString = ''
    if (!availability.beginDate?.isValid) {
      beginString = `from ${dateToString(availability.endDate as DateTime)}`
    }

    return `Used in configuration "${configString}" ${beginString} ${endString}`
  }
}

</script>

<style scoped>

.v-list-item__action{
  pointer-events: all;
}
</style>
