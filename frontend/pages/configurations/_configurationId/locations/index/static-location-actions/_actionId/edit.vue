<!--
SPDX-FileCopyrightText: 2020 - 2023
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
      ref="editStaticLocationForm"
      v-model="valueCopy"
    >
      <template #actions>
        <v-card-actions v-if="$auth.loggedIn">
          <v-spacer />
          <v-btn small @click="closeEditStaticLocationForm">
            Cancel
          </v-btn>
          <v-btn color="accent" small @click="saveEditedStaticLocation">
            Apply
          </v-btn>
        </v-card-actions>
      </template>
    </StaticLocationActionDataForm>
  </div>
</template>

<script lang="ts">
import { Component, Vue, mixins } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import CheckEditAccess from '@/mixins/CheckEditAccess'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import {
  ConfigurationsState, LoadLocationActionTimepointsAction,
  LoadStaticLocationActionAction,
  UpdateStaticLocationActionAction
} from '@/store/configurations'
import StaticLocationActionDataForm from '@/components/configurations/StaticLocationActionDataForm.vue'
@Component({
  components: { StaticLocationActionDataForm },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['staticLocationAction']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('configurations', ['loadStaticLocationAction', 'updateStaticLocationAction', 'loadLocationActionTimepoints']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class StaticLocationActionEdit extends mixins(CheckEditAccess) {
  private valueCopy: StaticLocationAction = new StaticLocationAction()

  // vuex definition for typescript check
  staticLocationAction!: ConfigurationsState['staticLocationAction']
  loadStaticLocationAction!: LoadStaticLocationActionAction
  updateStaticLocationAction!: UpdateStaticLocationActionAction
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  isLoading!: LoadingSpinnerState['isLoading']
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

  async created () {
    try {
      this.setLoading(true)
      await this.loadStaticLocationAction(this.actionId)
      if (this.staticLocationAction) {
        this.valueCopy = StaticLocationAction.createFromObject(this.staticLocationAction)
      }
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Failed to load action')
    } finally {
      this.setLoading(false)
    }
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  closeEditStaticLocationForm (): void {
    this.$router.push('/configurations/' + this.configurationId + '/locations/static-location-actions/' + this.actionId)
  }

  async saveEditedStaticLocation () {
    if (!this.$auth.loggedIn) {
      return
    }
    if (!(this.$refs.editStaticLocationForm as Vue & { isValid: () => boolean }).isValid()) {
      this.$store.commit('snackbar/setError', 'Please correct the errors')
      return
    }
    this.setLoading(true)
    try {
      await this.updateStaticLocationAction({
        configurationId: this.configurationId,
        staticLocationAction: this.valueCopy
      })
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      await this.loadStaticLocationAction(this.actionId)
      this.loadLocationActionTimepoints(this.configurationId)
      this.closeEditStaticLocationForm()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
