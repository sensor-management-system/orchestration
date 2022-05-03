<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/basic'"
        @save="save"
      />
    </v-card-actions>
    <PlatformBasicDataForm
      ref="basicForm"
      v-model="platformCopy"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/basic'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapActions, mapState } from 'vuex'
import PlatformBasicDataForm from '@/components/PlatformBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Platform } from '@/models/Platform'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    PlatformBasicDataForm,
    ProgressIndicator
  },
  middleware: ['auth'],
  computed: mapState('platforms', ['platform']),
  methods: mapActions('platforms', ['loadPlatform', 'savePlatform'])
})
export default class PlatformEditBasicPage extends Vue {
  private platformCopy: Platform = new Platform()
  private isSaving: boolean = false

  // vuex definition for typescript check
  platform!: Platform
  savePlatform!: (platform: Platform) => Promise<Platform>
  loadPlatform!: ({ platformId, includeContacts, includePlatformAttachments }: {platformId: string, includeContacts: boolean, includePlatformAttachments: boolean}) => void

  created () {
    this.platformCopy = Platform.createFromObject(this.platform)
  }

  get platformId () {
    return this.$route.params.platformId
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.isSaving = true
      await this.savePlatform(this.platformCopy)
      this.loadPlatform({
        platformId: this.platformId,
        includeContacts: false,
        includePlatformAttachments: false
      })
      this.$router.push('/platforms/' + this.platformId + '/basic')
      this.$store.commit('snackbar/setSuccess', 'Platform updated')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isSaving = false
    }
  }
}
</script>
