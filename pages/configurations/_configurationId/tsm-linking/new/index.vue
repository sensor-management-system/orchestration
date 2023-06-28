<!--
 Web client of the Sensor Management System software developed within the
 Helmholtz DataHub Initiative by GFZ and UFZ.

 Copyright (C) 2020 - 2023
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
    />
    <v-card-actions>
      <v-card-title class="pl-0">
        New TSM-Linking
      </v-card-title>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        :disabled="isSaving"
        small
        text
        nuxt
        :to="'/configurations/' + configurationId + '/tsm-linking'"
      >
        cancel
      </v-btn>
    </v-card-actions>

    <tsm-linking-wizard
      ref="tsmWizard"
    >
      <template #save>
        <v-btn
          block
          color="primary"
          :disabled="isSaving"
          @click="save()"
        >
          Submit
        </v-btn>
      </template>
    </tsm-linking-wizard>
    <NavigationGuardDialog
      v-model="showNavigationWarning"
      :has-entity-changed="true"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import { RawLocation } from 'vue-router'

import TsmLinkingWizard from '@/components/configurations/tsmLinking/TsmLinkingWizard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { TsmLinking } from '@/models/TsmLinking'
import {
  AddConfigurationTsmLinkingAction,
  ITsmLinkingState,
  LoadConfigurationTsmLinkingsAction
} from '@/store/tsmLinking'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'

@Component({
  components: {
    NavigationGuardDialog,
    ProgressIndicator,
    TsmLinkingWizard
  },
  middleware: ['auth'],
  computed: {
    ...mapState('tsmLinking', ['newLinkings'])
  },
  methods: {
    ...mapActions('tsmLinking', ['addConfigurationTsmLinking', 'loadConfigurationTsmLinkings'])
  }
})
export default class ConfigurationNewTsmLinkingPageChild extends Vue {
  private isSaving = false
  private hasSaved = false
  private errorLinkings: TsmLinking[] = []
  private to: RawLocation | null = null
  private showNavigationWarning = false

  // vuex definition for typescript check
  newLinkings!: ITsmLinkingState['newLinkings']
  addConfigurationTsmLinking!: AddConfigurationTsmLinkingAction
  loadConfigurationTsmLinkings!: LoadConfigurationTsmLinkingsAction

  get configurationId () {
    return this.$route.params.configurationId
  }

  get redirectRoute () {
    return '/configurations/' + this.configurationId + '/tsm-linking'
  }

  async save () {
    if (this.newLinkings.length === 0) {
      return
    }

    if (!(this.$refs.tsmWizard as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your inputs in step 3 "Add linking information"')
      return
    }

    this.isSaving = true

    for (const newLinking of this.newLinkings) {
      try {
        await this.addConfigurationTsmLinking(newLinking)
      } catch (_e) {
        this.errorLinkings.push(newLinking)
      }
    }

    this.isSaving = false
    this.hasSaved = true

    if (this.errorLinkings.length > 0) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } else {
      await this.loadConfigurationTsmLinkings(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Linkings saved')
      this.$router.push(this.redirectRoute)
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (!this.hasSaved) {
      if (this.to) {
        next()
      } else {
        this.to = to
        this.showNavigationWarning = true
      }
    } else {
      return next()
    }
  }
}
</script>

<style scoped>

</style>
