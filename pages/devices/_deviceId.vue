<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
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
      <NuxtChild />
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

import { SetTitleAction, SetTabsAction } from '@/store/appbar'
import { DevicesState, LoadDeviceAction } from '@/store/devices'
import { CanAccessEntityGetter, CanModifyEntityGetter, CanDeleteEntityGetter } from '@/store/permissions'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import ModificationInfo from '@/components/ModificationInfo.vue'

@Component({
  components: {
    ProgressIndicator,
    ModificationInfo
  },
  computed: {
    ...mapState('devices', ['device']),
    ...mapGetters('permissions', ['canAccessEntity', 'canModifyEntity', 'canDeleteEntity'])
  },
  methods: {
    ...mapActions('devices', ['loadDevice']),
    ...mapActions('appbar', ['setTitle', 'setTabs'])

  }
})
export default class DevicePage extends Vue {
  @ProvideReactive()
    editable: boolean = false

  @ProvideReactive()
    deletable: boolean = false

  private isLoading: boolean = false

  // vuex definition for typescript check
  device!: DevicesState['device']
  loadDevice!: LoadDeviceAction
  canAccessEntity!: CanAccessEntityGetter
  canModifyEntity!: CanModifyEntityGetter
  canDeleteEntity!: CanDeleteEntityGetter
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction

  mounted () {
    this.initializeAppBar()
  }

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      await this.loadDevice({
        deviceId: this.deviceId,
        includeContacts: false,
        includeCustomFields: false,
        includeDeviceProperties: false,
        includeDeviceAttachments: false,
        includeCreatedBy: true,
        includeUpdatedBy: true
      })

      if (!this.device || !this.canAccessEntity(this.device)) {
        this.$router.replace('/devices/')
        this.$store.commit('snackbar/setError', 'You\'re not allowed to access this device.')
        return
      }

      this.editable = this.canModifyEntity(this.device)
      this.deletable = this.canDeleteEntity(this.device)

      if (this.isBasePath()) {
        this.$router.replace('/devices/' + this.deviceId + '/basic')
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of device failed')
    } finally {
      this.isLoading = false
    }
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  isBasePath () {
    return this.$route.path === '/devices/' + this.deviceId || this.$route.path === '/devices/' + this.deviceId + '/'
  }

  initializeAppBar () {
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
        to: '/devices/' + this.deviceId + '/customfields',
        name: 'Custom Fields'
      },
      {
        to: '/devices/' + this.deviceId + '/attachments',
        name: 'Attachments'
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

  @Watch('device', { immediate: true, deep: true })
  onDeviceChanged (val: DevicesState['device']) {
    if (val && val.id) {
      this.setTitle(val.shortName)
    }
  }
}
</script>
