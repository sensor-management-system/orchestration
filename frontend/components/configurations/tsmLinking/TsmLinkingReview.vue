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
  <v-container>
    <v-row>
      <v-col>
        <v-card>
          <v-simple-table
            fixed-header
          >
            <thead>
              <tr>
                <th>Device</th>
                <th>Mount range</th>
                <th>Offsets (X | Y | Z)</th>
                <th>Measured Quantity</th>
                <th>Datasource</th>
                <th>Thing</th>
                <th>Datastream</th>
                <th>Date range</th>
                <th>License</th>
                <th>Aggregation</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(formLinking,index) in tsmLinkings"
                :key="index"
              >
                <td>
                  <ExtendedItemName :value="formLinking.device" />
                </td>
                <td>
                  <tsm-linking-dates
                    :from="formLinking.deviceMountAction.beginDate"
                    :to="formLinking.deviceMountAction.endDate"
                  />
                </td>
                <td>
                  ({{ formLinking.deviceMountAction.offsetX }} | {{ formLinking.deviceMountAction.offsetY }} | {{ formLinking.deviceMountAction.offsetZ }})
                </td>
                <td>
                  {{ formLinking.deviceProperty | generatePropertyTitle }}
                </td>
                <td>{{ formLinking.datasource?.name }}</td>
                <td>{{ formLinking.thing?.name }}</td>
                <td>{{ formLinking.datastream?.name }}</td>
                <td>
                  <tsm-linking-dates
                    :from="formLinking.startDate"
                    :to="formLinking.endDate"
                  />
                </td>
                <td>{{ formLinking.licenseName }}</td>
                <td>{{ formLinking.aggregationText }}</td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-spacer />
      <slot name="save" />
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { generatePropertyTitle } from '@/utils/stringHelpers'
import TsmLinkingDates from '@/components/configurations/tsmLinking/TsmLinkingDates.vue'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

@Component({
  components: { ExtendedItemName, TsmLinkingDates },
  filters: { generatePropertyTitle }
})
export default class TsmLinkingReview extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  private tsmLinkings!: []
}
</script>

<style scoped>

</style>
