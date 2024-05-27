<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
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
