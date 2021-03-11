<template>
  <div>
    <NuxtChild
      v-if="isEditModeForField"
      v-model="field"
    />
    <CustomFieldCard
      v-else
      v-model="field"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import CustomFieldCard from '@/components/CustomFieldCard.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { CustomTextField } from '@/models/CustomTextField'

@Component({
  components: {
    CustomFieldCard,
    ProgressIndicator
  }
})
export default class DeviceCustomFieldsIdPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: CustomTextField

  get field (): CustomTextField {
    return this.value
  }

  set field (value: CustomTextField) {
    this.$emit('input', value)
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isEditModeForField () {
    return this.$route.path === '/devices/' + this.deviceId + '/customfields/' + this.value.id + '/edit'
  }
}
</script>
