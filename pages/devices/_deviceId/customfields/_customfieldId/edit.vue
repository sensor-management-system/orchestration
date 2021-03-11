<template>
  <div>
    <ProgressIndicator
      v-model="isSaving"
      dark
    />
    <CustomFieldCardForm
      ref="customFieldCardForm"
      v-model="valueCopy"
    >
      <template #actions>
        <v-btn
          v-if="isLoggedIn"
          text
          small
          nuxt
          :to="'/devices/' + deviceId + '/customfields'"
        >
          Cancel
        </v-btn>
        <v-btn
          v-if="isLoggedIn"
          color="green"
          small
          @click="save()"
        >
          Apply
        </v-btn>
      </template>
    </CustomFieldCardForm>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

import { CustomTextField } from '@/models/CustomTextField'

import CustomFieldCardForm from '@/components/CustomFieldCardForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: {
    CustomFieldCardForm,
    ProgressIndicator
  }
})
export default class DeviceCustomFieldsShowPage extends Vue {
  private isSaving: boolean = false
  private valueCopy: CustomTextField = new CustomTextField()

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: CustomTextField

  created () {
    this.valueCopy = CustomTextField.createFromObject(this.value)
  }

  mounted () {
    (this.$refs.customFieldCardForm as Vue & { focus: () => void}).focus()
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  save (): void {
    this.isSaving = true
    this.$api.customfields.update(this.deviceId, this.valueCopy).then(() => {
      this.isSaving = false
      this.$emit('input', this.valueCopy)
      this.$router.push('/devices/' + this.deviceId + '/customfields')
    }).catch((_e: Error) => {
      this.isSaving = false
      this.$store.commit('snackbar/setError', 'Failed to save custom field')
    })
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onValueChanged (val: Device) {
    this.valueCopy = CustomTextField.createFromObject(val)
  }
}
</script>
