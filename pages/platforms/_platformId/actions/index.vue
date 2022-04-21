<template>
<div>
  <v-card-actions>
    <v-spacer />
    <v-btn
      v-if="$auth.loggedIn"
      color="primary"
      small
      :to="'/platforms/' + platformId + '/actions/new'"
    >
      Add Action
    </v-btn>
  </v-card-actions>
  <hint-card v-if="actions.length === 0">
    There are no actions for this platform.
  </hint-card>
  <PlatformActionTimeline
    :value="actions"
    :platform-id="platformId"
    :action-api-dispatcher="apiDispatcher"
    :is-user-authenticated="$auth.loggedIn"
  />
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import PlatformActionTimeline from '@/components/actions/PlatformActionTimeline.vue'
import HintCard from '@/components/HintCard.vue'
import { mapGetters } from 'vuex'

import { PlatformActionApiDispatcher } from '@/modelUtils/actionHelpers'

@Component({
  components: { HintCard, PlatformActionTimeline },
  computed:mapGetters('platforms',['actions'])
})
export default class PlatformActionsShowPage extends Vue {
  get platformId (): string {
    return this.$route.params.platformId
  }
  get apiDispatcher () { // Todo überarbeiten, da z.B. beim Löschen mit dieser Methode die Actions nicht neu geladen werden
    return new PlatformActionApiDispatcher(this.$api)
  }
}
</script>

<style scoped>

</style>
