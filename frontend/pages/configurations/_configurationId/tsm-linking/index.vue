<!--
 SPDX-FileCopyrightText: 2020 - 2024

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <v-alert text type="info">
      The feature to link measured quantities to datastreams of time series management systems is currently in an experimental phase.
      It could be that some of the functionality is only accessible from your institutes intranet.
      If you encounter any problems, feel free to use the gitlab service desk &amp; report the issue.
    </v-alert>
    <v-card flat>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="editable"
          color="primary"
          small
          nuxt
          :to="'/configurations/' + configurationId + '/tsm-linking/new'"
        >
          Add Data Linking
        </v-btn>
      </v-card-actions>
    </v-card>
    <TsmLinkingOverviewTable :devices="availableDevices" />
  </div>
</template>

<script lang="ts">
import { Component, InjectReactive, Vue } from 'nuxt-property-decorator'
import { mapActions, mapGetters } from 'vuex'
import TsmLinkingOverviewTable from '@/components/configurations/tsmLinking/TsmLinkingOverviewTable.vue'
import { AvailableDevicesGetter } from '@/store/configurations'

@Component({
  components: { TsmLinkingOverviewTable },
  computed: {
    ...mapGetters('configurations', ['availableDevices'])
  },
  methods: {
    ...mapActions('configurations', ['loadDeviceMountActionsIncludingDeviceInformation'])
  }
})
export default class ConfigurationShowTsmLinkingPage extends Vue {
  @InjectReactive()
    editable!: boolean

  availableDevices!: AvailableDevicesGetter

  get configurationId (): string {
    return this.$route.params.configurationId
  }
}
</script>

<style scoped>

</style>
