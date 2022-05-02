<template>
  <v-card
    class="mb-2"
  >
    <v-card-text>
      <v-row
        no-gutters
      >
        <v-col
          cols="12"
          md="2"
        >
          <label>Key:</label>
          {{ customField.key }}
        </v-col>
        <v-col
          cols="12"
          md="8"
        >
          <label>Value:</label>
          {{ customField.value }}
        </v-col>
        <v-col
          cols="12"
          md="2"
          class="text-right"
          align-self="center"
        >
          <v-row>
            <v-row>
              <v-col align-self="end" class="text-right">
                <v-btn
                  v-if="$auth.loggedIn"
                  color="primary"
                  text
                  small
                  nuxt
                  :to="'/devices/' + deviceId + '/customfields/' + customField.id + '/edit'"
                >
                  Edit
                </v-btn>
                <DotMenu
                  v-if="$auth.loggedIn"
                >
                  <template #actions>
                    <slot name="dot-menu-items" />
                  </template>
                </DotMenu>
              </v-col>
            </v-row>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Prop } from 'nuxt-property-decorator'
import { CustomTextField } from '@/models/CustomTextField'
import DotMenu from '@/components/DotMenu.vue'
@Component({
  components: { DotMenu }
})
export default class DevicesCustomFieldListItem extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private customField!: CustomTextField

  @Prop({
    required: true
  })
  private deviceId!: string
}
</script>

<style scoped>

</style>
