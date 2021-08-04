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
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn && isActionsPage"
        color="primary"
        small
        :to="'/platforms/' + platformId + '/actions/new'"
      >
        Add Action
      </v-btn>
    </v-card-actions>

    <template v-if="isAddActionPage">
      <NuxtChild
        @input="$fetch"
        @showsave="showsave"
      />
    </template>

    <template v-else-if="isEditActionPage">
      <NuxtChild
        @input="$fetch"
        @showload="showload"
        @showsave="showsave"
      />
    </template>

    <template v-else>
      <div v-if="actions.length === 0">
        <v-card flat>
          <v-card-text>
            <p class="text-center">
              There are no actions for this platform.
            </p>
          </v-card-text>
        </v-card>
      </div>
      <PlatformActionTimeline
        v-else
        :value="actions"
        :platform-id="platformId"
        :action-api-dispatcher="apiDispatcher"
        @input="$fetch"
        @showdelete="showsave"
      />
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import PlatformActionTimeline from '@/components/actions/PlatformActionTimeline.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { IActionCommonDetails } from '@/models/ActionCommonDetails'
import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { PlatformMountAction } from '@/models/views/platforms/actions/PlatformMountAction'
import { PlatformUnmountAction } from '@/models/views/platforms/actions/PlatformUnmountAction'
import { PlatformMountActionWrapper } from '@/viewmodels/PlatformMountActionWrapper'
import { PlatformUnmountActionWrapper } from '@/viewmodels/PlatformUnmountActionWrapper'

import { DateComparator, isDateCompareable } from '@/modelUtils/Compareables'
import { PlatformActionApiDispatcher } from '@/modelUtils/actionHelpers'

@Component({
  components: {
    ProgressIndicator,
    PlatformActionTimeline
  }
})
export default class PlatformActionsPage extends Vue {
  private isSaving: boolean = false
  private isLoading: boolean = false
  private actions: IActionCommonDetails[] = []

  async fetch () {
    this.showload(true)
    await this.fetchActions()
    this.showload(false)
  }

  async fetchActions (): Promise<void> {
    this.actions = []
    await Promise.all([
      this.fetchGenericActions(),
      this.fetchSoftwareUpdateActions(),
      this.fetchMountActions(),
      this.fetchUnmountActions()
    ])
    // sort the actions
    const comparator = new DateComparator()
    this.actions.sort((i: IActionCommonDetails, j: IActionCommonDetails): number => {
      if (isDateCompareable(i) && isDateCompareable(j)) {
        // multiply result with -1 to get descending order
        return comparator.compare(i, j) * -1
      }
      if (isDateCompareable(i)) {
        return -1
      }
      if (isDateCompareable(j)) {
        return 1
      }
      return 0
    })
  }

  async fetchGenericActions (): Promise<void> {
    const actions: GenericAction[] = await this.$api.platforms.findRelatedGenericActions(this.platformId)
    actions.forEach((action: GenericAction) => this.actions.push(action))
  }

  async fetchSoftwareUpdateActions (): Promise<void> {
    const actions: SoftwareUpdateAction[] = await this.$api.platforms.findRelatedSoftwareUpdateActions(this.platformId)
    actions.forEach((action: SoftwareUpdateAction) => this.actions.push(action))
  }

  async fetchMountActions (): Promise<void> {
    const actions: PlatformMountAction[] = await this.$api.platforms.findRelatedMountActions(this.platformId)
    actions.forEach((action: PlatformMountAction) => this.actions.push(new PlatformMountActionWrapper(action)))
  }

  async fetchUnmountActions (): Promise<void> {
    const actions: PlatformUnmountAction[] = await this.$api.platforms.findRelatedUnmountActions(this.platformId)
    actions.forEach((action: PlatformUnmountAction) => this.actions.push(new PlatformUnmountActionWrapper(action)))
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get isActionsPage (): boolean {
    return !this.isEditActionPage && !this.isAddActionPage
  }

  get isAddActionPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const addUrl = '^\/platforms\/' + this.platformId + '\/actions\/new$'
    return !!this.$route.path.match(addUrl)
  }

  get isEditActionPage (): boolean {
    // eslint-disable-next-line no-useless-escape
    const editUrl = '^\/platforms\/' + this.platformId + '\/actions\/[a-zA-Z-]+\/[0-9]+\/edit$'
    return !!this.$route.path.match(editUrl)
  }

  showsave (isSaving: boolean) {
    this.isSaving = isSaving
  }

  showload (isLoading: boolean) {
    this.isLoading = isLoading
  }

  get apiDispatcher () {
    return new PlatformActionApiDispatcher(this.$api)
  }
}
</script>
