<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
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
    <v-card
      flat
    >
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="actionTypeItems"
          :item-text="(x) => x.name"
          :item-value="(x) => x"
          clearable
          label="Action Type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
          return-object
          @change="updateRoute"
        />
      </v-card-text>
    </v-card>
    <NuxtChild/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { IActionType, ActionType } from '@/models/ActionType'

import { ACTION_TYPE_API_FILTER_PLATFORM } from '@/services/cv/ActionTypeApi'

import GenericActionForm from '@/components/actions/GenericActionForm.vue'
import SoftwareUpdateActionForm from '@/components/actions/SoftwareUpdateActionForm.vue'
import ActionButtonTray from '@/components/actions/ActionButtonTray.vue'
import { mapActions, mapState } from 'vuex'

const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION = 'generic_platform_action'
const KIND_OF_ACTION_TYPE_UNKNOWN = 'unknown'
type KindOfActionType = typeof KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE | typeof KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION | typeof KIND_OF_ACTION_TYPE_UNKNOWN

type IOptionsForActionType = Pick<IActionType, 'id' | 'name' | 'uri'> & {
  kind: KindOfActionType
}

@Component({
  components: {
    ActionButtonTray,
    GenericActionForm,
    SoftwareUpdateActionForm
  },
  middleware: ['auth'],
  computed:{
    ...mapState('vocabulary',['platformGenericActionTypes']),
    ...mapState('platforms',['chosenKindOfPlatformAction'])
  },
  methods:{
    ...mapActions('vocabulary',['loadPlatformGenericActionTypes']),
    ...mapActions('platforms',['loadPlatformAttachments','setChosenKindOfPlatformAction'])
  }
})
export default class NewPlatformAction extends Vue {
  private specialActionTypes: IOptionsForActionType[] = [
    {
      id: 'software_update',
      name: 'Software Update',
      uri: '',
      kind: KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
    }
  ]

  async created(){
    try {
      await this.loadPlatformGenericActionTypes()
      await this.loadPlatformAttachments(this.platformId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action types')
    }
  }

  get chosenKindOfAction(){
    return this.chosenKindOfPlatformAction
  }

  set chosenKindOfAction(newVal){
    this.setChosenKindOfPlatformAction(newVal)
  }

  updateRoute(){
    if(this.genericActionChosen){
      this.$router.push(`/platforms/${this.platformId}/actions/new/generic-platform-actions`)
    }
    if(this.softwareUpdateChosen){
      this.$router.push(`/platforms/${this.platformId}/actions/new/software-update-actions`)
    }

    if(!this.chosenKindOfAction){
      this.$router.push(`/platforms/${this.platformId}/actions/new`)
    }

  }

  get genericActionChosen (): boolean {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION
  }

  get softwareUpdateChosen () {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  }

  get platformId (): string {
    return this.$route.params.platformId
  }
  get actionTypeItems (): IOptionsForActionType[] { // Todo in store auslagern
    return [
      ...this.specialActionTypes,
      ...this.platformGenericActionTypes.map((i) => {
        return {
          id: i.id,
          name: i.name,
          uri: i.uri,
          kind: KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION
        }
      })
    ].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase())) as IOptionsForActionType[]
  }
}
</script>
