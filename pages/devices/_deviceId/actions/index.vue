<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        color="primary"
        small
        :to="'/devices/' + deviceId + '/actions/new'"
      >
        Add Action
      </v-btn>
    </v-card-actions>
      <hint-card v-if="actions.length === 0">
        There are no actions for this device.
      </hint-card>
      <DeviceActionTimeline
        :value="actions"
        :device-id="deviceId"
        :action-api-dispatcher="apiDispatcher"
        :is-user-authenticated="$auth.loggedIn"
      />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { mapGetters } from 'vuex'
import { DeviceActionApiDispatcher } from '@/modelUtils/actionHelpers'
import HintCard from '@/components/HintCard.vue'
import DeviceActionTimeline from '@/components/actions/DeviceActionTimeline.vue'

@Component({
  components: { DeviceActionTimeline, HintCard },
  computed:mapGetters('devices',['actions'])
})
export default class DeviceActionsShowPage extends Vue {
  get deviceId (): string {
    return this.$route.params.deviceId
  }
  get apiDispatcher () { //Todo überarbeiten (siehe auch anmerkung bei pages/platforms/_platformId/actions/index.vue)
    return new DeviceActionApiDispatcher(this.$api)
  }
}
</script>

<style scoped>

</style>
