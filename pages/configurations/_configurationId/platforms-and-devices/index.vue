<template>
<div>
  <v-card-actions>
    <v-spacer />
    <v-btn
      v-if="$auth.loggedIn"
      color="primary"
      small
      nuxt
      :to="'/configurations/' + configurationId + '/platforms-and-devices/mount'"
    >
      Mount Platform or Device
    </v-btn>
    <v-btn
      v-if="$auth.loggedIn"
      color="secondary"
      small
      nuxt
      :to="'/configurations/' + configurationId + '/platforms-and-devices/unmount'"
    >
      -Un-mount Platform or Device
    </v-btn>
  </v-card-actions>
  <v-row>
    <v-col cols="12" md="3">
      <DateTimePicker
        v-model="selectedDate"
        placeholder="e.g. 2000-01-31 12:00"
        label="Configuration at date"
      />
    </v-col>
    <v-col>
      <v-select
        v-model="selectedDate"
        :item-value="(x) => x.date"
        :item-text="(x) => x.text"
        :items="mountingActionsDates"
        label="Dates defined by actions"
        hint="The referenced time zone is UTC."
        persistent-hint
      />
    </v-col>
  </v-row>
  <v-row justify="center">
    <v-col cols="12" md="6">
      <v-card>
        <v-container>
          <v-card-title>Mounted devices and platforms</v-card-title>
          <ConfigurationsTreeView
            v-if="configuration"
            ref="treeView"
            v-model="selectedNode"
            :items="tree"
          />
        </v-container>
      </v-card>
    </v-col>
    <v-col>
      <v-slide-x-reverse-transition>
        <div v-show="selectedNode">
          <v-card-title>Selected node information</v-card-title>
          <ConfigurationsTreeNodeDetail
            v-if="selectedNode"
            :node="selectedNode"
          />
        </div>
      </v-slide-x-reverse-transition>
    </v-col>
  </v-row>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import DateTimePicker from '@/components/DateTimePicker.vue'
import { DateTime } from 'luxon'
import { mapGetters, mapState } from 'vuex'
import { buildConfigurationTree } from '@/modelUtils/mountHelpers'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsTreeNodeDetail from '@/components/configurations/ConfigurationsTreeNodeDetail.vue'
@Component({
  components: { ConfigurationsTreeNodeDetail, ConfigurationsTreeView, DateTimePicker },
  computed:{
    ...mapGetters('configurations',['mountingActionsDates']),
    ...mapState('configurations',['configuration'])
  }
})
export default class ConfigurationShowPlatformsAndDevicesPage extends Vue {

  private selectedNode: ConfigurationsTreeNode | null = null
  private selectedDate = DateTime.utc()

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get tree () {
    const selectedNodeId = this.selectedNode?.id
    const tree = buildConfigurationTree(this.configuration, this.selectedDate)
    if (selectedNodeId) {
      const node = tree.getById(selectedNodeId)
      if (node) {
        this.selectedNode = node
      }
    }
    return tree.toArray()
  }
  // setSelectedNode (node: ConfigurationsTreeNode) {
  //   this.selectedNode = node
  // }
}
</script>

<style scoped>

</style>
