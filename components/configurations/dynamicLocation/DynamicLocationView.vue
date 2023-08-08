<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <dynamic-location-action-data
      v-if="action"
      :value="action"
      :devices="devicesForDynamicLocation"
    >
      <template
        v-if="editable"
        #dot-menu
      >
        <DotMenu>
          <template #actions>
            <DotMenuActionEdit
              @click="openEditDynamicLocationForm"
            />
            <DotMenuActionDelete
              @click="openDeleteDynamicLocationDialog"
            />
          </template>
        </DotMenu>
      </template>
    </dynamic-location-action-data>
    <DeleteDialog
      v-if="editable"
      v-model="showDeleteDialog"
      title="Delete Dynamic Location"
      :disabled="isLoading"
      @cancel="closeDeleteDialog"
      @delete="deleteAndCloseDialog"
    >
      <div>
        Do you really want to delete the dynamic location<em v-if="action.label"> {{ action.label }}</em>?
      </div>
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState, mapGetters } from 'vuex'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
import { IDynamicLocationAction } from '@/models/DynamicLocationAction'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionEdit from '@/components/DotMenuActionEdit.vue'
import {
  DeleteDynamicLocationActionAction,
  DevicesForDynamicLocationGetter, LoadDynamicLocationActionAction, LoadLocationActionTimepointsAction,
  UpdateDynamicLocationActionAction
} from '@/store/configurations'
import DynamicLocationActionData from '@/components/configurations/dynamicLocation/DynamicLocationActionData.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
@Component({
  components: { DeleteDialog, DynamicLocationActionData, DotMenuActionEdit, DotMenuActionDelete, DotMenu },
  computed: {
    ...mapState('progressindicator', ['isLoading']),
    ...mapGetters('configurations', ['devicesForDynamicLocation'])
  },
  methods: {
    ...mapActions('configurations', ['updateDynamicLocationAction', 'deleteDynamicLocationAction', 'loadDynamicLocationAction', 'loadLocationActionTimepoints']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class DynamicLocationView extends Vue {
  private showDeleteDialog = false

  // vuex definition for typescript check
  devicesForDynamicLocation!: DevicesForDynamicLocationGetter
  updateDynamicLocationAction!: UpdateDynamicLocationActionAction
  deleteDynamicLocationAction!: DeleteDynamicLocationActionAction
  loadDynamicLocationAction!: LoadDynamicLocationActionAction
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

  @Prop({
    type: String
  })
    configurationId!: string

  @Prop({
    type: Object
  })
    action!: IDynamicLocationAction

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private editable!: boolean

  openEditDynamicLocationForm () {
    this.$router.push('/configurations/' + this.configurationId + '/locations/dynamic-location-actions/' + this.action.id + '/edit')
  }

  openDeleteDynamicLocationDialog () {
    this.showDeleteDialog = true
  }

  closeDeleteDialog () {
    this.showDeleteDialog = false
  }

  async deleteAndCloseDialog () {
    try {
      this.setLoading(true)
      await this.deleteDynamicLocationAction(this.action.id)
      await this.loadLocationActionTimepoints(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Deletion successful')
      this.$router.push('/configurations/' + this.configurationId + '/locations')
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Deletion failed')
    } finally {
      this.setLoading(false)
      this.closeDeleteDialog()
    }
  }
}
</script>

<style scoped>

</style>
