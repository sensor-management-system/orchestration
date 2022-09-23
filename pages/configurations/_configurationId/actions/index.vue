<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <div>
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/configurations/' + configurationId + '/actions/new'"
      >
        Add Action
      </v-btn>
    </v-card-actions>
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
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapGetters } from 'vuex'

import { TimelineActionsGetter } from '@/store/configurations'

import HintCard from '@/components/HintCard.vue'
import ConfigurationsTimelineActionCard from '@/components/configurations/ConfigurationsTimelineActionCard.vue'

@Component({
  components: { ConfigurationsTimelineActionCard, HintCard },
  computed: mapGetters('configurations', ['timelineActions'])
})
export default class ConfigurationShowActionPage extends Vue {
  timelineActions!: TimelineActionsGetter

    @InjectReactive()
      editable!: boolean

    get configurationId (): string {
      return this.$route.params.configurationId
    }
}
</script>

<style scoped>

</style>
