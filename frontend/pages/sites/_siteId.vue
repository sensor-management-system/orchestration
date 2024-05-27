<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <center>
        <v-alert
          v-if="site && site.archived"
          icon="mdi-alert"
          type="warning"
          color="orange"
          text
          border="left"
          dense
          outlined
          prominent
        >
          The site / lab is archived. It is not possible to change the values. To edit it, ask a group administrator to restore the entity.
        </v-alert>
      </center>
      <NuxtChild
        v-if="site"
      />
      <modification-info
        v-if="site"
        v-model="site"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, ProvideReactive, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState, mapGetters } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'

import { SetLoadingAction } from '@/store/progressindicator'
import ModificationInfo from '@/components/ModificationInfo.vue'
import { LoadSiteAction, LoadSiteConfigurationsAction, SitesState } from '@/store/sites'
import { CanAccessEntityGetter, CanArchiveEntityGetter, CanDeleteEntityGetter, CanModifyEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'

@Component({
  components: {
    ModificationInfo
  },
  computed: {
    ...mapState('sites', ['site', 'siteConfigurations']),
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity'])

  },
  methods: {
    ...mapActions('sites', ['loadSite', 'loadSiteConfigurations']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])

  }
})
export default class SitePage extends Vue {
  @ProvideReactive()
    editable: boolean = false

  @ProvideReactive()
    deletable: boolean = false

  @ProvideReactive()
    archivable: boolean = false

  @ProvideReactive()
    restoreable: boolean = false

  // vuex definition for typescript check
  site!: SitesState['site']
  loadSite!: LoadSiteAction
  loadSiteConfigurations!: LoadSiteConfigurationsAction
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction

  mounted () {
    this.initializeAppBar()
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await this.loadSite({
        siteId: this.siteId,
        includeImages: true
      })
      if (this.site) {
        await this.loadSiteConfigurations(this.siteId)
      }

      if (!this.site || !this.canAccessEntity(this.site)) {
        this.$router.replace('/sites/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to access this site / lab.')
        return
      }

      this.updatePermissions(this.site)

      if (this.isBasePath()) {
        this.$router.replace('/sites/' + this.siteId + '/basic')
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of site / lab failed')
    } finally {
      this.setLoading(false)
    }
  }

  get siteId () {
    return this.$route.params.siteId
  }

  isBasePath () {
    return this.$route.path === '/sites/' + this.siteId || this.$route.path === '/sites/' + this.siteId + '/'
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    this.setTabs([
      {
        to: '/sites/' + this.siteId + '/basic',
        name: 'Basic Data'
      },
      {
        to: '/sites/' + this.siteId + '/contacts',
        name: 'Contacts'
      },
      {
        to: '/sites/' + this.siteId + '/related',
        name: 'Related'
      },
      {
        to: '/sites/' + this.siteId + '/locations',
        name: 'Locations'
      },
      {
        to: '/sites/' + this.siteId + '/attachments',
        name: 'Attachments'
      }
    ])
    if (this.site) {
      this.setTitle(this.site.label)
    }
  }

  updatePermissions (site: SitesState['site']) {
    if (site) {
      this.editable = this.canModifyEntity(site)
      this.deletable = this.canDeleteEntity(site)
      this.restoreable = this.canRestoreEntity(site)
      this.archivable = this.canArchiveEntity(site)
    }
  }

  @Watch('site', { immediate: true, deep: true })
  onSiteChanged (val: SitesState['site']) {
    if (val && val.id) {
      this.setTitle(val.label)
      this.updatePermissions(val)
    }
  }
}
</script>
