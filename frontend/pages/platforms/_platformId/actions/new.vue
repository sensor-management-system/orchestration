<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      flat
    >
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="platformActionTypeItems"
          :item-text="(x) => x.name"
          clearable
          label="Action type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
          return-object
          @change="updateRoute"
        >
          <template #append-outer>
            <v-btn icon @click="showNewActionTypeDialog = true">
              <v-icon>
                mdi-tooltip-plus-outline
              </v-icon>
            </v-btn>
          </template>
        </v-select>
      </v-card-text>
    </v-card>
    <v-card-actions v-if="!chosenKindOfAction">
      <v-spacer />
      <v-btn
        small
        text
        nuxt
        :to="'/platforms/' + platformId + '/actions'"
      >
        cancel
      </v-btn>
    </v-card-actions>
    <NuxtChild />
    <action-type-dialog
      v-model="showNewActionTypeDialog"
      :initial-action-type-api-filter-type="selectedActionCategory"
      @aftersubmit="setChosenKindOfPlatformActionAndUpdateRoute"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import ActionTypeDialog from '@/components/shared/ActionTypeDialog.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import CheckEditAccess from '@/mixins/CheckEditAccess'
import { ActionType } from '@/models/ActionType'

import { ACTION_TYPE_API_FILTER_PLATFORM } from '@/services/cv/ActionTypeApi'

import { LoadPlatformGenericActionTypesAction, PlatformActionTypeItemsGetter } from '@/store/vocabulary'
import {
  LoadPlatformAttachmentsAction,
  LoadPlatformParametersAction,
  PlatformsState,
  SetChosenKindOfPlatformActionAction,
  SetPlatformPresetParameterAction
} from '@/store/platforms'
import {
  KIND_OF_ACTION_TYPE_GENERIC_ACTION,
  KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION,
  KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
} from '@/models/ActionKind'

@Component({
  components: { ActionTypeDialog },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['platformActionTypeItems']),
    ...mapState('platforms', ['chosenKindOfPlatformAction'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadPlatformGenericActionTypes']),
    ...mapActions('platforms', ['loadPlatformAttachments', 'setChosenKindOfPlatformAction', 'loadPlatformParameters', 'setPlatformPresetParameter']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class NewPlatformAction extends mixins(CheckEditAccess) {
  private showNewActionTypeDialog = false

  // vuex definition for typescript check
  platformActionTypeItems!: PlatformActionTypeItemsGetter
  loadPlatformGenericActionTypes!: LoadPlatformGenericActionTypesAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  chosenKindOfPlatformAction!: PlatformsState['chosenKindOfPlatformAction']
  loadPlatformParameters!: LoadPlatformParametersAction
  setChosenKindOfPlatformAction!: SetChosenKindOfPlatformActionAction
  setLoading!: SetLoadingAction
  setPlatformPresetParameter!: SetPlatformPresetParameterAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/platforms/' + this.platformId + '/actions'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this platform.'
  }

  get isBasePath (): boolean {
    return this.$route.path === '/platforms/' + this.platformId + '/actions/new'
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      if (this.isBasePath) {
        this.chosenKindOfAction = null
        this.setPlatformPresetParameter(null)
      }

      await Promise.all([
        this.loadPlatformGenericActionTypes(),
        this.loadPlatformAttachments(this.platformId),
        this.loadPlatformParameters(this.platformId)
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action types')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get chosenKindOfAction () {
    return this.chosenKindOfPlatformAction
  }

  set chosenKindOfAction (newVal) {
    this.setChosenKindOfPlatformAction(newVal)
  }

  setChosenKindOfPlatformActionAndUpdateRoute (newVal: ActionType) {
    this.setChosenKindOfPlatformAction({
      kind: KIND_OF_ACTION_TYPE_GENERIC_ACTION,
      id: newVal.id,
      name: newVal.name,
      uri: newVal.uri
    })
    this.updateRoute()
  }

  get selectedActionCategory (): string {
    return ACTION_TYPE_API_FILTER_PLATFORM
  }

  get genericActionChosen (): boolean {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_ACTION
  }

  get softwareUpdateChosen () {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  }

  get parameterChangeActionChosen () {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
  }

  updateRoute () {
    if (this.genericActionChosen) {
      this.$router.push(`/platforms/${this.platformId}/actions/new/generic-platform-actions`)
      return
    }
    if (this.softwareUpdateChosen) {
      this.$router.push(`/platforms/${this.platformId}/actions/new/software-update-actions`)
      return
    }
    if (this.parameterChangeActionChosen) {
      this.$router.push(`/platforms/${this.platformId}/actions/new/parameter-change-actions`)
      return
    }
    if (!this.chosenKindOfAction) {
      this.$router.push(`/platforms/${this.platformId}/actions/new`)
    }
  }
}
</script>
