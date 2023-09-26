<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022 - 2023
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
    <v-row
      dense
    >
      <v-col
        cols="12"
        md="3"
      >
        <label>Given name:</label>
        {{ contact.givenName }}
      </v-col>
      <v-col
        cols="12"
        md="3"
      >
        <label>Family name:</label>
        {{ contact.familyName }}
      </v-col>
    </v-row>
    <v-row
      dense
    >
      <v-col
        cols="12"
        md="3"
      >
        <label>E-Mail:</label>
        {{ contact.email | orDefault }}
        <a v-if="contact.email.length > 0" :href="'mailto:' + contact.email">
          <v-icon
            small
          >
            mdi-email
          </v-icon>
        </a>
      </v-col>
      <v-col
        cols="12"
        md="6"
      >
        <label>Website:</label>
        {{ contact.website | orDefault }}
        <a v-if="contact.website.length > 0" :href="contact.website" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col
        cols="4"
        xs="4"
        sm="3"
        md="2"
        lg="2"
        xl="1"
        class="font-weight-medium"
      >
        ORCID:
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
        {{ contact.orcid | orDefault }}
        <a v-if="contact.orcid.length > 0" :href="'https://orcid.org/' + contact.orcid" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
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
        Organization:
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
        {{ contact.organization | orDefault }}
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'

@Component({})
export default class ContactRolePanel extends Vue {
  @Prop({
    type: Object,
    required: true
  })
  private readonly value!: ContactRole

  get contact (): Contact {
    return this.value.contact!
  }
}
</script>
