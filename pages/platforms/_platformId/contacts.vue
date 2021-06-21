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
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <NuxtChild
      v-model="contacts"
    />
    <v-card-actions
      v-if="!isAddContactPage"
    >
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
    <v-expansion-panels>
      <v-expansion-panel
        v-for="contact in contacts"
        :key="contact.id"
      >
        <v-expansion-panel-header>
          <v-row
            no-gutters
          >
            <v-col class="text-subtitle-1">
              {{ contact.toString() }}
            </v-col>
            <v-col
              align-self="end"
              class="text-right"
            >
              <v-menu
                v-if="isLoggedIn"
                close-on-click
                close-on-content-click
                offset-x
                left
                z-index="999"
              >
                <template #activator="{ on }">
                  <v-btn
                    data-role="property-menu"
                    icon
                    small
                    v-on="on"
                  >
                    <v-icon
                      dense
                      small
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item
                    dense
                    @click="removeContact(contact.id)"
                  >
                    <v-list-item-content>
                      <v-list-item-title
                        class="red--text"
                      >
                        <v-icon
                          left
                          small
                          color="red"
                        >
                          mdi-delete
                        </v-icon>
                        Remove
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <template #default>
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
                    <v-icon>
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
                    <v-icon>
                      mdi-open-in-new
                    </v-icon>
                  </a>
                </v-col>
              </v-row>
            </div>
          </template>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-card-actions
      v-if="!isAddContactPage && contacts.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Contact } from '@/models/Contact'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  }
})
export default class PlatformContactsPage extends Vue {
  private contacts: Contact[] = []
  private isLoading = false
  private isSaving = false

  mounted () {
    this.isLoading = true
    this.$api.platforms.findRelatedContacts(this.platformId).then((foundContacts) => {
      this.contacts = foundContacts
      this.isLoading = false
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
      this.isLoading = false
    })
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isAddContactPage (): boolean {
    return this.$route.path === '/platforms/' + this.platformId + '/contacts/new'
  }

  removeContact (contactId: string): void {
    this.isSaving = true
    this.$api.platforms.removeContact(this.platformId, contactId).then(() => {
      const searchIndex = this.contacts.findIndex(c => c.id === contactId)
      if (searchIndex > -1) {
        this.contacts.splice(searchIndex, 1)
      }
      this.isSaving = false
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Removing contact failed')
      this.isSaving = false
    })
  }
}
</script>
