<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
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
        <a v-if="value.email.length > 0" :href="'mailto:' + value.email">
          <v-icon
            small
          >
            mdi-email
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Website</label>
        {{ value.website | orDefault }}
        <a v-if="value.website.length > 0" :href="value.website" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>ORCID</label>
        {{ value.orcid | orDefault }}
        <a v-if="value.orcid.length > 0" :href="'https://orcid.org/' + value.orcid" target="_blank">
          <v-icon
            small
          >
            mdi-open-in-new
          </v-icon>
        </a>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <label>Organization</label>
        {{ value.organization | orDefault }}
      </v-col>
    </v-row>
  </div>
</template>

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

<style lang="scss">
@import "@/assets/styles/_readonly_views.scss";
</style>
