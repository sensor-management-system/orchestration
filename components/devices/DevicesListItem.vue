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
            {{ device.shortName }}
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <v-btn
              :to="'/devices/' + device.id"
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
                {{ getTextOrDefault(device.manufacturerName) }}
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
                {{ getTextOrDefault(device.model) }}
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
                {{ getTextOrDefault(device.serialNumber) }}
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
                {{ getTextOrDefault(device.inventoryNumber) }}
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
                {{ getTextOrDefault(device.description) }}
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
import { Device } from '@/models/Device'
import { Prop } from 'nuxt-property-decorator'
import { PlatformType } from '@/models/PlatformType'
import { Platform } from '@/models/Platform'
import { Status } from '@/models/Status'
import { mapGetters } from 'vuex'
import { DeviceType } from '@/models/DeviceType'
import DotMenu from '@/components/DotMenu.vue'
import StatusBadge from '@/components/StatusBadge.vue'

@Component({
  components: { StatusBadge, DotMenu },
  computed: mapGetters('vocabulary',['getDeviceTypeByUri','getEquipmentstatusByUri'])
})
export default class DevicesListItem extends Vue {
  @Prop({
    required:true,
    type: Object
  })
  private device!:Device
  private show = false
  public readonly NO_TYPE: string = 'Unknown type'

  getTextOrDefault = (text: string): string => text || '-'

  getType () {
    if (this.device.deviceTypeName) {
      return this.device.deviceTypeName
    }

    if(this.getDeviceTypeByUri(this.device.deviceTypeUri)){
      const deviceType:DeviceType = this.getDeviceTypeByUri(this.device.deviceTypeUri)
      return deviceType.name
    }
    return this.NO_TYPE
  }

  getStatus () {
    if (this.device.statusName) {
      return this.device.statusName
    }
    if (this.getEquipmentstatusByUri(this.device.statusUri)) {
      const deviceStatus:Status = this.getEquipmentstatusByUri(this.device.statusUri)
      return deviceStatus.name
    }
    return ''
  }
}
</script>

<style scoped>

</style>
