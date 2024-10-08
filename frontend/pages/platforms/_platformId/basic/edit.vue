<!--
SPDX-FileCopyrightText: 2020 - 2024
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/basic'"
        @save="save"
      />
    </v-card-actions>
    <PlatformBasicDataForm
      ref="basicForm"
      v-model="platformCopy"
      :country-names="countryNames"
    />
    <NonModelOptionsForm
      v-model="editOptions"
      :entity="platformCopy"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/platforms/' + platformId + '/basic'"
        @save="save"
      />
    </v-card-actions>

    <navigation-guard-dialog
      v-model="showNavigationWarning"
      :has-entity-changed="platformHasBeenEdited"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'

import { RawLocation } from 'vue-router'
import { mapActions, mapGetters, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { PlatformsState, LoadPlatformAction, SavePlatformAction, LoadPlatformAttachmentsAction, SavePlatformImagesAction, CreatePidAction } from '@/store/platforms'

import { Platform } from '@/models/Platform'

import PlatformBasicDataForm from '@/components/PlatformBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'
import { LoadCountriesAction } from '@/store/vocabulary'

@Component({
  components: {
    SaveAndCancelButtons,
    PlatformBasicDataForm,
    NavigationGuardDialog,
    NonModelOptionsForm
  },
  middleware: ['auth'],
  computed: {
    ...mapState('platforms', ['platform', 'platformAttachments']),
    ...mapGetters('vocabulary', ['countryNames'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadCountries']),
    ...mapActions('platforms', ['loadPlatform', 'savePlatform', 'createPid', 'savePlatformImages', 'loadPlatformAttachments']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformEditBasicPage extends mixins(CheckEditAccess) {
  private platformCopy: Platform | null = null

  private hasSaved: boolean = false
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null
  private editOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  platform!: PlatformsState['platform']
  savePlatform!: SavePlatformAction
  loadPlatform!: LoadPlatformAction
  createPid!: CreatePidAction
  setLoading!: SetLoadingAction
  loadCountries!: LoadCountriesAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  savePlatformImages!: SavePlatformImagesAction
  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/platforms/' + this.platformId + '/basic'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this platform.'
  }

  async created () {
    if (this.platform) {
      this.platformCopy = Platform.createFromObject(this.platform)
      try {
        this.setLoading(true)
        await this.loadPlatformAttachments(this.platformId)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'failed to fetch attachments')
      } finally {
        this.setLoading(false)
      }
    }
    await this.loadCountries()
  }

  get platformId () {
    return this.$route.params.platformId
  }

  get platformHasBeenEdited () {
    if (!this.platformCopy) {
      return false
    }
    return (JSON.stringify(this.platform) !== JSON.stringify(this.platformCopy))
  }

  async save () {
    if (!this.platformCopy) {
      return
    }
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    // handle images first
    try {
      this.setLoading(true)
      const savedImagesWithIds = await this.savePlatformImages({ platformId: this.platformId, platformImages: this.platform!.images, platformCopyImages: this.platformCopy.images })
      this.platformCopy.images = savedImagesWithIds
    } catch (e) {
      this.$store.commit('snackbar/setWarning', 'Save of images failed')
    }

    try {
      this.setLoading(true)
      const savedPlatform = await this.savePlatform(this.platformCopy)
      if (this.editOptions.persistentIdentifierShouldBeCreated) {
        try {
          savedPlatform.persistentIdentifier = await this.createPid(savedPlatform.id)
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Creation of Persistent Identifier failed')
        }
      }
      await this.loadPlatform({
        platformId: this.platformId,
        includeContacts: false,
        includeImages: true,
        includePlatformAttachments: false
      })
      this.hasSaved = true

      this.$router.push('/platforms/' + this.platformId + '/basic')
      this.$store.commit('snackbar/setSuccess', 'Platform updated')
      this.$router.push('/platforms/' + this.platformId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (this.platformHasBeenEdited && !this.hasSaved) {
      if (this.to) {
        next()
      } else {
        this.to = to
        this.showNavigationWarning = true
      }
    } else {
      return next()
    }
  }
}
</script>
