<template>
  <v-card
    flat
  >
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        small
        text
        nuxt
        :to="'/devices/' + this.deviceId + '/measuredquantities'"
      >
        Cancel
      </v-btn>
      <v-btn
        v-if="$auth.loggedIn"
        color="green"
        small
        @click="save"
      >
        Add
      </v-btn>
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
      <v-btn
        v-if="$auth.loggedIn"
        small
        text
        nuxt
        :to="'/devices/' + this.deviceId + '/measuredquantities'"
      >
        Cancel
      </v-btn>
      <v-btn
        v-if="$auth.loggedIn"
        color="green"
        small
        @click="save"
      >
        Add
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { DeviceProperty } from '@/models/DeviceProperty'
import { mapActions, mapState } from 'vuex'
import DevicePropertyForm from '@/components/DevicePropertyForm.vue'

@Component({
  components: { DevicePropertyForm },
  computed:mapState('vocabulary',['compartments','samplingMedia','properties','units','measuredQuantityUnits']),
  methods:{
    ...mapActions('devices',['addDeviceMeasuredQuantity','loadDeviceMeasuredQuantities']),
    ...mapActions('vocabulary',['loadCompartments','loadSamplingMedia','loadProperties','loadUnits','loadMeasuredQuantityUnits']),
  }
})
export default class DevicePropertyAddPage extends Vue
{
  private valueCopy: DeviceProperty = new DeviceProperty()

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save (): Promise<void> {

    try {
      await this.addDeviceMeasuredQuantity({
        deviceId: this.deviceId,
        deviceMeasuredQuantity: this.valueCopy
      })
      this.loadDeviceMeasuredQuantities(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/measuredquantities')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save measured qauntity')
    }
  }
}
</script>

<style scoped>

</style>
