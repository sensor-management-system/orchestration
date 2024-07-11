<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <center>
        <v-alert
          v-if="configuration && configuration.archived"
          icon="mdi-alert"
          type="warning"
          color="orange"
          text
          border="left"
          dense
          outlined
          prominent
        >
          The configuration is archived. It is not possible to change the values. To edit it, ask a group administrator to restore the entity.
        </v-alert>
      </center>
      <NuxtChild
        v-if="configuration"
      />
      <modification-info
        v-if="configuration"
        v-model="configuration"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, ProvideReactive, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'
import { CanAccessEntityGetter, CanModifyEntityGetter, CanDeleteEntityGetter, CanArchiveEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'
import { SetLoadingAction } from '@/store/progressindicator'
import { ConfigurationsState, LoadConfigurationAction } from '@/store/configurations'

import { Configuration } from '@/models/Configuration'

import ModificationInfo from '@/components/ModificationInfo.vue'

@Component({
  components: {
    ModificationInfo
  },
  computed: {
    ...mapState('configurations', ['configuration']),
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity'])
  },
  methods: {
    ...mapActions('configurations', ['loadConfiguration']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
// @ts-ignore
export default class ConfigurationsIdPage extends Vue {
  @ProvideReactive()
    editable: boolean = false

  @ProvideReactive()
    deletable: boolean = false

  @ProvideReactive()
    archivable: boolean = false

  @ProvideReactive()
    restoreable: boolean = false

  // vuex definition for typescript check
  configuration!: Configuration | null
  loadConfiguration!: LoadConfigurationAction
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction

  async created () {
    try {
      this.setLoading(true)
      this.initializeAppBar()
      await this.loadConfiguration(this.configurationId)

      if (!this.configuration) {
        throw new Error('initialization of configuration failed')
      }

      if (!this.canAccessEntity(this.configuration)) {
        this.$router.replace('/configurations/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to access this configuration.')
        return
      }

      this.updatePermissions(this.configuration)

      if (this.isBasePath()) {
        this.$router.replace('/configurations/' + this.configurationId + '/basic')
      }
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Loading configuration failed')
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
        to: '/configurations/' + this.configurationId + '/basic',
        name: 'Basic Data'
      },
      {
        to: '/configurations/' + this.configurationId + '/contacts',
        name: 'Contacts'
      },
      {
        to: '/configurations/' + this.configurationId + '/platforms-and-devices',
        name: 'Platforms and Devices'
      },
      {
        to: '/configurations/' + this.configurationId + '/locations',
        name: 'Locations'
      },
      {
        to: '/configurations/' + this.configurationId + '/parameters',
        name: 'Parameters'
      },
      {
        to: '/configurations/' + this.configurationId + '/customfields',
        name: 'Custom Fields'
      },
      {
        to: '/configurations/' + this.configurationId + '/attachments',
        name: 'Attachments'
      },
      {
        to: '/configurations/' + this.configurationId + '/actions',
        name: 'Actions'
      },
      {
        to: '/configurations/' + this.configurationId + '/tsm-linking',
        name: 'Data Linking',
        disabled: !this.$auth.loggedIn
      }
    ])
    this.setTitle(this.configuration?.label || 'Configuration')
  }

  get configurationId () {
    return this.$route.params.configurationId
  }

  isBasePath () {
    return this.$route.path === '/configurations/' + this.configurationId ||
      this.$route.path === '/configurations/' + this.configurationId + '/'
  }

  updatePermissions (configuration: ConfigurationsState['configuration']) {
    if (configuration) {
      this.editable = this.canModifyEntity(configuration)
      this.deletable = this.canDeleteEntity(configuration)
      this.archivable = this.canArchiveEntity(configuration)
      this.restoreable = this.canRestoreEntity(configuration)
    }
  }

  @Watch('configuration', { immediate: true, deep: true })
  onConfigurationChanged (val: Configuration): void {
    if (val && val.id) {
      this.setTitle(val.label || 'Configuration')
      this.updatePermissions(val)
    }
  }
}
</script>
