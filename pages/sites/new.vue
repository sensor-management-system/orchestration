<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
      dark
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/sites'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
      <SiteBasicDataForm
        ref="basicForm"
        v-model="site"
        :site-usages="siteUsages"
        :site-types="siteTypes"
        :country-names="countryNames"
      />
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          :to="'/sites'"
          save-btn-text="create"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState, mapGetters } from 'vuex'

import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import SiteBasicDataForm from '@/components/sites/SiteBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { Site } from '@/models/Site'
import { SaveSiteAction } from '@/store/sites'
import { SetTabsAction, SetTitleAction } from '@/store/appbar'
import { LoadEpsgCodesAction, LoadSiteUsagesAction, LoadSiteTypesAction, VocabularyState, LoadCountriesAction, CountryNamesGetter } from '@/store/vocabulary'

import { hasSelfIntersection } from '@/utils/mapHelpers'

@Component({
  components: {
    SaveAndCancelButtons, SiteBasicDataForm, ProgressIndicator
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['countryNames']),
    ...mapState('vocabulary', ['siteUsages', 'siteTypes'])
  },
  methods: {
    ...mapActions('sites', ['saveSite']),
    ...mapActions('vocabulary', ['loadEpsgCodes', 'loadSiteUsages', 'loadSiteTypes', 'loadCountries']),

    ...mapActions('appbar', ['setTitle', 'setTabs'])
  }
})
// @ts-ignore
export default class SiteNewPage extends Vue {
  private isLoading = false
  private site: Site = new Site()

  // vuex definition for typescript check
  loadEpsgCodes!: LoadEpsgCodesAction
  saveSite!: SaveSiteAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  siteUsages!: VocabularyState['siteUsages']
  loadSiteUsages!: LoadSiteUsagesAction
  siteTypes!: VocabularyState['siteTypes']
  loadSiteTypes!: LoadSiteTypesAction
  loadCountries!: LoadCountriesAction
  countryNames!: CountryNamesGetter

  async created () {
    this.initializeAppBar()
    try {
      await Promise.all([
        this.loadEpsgCodes(),
        this.loadSiteUsages(),
        this.loadSiteTypes(),
        this.loadCountries()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to load usages or types')
    }
  }

  async save () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    if (this.site.geometry.length !== 0 && this.site.geometry.length < 3) {
      this.$store.commit('snackbar/setError', 'Please draw at least 3 markers.')
      return
    }

    if (hasSelfIntersection(this.site.geometry)) {
      this.$store.commit('snackbar/setError', 'Area must not intersect')
      return
    }

    try {
      this.isLoading = true
      const savedSite = await this.saveSite(this.site)

      this.$store.commit('snackbar/setSuccess', 'Site / Lab created')
      this.$router.push('/sites/' + savedSite.id)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.isLoading = false
    }
  }

  initializeAppBar () {
    this.setTabs([
      {
        to: '/sites/new/',
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      }
    ])
    this.setTitle('New Site / Lab')
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
