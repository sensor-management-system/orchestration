<template>
  <div>
    <v-row v-if="isLoggedIn">
      <v-col>
        <v-btn nuxt :to="'/devices/show/' + deviceId + '/contacts/new'">
          Add contact
        </v-btn>
      </v-col>
    </v-row>
    <div v-if="isLoading">
      <v-progress-circular indeterminate />
    </div>
    <div v-else>
      <v-expansion-panels>
        <v-expansion-panel
          v-for="contact in contacts"
          :key="contact.id"
        >
          <v-expansion-panel-header>
            {{ contact.toString() }}
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <template>
              <div>
                <v-row
                  dense
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
                  >
                    {{ contact.familyName }}
                  </v-col>
                </v-row>
                <v-row
                  dense
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
                    E-Mail:
                  </v-col>
                  <v-col
                    cols="8"
                    xs="8"
                    sm="9"
                    md="4"
                    lg="4"
                    xl="5"
                  >
                    {{ contact.email }}
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
                    {{ contact.website }}
                  </v-col>
                </v-row>
                <v-row v-if="isLoggedIn">
                  <v-btn @click="removeContact(contact.id)">
                    Remove from device
                  </v-btn>
                </v-row>
              </div>
            </template>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { Contact } from '@/models/Contact'

@Component({
})
export default class DeviceShowContactsPage extends Vue {
  private contacts: Contact[] = []
  private isLoading = true

  mounted () {
    this.$api.devices.findRelatedContacts(this.deviceId).then((foundContacts) => {
      this.contacts = foundContacts
      this.isLoading = false
    })
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }

  removeContact (contactId: string) {
    this.$api.devices.removeContact(this.deviceId, contactId).then(() => {
      const searchIndex = this.contacts.findIndex(c => c.id === contactId)
      if (searchIndex > -1) {
        this.contacts.splice(searchIndex, 1)
      }
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Removing contact failed')
    })
  }
}
</script>
