<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/devices/' + deviceId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu
        v-if="$auth.loggedIn"
      >
        <template #actions>
          <DotMenuActionCopy
            :path="'/devices/copy/' + deviceId"
          />
          <DotMenuActionDelete
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>
    <DeviceBasicData
      v-if="device"
      v-model="device"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        nuxt
        :to="'/devices/' + deviceId + '/basic/edit'"
      >
        Edit
      </v-btn>
      <DotMenu
        v-if="$auth.loggedIn"
      >
        <template #actions>
          <DotMenuActionCopy
            :path="'/devices/copy/' + deviceId"
          />
          <DotMenuActionDelete
            @click="initDeleteDialog"
          />
        </template>
      </DotMenu>
    </v-card-actions>
    <DeviceDeleteDialog
      v-if="device"
      v-model="showDeleteDialog"
      :device-to-delete="device"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import DeviceDeleteDialog from '@/components/devices/DeviceDeleteDialog.vue'
import DeviceBasicData from '@/components/DeviceBasicData.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionCopy from '@/components/DotMenuActionCopy.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Device } from '@/models/Device'
import { mapActions, mapState } from 'vuex'


@Component({
  components: {
    ProgressIndicator,
    DotMenuActionDelete,
    DotMenuActionCopy,
    DotMenu,
    DeviceDeleteDialog,
    DeviceBasicData
  },
  computed: mapState('devices',['device']),
  methods:mapActions('devices',['deleteDevice'])
})
export default class DeviceShowBasicPage extends Vue {
  private isSaving = false

  private showDeleteDialog: boolean = false

  get deviceId () {
    return this.$route.params.deviceId
  }

  initDeleteDialog () {
    this.showDeleteDialog = true
  }

  closeDialog () {
    this.showDeleteDialog = false
  }

  async deleteAndCloseDialog () {
    this.showDeleteDialog = false
    if (this.device === null) {
      return
    }
    try {
      this.isSaving=true
      this.deleteDevice(this.device.id)
      this.$store.commit('snackbar/setSuccess', 'Device deleted')
      this.$router.push('/devices')
    }catch (e){
      this.$store.commit('snackbar/setError', 'Device could not be deleted')
    }finally {
      this.isSaving=false
    }
  }
}
</script>
