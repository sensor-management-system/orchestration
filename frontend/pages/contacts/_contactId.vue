<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <NuxtChild
      v-if="contact"
    />
  </div>
</template>
<script lang="ts">
import { Component, Vue, Watch, ProvideReactive } from 'nuxt-property-decorator'

import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetShowBackButtonAction } from '@/store/appbar'
import { ContactsState, LoadContactAction } from '@/store/contacts'

import { SetLoadingAction } from '@/store/progressindicator'
import { CanDeleteContactGetter, CanModifyContactGetter } from '@/store/permissions'

@Component({
  computed: {
    ...mapState('contacts', ['contact']),
    ...mapGetters('permissions', ['canModifyContact', 'canDeleteContact'])
  },
  methods: {
    ...mapActions('contacts', ['loadContact']),
    ...mapActions('appbar', ['setTitle', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ContactShowPage extends Vue {
  @ProvideReactive()
    editable: boolean = false

  @ProvideReactive()
    deletable: boolean = false

  // vuex definition for typescript check
  contact!: ContactsState['contact']
  loadContact!: LoadContactAction
  setTitle!: SetTitleAction
  canModifyContact!: CanModifyContactGetter
  canDeleteContact!: CanDeleteContactGetter
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction

  async created () {
    if (!this.$auth.loggedIn) {
      this.$router.replace('/', () => {
        this.$store.commit('snackbar/setError', 'Login is required to see this page.')
      })
      return
    }

    try {
      this.setLoading(true)
      this.initializeAppBar()
      await this.loadContact(this.contactId)
      this.updatePermissions(this.contact)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading contact failed')
    } finally {
      this.setLoading(false)
    }
  }

  get contactId () {
    return this.$route.params.contactId
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    if (this.contact) {
      this.setTitle(this.contact.toString())
    }
  }

  updatePermissions (contact: ContactsState['contact']) {
    if (contact) {
      this.editable = this.canModifyContact(contact)
      this.deletable = this.canDeleteContact(contact)
    }
  }

  @Watch('contact', { immediate: true, deep: true })
  onContactChanged (val: ContactsState['contact'] | null): void {
    if (val && val.id) {
      this.setTitle(val?.toString())
      this.updatePermissions(val)
    }
  }
}
</script>
