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
  <v-hover
    v-slot="{ hover }"
  >
    <v-card
      :elevation="hover ? 6 : 2"
      class="ma-2"
    >
      <v-card-text
        @click.stop.prevent="show = !show"
      >
        <v-row
          no-gutters
        >
          <v-col>
            <StatusBadge
              :value="getStatus()"
            >
              <div :class="'text-caption' + (getType() === NO_TYPE ? ' text--disabled' : '')">
                {{ getType() }}
              </div>
            </StatusBadge>
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <DotMenu>
              <template #actions>
                <slot name="dot-menu-items" />
              </template>
            </DotMenu>
          </v-col>
        </v-row>
        <v-row
          no-gutters
        >
          <v-col class="text-subtitle-1">
            {{ platform.shortName }}
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <v-btn
              :to="'/platforms/' + platform.id"
              color="primary"
              text
              @click.stop.prevent
            >
              View
            </v-btn>
            <v-btn
              icon
              @click.stop.prevent="show = !show"
            >
              <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-expand-transition>
        <v-card
          v-show="show"
          flat
          tile
          color="grey lighten-5"
        >
          <v-card-text>
            <v-row
              dense
            >
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Manufacturer:
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ getTextOrDefault(platform.manufacturerName) }}
              </v-col>
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Model:
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ getTextOrDefault(platform.model) }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Serial number:
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ getTextOrDefault(platform.serialNumber) }}
              </v-col>
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Inventory number:
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="4"
                lg="4"
                xl="5"
                class="nowrap-truncate"
              >
                {{ getTextOrDefault(platform.inventoryNumber) }}
              </v-col>
            </v-row>
            <v-row
              dense
            >
              <v-col
                cols="4"
                xs="4"
                sm="3"
                md="2"
                lg="2"
                xl="1"
                class="font-weight-medium"
              >
                Description:
              </v-col>
              <v-col
                cols="8"
                xs="8"
                sm="9"
                md="10"
                lg="10"
                xl="11"
                class="nowrap-truncate"
              >
                {{ getTextOrDefault(platform.description) }}
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-expand-transition>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Prop } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'
import { Platform } from '@/models/Platform'
import DotMenu from '@/components/DotMenu.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

@Component({
  components: { StatusBadge, DotMenu },
  computed: mapGetters('vocabulary', ['getPlatformTypeByUri', 'getEquipmentstatusByUri'])
})
export default class PlatformsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private platform!: Platform

  public readonly NO_TYPE: string = 'Unknown type'
  private show = false

  // vuex definition for typescript check
  getPlatformTypeByUri!: (uri: string)=> PlatformType | undefined;
  getEquipmentstatusByUri!: (uri: string)=> Status | undefined;

  getTextOrDefault = (text: string): string => text || '-'

  getType () {
    if (this.platform.platformTypeName) {
      return this.platform.platformTypeName
    }

    if (this.getPlatformTypeByUri(this.platform.platformTypeUri)) {
      const platformType: PlatformType|undefined = this.getPlatformTypeByUri(this.platform.platformTypeUri)
      return platformType!.name
    }
    return this.NO_TYPE
  }

  getStatus () {
    if (this.platform.statusName) {
      return this.platform.statusName
    }
    if (this.getEquipmentstatusByUri(this.platform.statusUri)) {
      const platformStatus: Status|undefined = this.getEquipmentstatusByUri(this.platform.statusUri)
      return platformStatus!.name
    }
    return ''
  }
}
</script>

<style scoped>

</style>
