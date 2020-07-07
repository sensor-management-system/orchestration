<template>
  <div>
    <v-form>
      <v-card
        outlined
      >
        <v-tabs-items
          v-model="activeTab"
        >
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-dialog
                      ref="startDateDialog"
                      v-model="startDateModal"
                      :return-value.sync="startDate"
                      persistent
                      width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model="startDate"
                          label="Start date"
                          prepend-icon="mdi-calendar-range"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                        />
                      </template>
                      <v-date-picker v-model="startDate" scrollable>
                        <v-spacer />
                        <v-btn text color="primary" @click="startDateModal = false">
                          Cancel
                        </v-btn>
                        <v-btn text color="primary" @click="$refs.startDateDialog.save(startDate)">
                          OK
                        </v-btn>
                      </v-date-picker>
                    </v-dialog>
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-dialog
                      ref="endDateDialog"
                      v-model="endDateModal"
                      :return-value.sync="endDate"
                      persistent
                      width="290px"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model="endDate"
                          label="End date"
                          prepend-icon="mdi-calendar-range"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                        />
                      </template>
                      <v-date-picker v-model="endDate" scrollable>
                        <v-spacer />
                        <v-btn text color="primary" @click="endDateModal = false">
                          Cancel
                        </v-btn>
                        <v-btn text color="primary" @click="$refs.endDateDialog.save(endDate)">
                          OK
                        </v-btn>
                      </v-date-picker>
                    </v-dialog>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="locationType"
                      label="Location type"
                      :items="['Stationary', 'Dynamic']"
                    />
                  </v-col>
                </v-row>
                <div v-if="locationType === 'Stationary'">
                  <v-row>
                    <v-col cols="12" md="3">
                      <v-text-field
                        v-model.lazy="longitude"
                        label="Longitude (WGS84)"
                      />
                    </v-col>
                    <v-col cols="12" md="3">
                      <v-text-field
                        v-model.lazy="latitude"
                        label="Latitude (WGS84)"
                      />
                    </v-col>
                    <v-col cols="12" md="3">
                      <v-text-field
                        v-model="elevation"
                        label="Elevation (m asl)"
                      />
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" md="6">
                      <div id="map-wrap" style="height: 300px">
                        <no-ssr>
                          <l-map :zoom="10" :center="location">
                            <l-tile-layer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png" />
                            <l-marker :lat-lng="location" />
                          </l-map>
                        </no-ssr>
                      </div>
                    </v-col>
                  </v-row>
                </div>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-text>
                <v-row>
                  <v-col cols="3">
                    <ContactSelect v-model="contacts" :readonly="false" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item :eager="true">
            <v-card
              flat
            >
              <v-card-text>
                <v-row>
                  <v-col cols="12" md="6">
                    <v-treeview
                      :active.sync="selectedNodeIds"
                      :items="tree"
                      activatable
                      hoverable
                      rounded
                      open-all
                    >
                      <template v-slot:prepend="{ item }">
                        <v-icon v-if="nodeIsPlatform(item)">
                          mdi-rocket-outline
                        </v-icon>
                        <v-icon v-else>
                          mdi-network-outline
                        </v-icon>
                      </template>
                    </v-treeview>
                  </v-col>
                  <v-col cols="6" md="6">
                    <v-card v-if="selectedPlatform || selectedDevice">
                      <v-breadcrumbs :items="breadcrumbs" divider=">" />
                      <v-card-text>
                        <v-row v-if="selectedPlatform">
                          <v-col cols="12" md="9">
                            <template v-if="selectedPlatform.description">
                              {{ selectedPlatform.description }}
                            </template>
                            <template v-else>
                              The selected platform has no description.
                            </template>
                          </v-col>
                        </v-row>
                        <v-row v-else-if="selectedDevice">
                          <v-col cols="12" md="9">
                            <template v-if="selectedDevice.description">
                              {{ selectedDevice.description }}
                            </template>
                            <template v-else>
                              The selected device has no description.
                            </template>
                          </v-col>
                        </v-row>
                      </v-card-text>
                      <v-card-actions>
                        <v-btn
                          v-if="selectedPlatform || selectedDevice"
                          color="red"
                          text
                          @click="removeSelectedNode"
                        >
                          remove
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                    <v-alert 
                      type="info"
                      outlined
                      v-else
                    >
                      Select a platform on the left side to add devices or platforms to it.<br>
                      To add a device or platform to the root of this configuration, deselect any previously selected device or platform.
                    </v-alert>
                    <template v-if="!selectedDevice">
                      <v-subheader v-if="selectedPlatform">Add platforms and devices to the selected platform:</v-subheader>
                      <v-subheader v-else>Add platforms and devices to the configuration:</v-subheader>
                      <v-row>
                        <v-col cols="12" md="3">
                          <v-select
                            v-model="searchOptions.searchType"
                            label="Type"
                            :items="searchTypes"
                          />
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-text-field
                            v-model="searchOptions.text"
                            label="Name"
                          />
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-btn
                            color="primary"
                            @click="search"
                          >
                            search
                          </v-btn>
                        </v-col>
                      </v-row>
                      <v-row v-if="platforms">
                        <v-col cols="12">
                          <v-list two-line>
                            <v-list-item-group
                              v-model="platformItem"
                              color="primary"
                            >
                              <template
                                v-for="(item, index) in platforms"
                              >
                                <v-list-item
                                  :key="item.shortName"
                                  :disabled="isNodeInTree(item.id) ? true : false"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title v-text="item.shortName" />
                                    <v-list-item-subtitle class="text--primary" v-text="item.longName" />
                                    <v-list-item-subtitle>URN (TODO)</v-list-item-subtitle>
                                  </v-list-item-content>
                                  <v-list-item-action>
                                    <v-btn
                                      :disabled="isNodeInTree(item.id) ? true : false"
                                      @click="addPlatformNode(item)"
                                    >
                                      add
                                    </v-btn>
                                  </v-list-item-action>
                                </v-list-item>
                                <v-divider
                                  v-if="index + 1 < platforms.length"
                                  :key="index"
                                />
                              </template>
                            </v-list-item-group>
                          </v-list>
                        </v-col>
                      </v-row>
                      <v-row v-if="devices">
                        <v-col cols="12">
                          <v-list two-line>
                            <v-list-item-group
                              v-model="deviceItem"
                              color="primary"
                            >
                              <template
                                v-for="(item, index) in devices"
                              >
                                <v-list-item
                                  :key="item.shortName"
                                  :disabled="isNodeInTree(item.id) ? true : false"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title v-text="item.shortName" />
                                    <v-list-item-subtitle class="text--primary" v-text="item.longName" />
                                    <v-list-item-subtitle>URN (TODO)</v-list-item-subtitle>
                                  </v-list-item-content>
                                  <v-list-item-action>
                                    <v-btn
                                      :disabled="isNodeInTree(item.id) ? true : false"
                                      @click="addDeviceNode(item)"
                                    >
                                      add
                                    </v-btn>
                                  </v-list-item-action>
                                </v-list-item>
                                <v-divider
                                  v-if="index + 1 < devices.length"
                                  :key="index"
                                />
                              </template>
                            </v-list-item-group>
                          </v-list>
                        </v-col>
                      </v-row>
                    </template>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <v-btn
          v-if="!isInEditMode"
          fab
          fixed
          bottom
          right
          color="secondary"
          @click="toggleEditMode"
        >
          <v-icon>
            mdi-pencil
          </v-icon>
        </v-btn>
      </v-card>
    </v-form>
  </div>
</template>

<style lang="scss">
@import "~/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Vue, Component, Watch } from 'nuxt-property-decorator'

// @ts-ignore
import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'
// @ts-ignore
import AppBarTabsExtension from '@/components/AppBarTabsExtension.vue'

// @ts-ignore
import ContactSelect from '@/components/ContactSelect.vue'
// @ts-ignore
import Contact from '@/models/Contact'

// @ts-ignore
import Platform from '@/models/Platform'
// @ts-ignore
import Device from '@/models/Device'
// @ts-ignore
import { PlatformNode } from '@/models/PlatformNode'
// @ts-ignore
import { DeviceNode } from '@/models/DeviceNode'
// @ts-ignore
import Manufacturer from '@/models/Manufacturer'
// @ts-ignore
import SmsService from '@/services/SmsService'

type Node = DeviceNode|PlatformNode

enum SearchType {
  Platform = 'Platform',
  Device = 'Device'
}

interface ISearchOptions {
  searchType: SearchType
  text: string
}

@Component
// @ts-ignore
export class AppBarTabsExtensionExtended extends AppBarTabsExtension {
  get tabs (): String[] {
    return [
      'Configuration',
      'Contacts',
      'Platforms and Devices'
    ]
  }
}

@Component({
  components: {
    ContactSelect
  }
})
// @ts-ignore
export default class ConfigurationsIdPage extends Vue {
  private activeTab: number = 0
  private editMode: boolean = false

  private startDateModal: boolean = false
  private endDateModal: boolean = false
  private startDate: Date | null = null
  private endDate: Date | null = null

  private locationType: string = ''

  private longitude: number = 0
  private latitude: number = 0
  private elevation: number = 0

  private contacts: Contact[] = []

  private selectedNodeIds: number[] = []
  private selectedPlatform: Platform | null = null
  private selectedDevice: Device | null = null

  private searchTypes: string[] = [
    SearchType.Platform,
    SearchType.Device
  ]

  private searchOptions: ISearchOptions = {
    searchType: SearchType.Platform,
    text: ''
  }

  private platformsResult: Platform[] = [] as Platform[]
  private devicesResult: Device[] = [] as Device[]

  private tree: Node[] = [] as Node[]

  private platformItem: string = ''
  private deviceItem: string = ''

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
    this.$nuxt.$on('AppBarContent:save-button-click', () => {
      this.save()
    })
    this.$nuxt.$on('AppBarContent:cancel-button-click', () => {
      this.toggleEditMode()
      // this.$router.push('/configurations')
    })

    this.$nuxt.$emit('app-bar-extension', AppBarTabsExtensionExtended)
    this.$nuxt.$on('AppBarExtension:change', (tab: number) => {
      this.activeTab = tab
    })

    this.tree = this.getDemoTree()
  }

  mounted () {
    this.$nextTick(() => {
      if (!this.$route.params.id) {
        this.$nuxt.$emit('AppBarContent:title', 'Add Configuration')
      }
      this.$nuxt.$emit('AppBarContent:save-button-hidden', !this.editMode)
      this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !this.editMode)
    })
  }

  beforeDestroy () {
    this.$nuxt.$emit('app-bar-content', null)
    this.$nuxt.$emit('app-bar-extension', null)
    this.$nuxt.$off('AppBarContent:save-button-click')
    this.$nuxt.$off('AppBarContent:cancel-button-click')
    this.$nuxt.$off('AppBarExtension:change')
  }

  get isInEditMode (): boolean {
    return this.editMode
  }

  save () {
    this.toggleEditMode()
  }

  set isInEditMode (editMode: boolean) {
    this.editMode = editMode
  }

  @Watch('editMode', { immediate: true, deep: true })
  // @ts-ignore
  onEditModeChanged (editMode: boolean) {
    this.$nuxt.$emit('AppBarContent:save-button-hidden', !editMode)
    this.$nuxt.$emit('AppBarContent:cancel-button-hidden', !editMode)
  }

  toggleEditMode () {
    this.isInEditMode = !this.isInEditMode
  }

  get readonly () {
    return !this.isInEditMode
  }

  get location (): number[] {
    return [
      this.longitude,
      this.latitude
    ]
  }

  /**
   * returns whether a node is a PlatformNode or not
   *
   * @param {Node} node - the node to check for
   * @return {boolean} true if the node is a PlatformNode
   */
  nodeIsPlatform (node: Node): boolean {
    return node instanceof PlatformNode
  }

  get breadcrumbs (): Object[] {
    if (!this.selectedNodeIds.length) {
      return []
    }
    const nodeId = this.selectedNodeIds[0]
    return this.getNodePath(nodeId).map((t: string): Object => { return { text: t } })
  }

  /**
   * returns the path in the tree to the node
   *
   * @param {number} nodeId - the node to get the path for
   * @return {string[]} an array of node names
   */
  getNodePath (nodeId: number): string[] {
    const getNodePathRecursive = (nodeId: number, nodes: Node[], path: string[]): boolean => {
      for (const node of nodes) {
        if (node.id === nodeId) {
          path.push(node.name)
          return true
        }
        if (!node.canHaveChildren()) {
          continue
        }
        if (getNodePathRecursive(nodeId, (node as PlatformNode).getChildren(), path)) {
          path.unshift(node.name)
          return true
        }
      }
      return false
    }

    const paths: string[] = []
    getNodePathRecursive(nodeId, this.tree, paths)
    return paths
  }

  /**
   * finds a node in the tree by its id
   *
   * @param {number} nodeId - the id of the node to search
   * @return {Node|null} the found node, null if it was not found
   */
  getNodeById (nodeId: number): Node | null {
    const getNodeByIdRecursive = (nodeId: number, nodes: Node[]): Node | null => {
      for (const node of nodes) {
        if (node.id === nodeId) {
          return node
        }
        if (!node.canHaveChildren()) {
          continue
        }
        const found = getNodeByIdRecursive(nodeId, (node as PlatformNode).getChildren())
        if (!found) {
          continue
        }
        return found
      }
      return null
    }
    return getNodeByIdRecursive(nodeId, this.tree)
  }

  /**
   * returns the parent of a node in the tree
   *
   * @param {Node} node - the node to get the parent of
   * @return {Node|null} the parent of the node, null if the node has not parent
   */
  getParentNode (node: Node): Node | null {
    const getParentNodeRecursive = (node: Node, parentNode: Node | null, nodes: Node[]): Node | null => {
      for (const aNode of nodes) {
        if (node === aNode) {
          return parentNode
        }
        if (!aNode.canHaveChildren()) {
          continue
        }
        const found = getParentNodeRecursive(node, aNode, (aNode as PlatformNode).getChildren())
        if (!found) {
          continue
        }
        return found
      }
      return null
    }
    return getParentNodeRecursive(node, null, this.tree)
  }

  /**
   * returns whether a node is in the tree or not
   *
   * @param {number} nodeId - the id of the node
   * @return {boolean} wheter the node was found or not
   */
  isNodeInTree (nodeId: number): boolean {
    return !!this.getNodeById(nodeId)
  }

  /**
   * returns the selected node in the tree
   *
   * @return {Node|null} the selected node
   */
  getSelectedNode (): Node | null {
    if (!this.selectedNodeIds.length) {
      return null
    }
    return this.getNodeById(this.selectedNodeIds[0])
  }

  /**
   * sets the selected node in the tree
   *
   * @param {Node|null} node - the node to select
   */
  setSelectedNode (node: Node | null) {
    if (node) {
      const id = node.unpack().id
      if (id) {
        this.selectedNodeIds = [id]
      }
    } else {
      this.selectedNodeIds = []
    }
  }

  get platforms (): Platform[] {
    return this.platformsResult
  }

  set platforms (platforms: Platform[]) {
    this.platformsResult = platforms
    if (platforms.length) {
      this.devicesResult = [] as Device[]
    }
  }

  get devices (): Device[] {
    return this.devicesResult
  }

  set devices (devices: Device[]) {
    this.devicesResult = devices
    if (devices.length) {
      this.platformsResult = [] as Platform[]
    }
  }

  /**
   * adds a PlatformNode to the tree
   *
   * @param {Platform} platform - the node to add
   */
  addPlatformNode (platform: Platform) {
    const node: Node | null = this.getSelectedNode()
    if (!node) {
      this.tree.push(
        new PlatformNode(platform)
      )
      return
    }

    if (!node.canHaveChildren()) {
      throw new Error('selected node-type cannot have children')
    }

    (node as PlatformNode).setChildren(
      [
        ...(node as PlatformNode).getChildren(),
        new PlatformNode(platform)
      ]
    )
  }

  /**
   * adds a DeviceNode to the tree
   *
   * @param {Device} device - the node to add
   */
  addDeviceNode (device: Device) {
    const node: Node | null = this.getSelectedNode()
    if (!node) {
      this.tree.push(
        new DeviceNode(device)
      )
      return
    }

    if (!node.canHaveChildren()) {
      throw new Error('selected node-type cannot have children')
    }

    (node as PlatformNode).setChildren(
      [
        ...(node as PlatformNode).getChildren(),
        new DeviceNode(device)
      ]
    )
  }

  /**
   * removes a node from the tree
   *
   * @param {Node} node - the node to remove
   * @return {boolean} whether the node was removed or not
   */
  removeNode (node: Node): boolean {
    const removeNodeRecursive = (node: Node, nodes: Node[]): boolean => {
      for (let i: number = 0; i < nodes.length; i++) {
        const aNode: Node = nodes[i]
        if (aNode === node) {
          nodes.splice(i, 1)
          return true
        }
        if (!aNode.canHaveChildren()) {
          continue
        }
        const removed = removeNodeRecursive(node, (aNode as PlatformNode).getChildren())
        if (!removed) {
          continue
        }
        return true
      }
      return false
    }
    return removeNodeRecursive(node, this.tree)
  }

  /**
   * removes the selected node
   */
  removeSelectedNode () {
    const node: Node | null = this.getSelectedNode()
    if (!node) {
      return
    }
    const parentNode = this.getParentNode(node)
    this.removeNode(node)
    this.setSelectedNode(parentNode)
  }

  /**
   * searches for platforms or devices depending on the searchType
   *
   * @async
   */
  async search () {
    switch (this.searchOptions.searchType) {
      case SearchType.Platform:
        this.platforms = await SmsService.findPlatforms(
          this.searchOptions.text,
          [] as Manufacturer[]
        )
        break
      case SearchType.Device:
        this.devices = await SmsService.findDevices(
          this.searchOptions.text,
          [] as Manufacturer[]
        )
        break
      default:
        throw new TypeError('search function not defined for unknown value')
    }
  }

  @Watch('selectedNodeIds')
  onItemSelect () {
    const node: Node | null = this.getSelectedNode()
    if (!node) {
      this.selectedPlatform = null
      this.selectedDevice = null
      return
    }
    switch (true) {
      case node instanceof PlatformNode:
        this.selectedPlatform = node.unpack() as Platform
        this.selectedDevice = null
        break
      case node instanceof DeviceNode:
        this.selectedDevice = node.unpack() as Device
        this.selectedPlatform = null
        break
    }
  }

  getDemoTree (): Array<Node> {
    return [
      ((): PlatformNode => {
        const n = new PlatformNode(
          ((): Platform => {
            const o = new Platform()
            o.id = -1
            o.shortName = 'Platform 01'
            o.longName = 'Platform 01 Bla blub'
            o.description = 'A platform on which various light instruments can be mounted. Consists of wood, dry and rotten wood.'
            return o
          })()
        )
        n.setChildren(
          [
            ((): PlatformNode => {
              const n = new PlatformNode(
                ((): Platform => {
                  const o = new Platform()
                  o.id = -2
                  o.shortName = 'Platform 02'
                  return o
                })()
              )
              n.setChildren(
                [
                  new DeviceNode(
                    ((): Device => {
                      const o = new Device()
                      o.id = -3
                      o.shortName = 'Device 01'
                      return o
                    })()
                  ),
                  new DeviceNode(
                    ((): Device => {
                      const o = new Device()
                      o.id = -4
                      o.shortName = 'Device 02'
                      return o
                    })()
                  ),
                  new DeviceNode(
                    ((): Device => {
                      const o = new Device()
                      o.id = -5
                      o.shortName = 'Device 03'
                      return o
                    })()
                  )
                ]
              )
              return n
            })()
          ]
        )
        return n
      })(),
      new PlatformNode(
        ((): Platform => {
          const o = new Platform()
          o.id = -6
          o.shortName = 'Platform 03'
          return o
        })()
      )
    ]
  }
}
</script>
