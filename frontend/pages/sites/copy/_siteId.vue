<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="siteToCopy"
          :disabled="!canModifyEntity(siteToCopy)"
          :to="'/sites'"
          save-btn-text="Copy"
          @save="save"
        />
      </v-card-actions>
      <v-alert
        border="left"
        colored-border
        color="primary"
        dense
      >
        <v-row dense>
          <v-col>
            <h3>Copy</h3>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyContacts" label="Contacts" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyAttachments" label="Attachments" />
          </v-col>
        </v-row>
      </v-alert>
      <SiteBasicDataForm
        v-if="siteToCopy"
        ref="basicForm"
        v-model="siteToCopy"
        :site-usages="siteUsages"
        :site-types="siteTypes"
        :country-names="countryNames"
      />
      <v-alert
        border="left"
        colored-border
        color="primary"
        dense
        class="mt-2"
      >
        <v-row dense>
          <v-col>
            <h3>Copy</h3>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyContacts" label="Contacts" />
          </v-col>
          <v-col cols="12" md="2">
            <v-checkbox v-model="copyAttachments" label="Attachments" />
          </v-col>
        </v-row>
      </v-alert>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          v-if="siteToCopy"
          :disabled="!canModifyEntity(siteToCopy)"
          :to="'/sites'"
          save-btn-text="Copy"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'
import { CanAccessEntityGetter, CanModifyEntityGetter, UserGroupsGetter } from '@/store/permissions'
import { LoadSiteAction, CopySiteAction, SitesState, LoadSiteAttachmentsAction } from '@/store/sites'
import { LoadSiteUsagesAction, LoadSiteTypesAction, VocabularyState, LoadCountriesAction, CountryNamesGetter } from '@/store/vocabulary'
import { Site } from '@/models/Site'

import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import SiteBasicDataForm from '@/components/sites/SiteBasicDataForm.vue'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { hasSelfIntersection } from '@/utils/mapHelpers'

@Component({
  components: {
    SaveAndCancelButtons,
    SiteBasicDataForm
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'userGroups']),
    ...mapGetters('vocabulary', ['countryNames']),
    ...mapState('sites', ['site']),
    ...mapState('vocabulary', ['siteUsages', 'siteTypes']),
    ...mapState('progressindicator', ['isLoading'])

  },
  methods: {
    ...mapActions('sites', ['copySite', 'loadSite', 'createPid', 'loadSiteAttachments']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('vocabulary', ['loadSiteUsages', 'loadSiteTypes', 'loadCountries']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class SiteCopyPage extends Vue {
  private siteToCopy: Site | null = null

  private copyContacts: boolean = true
  private copyAttachments: boolean = false

  // vuex definition for typescript check
  site!: SitesState['site']
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  userGroups!: UserGroupsGetter
  loadSite!: LoadSiteAction
  copySite!: CopySiteAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  siteUsages!: VocabularyState['siteUsages']
  loadSiteUsages!: LoadSiteUsagesAction
  siteTypes!: VocabularyState['siteTypes']
  loadSiteTypes!: LoadSiteTypesAction
  countryNames!: CountryNamesGetter
  loadCountries!: LoadCountriesAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction
  loadSiteAttachments!: LoadSiteAttachmentsAction

  async created () {
    this.initializeAppBar()
    try {
      this.setLoading(true)
      await this.loadSite({
        siteId: this.siteId,
        includeImages: true
      })

      try {
        await Promise.all([
          this.loadSiteUsages(),
          this.loadSiteTypes(),
          this.loadCountries(),
          this.loadSiteAttachments(this.siteId)
        ])
      } catch (e) {
        this.$store.commit('snackbar/setError', 'Failed to load types or usages')
      }

      if (!this.site || !this.canAccessEntity(this.site)) {
        this.$router.replace('/sites/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to copy this site / lab.')
        return
      }

      const siteCopy = this.getPreparedSiteForCopy()
      if (siteCopy) {
        this.siteToCopy = siteCopy
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading site / lab failed')
    } finally {
      this.setLoading(false)
    }
  }

  get siteId () {
    return this.$route.params.siteId
  }

  getPreparedSiteForCopy (): Site | null {
    if (!this.site) {
      return new Site()
    }
    const siteToEdit = Site.createFromObject(this.site)
    siteToEdit.id = ''
    siteToEdit.permissionGroups = this.userGroups.filter(userGroup => this.site?.permissionGroups.filter(group => userGroup.equals(group)).length)
    return siteToEdit
  }

  async save () {
    if (!this.siteToCopy) {
      return
    }

    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    if (this.siteToCopy.geometry.length !== 0 && this.siteToCopy.geometry.length < 3) {
      this.$store.commit('snackbar/setError', 'Please draw at least 3 markers.')
      return
    }

    if (hasSelfIntersection(this.siteToCopy.geometry)) {
      this.$store.commit('snackbar/setError', 'Area must not intersect')
      return
    }

    try {
      this.setLoading(true)
      const savedSiteId = await this.copySite({
        site: this.siteToCopy,
        copyContacts: this.copyContacts,
        copyAttachments: this.copyAttachments,
        originalSiteId: this.siteId
      })
      this.$store.commit('snackbar/setSuccess', 'Site / Lab copied')
      this.$router.push('/sites/' + savedSiteId)
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Copy failed')
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
        to: '/sites/copy/' + this.siteId,
        name: 'Basic Data'
      },
      {
        name: 'Contacts',
        disabled: true
      },
      {
        name: 'Related',
        disabled: true
      },
      {
        name: 'Locations',
        disabled: true
      },
      {
        name: 'Attachments',
        disabled: true
      }
    ])
    this.setTitle('Copy Site / Lab')
  }

  @Watch('site', { immediate: true, deep: true })
  onSiteChanged (val: SitesState['site']) {
    if (val && val.id) {
      this.setTitle('Copy ' + val.label)
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
