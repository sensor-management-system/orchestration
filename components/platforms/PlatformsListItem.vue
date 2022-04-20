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
              :value="getStatus(platform)"
            >
              <div :class="'text-caption' + (getType(platform) === NO_TYPE ? ' text--disabled' : '')">
                {{ getType(platform) }}
              </div>
            </StatusBadge>
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <DotMenu>
              <template #actions>
                <slot name="dot-menu-items">
                </slot>
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
import { Platform } from '@/models/Platform'
import { Prop } from 'nuxt-property-decorator'
import DotMenu from '@/components/DotMenu.vue'
import StatusBadge from '@/components/StatusBadge.vue'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'
import {mapGetters} from 'vuex'

@Component({
  components: { StatusBadge, DotMenu },
  computed: mapGetters('vocabulary',['getPlatformTypeByUri','getEquipmentstatusByUri'])
})
export default class PlatformsListItem extends Vue {

  @Prop({
    required:true,
    type: Object
  })
  private platform!:Platform;
  public readonly NO_TYPE: string = 'Unknown type'
  private show = false;

  getTextOrDefault = (text: string): string => text || '-'

  getType () {
    if (this.platform.platformTypeName) {
      return this.platform.platformTypeName
    }

    if(this.getPlatformTypeByUri(this.platform.platformTypeUri)){
      const platformType:PlatformType = this.getPlatformTypeByUri(this.platform.platformTypeUri)
      return platformType.name
    }
     return this.NO_TYPE
  }

  getStatus (platform: Platform) {
    if (platform.statusName) {
      return platform.statusName
    }
    if (this.getEquipmentstatusByUri(this.platform.statusUri)) {
      const platformStatus:Status = this.getEquipmentstatusByUri(this.platform.statusUri)
      return platformStatus.name
    }
    return ''
  }
}
</script>

<style scoped>

</style>
