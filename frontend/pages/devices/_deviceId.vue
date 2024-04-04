<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <v-card flat>
      <center>
        <v-alert
          v-if="device && device.archived"
          icon="mdi-alert"
          type="warning"
          color="orange"
          text
          border="left"
          dense
          outlined
          prominent
        >
          The device is archived. It is not possible to change the values. To edit it, ask a group administrator to restore the entity.
        </v-alert>
      </center>
      <NuxtChild
        v-if="device"
      />
      <modification-info
        v-if="device"
        v-model="device"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, ProvideReactive, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { SetTitleAction, SetTabsAction, SetShowBackButtonAction } from '@/store/appbar'
import { DevicesState, LoadDeviceAction } from '@/store/devices'
import { CanAccessEntityGetter, CanModifyEntityGetter, CanDeleteEntityGetter, CanArchiveEntityGetter, CanRestoreEntityGetter } from '@/store/permissions'

import { SetLoadingAction } from '@/store/progressindicator'
import ModificationInfo from '@/components/ModificationInfo.vue'

@Component({
  components: {
    ModificationInfo
  },
  computed: {
    ...mapState('devices', ['device']),
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'canDeleteEntity', 'canArchiveEntity', 'canRestoreEntity'])
  },
  methods: {
    ...mapActions('devices', ['loadDevice']),
    ...mapActions('appbar', ['setTitle', 'setTabs', 'setShowBackButton']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DevicePage extends Vue {
  @ProvideReactive()
    editable: boolean = false

  @ProvideReactive()
    deletable: boolean = false

  @ProvideReactive()
    archivable: boolean = false

  @ProvideReactive()
    restoreable: boolean = false

  // vuex definition for typescript check
  device!: DevicesState['device']
  loadDevice!: LoadDeviceAction
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
      await this.loadDevice({
        deviceId: this.deviceId,
        includeContacts: false,
        includeCustomFields: false,
        includeDeviceProperties: false,
        includeDeviceAttachments: false,
        includeImages: true,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })

      if (!this.device || !this.canAccessEntity(this.device)) {
        this.$router.replace('/devices/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to access this device.')
        return
      }

      this.updatePermissions(this.device)

      if (this.isBasePath()) {
        this.$router.replace('/devices/' + this.deviceId + '/basic')
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of device failed')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  isBasePath () {
    return this.$route.path === '/devices/' + this.deviceId || this.$route.path === '/devices/' + this.deviceId + '/'
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    this.setTabs([
      {
        to: '/devices/' + this.deviceId + '/basic',
        name: 'Basic Data'
      },
      {
        to: '/devices/' + this.deviceId + '/contacts',
        name: 'Contacts'
      },
      {
        to: '/devices/' + this.deviceId + '/measuredquantities',
        name: 'Measured Quantities'
      },
      {
        to: '/devices/' + this.deviceId + '/parameters',
        name: 'Parameters'
      },
      {
        to: '/devices/' + this.deviceId + '/customfields',
        name: 'Custom Fields'
      },
      {
        to: '/devices/' + this.deviceId + '/attachments',
        name: 'Attachments'
      },
      {
        to: '/devices/' + this.deviceId + '/export-control',
        name: 'Export Control'
      },
      {
        to: '/devices/' + this.deviceId + '/actions',
        name: 'Actions'
      }
    ])
    if (this.device) {
      this.setTitle(this.device.shortName)
    }
  }

  updatePermissions (device: DevicesState['device']) {
    if (device) {
      this.editable = this.canModifyEntity(device)
      this.deletable = this.canDeleteEntity(device)
      this.restoreable = this.canRestoreEntity(device)
      this.archivable = this.canArchiveEntity(device)
    }
  }

  @Watch('device', { immediate: true, deep: true })
  onDeviceChanged (val: DevicesState['device']) {
    if (val && val.id) {
      this.setTitle(val.shortName)
      this.updatePermissions(val)
    }
  }
}
</script>
