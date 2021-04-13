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
        <v-autocomplete :items="allExceptSelected" :item-text="(x) => x" :item-value="(x) => x.id" label="New contact" @change="select" />
      </v-col>
      <v-col
        cols="12"
        md="2"
        align-self="center"
      >
        <v-btn
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
          :to="'/platforms/' + platformId + '/contacts'"
        >
          Cancel
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Contact } from '@/models/Contact'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    ProgressIndicator
  }
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
      this.isLoading = false
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to fetch related contacts')
      this.isLoading = false
    })
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  addContact (): void {
    if (this.selectedContact && this.selectedContact.id && this.isLoggedIn) {
      this.isSaving = true
      this.$api.platforms.addContact(this.platformId, this.selectedContact.id).then(() => {
        this.isSaving = false
        this.alreadyUsedContacts.push(this.selectedContact as Contact)
        this.$emit('input', this.alreadyUsedContacts)
        this.$router.push('/platforms/' + this.platformId + '/contacts')
      }).catch(() => {
        this.isSaving = false
        this.$store.commit('snackbar/setError', 'Failed to save contacts')
      })
    }
  }

  select (newContactId: string): void {
    const idx = this.allContacts.findIndex((c: Contact) => c.id === newContactId)
    if (idx > -1) {
      this.selectedContact = this.allContacts[idx]
    } else {
      this.selectedContact = null
    }
  }

  get allExceptSelected (): Contact[] {
    return this.allContacts.filter(c => !this.alreadyUsedContacts.find(rc => rc.id === c.id))
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
