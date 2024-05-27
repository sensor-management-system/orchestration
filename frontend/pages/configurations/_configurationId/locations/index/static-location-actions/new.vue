<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <StaticLocationActionDataForm
      ref="newStaticLocationForm"
      v-model="newAction"
    >
      <template #actions>
        <v-card-actions v-if="$auth.loggedIn">
          <v-spacer />
          <v-btn small @click="closeNewStaticLocationForm">
            Cancel
          </v-btn>
          <v-btn color="accent" small @click="saveNewStaticLocation">
            Save
          </v-btn>
        </v-card-actions>
      </template>
    </StaticLocationActionDataForm>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'
import { mapActions, mapState } from 'vuex'
import CheckEditAccess from '@/mixins/CheckEditAccess'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { VocabularyState } from '@/store/vocabulary'
import {
  AddStaticLocationBeginActionAction,
  ConfigurationsState,
  LoadLocationActionTimepointsAction
} from '@/store/configurations'
import { currentAsUtcDateSecondsAsZeros } from '@/utils/dateHelper'
import { SetLoadingAction } from '@/store/progressindicator'
import StaticLocationActionDataForm from '@/components/configurations/StaticLocationActionDataForm.vue'
@Component({
  components: { StaticLocationActionDataForm },
  middleware: ['auth'],
  methods: {
    ...mapActions('configurations', ['addStaticLocationBeginAction', 'loadLocationActionTimepoints']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  computed: {
    ...mapState('configurations', ['selectedLocationDate'])
  }
})
export default class StaticLocationActionNew extends mixins(CheckEditAccess) {
  private newAction: StaticLocationAction = new StaticLocationAction()

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']
  configurationLocationActionTimepoints!: ConfigurationsState['configurationLocationActionTimepoints']
  selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  addStaticLocationBeginAction!: AddStaticLocationBeginActionAction
  setLoading!: SetLoadingAction

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/configurations/' + this.configurationId + '/locations'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this configuration.'
  }

  created () {
    this.newAction.beginDate = this.selectedDate
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get selectedDate (): DateTime {
    return this.selectedLocationDate ?? currentAsUtcDateSecondsAsZeros()
  }

  closeNewStaticLocationForm (): void {
    this.$router.push('/configurations/' + this.configurationId + '/locations')
  }

  async saveNewStaticLocation () {
    if (!(this.$refs.newStaticLocationForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    try {
      this.setLoading(true)
      const newId = await this.addStaticLocationBeginAction({
        configurationId: this.configurationId,
        staticLocationAction: this.newAction
      })
      this.loadLocationActionTimepoints(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.$router.push('/configurations/' + this.configurationId + '/locations/static-location-actions/' + newId)
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
