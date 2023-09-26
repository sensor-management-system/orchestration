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
    <v-card-actions>
      <v-card-title class="pl-0">
        Edit TSM-Linking
      </v-card-title>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="$auth.loggedIn"
        save-btn-text="Apply"
        :to="redirectRoute"
        :disabled="isLoading"
        @save="save"
      />
    </v-card-actions>

    <v-card>
      <v-container>
        <v-row>
          <v-col>
            <TsmLinkingFormItemHeader
              :selected-device-action="linking.deviceMountAction"
              :selected-measured-quantity="linking.deviceProperty"
            />
          </v-col>
        </v-row>
      </v-container>
      <TsmLinkingForm
        ref="tsmLinkingForm"
        v-model="editLinking"
        :selected-device-action-property-combination="selectedDeviceActionMeasuredQuantities"
      />
    </v-card>

    <v-card-actions>
      <v-spacer />
      <SaveAndCancelButtons
        v-if="$auth.loggedIn"
        save-btn-text="Apply"
        :to="redirectRoute"
        :disabled="isLoading"
        @save="save"
      />
    </v-card-actions>
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

import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import TsmLinkingForm from '@/components/configurations/tsmLinking/TsmLinkingForm.vue'
import { TsmDeviceMountPropertyCombination } from '@/utils/configurationInterfaces'
import { TsmLinking } from '@/models/TsmLinking'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import {
  ITsmLinkingState,
  LoadConfigurationTsmLinkingsAction,
  LoadDatasourcesAction,
  LoadDatastreamsForDatasourceAndThingAction,
  LoadThingsForDatasourceAction,
  LoadTsmEndpointsAction,
  UpdateConfigurationTsmLinkingAction
} from '@/store/tsmLinking'
import TsmLinkingFormItemHeader from '@/components/configurations/tsmLinking/TsmLinkingFormItemHeader.vue'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'
import { LoadLicensesAction } from '@/store/vocabulary'

@Component({
  components: {
    NavigationGuardDialog,
    TsmLinkingFormItemHeader,
    SaveAndCancelButtons,
    TsmLinkingForm
  },
  middleware: ['auth'],
  computed: {
    ...mapState('tsmLinking', ['linking']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('tsmLinking', [
      'loadConfigurationTsmLinkings', 'updateConfigurationTsmLinking', 'loadThingsForDatasource', 'loadDatastreamsForDatasourceAndThing', 'loadDatasources'
    ]),
    ...mapActions('vocabulary', ['loadLicenses']),
    ...mapActions('progressindicator', ['setLoading'])
  }

})
export default class TsmLinkingEditPage extends Vue {
  private editLinking: TsmLinking | null = null
  private hasSaved = false
  private to: RawLocation | null = null
  private showNavigationWarning = false

  // vuex definition for typescript check
  linking!: ITsmLinkingState['linking']
  loadDatasources !: LoadDatasourcesAction
  loadConfigurationTsmLinkings!: LoadConfigurationTsmLinkingsAction
  updateConfigurationTsmLinking!: UpdateConfigurationTsmLinkingAction
  loadTsmEndpoints!: LoadTsmEndpointsAction
  loadThingsForDatasource!: LoadThingsForDatasourceAction
  loadDatastreamsForDatasourceAndThing!: LoadDatastreamsForDatasourceAndThingAction
  loadLicenses!: LoadLicensesAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  async created () {
    this.editLinking = TsmLinking.createFromObject(this.linking!)
    await Promise.all([
      this.loadDatasources({ endpoint: this.editLinking.tsmEndpoint! }),
      this.loadThingsForDatasource({ endpoint: this.editLinking.tsmEndpoint!, datasource: this.editLinking.datasource! }),
      this.loadDatastreamsForDatasourceAndThing({
        endpoint: this.editLinking.tsmEndpoint!,
        datasource: this.editLinking.datasource!,
        thing: this.editLinking.thing!
      }),
      this.loadLicenses()
    ])
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get selectedDeviceActionMeasuredQuantities (): TsmDeviceMountPropertyCombination {
    return {
      action: this.linking!.deviceMountAction!,
      measuredQuantities: [this.linking!.deviceProperty!]
    }
  }

  get redirectRoute () {
    return '/configurations/' + this.configurationId + '/tsm-linking'
  }

  async save () {
    if (!this.editLinking) {
      return
    }

    if (!(this.$refs.tsmLinkingForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.setLoading(true)
      await this.updateConfigurationTsmLinking(this.editLinking)
      await this.loadConfigurationTsmLinkings(this.configurationId)
      this.$store.commit('tsmLinking/setLinking', null)
      this.$store.commit('snackbar/setSuccess', 'Linking updated')
      this.hasSaved = true
      this.$router.push(this.redirectRoute)
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
      this.hasSaved = true
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
