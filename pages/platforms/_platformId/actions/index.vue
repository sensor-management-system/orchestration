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
    :is-user-authenticated="$auth.loggedIn"
  />
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import PlatformActionTimeline from '@/components/actions/PlatformActionTimeline.vue'
import HintCard from '@/components/HintCard.vue'
import { mapGetters } from 'vuex'
@Component({
  components: { HintCard, PlatformActionTimeline },
  computed:mapGetters('platforms',['actions'])
})
export default class PlatformActionsShowPage extends Vue {
  get platformId (): string {
    return this.$route.params.platformId
  }
}
</script>

<style scoped>

</style>
