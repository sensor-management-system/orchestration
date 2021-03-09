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
        :to="'/devices/' + deviceId + '/contacts/new'"
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
                <template v-slot:activator="{ on }">
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
                        Remove contact
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
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
                </v-col>
                <v-col
                  cols="12"
                  md="6"
                >
                  <label>Website:</label>
                  {{ contact.website | orDefault }}
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
        :to="'/devices/' + deviceId + '/contacts/new'"
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
export default class DeviceContactsPage extends Vue {
  private contacts: Contact[] = []
  private isLoading = false
  private isSaving = false

  mounted () {
    this.isLoading = true
    this.$api.devices.findRelatedContacts(this.deviceId).then((foundContacts) => {
      this.contacts = foundContacts
      this.isLoading = false
    }).catch((e) => {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
      this.isLoading = false
    })
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isAddContactPage (): boolean {
    return this.$route.path === '/devices/' + this.deviceId + '/contacts/new'
  }

  removeContact (contactId: string): void {
    this.isSaving = true
    this.$api.devices.removeContact(this.deviceId, contactId).then(() => {
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
