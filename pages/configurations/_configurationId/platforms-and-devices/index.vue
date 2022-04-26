<template>
<div>
  <v-card-actions>
    <v-spacer />
    <v-btn
      v-if="$auth.loggedIn"
      color="primary"
      small
      nuxt
      :to="'/configurations/' + configurationId + '/platforms-and-devices/new'"
    >
      Add Platform or Device
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
  <v-row>
    <v-col cols="12" md="6">
      <v-card>
        <v-card-title>Mounted devices and platforms</v-card-title>
        <ConfigurationsTreeView
          v-if="configuration"
          ref="treeView"
          v-model="tree"
          :selected="selectedNode"
          @select="setSelectedNode"
        />
      </v-card>
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
@Component({
  components: { ConfigurationsTreeView, DateTimePicker },
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
    return tree
  }
  setSelectedNode (node: ConfigurationsTreeNode) {
    this.selectedNode = node
  }
}
</script>

<style scoped>

</style>
