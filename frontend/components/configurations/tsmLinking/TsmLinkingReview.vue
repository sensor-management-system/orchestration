<!--
SPDX-FileCopyrightText: 2020 - 2024
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

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
                <th v-if="linkingsWithDuplicateUsedDatastreams.length>0" class="text-center">
                  <v-icon small>
                    mdi-information
                  </v-icon>
                </th>
                <th />
                <th>Device</th>
                <th>Measured quantity</th>
                <th>Offsets (X | Y | Z)</th>
                <th>Mount range</th>
                <th>Datasource/Thing/Datastream</th>
                <th>Linking date range</th>
                <th>License</th>
                <th>Aggregation</th>
                <th>Involved devices</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(formLinking,index) in tsmLinkings"
                :key="index"
                :class="linkingHighlightClasses(formLinking)"
              >
                <td v-if="linkingsWithDuplicateUsedDatastreams.length>0">
                  <div v-if="allIntersectingLinkingsUsingSameDatastreamAsLinking(formLinking).length > 0">
                    <v-tooltip
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          color="orange"
                          v-bind="attrs"
                          v-on="on"
                          @mouseenter="currentlyHoveredLinking = formLinking"
                          @mouseleave="currentlyHoveredLinking = null"
                        >
                          mdi-alert
                        </v-icon>
                      </template>
                      <span>This datastream is used in multiple linkings with temporal overlap</span>
                    </v-tooltip>
                  </div>
                  <div v-else-if="allLinkingsUsingSameDatastreamAsLinking(formLinking).length > 0">
                    <v-tooltip
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          v-bind="attrs"
                          v-on="on"
                          @mouseenter="currentlyHoveredLinking = formLinking"
                          @mouseleave="currentlyHoveredLinking = null"
                        >
                          mdi-information
                        </v-icon>
                      </template>
                      This datastream is used in multiple linkings with no temporal overlap.
                    </v-tooltip>
                  </div>
                </td>
                <td>
                  <div class="mb-2">
                    <v-tooltip bottom style="z-index: 101">
                      <template #activator="{ on, attrs }">
                        <v-icon
                          v-bind="attrs"
                          @click="scrollToForm(formLinking)"
                          v-on="on"
                        >
                          mdi-arrow-up-left
                        </v-icon>
                      </template>
                      <span>Go to the corresponding form</span>
                    </v-tooltip>
                  </div>
                </td>
                <td>
                  <ExtendedItemName :value="formLinking.device" />
                </td>
                <td>
                  {{ formLinking.deviceProperty | generatePropertyTitle }}
                </td>
                <td>
                  ({{ formLinking.deviceMountAction.offsetX }} | {{ formLinking.deviceMountAction.offsetY }} |
                  {{ formLinking.deviceMountAction.offsetZ }})
                </td>
                <td>
                  <tsm-linking-dates
                    :from="formLinking.deviceMountAction.beginDate"
                    :to="formLinking.deviceMountAction.endDate"
                  />
                </td>
                <td>
                  <div>
                    <v-tooltip bottom>
                      <template #activator="{ on, attrs }">
                        <span
                          v-bind="attrs"
                          v-on="on"
                        >
                          {{ formLinking.datasource?.name ?? '-' }}
                        </span>
                      </template>
                      <span>Datasource: {{ formLinking.datasource?.name ?? '-' }}</span>
                    </v-tooltip>
                  </div>
                  <div>
                    <v-tooltip bottom>
                      <template #activator="{ on, attrs }">
                        <span
                          v-bind="attrs"
                          v-on="on"
                        >
                          {{ formLinking.thing?.name ?? '-' }}
                        </span>
                      </template>
                      <span>Thing: {{ formLinking.thing?.name ?? '-' }}</span>
                    </v-tooltip>
                  </div>
                  <div>
                    <v-tooltip bottom>
                      <template #activator="{ on, attrs }">
                        <span
                          v-bind="attrs"
                          v-on="on"
                        >
                          {{ formLinking.datastream?.name ?? '-' }}
                        </span>
                      </template>
                      <span>Datastream: {{ formLinking.datastream?.name ?? '-' }}</span>
                    </v-tooltip>
                  </div>
                </td>
                <td>
                  <tsm-linking-dates
                    :from="formLinking.startDate"
                    :to="formLinking.endDate"
                  />
                </td>
                <td>
                  {{ formLinking.licenseName }}
                  <a v-if="formLinking.licenseUri" target="_blank" :href="formLinking.licenseUri">
                    <v-icon small>
                      mdi-open-in-new
                    </v-icon>
                  </a>
                </td>
                <td>{{ formLinking.aggregationText }}</td>
                <td>{{ formLinking.filterInvolvedDevices(devices) | sparseJoin }}</td>
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
import { DateTime } from 'luxon'
import { generatePropertyTitle } from '@/utils/stringHelpers'
import TsmLinkingDates from '@/components/configurations/tsmLinking/TsmLinkingDates.vue'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import { Device } from '@/models/Device'
import { TsmLinking } from '@/models/TsmLinking'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'

type DatastreamLinkingMap = { datastream: TsmdlDatastream, linkings: TsmLinking[] }

@Component({
  components: { ExtendedItemName, TsmLinkingDates },
  filters: { generatePropertyTitle }
})
export default class TsmLinkingReview extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  private tsmLinkings!: TsmLinking[]

  @Prop({
    required: true,
    type: Array
  })
  private devices!: Device[]

  private currentlyHoveredLinking: TsmLinking|null = null

  linkingHighlightClasses (linking: TsmLinking) {
    if (!this.currentlyHoveredLinking) { return {} }
    const intersectingLinkingsWithSameDatastream = this.allIntersectingLinkingsUsingSameDatastreamAsLinking(this.currentlyHoveredLinking!)
    if (intersectingLinkingsWithSameDatastream.length > 0) {
      if (this.currentlyHoveredLinking.equalsByIdOrMountActionAndDeviceProperty(linking) || intersectingLinkingsWithSameDatastream.findIndex(otherLinking => otherLinking.equalsByIdOrMountActionAndDeviceProperty(linking)) !== -1) {
        return { 'highlight-duplicate-critical': true }
      }
    }
    const linkingsWithSameDatastream = this.allLinkingsUsingSameDatastreamAsLinking(this.currentlyHoveredLinking!)
    if (linkingsWithSameDatastream.length > 0) {
      if (this.currentlyHoveredLinking.equalsByIdOrMountActionAndDeviceProperty(linking) || linkingsWithSameDatastream.findIndex(otherLinking => otherLinking.equalsByIdOrMountActionAndDeviceProperty(linking)) !== -1) {
        return { 'highlight-duplicate': true }
      }
    }
    return {}
  }

  get linkingsWithDuplicateUsedDatastreams (): TsmLinking[][] {
    const sets: TsmLinking[][] = []
    for (const tsmLinking of this.tsmLinkings) {
      if (sets.some(set => set.filter(linking => linking.id === tsmLinking.id))) {
        continue
      }
      if (!tsmLinking.datastream?.id) { continue }
      const matches = this.tsmLinkings.filter(linking => linking.datastream?.id === tsmLinking.datastream!.id)
      if (matches.length > 1) {
        sets.push(matches)
      }
    }
    return sets
  }

  get duplicateDatastreams (): DatastreamLinkingMap[] {
    const datastreamMap: DatastreamLinkingMap[] = []
    for (const tsmLinking of this.tsmLinkings) {
      if (!tsmLinking.datastream?.id) { continue }
      const foundIndex = datastreamMap.findIndex(entry => entry.datastream.id === tsmLinking.datastream!.id)
      if (foundIndex !== -1) {
        datastreamMap[foundIndex].linkings.push(tsmLinking)
        continue
      }
      datastreamMap.push({
        datastream: tsmLinking.datastream,
        linkings: [tsmLinking]
      })
    }
    return datastreamMap.filter(entry => entry.linkings.length > 1)
  }

  allLinkingsUsingSameDatastreamAsLinking (formLinking: TsmLinking): TsmLinking[] {
    if (!formLinking.datastream) { return [] }
    const allLinkings = this.duplicateDatastreams.find(entry => entry.datastream.id === formLinking.datastream!.id)?.linkings ?? []
    return allLinkings.filter(linking => !linking.equalsByIdOrMountActionAndDeviceProperty(formLinking))
  }

  allIntersectingLinkingsUsingSameDatastreamAsLinking (formLinking: TsmLinking): TsmLinking[] {
    const allLinkings = this.allLinkingsUsingSameDatastreamAsLinking(formLinking)
    return allLinkings.filter(linking => this.checkDateIntersectForLinkings(formLinking, linking))
  }

  checkDateIntersectForLinkings (a: TsmLinking, b: TsmLinking): boolean {
    let start1: DateTime | number = 0
    let start2: DateTime | number = 0
    let end1: DateTime | number = Infinity
    let end2: DateTime | number = Infinity

    if (a.startDate) {
      start1 = a.startDate
    } else if (a.deviceMountAction!.beginDate) {
      start1 = a.deviceMountAction!.beginDate
    }

    if (a.endDate) {
      end1 = a.endDate
    } else if (a.deviceMountAction!.endDate) {
      end1 = a.deviceMountAction!.endDate
    }

    if (b.startDate) {
      start2 = b.startDate
    } else if (b.deviceMountAction!.beginDate) {
      start2 = b.deviceMountAction!.beginDate
    }

    if (b.endDate) {
      end2 = b.endDate
    } else if (b.deviceMountAction!.endDate) {
      end2 = b.deviceMountAction!.endDate
    }

    return start1 < end2 && end1 > start2
  }

  scrollToForm (linking: TsmLinking) {
    this.$emit('scroll-to-form', linking)
  }
}
</script>

<style scoped>
.highlight-duplicate {
  background-color: #fff6ca !important;
}
.highlight-duplicate-critical {
  background-color: #ffecdd !important;
}

tr {
  transition: background-color .2s;
}
</style>
