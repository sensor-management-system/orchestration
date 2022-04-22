<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/devices/' + deviceId + '/contacts/new'"
      >
        Add contact
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceContacts.length === 0">
      There are no contacts for this device.
    </hint-card>
    <v-expansion-panels>
      <v-expansion-panel
        v-for="contact in deviceContacts"
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
      v-if="deviceContacts.length>3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
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
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import HintCard from '@/components/HintCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator, HintCard },
  computed:mapState('devices',['deviceContacts']),
  methods:mapActions('devices',['loadDeviceContacts','removeDeviceContact'])
})
export default class DeviceShowContactPage extends Vue {

  private isSaving = false

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async removeContact(contactId:string):void{

    try {
      this.isSaving = true
      await this.removeDeviceContact({
        deviceId: this.deviceId,
        contactId: contactId
      })
      this.loadDeviceContacts(this.deviceId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Removing contact failed')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
