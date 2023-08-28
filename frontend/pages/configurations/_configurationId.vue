<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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

import { SetTitleAction, SetTabsAction } from '@/store/appbar'
import { CanAccessEntityGetter, CanModifyEntityGetter, CanDeleteEntityGetter, CanArchiveEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'

import { Configuration } from '@/models/Configuration'

import { SetLoadingAction } from '@/store/progressindicator'
import ModificationInfo from '@/components/ModificationInfo.vue'
import { ConfigurationsState } from '@/store/configurations'

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
    ...mapActions('appbar', ['setTitle', 'setTabs']),
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
  loadConfiguration!: (id: string) => void
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  canArchiveEntity!: CanArchiveEntityGetter
  canRestoreEntity!: CanRestoreEntityGetter
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  setLoading!: SetLoadingAction

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
        name: 'TSM-Linkings',
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
