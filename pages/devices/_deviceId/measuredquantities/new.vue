<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/devices/' + this.deviceId + '/measuredquantities'"
          @save="save"
        />
      </v-card-actions>
      <v-card-text>
        <DevicePropertyForm
          ref="propertyForm"
          v-model="valueCopy"
          :readonly="false"
          :compartments="compartments"
          :sampling-medias="samplingMedia"
          :properties="properties"
          :units="units"
          :measured-quantity-units="measuredQuantityUnits"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/devices/' + this.deviceId + '/measuredquantities'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { DeviceProperty } from '@/models/DeviceProperty'
import { mapActions, mapState } from 'vuex'
import DevicePropertyForm from '@/components/DevicePropertyForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

@Component({
  components: { SaveAndCancelButtons, DevicePropertyForm },
  computed:mapState('vocabulary',['compartments','samplingMedia','properties','units','measuredQuantityUnits']),
  methods:{
    ...mapActions('devices',['addDeviceMeasuredQuantity','loadDeviceMeasuredQuantities']),
    ...mapActions('vocabulary',['loadCompartments','loadSamplingMedia','loadProperties','loadUnits','loadMeasuredQuantityUnits']),
  }
})
export default class DevicePropertyAddPage extends Vue {
  private isSaving = false
  private valueCopy: DeviceProperty = new DeviceProperty()

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save (): Promise<void> {

    try {
      this.isSaving=true
      await this.addDeviceMeasuredQuantity({
        deviceId: this.deviceId,
        deviceMeasuredQuantity: this.valueCopy
      })
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'New measured qauntity added')
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save measured qauntity')
    }finally {
      this.isSaving=false
    }
  }
}
</script>

<style scoped>

</style>
