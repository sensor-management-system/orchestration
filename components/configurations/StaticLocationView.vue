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
    <ProgressIndicator
      v-model="isLoading"
    />
    <StaticLocationActionData
      v-if="action"
      :value="action"
    >
      <template
        v-if="editable"
        #dot-menu
      >
        <DotMenu>
          <template #actions>
            <DotMenuActionEdit
              @click="openEditStaticLocationForm"
            />
            <DotMenuActionDelete
              @click="openDeleteStaticLocationDialog"
            />
          </template>
        </DotMenu>
      </template>
    </StaticLocationActionData>
    <DeleteDialog
      v-if="editable"
      v-model="showBeginDeleteDialog"
      title="Delete Static Location"
      @cancel="closeBeginDeleteDialog"
      @delete="deleteAndCloseBeginDeleteDialog"
    >
      <div>
        Do you really want to delete the static location<em v-if="action.label"> {{ action.label }}</em>?
      </div>
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'
import { IStaticLocationAction } from '@/models/StaticLocationAction'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import DotMenu from '@/components/DotMenu.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DotMenuActionEdit from '@/components/DotMenuActionEdit.vue'
import {
  DeleteStaticLocationActionAction,
  LoadLocationActionTimepointsAction,
  LoadStaticLocationActionAction
} from '@/store/configurations'
import StaticLocationActionData from '@/components/configurations/StaticLocationActionData.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
@Component({
  components: { DeleteDialog, StaticLocationActionData, DotMenuActionEdit, DotMenuActionDelete, DotMenu, ProgressIndicator },
  middleware: ['auth'],
  methods: {
    ...mapActions('configurations', ['loadStaticLocationAction', 'updateStaticLocationAction', 'deleteStaticLocationAction', 'loadLocationActionTimepoints'])
  }
})
export default class StaticLocationView extends Vue {
  @Prop({
    type: Object
  })
    action!: IStaticLocationAction

  @Prop({
    type: String
  })
    configurationId!: string

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private editable!: boolean

  private isLoading = false
  private showBeginDeleteDialog = false

  // vuex definition for typescript check
  loadStaticLocationAction!: LoadStaticLocationActionAction
  deleteStaticLocationAction!: DeleteStaticLocationActionAction
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction

  openEditStaticLocationForm () {
    this.$router.push('/configurations/' + this.configurationId + '/locations/static-location-actions/' + this.action.id + '/edit')
  }

  openDeleteStaticLocationDialog () {
    this.showBeginDeleteDialog = true
  }

  closeBeginDeleteDialog () {
    this.showBeginDeleteDialog = false
  }

  async deleteAndCloseBeginDeleteDialog () {
    this.closeBeginDeleteDialog()

    try {
      this.isLoading = true
      await this.deleteStaticLocationAction(this.action.id)
      await this.loadLocationActionTimepoints(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Deletion successful')
      this.$router.push('/configurations/' + this.configurationId + '/locations')
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Deletion failed')
    } finally {
      this.isLoading = false
    }
  }
}
</script>

<style scoped>

</style>
