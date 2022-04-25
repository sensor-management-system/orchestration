<template>
  <div>
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
          :to="'/devices/' + this.deviceId + '/customfields'"
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
            <CustomFieldForm
              v-model="customField"
              :readonly="false"
            />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="$auth.loggedIn"
          small
          text
          nuxt
          :to="'/devices/' + this.deviceId + '/customfields'"
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import CustomFieldForm from '@/components/CustomFieldForm.vue'
import { CustomTextField } from '@/models/CustomTextField'
import { mapActions } from 'vuex'
@Component({
  components: { CustomFieldForm },
  methods:mapActions('devices',['addDeviceCustomField','loadDeviceCustomFields'])
})
export default class DeviceCustomFieldAddPage extends Vue {
  private customField:CustomTextField = new CustomTextField()

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  async save (): Promise<void> {

    try {
      await this.addDeviceCustomField({
        deviceId: this.deviceId,
        deviceCustomField: this.customField
      })
      this.loadDeviceCustomFields(this.deviceId)
      this.$router.push('/devices/' + this.deviceId + '/customfields')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    }
  }
}
</script>

<style scoped>

</style>
