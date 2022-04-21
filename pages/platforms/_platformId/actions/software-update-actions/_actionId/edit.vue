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
        v-if="$auth.loggedIn"
        :cancel-url="'/platforms/' + platformId + '/actions'"
        :is-saving="isSaving"
        @apply="save"
      />
    </v-card-actions>

    <SoftwareUpdateActionForm
      ref="softwareUpdateActionForm"
      v-model="action"
      :attachments="platformAttachments"
      :current-user-mail="$auth.user.email"
    />

    <v-card-actions>
      <v-spacer />
      <ActionButtonTray
        v-if="$auth.loggedIn"
        :cancel-url="'/platforms/' + platformId + '/actions'"
        :is-saving="isSaving"
        @apply="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'
import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import { mapActions, mapState } from 'vuex'
import { GenericAction } from '@/models/GenericAction'

@Component({
  components: {
    SoftwareUpdateActionForm,
    ActionButtonTray
  },
  scrollToTop: true,
  middleware: ['auth'],
  computed:mapState('platforms',['platformSoftwareUpdateAction','platformAttachments']),
  methods:mapActions('platforms',['loadPlatformSoftwareUpdateAction','loadAllPlatformActions','loadPlatformAttachments','updatePlatformSoftwareUpdateAction'])
})
export default class PlatformSoftwareUpdateActionEditPage extends Vue {
  private action: SoftwareUpdateAction = new SoftwareUpdateAction()
  private isSaving: boolean = false

  async created(){
    try {
      await this.loadPlatformSoftwareUpdateAction(this.actionId)
      this.action = SoftwareUpdateAction.createFromObject(this.platformSoftwareUpdateAction)
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action')
    }
    try {
      await this.loadPlatformAttachments(this.platformId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  async save (): void {
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    try {
      this.isSaving = true
      await this.updatePlatformSoftwareUpdateAction({
        platformId: this.platformId,
        softwareUpdateAction: this.action
      });
      this.loadAllPlatformActions(this.platformId);
      this.$router.push('/platforms/' + this.platformId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.isSaving = false
    }
  }
}
</script>
