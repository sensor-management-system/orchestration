<template>
  <CustomFieldCard
    v-model="value"
  >
    <template #actions>
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        text
        small
        nuxt
        :to="'/devices/' + deviceId + '/customfields/' + value.id + '/edit'"
      >
        Edit
      </v-btn>
      <v-menu
        v-if="isLoggedIn"
        close-on-click
        close-on-content-click
        offset-x
        left
        z-index="999"
      >
        <template v-slot:activator="{ on }">
          <v-btn
            data-role="property-menu"
            icon
            small
            v-on="on"
          >
            <v-icon
              dense
              small
            >
              mdi-dots-vertical
            </v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            dense
            @click="deleteField"
          >
            <v-list-item-content>
              <v-list-item-title
                class="red--text"
              >
                <v-icon
                  left
                  small
                  color="red"
                >
                  mdi-delete
                </v-icon>
                Remove field
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </CustomFieldCard>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { CustomTextField } from '@/models/CustomTextField'
import CustomFieldCard from '@/components/CustomFieldCard.vue'

@Component({
  components: {
    CustomFieldCard
  }
})
export default class DeviceCustomFieldsShowPage extends Vue {
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

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  deleteField (): void {
    this.$emit('delete', this.value)
  }
}
</script>
