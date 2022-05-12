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
        class="py-2 px-3"
        @click.stop.prevent="show = !show"
      >
        <div class="d-flex align-center">
          <div class="'text-caption text-disabled">
            {{ contact.email }}
          </div>
          <v-spacer />
          <DotMenu>
            <template #actions>
              <slot name="dot-menu-items" />
            </template>
          </DotMenu>
        </div>
        <v-row
          no-gutters
        >
          <v-col class="text-subtitle-1">
            {{ contact.fullName }}
          </v-col>
          <v-col
            align-self="end"
            class="text-right"
          >
            <v-btn
              :to="'/contacts/' + contact.id"
              color="primary"
              text
              small
              @click.stop.prevent
            >
              View
            </v-btn>
            <v-btn
              icon
              small
              @click.stop.prevent="show = !show"
            >
              <v-icon
                small
              >
                {{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
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
          <v-card-text
            class="py-2 px-3"
          >
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
                Website:
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
                {{ contact.website }}
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-expand-transition>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'

import { Contact } from '@/models/Contact'

import DotMenu from '@/components/DotMenu.vue'

@Component({
  components: {
    DotMenu
  }
})
export default class ContactsListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private contact!: Contact

  private show = false
}
</script>

<style scoped>

</style>
