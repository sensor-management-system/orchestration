<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
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
        {{ mountAction.beginDate | ISOToDateTimeString }}
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
        {{ mountAction.endDate | ISOToDateTimeString }}
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
        {{ `X = ${mountAction.offsetX} | Y = ${mountAction.offsetY} | Z = ${mountAction.offsetZ}` }}
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
    <v-row>
      <v-col>
        <v-btn
          small
          color="primary"
          nuxt
          :to="editLink"
        >
          Edit mount information
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'

import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import { ISOToDateTimeString } from '@/utils/dateHelper'
import { removeTrailingSlash } from '@/utils/urlHelpers'

@Component({
  components: {
  },
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

  get editLink (): RawLocation {
    return {
      path: removeTrailingSlash(this.$route.path) + '/' + ('device' in this.mountAction ? 'device-mount-actions' : 'platform-mount-actions') + '/' + this.mountAction.id + '/edit'
    }
  }
}
</script>
