<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
