<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <base-expandable-list-item
    expandable-color="grey lighten-5"
  >
    <template #header>
      <div class="text-caption">
        {{ contact.email }}
      </div>
    </template>
    <template #dot-menu-items>
      <slot name="dot-menu-items" />
    </template>
    <template #actions>
      <slot name="actions" />
    </template>
    <template #default>
      <span>{{ contact.fullName }}</span>
    </template>
    <template #expandable>
      <v-row
        no-gutters
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
          Given name:
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
          {{ contact.givenName }}
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
          Family name:
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
          {{ contact.familyName }}
        </v-col>
      </v-row>
      <v-row
        no-gutters
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
          Email:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
        >
          <ExpandableText
            :value="contact.email | orDefault"
            :shorten-at="35"
          />
          <a v-if="contact.email.length > 0" :href="'mailto:' + contact.email">
            <v-icon
              small
            >
              mdi-email
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
          Website:
        </v-col>
        <v-col
          cols="8"
          xs="8"
          sm="9"
          md="4"
          lg="4"
          xl="5"
        >
          <ExpandableText
            :value="contact.website | orDefault"
            :shorten-at="35"
          />
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
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import ExpandableText from '@/components/shared/ExpandableText.vue'

@Component({
  components: {
    BaseExpandableListItem,
    ExpandableText
  }
})
export default class ContactsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private contact!: Contact

  @Prop({
    default: '',
    type: String
  })
  private from!: string
}
</script>

<style scoped>

</style>
