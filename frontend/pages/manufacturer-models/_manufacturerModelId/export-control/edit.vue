<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2024
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
      <v-spacer />
      <save-and-cancel-buttons
        v-if="canHandleExportControl"
        save-btn-text="Apply"
        :to="'/manufacturer-models/' + manufacturerModelId + '/export-control'"
        @save="save"
      />
    </v-card-actions>
    <export-control-basic-data-form
      v-if="exportControlCopy"
      v-model="exportControlCopy"
    />
    <v-card-actions>
      <v-spacer />
      <save-and-cancel-buttons
        v-if="canHandleExportControl"
        save-btn-text="Apply"
        :to="'/manufacturer-models/' + manufacturerModelId + '/export-control'"
        @save="save"
      />
    </v-card-actions>

    <navigation-guard-dialog
      v-model="showNavigationWarning"
      :has-entity-changed="exportControlHasBeenEdited"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'
import { mapActions, mapGetters, mapState } from 'vuex'

import { ManufacturermodelsState, LoadExportControlAction, SaveExportControlAction } from '@/store/manufacturermodels'
import { CanHandleExportControlGetter } from '@/store/permissions'
import { SetLoadingAction } from '@/store/progressindicator'

import ExportControlBasicDataForm from '@/components/manufacturerModels/ExportControlBasicDataForm.vue'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'
import { ExportControl } from '@/models/ExportControl'

@Component({
  computed: {
    ...mapState('manufacturermodels', ['exportControl']),
    ...mapGetters('permissions', ['canHandleExportControl'])
  },
  methods: {
    ...mapActions('manufacturermodels', ['loadExportControl', 'saveExportControl']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  components: {
    ExportControlBasicDataForm,
    SaveAndCancelButtons,
    NavigationGuardDialog
  }
})
export default class ManufacturerModelEditExportControlPage extends Vue {
  private exportControlCopy: ExportControl | null = null
  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null
  private hasSaved: boolean = false

  // vuex definition for typescript check
  exportControl!: ManufacturermodelsState['exportControl']
  loadExportControl!: LoadExportControlAction
  canHandleExportControl!: CanHandleExportControlGetter
  setLoading!: SetLoadingAction
  saveExportControl!: SaveExportControlAction

  async created () {
    if (!this.canHandleExportControl) {
      this.$router.replace(this.getRedirectUrl(), () => {
        this.$store.commit('snackbar/setError', this.getRedirectMessage())
      })
    }
    try {
      this.setLoading(true)
      await this.loadExportControl({ manufacturerModelId: this.manufacturerModelId })
      this.exportControlCopy = ExportControl.createFromObject(this.exportControl!)
    } catch (e) {
      this.$store.commit('snachbar/setError', 'failed to fetch export control')
    } finally {
      this.setLoading(false)
    }
  }

  getRedirectUrl (): string {
    return '/manufacturer-models/' + this.manufacturerModelId + '/export-control'
  }

  getRedirectMessage (): string {
    return 'You\'re not allowed to edit the export control information.'
  }

  get manufacturerModelId () {
    return this.$route.params.manufacturerModelId
  }

  get exportControlHasBeenEdited () {
    if (!this.exportControlCopy) {
      return false
    }
    return (JSON.stringify(this.exportControl) !== JSON.stringify(this.exportControlCopy))
  }

  save () {
    if (!this.exportControlCopy) {
      return
    }
    try {
      this.setLoading(true)
      this.saveExportControl(this.exportControlCopy)
      this.hasSaved = true
      this.loadExportControl({ manufacturerModelId: this.manufacturerModelId })
      this.$store.commit('snackbar/setSuccess', 'Export control updated')
      this.$router.push('/manufacturer-models/' + this.manufacturerModelId + '/export-control')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } finally {
      this.setLoading(false)
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (this.exportControlHasBeenEdited && !this.hasSaved) {
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
