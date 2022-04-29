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
          :to="'/devices/' + this.deviceId + '/customfields'"
          @save="save"
        />
      </v-card-actions>
      <v-card-text>
            <CustomFieldForm
              v-model="customField"
              :readonly="false"
            />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/devices/' + this.deviceId + '/customfields'"
          @save="save"
        />
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import CustomFieldForm from '@/components/CustomFieldForm.vue'
import SaveAndCancelButtons from '@/components/configurations/SaveAndCancelButtons.vue'

import { CustomTextField } from '@/models/CustomTextField'
import { mapActions } from 'vuex'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  middleware: ['auth'],
  components: { ProgressIndicator, SaveAndCancelButtons, CustomFieldForm },
  methods:mapActions('devices',['addDeviceCustomField','loadDeviceCustomFields'])
})
export default class DeviceCustomFieldAddPage extends Vue {
  private isSaving = false

  private customField:CustomTextField = new CustomTextField()

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save (): Promise<void> {

    try {
      this.isSaving=true

      await this.addDeviceCustomField({
        deviceId: this.deviceId,
        deviceCustomField: this.customField
      })
      this.loadDeviceCustomFields(this.deviceId)
      this.$store.commit('snackbar/setSuccess', 'New custom field added')
      this.$router.push('/devices/' + this.deviceId + '/customfields')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    }finally {
      this.isSaving=false
    }
  }
}
</script>

<style scoped>

</style>
