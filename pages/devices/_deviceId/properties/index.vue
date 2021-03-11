<template>
  <DevicePropertyExpansionPanel
    v-model="value"
  >
    <template #actions>
      <v-btn
        v-if="isLoggedIn"
        color="primary"
        text
        small
        nuxt
        :to="'/devices/' + deviceId + '/properties/' + value.id + '/edit'"
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
            @click="deleteProperty"
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
                Remove Property
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
    <template>
      <em>TODO:</em> <tt>DeviceProperty</tt> component for view mode, <tt>DevicePropertyForm</tt> for edit mode
    </template>
  </DevicePropertyExpansionPanel>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { DeviceProperty } from '@/models/DeviceProperty'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import DevicePropertyExpansionPanel from '@/components/DevicePropertyExpansionPanel.vue'

@Component({
  components: {
    DevicePropertyExpansionPanel,
    ProgressIndicator
  }
})
export default class DevicePropertiesShowPage extends Vue {
  private isLoading = false
  private isSaving = false

  /**
   * a DeviceProperty
   */
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: DeviceProperty

  mounted () {
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  get isLoggedIn (): boolean {
    return this.$store.getters['oidc/isAuthenticated']
  }

  deleteProperty () {
  }
}
</script>
