<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
    <v-list>
      <v-list-item-group
        v-model="selectedEntities"
        :value-comparator="compareEntities"
        multiple
        color="primary"
      >
        <template v-for="(item, i) in items">
          <v-list-item
            :key="`item-${i}`"
            :value="item"
            active-class="primary--text text--accent-4"
            :disabled="!isAvailable(item)"
          >
            <template #default="{ active }">
              <v-list-item-content>
                <v-list-item-title v-text="item.shortName" />
              </v-list-item-content>

              <v-list-item-action>
                <v-checkbox
                  v-if="isAvailable(item)"
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
                  <span>{{ availabilityReason(getAvailability(item)) }}</span>
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
import { Availability } from '@/models/Availability'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'
import { dateToString } from '@/utils/dateHelper'

@Component
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

  get selectedEntities (): [Platform | Device] {
    return this.value
  }

  set selectedEntities (entities: [Platform | Device]) {
    this.$emit('selectEntity', entities)
  }

  getAvailability (entity: Platform | Device): Availability | undefined {
    const availability = this.availabilities.find(availability => availability.id === entity.id)
    return availability
  }

  isAvailable (entity: Platform | Device): boolean {
    return this.getAvailability(entity)?.available || false
  }

  compareEntities (a: Platform | Device, b: Platform | Device) {
    return a.id === b.id
  }

  availabilityReason (availability?: Availability): string {
    if (!availability) {
      return 'Not available'
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

    return `Used in configuration ${availability.configurationID} ${beginString} ${endString}`
  }
}

</script>

<style scoped>

.v-list-item__action{
  pointer-events: all;
}
</style>
