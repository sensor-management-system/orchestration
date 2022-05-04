<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
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
      v-model="contactRoles"
    />
    <v-card-actions
      v-if="!isAddContactPage"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/platforms/' + platformId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
    <hint-card v-if="contactRoles.length === 0 && !isAddContactPage">
      There are no contacts for this platform.
    </hint-card>
    <v-expansion-panels>
      <v-expansion-panel
        v-for="contactRole in contactRoles"
        :key="contactRole.id"
      >
        <v-expansion-panel-header>
          <contact-role-header-row :value="contactRole">
            <v-menu
              v-if="$auth.loggedIn"
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
                  @click="removeContactRole(contactRole.id)"
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
          </contact-role-header-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <template #default>
            <contact-role-panel :value="contactRole" />
          </template>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-card-actions
      v-if="!isAddContactPage && contactRoles.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
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
import { ContactRole } from '@/models/ContactRole'

import HintCard from '@/components/HintCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import ContactRoleHeaderRow from '@/components/contacts/ContactRoleHeaderRow.vue'
import ContactRolePanel from '@/components/contacts/ContactRolePanel.vue'

@Component({
  components: {
    ContactRoleHeaderRow,
    ContactRolePanel,
    HintCard,
    ProgressIndicator
  }
})
export default class PlatformContactsPage extends Vue {
  private contactRoles: ContactRole[] = []
  private isLoading = false
  private isSaving = false

  async fetch () {
    this.isLoading = true
    try {
      this.contactRoles = await this.$api.platforms.findRelatedContactRoles(this.platformId)
    } catch (_err) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contact roles')
    } finally {
      this.isLoading = false
    }
  }

  head () {
    return {
      titleTemplate: 'Contacts - %s'
    }
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isAddContactPage (): boolean {
    return this.$route.path === '/platforms/' + this.platformId + '/contacts/new'
  }

  async removeContactRole (contactRoleId: string) {
    try {
      this.isSaving = true
      await this.$api.platforms.removeContact(contactRoleId)
      const searchIndex = this.contactRoles.findIndex(cr => cr.id === contactRoleId)
      if (searchIndex > -1) {
        this.contactRoles.splice(searchIndex, 1)
      }
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Removing contact failed')
    } finally {
      this.isSaving = false
    }
  }
}
</script>
