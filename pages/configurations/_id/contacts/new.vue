<template>
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-row>
      <v-col
        cols="12"
        md="5"
      >
        <v-autocomplete
          :items="allExceptSelected"
          :item-text="(x) => x"
          :item-value="(x) => x.id"
          label="New contact"
          @change="select"
        />
      </v-col>
      <v-col
        cols="12"
        md="2"
        align-self="center"
      >
        <v-btn
          v-if="isLoggedIn"
          small
          color="primary"
          :disabled="selectedContact == null"
          @click="addContact"
        >
          Add
        </v-btn>
        <v-btn
          small
          text
          nuxt
          :to="'/configurations/' + configurationId + '/contacts'"
        >
          Cancel
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Contact } from '@/models/Contact'

@Component({
  components: { ProgressIndicator }
})
export default class PlatformAddContactPage extends Vue {
  private alreadyUsedContacts: Contact[] = []
  private allContacts: Contact[] = []
  private selectedContact: Contact | null = null
  private isLoading: boolean = false
  private isSaving: boolean = false

  @Prop({
    default: () => [] as Contact[],
    required: true,
    type: Array
  })
  readonly value!: Contact[]

  created () {
    this.alreadyUsedContacts = [...this.value] as Contact[]
  }

  mounted () {
    this.isLoading = true
    this.$api.contacts.findAll().then((foundContacts) => {
      this.allContacts = foundContacts
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to fetch related contacts')
    }).finally(() => {
      this.isLoading = false
    })
  }

  get configurationId (): string {
    return this.$route.params.id
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get allExceptSelected (): Contact[] {
    return this.allContacts.filter(c => !this.alreadyUsedContacts.find(rc => rc.id === c.id))
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  select (newContactId: string): void {
    const idx = this.allContacts.findIndex((c: Contact) => c.id === newContactId)
    if (idx > -1) {
      this.selectedContact = this.allContacts[idx]
    } else {
      this.selectedContact = null
    }
  }

  addContact () {
    if (this.selectedContact && this.selectedContact.id && this.isLoggedIn) {
      this.isSaving = true
      this.$store.dispatch('contacts/addContactToConfiguration', {
        configurationId: this.configurationId,
        contactId: this.selectedContact.id
      }).then(() => {
        this.$router.push('/configurations/' + this.configurationId + '/contacts')
      }).catch(() => {
        this.$store.commit('snackbar/setError', 'Failed to add a contact')
      }).finally(() => {
        this.isSaving = false
      })
    }
  }
}
</script>

<style scoped>

</style>
