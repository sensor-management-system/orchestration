<template>
  <div>
    <v-card-actions
      v-if="$auth.loggedIn"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :to="'/devices/' + deviceId + '/measuredquantities/new'"
      >
        Add Measured Quantity
      </v-btn>
    </v-card-actions>
    <hint-card v-if="deviceMeasuredQuantities.length === 0">
      There are no measured qauntities for this device.
    </hint-card>
    <BaseList
      :list-items="deviceMeasuredQuantities"
    >
      <template v-slot:list-item="{item,index}">
        <DevicesMeasuredQuantitiesListItem
          :measured-quantity="item"
          :index="index"
          :device-id="deviceId"
          :compartments="compartments"
          :sampling-medias="samplingMedia"
          :properties="properties"
          :units="units"
          :measured-quantity-units="measuredQuantityUnits"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!$auth.loggedIn"
              @click="initDeleteDialog(item)"
            />
          </template>
        </DevicesMeasuredQuantitiesListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="deviceMeasuredQuantities.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/measuredquantities/new'"
      >
        Add Measured Quantity
      </v-btn>
    </v-card-actions>
    <DevicesMeasuredQuantitiesDeleteDialog
      v-model="showDeleteDialog"
      :measured-quantity="measuredQuantityToDelete"
      @cancel-deletion="closeDialog"
      @submit-deletion="deleteAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import DevicesMeasuredQuantitiesListItem from '@/components/devices/DevicesMeasuredQuantitiesListItem.vue'
import { mapActions, mapState } from 'vuex'
import { CustomTextField } from '@/models/CustomTextField'
import DevicesMeasuredQuantitiesDeleteDialog from '@/components/devices/DevicesMeasuredQuantitiesDeleteDialog.vue'
import { DeviceProperty } from '@/models/DeviceProperty'
import HintCard from '@/components/HintCard.vue'
import BaseList from '@/components/shared/BaseList.vue'
@Component({
  components: { BaseList, HintCard, DevicesMeasuredQuantitiesDeleteDialog, DevicesMeasuredQuantitiesListItem },
  computed:{
    ...mapState('vocabulary',['compartments','samplingMedia','properties','units','measuredQuantityUnits']),
    ...mapState('devices',['deviceMeasuredQuantities'])
  },
  methods:{
    ...mapActions('vocabulary',['loadCompartments','loadSamplingMedia','loadProperties','loadUnits','loadMeasuredQuantityUnits']),
    ...mapActions('devices',['deleteDeviceMeasuredQuantity','loadDeviceMeasuredQuantities'])
  }
})
export default class DevicePropertyShowPage extends Vue {

  private showDeleteDialog=false;
  private measuredQuantityToDelete:DeviceProperty|null=null

  async created(){
    await this.loadCompartments()
    await this.loadSamplingMedia()
    await this.loadProperties()
    await this.loadUnits()
    await this.loadMeasuredQuantityUnits()
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  initDeleteDialog (measuredQuantity: DeviceProperty) {
    this.showDeleteDialog = true
    this.measuredQuantityToDelete = measuredQuantity
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.measuredQuantityToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.measuredQuantityToDelete === null || this.measuredQuantityToDelete.id === null) {
      return
    }
    try {
      await this.deleteDeviceMeasuredQuantity(this.measuredQuantityToDelete.id)
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'Measured quantity deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete measured quantity')
    } finally {
      this.closeDialog()
    }
  }

}
</script>

<style scoped>

</style>
