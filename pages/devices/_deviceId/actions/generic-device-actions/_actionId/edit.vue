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
    <v-card-actions>
      <v-spacer />
      <ActionButtonTray
        :cancel-url="'/devices/' + deviceId + '/actions'"
        @apply="save"
      />
    </v-card-actions>

    <!-- just to be consistent with the new mask, we show the selected action type as an disabled v-select here -->
    <v-select
      :value="action.actionTypeName"
      :items="[action.actionTypeName]"
      :item-text="(x) => x"
      disabled
      label="Action Type"
    />
    <GenericActionForm
      ref="genericDeviceActionForm"
      v-model="action"
      :attachments="deviceAttachments"
      :current-user-mail="$auth.user.email"
    />

    <v-card-actions>
      <v-spacer />
      <ActionButtonTray
        :cancel-url="'/devices/' + deviceId + '/actions'"
        @apply="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'
import { mapActions, mapState } from 'vuex'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

@Component({
  components: {
    GenericActionForm,
    ActionButtonTray
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed:mapState('devices',['deviceGenericAction','deviceAttachments']),
  methods:mapActions('devices',['loadDeviceGenericAction','loadAllDeviceActions','loadDeviceAttachments','updateDeviceGenericAction'])
})
export default class GenericDeviceActionEditPage extends Vue {
  private action: GenericAction = new GenericAction()

  async created(){
    try {
      await this.loadDeviceGenericAction(this.actionId)
      this.action = GenericAction.createFromObject(this.deviceGenericAction)
    }catch (e){
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    }

    try {
      await this.loadDeviceAttachments(this.deviceId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  async save (): void {
    if (!(this.$refs.genericDeviceActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    try {
      await this.updateDeviceGenericAction({
        deviceId: this.deviceId,
        genericDeviceAction: this.action
      })
      this.loadAllDeviceActions(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }
  }
}
</script>
