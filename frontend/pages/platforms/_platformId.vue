<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <v-card flat>
      <center>
        <v-alert
          v-if="platform && platform.archived"
          icon="mdi-alert"
          type="warning"
          color="orange"
          text
          border="left"
          dense
          outlined
          prominent
        >
          The platform is archived. It is not possible to change the values. To edit it, ask a group administrator to restore the entity.
        </v-alert>
      </center>
      <NuxtChild
        v-if="platform"
      />
      <modification-info
        v-if="platform"
        v-model="platform"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, ProvideReactive, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'
import { PlatformsState, LoadPlatformAction } from '@/store/platforms'
import { CanAccessEntityGetter, CanModifyEntityGetter, CanDeleteEntityGetter, CanArchiveEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'

import { SetLoadingAction } from '@/store/progressindicator'
import ModificationInfo from '@/components/ModificationInfo.vue'

@Component({
  components: {
    ModificationInfo
  },
  computed: {
    ...mapState('platforms', ['platform']),
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity'])
  },
  methods: {
    ...mapActions('platforms', ['loadPlatform']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformPage extends Vue {
  @ProvideReactive()
    editable: boolean = false

  @ProvideReactive()
    deletable: boolean = false

  @ProvideReactive()
    archivable: boolean = false

  @ProvideReactive()
    restoreable: boolean = false

  // vuex definition for typescript check
  platform!: PlatformsState['platform']
  loadPlatform!: LoadPlatformAction
  initPlatformsPlatformIdAppBar!: (id: string) => void
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction

  created () {
    this.initializeAppBar()
  }

  async fetch () {
    try {
      this.setLoading(true)
      await this.loadPlatform({
        platformId: this.platformId,
        includeContacts: false,
        includePlatformAttachments: false,
        includeCreatedBy: true,
        includeUpdatedBy: true
      }
      )
      if (!this.platform || !this.canAccessEntity(this.platform)) {
        this.$router.replace('/platforms/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to access this platform.')
        return
      }

      this.updatePermissions(this.platform)

      if (this.isBasePath()) {
        this.$router.replace('/platforms/' + this.platformId + '/basic')
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading platform failed')
      this.$router.replace('/platforms/')
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
        to: '/platforms/' + this.platformId + '/basic',
        name: 'Basic Data'
      },
      {
        to: '/platforms/' + this.platformId + '/contacts',
        name: 'Contacts'
      },
      {
        to: '/platforms/' + this.platformId + '/parameters',
        name: 'Parameters'
      },
      {
        to: '/platforms/' + this.platformId + '/attachments',
        name: 'Attachments'
      },
      {
        to: '/platforms/' + this.platformId + '/actions',
        name: 'Actions'
      }
    ]
    )
    if (this.platform) {
      this.setTitle(this.platform.shortName || 'Platform')
    }
  }

  get platformId () {
    return this.$route.params.platformId
  }

  isBasePath () {
    return this.$route.path === '/platforms/' + this.platformId || this.$route.path === '/platforms/' + this.platformId + '/'
  }

  updatePermissions (platform: PlatformsState['platform']) {
    if (platform) {
      this.editable = this.canModifyEntity(platform)
      this.deletable = this.canDeleteEntity(platform)
      this.archivable = this.canArchiveEntity(platform)
      this.restoreable = this.canRestoreEntity(platform)
    }
  }

  @Watch('platform', { immediate: true, deep: true })
  onPlatformChanged (val: PlatformsState['platform']) {
    if (val && val.id) {
      this.setTitle(val.shortName)
      this.updatePermissions(val)
    }
  }
}
</script>
