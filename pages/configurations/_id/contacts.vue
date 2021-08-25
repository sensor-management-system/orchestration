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
        :to="'/configurations/' + configurationId + '/contacts/new'"
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
        :to="'/configurations/' + configurationId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

import ContactBasicData from '@/components/ContactBasicData.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator, ContactBasicData }
})
export default class ContactTab extends Vue {
  private contacts: Contact[] = []
  private isLoading = false
  private isSaving = false

  mounted () {
    this.loadConfigurationContacts()
  }

  beforeRouteUpdate (to: any, _from:any, next:any) {
    if (to.name === 'configurations-id-contacts') {
      this.loadConfigurationContacts()
    }
    next()
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  loadConfigurationContacts () {
    this.isLoading = true
    this.$api.configurations.findRelatedContacts(this.configurationId).then((foundContacts) => {
      this.contacts = foundContacts
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    }).finally(() => {
      this.isLoading = false
    })
  }

  get configurationId (): string {
    return this.$route.params.id
  }

  async removeContact (id: string) {
    try {
      this.isLoading = true
      await this.$store.dispatch('contacts/removeContactFromConfiguration', {
        configurationId: this.configurationId,
        contactId: id
      })
      // reloading contacts to refresh the list
      this.loadConfigurationContacts()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Removing contact failed')
    } finally {
      this.isLoading = false
    }
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isAddContactPage (): boolean {
    return this.$route.path === '/configurations/' + this.configurationId + '/contacts/new'
  }
}
</script>
