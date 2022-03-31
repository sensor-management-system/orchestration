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
  <div
    v-if="$auth.loggedIn"
  >
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <ActionButtonTray
          :cancel-url="'/platforms/' + platformId + '/actions'"
          :is-saving="isSaving"
          :show-apply="showApplyButton"
          @apply="onApplyButtonClick"
        />
      </v-card-actions>
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
        />
      </v-card-text>

      <!-- softwareUpdate -->
      <v-card-text
        v-if="softwareUpdateChosen"
      >
        <SoftwareUpdateActionForm
          ref="softwareUpdateActionForm"
          v-model="softwareUpdateAction"
          :attachments="attachments"
          :current-user-mail="$auth.user.email"
        />
      </v-card-text>

      <!-- genericAction -->
      <v-card-text
        v-if="genericActionChosen"
      >
        <GenericActionForm
          ref="genericPlatformActionForm"
          v-model="genericPlatformAction"
          :attachments="attachments"
          :current-user-mail="$auth.user.email"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <ActionButtonTray
          :cancel-url="'/platforms/' + platformId + '/actions'"
          :is-saving="isSaving"
          :show-apply="showApplyButton"
          @apply="onApplyButtonClick"
        />
      </v-card-actions>
    </v-card>
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
  middleware: ['auth']
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

  private genericActionTypes: ActionType[] = []
  private attachments: Attachment[] = []

  private _chosenKindOfAction: IOptionsForActionType | null = null

  private genericPlatformAction: GenericAction = new GenericAction()
  private softwareUpdateAction: SoftwareUpdateAction = new SoftwareUpdateAction()

  private _isSaving: boolean = false

  async fetch () {
    await Promise.all([
      this.fetchGenericActionTypes()
    ])
  }

  async fetchGenericActionTypes (): Promise<any> {
    this.genericActionTypes = await this.$api.actionTypes.newSearchBuilder().onlyType(ACTION_TYPE_API_FILTER_PLATFORM).build().findMatchingAsList()
  }

  mounted () {
    this.$api.platforms.findRelatedPlatformAttachments(this.platformId).then((foundAttachments) => {
      this.attachments = foundAttachments
    }).catch((_error) => {
      this.$store.commit('snackbar/setError', 'Failed to fetch attachments')
    })
  }

  get chosenKindOfAction () {
    return this.$data._chosenKindOfAction
  }

  set chosenKindOfAction (newValue: IOptionsForActionType | null) {
    if (this.$data._chosenKindOfAction !== newValue) {
      this.$data._chosenKindOfAction = newValue

      if (this.genericActionChosen) {
        this.genericPlatformAction = new GenericAction()
        this.genericPlatformAction.actionTypeName = newValue?.name || ''
        this.genericPlatformAction.actionTypeUrl = newValue?.uri || ''
      }
      if (this.softwareUpdateChosen) {
        this.softwareUpdateAction = new SoftwareUpdateAction()
      }
    }
  }

  get genericActionChosen (): boolean {
    return this.$data._chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION
  }

  get softwareUpdateChosen () {
    return this.$data._chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isSaving (): boolean {
    return this.$data._isSaving
  }

  set isSaving (value: boolean) {
    this.$data._isSaving = value
    this.$emit('showsave', value)
  }

  onApplyButtonClick () {
    switch (true) {
      case this.genericActionChosen:
        this.addGenericAction()
        return
      case this.softwareUpdateChosen:
        this.addSoftwareUpdateAction()
    }
  }

  addSoftwareUpdateAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!this.softwareUpdateChosen) {
      return
    }
    if (!this.softwareUpdateAction) {
      return
    }
    if (!(this.$refs.softwareUpdateActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.isSaving = true
    this.$api.platformSoftwareUpdateActions.add(this.platformId, this.softwareUpdateAction).then((action: SoftwareUpdateAction) => {
      this.$router.push('/platforms/' + this.platformId + '/actions', () => this.$emit('input', action))
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }).finally(() => {
      this.isSaving = false
    })
  }

  addGenericAction () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!this.genericActionChosen) {
      return
    }
    if (!(this.$refs.genericPlatformActionForm as Vue & { isValid: () => boolean }).isValid()) {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }

    this.genericPlatformAction.actionTypeName = this.chosenKindOfAction?.name || ''
    this.genericPlatformAction.actionTypeUrl = this.chosenKindOfAction?.uri || ''

    this.isSaving = true
    this.$api.genericPlatformActions.add(this.platformId, this.genericPlatformAction).then((action: GenericAction) => {
      this.$router.push('/platforms/' + this.platformId + '/actions', () => this.$emit('input', action))
    }).catch(() => {
      this.$store.commit('snackbar/setError', 'Failed to save the action')
    }).finally(() => {
      this.isSaving = false
    })
  }

  get showApplyButton (): boolean {
    return this.chosenKindOfAction !== null
  }

  get actionTypeItems (): IOptionsForActionType[] {
    return [
      ...this.specialActionTypes,
      ...this.genericActionTypes.map((i) => {
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
