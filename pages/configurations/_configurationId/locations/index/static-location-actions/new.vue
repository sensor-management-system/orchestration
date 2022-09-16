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
      v-model="isSaving"
      dark
    />
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
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'
import { mapActions, mapState } from 'vuex'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { VocabularyState } from '@/store/vocabulary'
import {
  AddStaticLocationBeginActionAction,
  ConfigurationsState,
  LoadLocationActionTimepointsAction
} from '@/store/configurations'
import { currentAsUtcDateSecondsAsZeros } from '@/utils/dateHelper'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import StaticLocationActionDataForm from '@/components/configurations/StaticLocationActionDataForm.vue'
@Component({
  components: { StaticLocationActionDataForm, ProgressIndicator },
  middleware: ['auth'],
  methods: mapActions('configurations', ['addStaticLocationBeginAction', 'loadLocationActionTimepoints']),
  computed: {
    ...mapState('configurations', ['selectedLocationDate'])
  }
})
export default class StaticLocationActionNew extends Vue {
  @InjectReactive()
    editable!: boolean

  private newAction: StaticLocationAction = new StaticLocationAction()
  private isSaving: boolean = false

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']
  configurationLocationActionTimepoints!: ConfigurationsState['configurationLocationActionTimepoints']
  selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  addStaticLocationBeginAction!: AddStaticLocationBeginActionAction

  created () {
    if (!this.editable) {
      this.$router.replace('/configurations/' + this.configurationId + '/locations', () => {
        this.$store.commit('snackbar/setError', 'You\'re not allowed to edit this configuration.')
      })
      return
    }
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
      this.isSaving = true
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
      this.isSaving = false
    }
  }
}
</script>

<style scoped>

</style>
