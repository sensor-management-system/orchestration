<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022 - 2024
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <v-row dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Begin date:
      </v-col>
      <v-col cols="8">
        {{ mountAction.beginDate | ISOToDateTimeString }} <span class="text-caption text--secondary">(UTC)</span>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        End date:
      </v-col>
      <v-col v-if="mountAction.endDate" cols="8">
        {{ mountAction.endDate | ISOToDateTimeString }} <span class="text-caption text--secondary">(UTC)</span>
      </v-col>
      <v-col v-else cols="8">
        open end
      </v-col>
    </v-row>
    <v-row dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Offsets:
      </v-col>
      <v-col cols="8">
        {{ getOffsets(mountAction) }}
      </v-col>
    </v-row>
    <v-row
      v-if="calculatedOffsets"
      dense
    >
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Absolute offsets:
        <v-tooltip
          bottom
        >
          <template #activator="{ on, attrs }">
            <v-icon
              small
              v-bind="attrs"
              v-on="on"
            >
              mdi-help-circle
            </v-icon>
          </template>
          The offsets of the selected node are included.
        </v-tooltip>
      </v-col>
      <v-col cols="8">
        {{ getOffsets(calculatedOffsets) }}
      </v-col>
    </v-row>
    <v-row v-if="(mountAction.x !== null) || (mountAction.y !== null)" dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Coordinates:
      </v-col>
      <v-col cols="8">
        {{ getCoordinates(mountAction) }}
      </v-col>
    </v-row>
    <v-row v-if="mountAction.z !== null" dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Height:
      </v-col>
      <v-col cols="8">
        {{ getHeight(mountAction) }}
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Contact:
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ mountAction.beginContact }}
      </v-col>
    </v-row>
    <v-row v-if="mountAction.endContact" dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        End contact:
      </v-col>
      <v-col cols="8">
        {{ mountAction.endContact }}
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Description
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
        :title="mountAction.beginDescription.length > 25 ? mountAction.beginDescription : ''"
      >
        {{ mountAction.beginDescription | shortenRight(25, '...') | orDefault }}
      </v-col>
    </v-row>
    <v-row v-if="mountAction.endDescription" dense>
      <v-col
        cols="4"
        class="font-weight-medium"
        :title="mountAction.endDescription.length > 25 ? mountAction.endDescription : ''"
      >
        End description:
      </v-col>
      <v-col cols="8">
        {{ mountAction.endDescription | shortenRight(25, '...') | orDefault }}
      </v-col>
    </v-row>
    <v-row
      v-if="editable"
    >
      <v-col>
        <v-btn
          small
          color="primary"
          nuxt
          :disabled="disabled"
          :to="editLink"
        >
          Edit mount information
        </v-btn>
        <v-btn
          v-if="deletable"
          small
          color="error"
          text
          :disabled="disabled"
          @click="$emit('delete', mountAction)"
        >
          Delete mount action
        </v-btn>
        <v-tooltip v-if="warning" right>
          <template #activator="{ on, attrs }">
            <v-icon v-bind="attrs" v-on="on">
              mdi-alert
            </v-icon>
          </template>
          <span>{{ warning }}</span>
        </v-tooltip>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, InjectReactive } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'

import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import { IOffsets } from '@/utils/configurationInterfaces'
import { ISOToDateTimeString } from '@/utils/dateHelper'
import { removeTrailingSlash } from '@/utils/urlHelpers'

@Component({
  filters: {
    ISOToDateTimeString
  }
})
export default class BaseMountInfo extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private mountAction!: DeviceMountAction | PlatformMountAction

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private editable!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private deletable!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private disabled!: boolean

  @Prop({
    default: '',
    required: false,
    type: String
  })
  private warning!: string

  @InjectReactive()
  readonly calculatedOffsets!: IOffsets | null

  get editLink (): RawLocation {
    return {
      path: removeTrailingSlash(this.$route.path) + '/' + ('device' in this.mountAction ? 'device-mount-actions' : 'platform-mount-actions') + '/' + this.mountAction.id + '/edit'
    }
  }

  getOffsets (valueWithOffsets: IOffsets): string {
    return `X = ${valueWithOffsets.offsetX} m | Y = ${valueWithOffsets.offsetY} m | Z = ${valueWithOffsets.offsetZ} m`
  }

  getCoordinates (value: DeviceMountAction | PlatformMountAction): string {
    const partXY = `X = ${value.x} | Y = ${value.y}`
    if (value.epsgCode) {
      return `${partXY} | EPSG code = ${value.epsgCode}`
    }
    return partXY
  }

  getHeight (value: DeviceMountAction | PlatformMountAction): string {
    const partZ = `Z = ${value.z}`
    if (value.elevationDatumName) {
      return `${partZ} | Elevation datum = ${value.elevationDatumName}`
    }
    return partZ
  }
}
</script>
