<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/platforms'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
      <PlatformBasicDataForm
        ref="basicForm"
        v-model="platform"
        :country-names="countryNames"
      />
      <NonModelOptionsForm
        v-model="createOptions"
        :entity="platform"
      />
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/platforms'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
    </v-card>
    <serial-number-warning-dialog v-model="showSerialNumberWarning" entity="platform" @confirm="saveWithoutSerialNumber" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'
import { CreatePidAction, SavePlatformAction, ClearPlatformAttachmentsAction } from '@/store/platforms'

import { SetLoadingAction } from '@/store/progressindicator'
import PlatformBasicDataForm from '@/components/PlatformBasicDataForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'
import SerialNumberWarningDialog from '@/components/shared/SerialNumberWarningDialog.vue'

import { Platform } from '@/models/Platform'
import { LoadCountriesAction } from '@/store/vocabulary'

@Component({
  components: {
    SaveAndCancelButtons,
    PlatformBasicDataForm,
    NonModelOptionsForm,
    SerialNumberWarningDialog
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['countryNames'])
  },
  methods: {
    ...mapActions('platforms', ['savePlatform', 'createPid', 'clearPlatformAttachments']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('vocabulary', ['loadCountries'])
  }
})
// @ts-ignore
export default class PlatformNewPage extends Vue {
  private platform: Platform = new Platform()

  private showSerialNumberWarning = false
  private wantsToSaveWithoutSerialNumber = false
  private createOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  savePlatform!: SavePlatformAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  createPid!: CreatePidAction
  setLoading!: SetLoadingAction
  loadCountries!: LoadCountriesAction
  setShowBackButton!: SetShowBackButtonAction
  clearPlatformAttachments!: ClearPlatformAttachmentsAction

  async created () {
    this.initializeAppBar()
    this.clearPlatformAttachments()

    try {
      await this.loadCountries()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load countries')
    }
  }

  saveWithoutSerialNumber () {
    this.wantsToSaveWithoutSerialNumber = true
    this.save()
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    if (this.platform.serialNumber === '') {
      if (!this.wantsToSaveWithoutSerialNumber) {
        this.showSerialNumberWarning = true
        return
      }
    }

    try {
      this.setLoading(true)
      const savedPlatform = await this.savePlatform(this.platform)
      if (this.createOptions.persistentIdentifierShouldBeCreated) {
        try {
          savedPlatform.persistentIdentifier = await this.createPid(savedPlatform.id)
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Creation of Persistent Identifier failed')
        }
      }
      this.$store.commit('snackbar/setSuccess', 'Platform created')
      this.$router.push('/platforms/' + savedPlatform.id)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Creation of platform failed')
    } finally {
      this.setLoading(false)
    }
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    this.setTabs([
      {
        to: '/platforms/new',
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      },
      {
        name: 'Parameters',
        disabled: true
      },
      {
        name: 'Attachments',
        disabled: true
      },
      {
        name: 'Export Control',
        disabled: true
      },
      {
        name: 'Actions',
        disabled: true
      }
    ])
    this.setTitle('New Platform')
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
