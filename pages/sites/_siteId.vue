<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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
    />
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
          The site is archived. It is not possible to change the values. To edit it, ask a group administrator to restore the entity.
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

import { SetTitleAction, SetTabsAction } from '@/store/appbar'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import ModificationInfo from '@/components/ModificationInfo.vue'
import { LoadSiteAction, LoadSiteConfigurationsAction, SitesState } from '@/store/sites'
import { CanAccessEntityGetter, CanArchiveEntityGetter, CanDeleteEntityGetter, CanModifyEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'

@Component({
  components: {
    ProgressIndicator,
    ModificationInfo
  },
  computed: {
    ...mapState('sites', ['site', 'siteConfigurations']),
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity'])

  },
  methods: {
    ...mapActions('sites', ['loadSite', 'loadSiteConfigurations']),
    ...mapActions('appbar', ['setTitle', 'setTabs'])

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

  private isLoading: boolean = false

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

  mounted () {
    this.initializeAppBar()
  }

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await this.loadSite({
        siteId: this.siteId
      })
      if (this.site) {
        await this.loadSiteConfigurations(this.siteId)
      }

      if (!this.site || !this.canAccessEntity(this.site)) {
        this.$router.replace('/sites/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to access this site.')
        return
      }

      this.updatePermissions(this.site)

      if (this.isBasePath()) {
        this.$router.replace('/sites/' + this.siteId + '/basic')
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of site failed')
    } finally {
      this.isLoading = false
    }
  }

  get siteId () {
    return this.$route.params.siteId
  }

  isBasePath () {
    return this.$route.path === '/sites/' + this.siteId || this.$route.path === '/sites/' + this.siteId + '/'
  }

  initializeAppBar () {
    this.setTabs([
      {
        to: '/sites/' + this.siteId + '/basic',
        name: 'Basic Data'
      },
      {
        to: '/sites/' + this.siteId + '/contacts',
        name: 'Contacts'
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
