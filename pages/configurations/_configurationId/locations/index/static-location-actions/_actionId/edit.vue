<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
      v-model="isInProgress"
      :dark="isSaving"
    />
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
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import {
  ConfigurationsState, LoadLocationActionTimepointsAction,
  LoadStaticLocationActionAction,
  UpdateStaticLocationActionAction
} from '@/store/configurations'
import StaticLocationActionDataForm from '@/components/configurations/StaticLocationActionDataForm.vue'
@Component({
  components: { StaticLocationActionDataForm, ProgressIndicator },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['staticLocationAction'])
  },
  methods: {
    ...mapActions('configurations', ['loadStaticLocationAction', 'updateStaticLocationAction', 'loadLocationActionTimepoints'])
  }
})
export default class StaticLocationActionEdit extends Vue {
  @InjectReactive()
    editable!: boolean

  private valueCopy: StaticLocationAction = new StaticLocationAction()
  private isSaving: boolean = false
  private isLoading: boolean = false

  // vuex definition for typescript check
  staticLocationAction!: ConfigurationsState['staticLocationAction']
  loadStaticLocationAction!: LoadStaticLocationActionAction
  updateStaticLocationAction!: UpdateStaticLocationActionAction
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction

  async created () {
    if (!this.editable) {
      this.$router.replace('/configurations/' + this.configurationId + '/locations', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this configuration.')
      })
      return
    }
    try {
      this.isLoading = true
      await this.loadStaticLocationAction(this.actionId)
      if (this.staticLocationAction) {
        this.valueCopy = StaticLocationAction.createFromObject(this.staticLocationAction)
      }
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Failed to load action')
    } finally {
      this.isLoading = false
    }
  }

  get actionId (): string {
    return this.$route.params.actionId
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
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
    this.isSaving = true
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
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
