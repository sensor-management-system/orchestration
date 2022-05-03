<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Create"
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>

    <GenericActionForm
      ref="genericPlatformActionForm"
      v-model="genericPlatformAction"
      :attachments="platformAttachments"
      :current-user-mail="$auth.user.email"
    />
    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        save-btn-text="Create"
        :to="'/platforms/' + platformId + '/actions'"
        @save="save"
      />
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapActions, mapState } from 'vuex'
import { GenericAction } from '@/models/GenericAction'
import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { IOptionsForActionType } from '@/store/platforms'

@Component({
  middleware: ['auth'],
  components: { ProgressIndicator, SaveAndCancelButtons, GenericActionForm },
  computed: mapState('platforms', ['platformAttachments', 'chosenKindOfPlatformAction']),
  methods: mapActions('platforms', ['addPlatformGenericAction', 'loadAllPlatformActions'])
})
export default class NewGenericPlatformAction extends Vue {
  private genericPlatformAction: GenericAction = new GenericAction()
  private isSaving: boolean = false

  // vuex definition for typescript check
  chosenKindOfPlatformAction!:IOptionsForActionType | null
  addPlatformGenericAction!:({ platformId, genericPlatformAction }: {platformId: string, genericPlatformAction: GenericAction})=> Promise<GenericAction>
  loadAllPlatformActions!:(id:string)=>void

  created () {
    if (this.chosenKindOfPlatformAction === null) {
      this.$router.push('/platforms/' + this.platformId + '/actions')
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  async save () {
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericPlatformAction.actionTypeName = this.chosenKindOfPlatformAction?.name || ''
    this.genericPlatformAction.actionTypeUrl = this.chosenKindOfPlatformAction?.uri || ''

    try {
      this.isSaving = true
      await this.addPlatformGenericAction({ platformId: this.platformId, genericPlatformAction: this.genericPlatformAction })
      this.loadAllPlatformActions(this.platformId)
      const successMessage = this.genericPlatformAction.actionTypeName ?? 'Action'
      this.$store.commit('snackbar/setSuccess', `${successMessage} created`)
      this.$router.push('/platforms/' + this.platformId + '/actions')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    } finally {
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
