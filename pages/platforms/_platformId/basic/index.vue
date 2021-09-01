<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
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
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </v-card-actions>
    <PlatformBasicData
      v-model="platform"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/basic/edit'"
      >
        Edit
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Platform } from '@/models/Platform'
import PlatformBasicData from '@/components/PlatformBasicData.vue'

@Component({
  components: {
    PlatformBasicData
  }
})
export default class PlatformShowBasicPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Platform

  get platform (): Platform {
    return this.value
  }

  set platform (value: Platform) {
    this.$emit('input', value)
  }

  get platformId () {
    return this.$route.params.platformId
  }
}
</script>
