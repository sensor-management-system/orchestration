<!--
 SPDX-FileCopyrightText: 2020 - 2024

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <v-card-actions>
      <v-card-title class="pl-0">
        Edit Data Linking
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
