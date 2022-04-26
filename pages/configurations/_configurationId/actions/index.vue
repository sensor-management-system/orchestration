<template>
  <v-card
    flat
  >
    <hint-card v-if="timelineActions.length === 0">
      There are no actions for this configuration.
    </hint-card>
    <v-card-text v-else>
      <v-timeline dense>
        <v-timeline-item
          v-for="action in timelineActions"
          :key="action.key"
          :color="action.color"
          :icon="action.icon"
          class="mb-4"
          small
        >
          <ConfigurationsTimelineActionCard
            :action="action"
          />
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import HintCard from '@/components/HintCard.vue'
import ConfigurationsTimelineActionCard from '@/components/configurations/ConfigurationsTimelineActionCard.vue'
import { mapGetters } from 'vuex'
@Component({
  components: { ConfigurationsTimelineActionCard, HintCard },
  computed:mapGetters('configurations',['timelineActions'])
})
export default class ConfigurationShowActionPage extends Vue {
}
</script>

<style scoped>

</style>
