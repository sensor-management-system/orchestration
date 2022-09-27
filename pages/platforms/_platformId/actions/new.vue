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
    <ProgressIndicator
      v-model="isLoading"
    />
    <v-card
      flat
    >
      <v-card-text>
        <v-select
          v-model="chosenKindOfAction"
          :items="platformActionTypeItems"
          :item-text="(x) => x.name"
          clearable
          label="Action Type"
          :hint="!chosenKindOfAction ? 'Please select an action type' : ''"
          persistent-hint
          return-object
          @change="updateRoute"
        />
      </v-card-text>
    </v-card>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { PlatformActionTypeItemsGetter, LoadPlatformGenericActionTypesAction } from '@/store/vocabulary'
import {
  PlatformsState,
  LoadPlatformAttachmentsAction,
  SetChosenKindOfPlatformActionAction
} from '@/store/platforms'

import ProgressIndicator from '@/components/ProgressIndicator.vue'

const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
const KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION = 'generic_platform_action'

@Component({
  components: { ProgressIndicator },
  middleware: ['auth'],
  computed: {
    ...mapGetters('vocabulary', ['platformActionTypeItems']),
    ...mapState('platforms', ['chosenKindOfPlatformAction'])
  },
  methods: {
    ...mapActions('vocabulary', ['loadPlatformGenericActionTypes']),
    ...mapActions('platforms', ['loadPlatformAttachments', 'setChosenKindOfPlatformAction'])
  }
})
export default class NewPlatformAction extends mixins(CheckEditAccess) {
  private isLoading: boolean = false

  // vuex definition for typescript check
  platformActionTypeItems!: PlatformActionTypeItemsGetter
  loadPlatformGenericActionTypes!: LoadPlatformGenericActionTypesAction
  loadPlatformAttachments!: LoadPlatformAttachmentsAction
  chosenKindOfPlatformAction!: PlatformsState['chosenKindOfPlatformAction']
  setChosenKindOfPlatformAction!: SetChosenKindOfPlatformActionAction

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

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
      this.chosenKindOfAction = null
      await Promise.all([
        this.loadPlatformGenericActionTypes(),
        this.loadPlatformAttachments(this.platformId)
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch action types')
    } finally {
      this.isLoading = false
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

  get genericActionChosen (): boolean {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_GENERIC_PLATFORM_ACTION
  }

  get softwareUpdateChosen () {
    return this.chosenKindOfAction?.kind === KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  }

  updateRoute () {
    if (this.genericActionChosen) {
      this.$router.push(`/platforms/${this.platformId}/actions/new/generic-platform-actions`)
    }
    if (this.softwareUpdateChosen) {
      this.$router.push(`/platforms/${this.platformId}/actions/new/software-update-actions`)
    }

    if (!this.chosenKindOfAction) {
      this.$router.push(`/platforms/${this.platformId}/actions/new`)
    }
  }
}
</script>
