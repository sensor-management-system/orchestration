<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
    <ProgressIndicator
      v-model="isLoading"
    />
    <NuxtChild />
  </div>
</template>
<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'

import { SetTitleAction } from '@/store/appbar'
import { ContactsState, LoadContactAction } from '@/store/contacts'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator },
  computed: {
    ...mapState('contacts', ['contact'])
  },
  methods: {
    ...mapActions('contacts', ['loadContact']),
    ...mapActions('appbar', ['setTitle'])
  }
})
export default class ContactShowPage extends Vue {
  private isLoading: boolean = false

  // vuex definition for typescript check
  contact!: ContactsState['contact']
  loadContact!: LoadContactAction
  setTitle!: SetTitleAction

  async created () {
    try {
      this.isLoading = true
      this.initializeAppBar()
      await this.loadContact(this.contactId)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Loading contact failed')
    } finally {
      this.isLoading = false
    }
  }

  get contactId () {
    return this.$route.params.contactId
  }

  initializeAppBar () {
    if (this.contact) {
      this.setTitle(this.contact.toString())
    }
  }

  @Watch('contact', { immediate: true, deep: true })
  onContactChanged (val: ContactsState['contact'] | null): void {
    if (val && val.id) {
      this.setTitle(val?.toString())
    }
  }
}
</script>
