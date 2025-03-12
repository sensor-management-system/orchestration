<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <DateTimePicker
          :value="selectedDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Configuration at date"
          hint=""
          @input="setSelectedDate"
        />
      </v-col>
      <v-col>
        <v-select
          :value="selectedDate"
          :items="mountActionDateItems"
          label="Dates defined by actions"
          hint="The referenced time zone is UTC."
          persistent-hint
          @input="setSelectedDate"
        />
      </v-col>
    </v-row>

    <v-card flat>
      <v-card-title class="primary white--text">
        Mounted devices and platforms
      </v-card-title>
      <v-card-text>
        <ConfigurationsTreeView
          v-if="selectedConfiguration && tree"
          ref="treeView"
          v-model="selectedNode"
          :tree="tree"
          :disable-per-node="true"
          :activatable="false"
          show-detailed-name
          selectable
          selection-type="independent"
          :selection.sync="selection"
        />
      </v-card-text>
    </v-card>
  </div>
</template>

<script lang="ts">
import { mapActions, mapGetters, mapState } from 'vuex'

import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'
import DateTimePicker from '@/components/DateTimePicker.vue'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import {
  ConfigurationsState,
  LoadMountingActionsAction,
  LoadMountingConfigurationForDateAction, SetSelectedDateAction
} from '@/store/configurations'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { Configuration } from '@/models/Configuration'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'
import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { MountAction } from '@/models/MountAction'
import { SetLoadingAction } from '@/store/progressindicator'
import { ContactsState } from '@/store/contacts'
import { Contact } from '@/models/Contact'

@Component({
  components: { ConfigurationsTreeView, DateTimePicker },
  computed: {
    ...mapState('configurations', [
      'selectedDate',
      'configurationMountingActionsForDate'
    ]),
    ...mapGetters('configurations', ['mountActionDateItems']),
    ...mapState('contacts', ['contacts'])
  },
  methods: {
    ...mapActions('configurations', [
      'setSelectedDate',
      'loadMountingActions',
      'loadMountingConfigurationForDate'
    ]),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ReuseSelectMount extends Vue {
  @Prop({
    required: true,
    type: Object
  })
    selectedConfiguration!: Configuration

  private tree: ConfigurationsTree = new ConfigurationsTree()
  private selectedNode: ConfigurationsTreeNode | null = null

  private selection: ConfigurationsTreeNode[] = []

  // vuex
  private selectedDate!: ConfigurationsState['selectedDate']
  private configurationMountingActionsForDate!: ConfigurationsState['configurationMountingActionsForDate']
  private setSelectedDate!: SetSelectedDateAction
  private loadMountingActions!: LoadMountingActionsAction
  private loadMountingConfigurationForDate!: LoadMountingConfigurationForDateAction
  private contacts!: ContactsState['contacts']
  private setLoading!: SetLoadingAction

  get currentUserMail (): string | null {
    return this.$auth.user?.email as string | null
  }

  get currentUserAsContact (): Contact | null {
    const foundUser = this.contacts.find((c: Contact) => c.email === this.currentUserMail)
    if (foundUser) {
      return foundUser
    }
    return null
  }

  get selectedTree (): ConfigurationsTree | null {
    if (this.selection.length > 0) {
      let temporaryTree = new ConfigurationsTree()

      const visitAndAddToResult = (node: ConfigurationsTreeNode, parent: ConfigurationsTreeNode | null) => {
        if (this.nodeIsinSelection(node)) {
          const copy = this.createNodeCopy(node)

          copy.children = []

          if (parent === null) { // we have the root node
            copy.disabled = true
            temporaryTree = ConfigurationsTree.fromArray([copy])
          } else {
            parent.children.push(copy)
          }

          for (const innerNode of node.children) {
            visitAndAddToResult(innerNode, copy)
          }
        }
      }

      for (const node of this.tree) {
        visitAndAddToResult(node, null)
      }

      if (temporaryTree.length > 0 && temporaryTree.at(0).children.length > 0) {
        // the root node alone does not make sense
        return temporaryTree
      }
    }
    return null
  }

  nodeIsinSelection (node: ConfigurationsTreeNode) {
    const found = this.selection.find((el: ConfigurationsTreeNode) => {
      return el.id === node.id
    })
    if (found) {
      return true
    }
    return false
  }

  createTreeWithConfigAsRootNode () {
    if (this.selectedConfiguration && this.configurationMountingActionsForDate) {
      // construct the configuration as the root node of the tree
      const rootNode = new ConfigurationNode(new ConfigurationMountAction(this.selectedConfiguration))
      rootNode.children = this.configurationMountingActionsForDate.toArray()
      // rootNode.disabled = true
      this.tree = ConfigurationsTree.fromArray([rootNode])
    }
  }

  private createNodeCopy (node: ConfigurationsTreeNode): ConfigurationsTreeNode {
    if (node.isPlatform()) {
      const newNode = PlatformNode.createFromObject(node as PlatformNode)
      const newNodeAction = newNode.unpack()
      this.setRelevantActionData(newNodeAction)
      return newNode
    }

    if (node.isDevice()) {
      const newNode = DeviceNode.createFromObject(node as DeviceNode)
      const newNodeAction = newNode.unpack()
      this.setRelevantActionData(newNodeAction)
      return newNode
    }

    return ConfigurationNode.createFromObject(node as ConfigurationNode)
  }

  setRelevantActionData (action: MountAction) {
    action.x = null
    action.y = null
    action.z = null
    action.epsgCode = ''
    action.elevationDatumName = ''
    action.elevationDatumUri = ''
    action.beginDescription = ''
    action.endDescription = ''
    action.label = ''
    action.beginContact = this.currentUserAsContact
    action.endContact = action.endContact ? this.currentUserAsContact : null
  }

  getAllDescendants (node: ConfigurationsTreeNode): ConfigurationsTreeNode[] {
    let descendants: ConfigurationsTreeNode[] = [] // Array to store all descendants

    function traverse (currentNode: ConfigurationsTreeNode) {
      if (!currentNode || !currentNode.children) {
        return
      }
      // Add children to the descendants array
      descendants = descendants.concat(currentNode.children)

      // Recursively traverse each child
      currentNode.children.forEach((child: ConfigurationsTreeNode) => traverse(child))
    }

    traverse(node) // Start traversing from the given node
    return descendants
  }

  diffArrays (arrayA: ConfigurationsTreeNode[], arrayB: ConfigurationsTreeNode[]) {
    return arrayA.filter((elA) => {
      const found = arrayB.find((elB) => {
        return elB.id === elA.id
      })
      if (found) {
        return false
      }
      return true
    })
  }

  removeChildrenFromSelection (childrenToRemove: ConfigurationsTreeNode[]) {
    for (const node of childrenToRemove) {
      if (node.children) {
        const allChildren = this.getAllDescendants(node)
        for (const child of allChildren) {
          const foundIndex = this.selection.findIndex(el => el.id === child.id)
          if (foundIndex !== -1) {
            this.selection.splice(foundIndex, 1)
          }
        }
      }
    }
  }

  addParentsToSelection (parentsToAdd: ConfigurationsTreeNode[]) {
    for (const node of parentsToAdd) {
      const parents = this.tree.getParents(node)
      for (const parent of parents) {
        const found = this.selection.find(el => el.id === parent.id)
        if (!found) {
          this.selection.push(parent)
        }
      }
    }
  }

  @Watch('selectedDate')
  async onPropertyChanged (_value: DateTime, _oldValue: DateTime) {
    if (!this.selectedConfiguration) {
      return
    }
    try {
      this.setLoading(true)

      this.selection.splice(0, this.selection.length)

      await this.loadMountingConfigurationForDate({ id: this.selectedConfiguration.id, timepoint: this.selectedDate })
      this.createTreeWithConfigAsRootNode()
    } catch (error) {
      this.$store.commit('snackbar/setError', 'Loading of configuration tree failed')
    } finally {
      this.setLoading(false)
    }
  }

  @Watch('selection', {
    immediate: true,
    deep: true
  })
  onSelectionChanged (newVal: ConfigurationsTreeNode[], oldVal: ConfigurationsTreeNode[]) {
    if (oldVal === undefined) {
      oldVal = []
    }
    // compare oldVal (previous selection) with newVal (current selection)
    const parentsToAdd = this.diffArrays(newVal, oldVal)
    const childrenToRemove = this.diffArrays(oldVal, newVal)

    this.removeChildrenFromSelection(childrenToRemove)
    this.addParentsToSelection(parentsToAdd)

    this.$emit('selected', this.selectedTree)
  }
}
</script>

<style scoped>

</style>
