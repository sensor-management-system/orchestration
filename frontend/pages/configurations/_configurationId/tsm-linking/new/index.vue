<!--
 SPDX-FileCopyrightText: 2020 - 2024

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <v-card-actions>
      <v-card-title class="pl-0">
        New Data Linking
      </v-card-title>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        :disabled="isLoading"
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
          :disabled="isLoading"
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
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
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
    TsmLinkingWizard
  },
  middleware: ['auth'],
  computed: {
    ...mapState('tsmLinking', ['newLinkings']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('tsmLinking', ['addConfigurationTsmLinking', 'loadConfigurationTsmLinkings']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationNewTsmLinkingPageChild extends Vue {
  private hasSaved = false
  private errorLinkings: TsmLinking[] = []
  private to: RawLocation | null = null
  private showNavigationWarning = false

  // vuex definition for typescript check
  newLinkings!: ITsmLinkingState['newLinkings']
  addConfigurationTsmLinking!: AddConfigurationTsmLinkingAction
  loadConfigurationTsmLinkings!: LoadConfigurationTsmLinkingsAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

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

    this.setLoading(true)

    for (const newLinking of this.newLinkings) {
      try {
        await this.addConfigurationTsmLinking(newLinking)
      } catch (_e) {
        this.errorLinkings.push(newLinking)
      }
    }

    this.setLoading(false)
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
