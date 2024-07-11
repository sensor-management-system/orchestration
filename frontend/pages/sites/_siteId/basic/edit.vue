<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/sites/' + siteId + '/basic'"
        @save="save"
      />
    </v-card-actions>
    <SiteBasicDataForm
      ref="basicForm"
      v-model="siteCopy"
      :site-usages="siteUsages"
      :site-types="siteTypes"
      :country-names="countryNames"
    />
    <non-model-options-form
      v-model="editOptions"
      :entity="siteCopy"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="editable"
        save-btn-text="Apply"
        :to="'/sites/' + siteId + '/basic'"
        @save="save"
      />
    </v-card-actions>

    <navigation-guard-dialog
      v-model="showNavigationWarning"
      :has-entity-changed="siteHasBeenEdited"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'

import { RawLocation } from 'vue-router'

import { mapActions, mapState, mapGetters } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { SitesState, LoadSiteAction, SaveSiteAction, LoadSiteAttachmentsAction, SaveSiteImagesAction, CreatePidAction } from '@/store/sites'

import { Site } from '@/models/Site'

import SiteBasicDataForm from '@/components/sites/SiteBasicDataForm.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'

import { hasSelfIntersection } from '@/utils/mapHelpers'
import { LoadSiteUsagesAction, LoadSiteTypesAction, VocabularyState, LoadCountriesAction, CountryNamesGetter } from '@/store/vocabulary'
import NonModelOptionsForm, { NonModelOptions } from '@/components/shared/NonModelOptionsForm.vue'

@Component({
  components: {
    SaveAndCancelButtons,
    SiteBasicDataForm,
    NavigationGuardDialog,
    NonModelOptionsForm
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['countryNames']),
    ...mapState('sites', ['site']),
    ...mapState('vocabulary', ['siteUsages', 'siteTypes'])
  },
  methods: {
    ...mapActions('sites', ['saveSite', 'loadSite', 'loadSiteAttachments', 'saveSiteImages', 'createPid']),
    ...mapActions('vocabulary', ['loadSiteUsages', 'loadSiteTypes', 'loadCountries']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class SiteEditBasicPage extends mixins(CheckEditAccess) {
  private siteCopy: Site | null = null
  private hasSaved: boolean = false
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null
  private editOptions: NonModelOptions = {
    persistentIdentifierShouldBeCreated: false
  }

  // vuex definition for typescript check
  site!: SitesState['site']
  siteAttachments!: SitesState['siteAttachments']
  saveSite!: SaveSiteAction
  loadSite!: LoadSiteAction
  siteUsages!: VocabularyState['siteUsages']
  loadSiteUsages!: LoadSiteUsagesAction
  siteTypes!: VocabularyState['siteTypes']
  loadSiteTypes!: LoadSiteTypesAction
  countryNames!: CountryNamesGetter
  loadCountries!: LoadCountriesAction
  setLoading!: SetLoadingAction
  loadSiteAttachments!: LoadSiteAttachmentsAction
  saveSiteImages!: SaveSiteImagesAction
  createPid!: CreatePidAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/sites/' + this.siteId + '/basic'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this Site / Lab.'
  }

  async fetch () {
    try {
      await Promise.all([
        this.loadSiteUsages(),
        this.loadSiteTypes(),
        this.loadCountries()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load site types or usages')
    }
  }

  async created () {
    if (this.site) {
      this.siteCopy = Site.createFromObject(this.site)
      try {
        this.setLoading(true)
        await this.loadSiteAttachments(this.siteId)
      } catch (e) {
        this.$store.commit('snackbar/setError', 'failed to fetch attachments')
      } finally {
        this.setLoading(false)
      }
    }
  }

  get siteId () {
    return this.$route.params.siteId
  }

  get siteHasBeenEdited () {
    if (!this.siteCopy) {
      return false
    }
    return (JSON.stringify(this.site) !== JSON.stringify(this.siteCopy))
  }

  async save () {
    if (!this.siteCopy) {
      return
    }
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    if (this.siteCopy.geometry.length !== 0 && this.siteCopy.geometry.length < 3) {
      this.$store.commit('snackbar/setError', 'Please draw at least 3 markers.')
      return
    }

    if (hasSelfIntersection(this.siteCopy.geometry)) {
      this.$store.commit('snackbar/setError', 'Area must not intersect')
      return
    }

    // handle images first
    try {
      this.setLoading(true)
      const savedImagesWithIds = await this.saveSiteImages({ siteId: this.siteId, siteImages: this.site!.images, siteCopyImages: this.siteCopy.images })
      this.siteCopy.images = savedImagesWithIds
    } catch (e) {
      this.$store.commit('snackbar/setWarning', 'Save of images failed')
    }

    try {
      this.setLoading(true)
      const savedSite = await this.saveSite(this.siteCopy)
      if (this.editOptions.persistentIdentifierShouldBeCreated) {
        try {
          savedSite.persistentIdentifier = await this.createPid(savedSite.id)
        } catch (e) {
          this.$store.commit('snackbar/setError', 'Creation of Persistent Identifier failed')
        }
      }
      await this.loadSite({
        siteId: savedSite.id,
        includeImages: true
      })
      this.hasSaved = true
      this.$store.commit('snackbar/setSuccess', 'Site / Lab updated')
      this.$router.push('/sites/' + this.siteId + '/basic')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (this.siteHasBeenEdited && !this.hasSaved) {
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
