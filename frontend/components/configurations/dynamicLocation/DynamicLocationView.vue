<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
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
