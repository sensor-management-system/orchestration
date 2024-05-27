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
      :disabled="isLoading"
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
import { mapActions, mapState } from 'vuex'
import { IStaticLocationAction } from '@/models/StaticLocationAction'
import { SetLoadingAction, LoadingSpinnerState } from '@/store/progressindicator'
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
  components: { DeleteDialog, StaticLocationActionData, DotMenuActionEdit, DotMenuActionDelete, DotMenu },
  computed: mapState('progressindicator', ['isLoading']),
  middleware: ['auth'],
  methods: {
    ...mapActions('configurations', ['loadStaticLocationAction', 'updateStaticLocationAction', 'deleteStaticLocationAction', 'loadLocationActionTimepoints']),
    ...mapActions('progressindicator', ['setLoading'])
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

  private showBeginDeleteDialog = false

  // vuex definition for typescript check
  loadStaticLocationAction!: LoadStaticLocationActionAction
  deleteStaticLocationAction!: DeleteStaticLocationActionAction
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction

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
    try {
      this.setLoading(true)
      await this.deleteStaticLocationAction(this.action.id)
      await this.loadLocationActionTimepoints(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Deletion successful')
      this.$router.push('/configurations/' + this.configurationId + '/locations')
    } catch (_e) {
      this.$store.commit('snackbar/setError', 'Deletion failed')
    } finally {
      this.setLoading(false)
      this.closeBeginDeleteDialog()
    }
  }
}
</script>

<style scoped>

</style>
