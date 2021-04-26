<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <label>Given name</label>
        {{ value.givenName | orDefault }}
      </v-col>
      <v-col cols="12" md="3">
        <label>Family name</label>
        {{ value.familyName | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>E-mail</label>
        {{ value.email | orDefault }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Website</label>
        {{ value.website | orDefault }}
        <a v-if="value.website.length > 0" :href="value.website" target="_blank">
          <v-icon>
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
  </div>
</template>
<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

@Component
export default class ContactBasicData extends Vue {
  @Prop({
    default: () => new Contact(),
    required: true,
    type: Contact
  })
  readonly value!: Contact
}

</script>
