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
                        <v-btn text color="primary" @click="startDateModal = false">Cancel</v-btn>
                        <v-btn text color="primary" @click="$refs.startDateDialog.save(startDate)">OK</v-btn>
                      </v-date-picker>
                    </v-dialog>
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-dialog
                      ref="endDateDialog"
                      v-model="endDateModal" :return-value.sync="endDate"
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
                        <v-btn text color="primary" @click="endDateModal = false">Cancel</v-btn>
                        <v-btn text color="primary" @click="$refs.endDateDialog.save(endDate)">OK</v-btn>
                      </v-date-picker>
                    </v-dialog>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" md="3">
                    <v-select
                      :items="['Stationary', 'Dynamic']"
                      label="Location type"
                      v-model="locationType"
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
                    <ContactSelect :selected-contacts.sync="contacts" :readonly="false" />
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
                  <v-col cols="6">
                    <v-treeview
                      :active.sync="selectedConfigurationItem"
                      :items="configurationItems"
                      :activatable="true"
                      :hoverable="true"
                      :rounded="true"
                      open-all
                    >
                      <template v-slot:prepend="{ item }">
                        <v-icon v-if="isPlatform(item)">
                          mdi-rocket-outline
                        </v-icon>
                        <v-icon v-else>
                          mdi-network-outline
                        </v-icon>
                      </template>
                    </v-treeview>
                  </v-col>
                  <v-col cols="6" md="6">
                    <v-breadcrumbs :items="breadcrumbs" divider=">" />
                    <v-row v-if="selectedPlatform">
                      <v-col cols="12" md="10">
                        <template v-if="selectedPlatform.description">
                          {{ selectedPlatform.description }}
                        </template>
                        <template v-else>
                          The selected platform has no description.
                        </template>
                      </v-col>
                      <v-col cols="12" md="2">
                        <v-btn
                          color="secondary"
                        >
                          remove
                        </v-btn>
                      </v-col>
                    </v-row>
                    <v-row v-else>
                      Add platforms and / or devices on the left side to the configuration.<br>
                      Select a platform to add platforms / or devices to the selected platform.
                    </v-row>
                    <v-row>
                      <v-col cols="12" md="3">
                        <v-select
                          :items="['Platforms', 'Devices']"
                          label="Type"
                        />
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          label="Name"
                        />
                      </v-col>
                      <v-col cols="12" md="3">
                        <v-btn
                          color="primary"
                        >
                          search
                        </v-btn>
                      </v-col>
                    </v-row>
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

type Node = DeviceNode|PlatformNode

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

  private selectedConfigurationItemId: number[] = []
  private selectedPlatform: Platform | null = null

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

  get configurationItems (): Array<Node> {
    return [
      ((): PlatformNode => {
        const n = new PlatformNode(
          ((): Platform => {
            const o = new Platform()
            o.id = 1
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
                  o.id = 2
                  o.shortName = 'Platform 02'
                  return o
                })()
              )
              n.setChildren(
                [
                  new DeviceNode(
                    ((): Device => {
                      const o = new Device()
                      o.id = 3
                      o.shortName = 'Device 01'
                      return o
                    })()
                  ),
                  new DeviceNode(
                    ((): Device => {
                      const o = new Device()
                      o.id = 4
                      o.shortName = 'Device 02'
                      return o
                    })()
                  ),
                  new DeviceNode(
                    ((): Device => {
                      const o = new Device()
                      o.id = 5
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
          o.id = 6
          o.shortName = 'Platform 03'
          return o
        })()
      )
    ]
  }

  isPlatform (node: Node): boolean {
    return node instanceof PlatformNode
  }

  get breadcrumbs (): Object[] {
    const root = { text: 'Configuration' }
    if (!this.selectedConfigurationItemId.length) {
      return [root, { text: 'No platform selected' }]
    }
    const nodeId = this.selectedConfigurationItemId[0]
    const nodeNames = this.getNodePath(nodeId).map((t: string): Object => { return { text: t } })
    return [
      root,
      ...nodeNames
    ]
  }

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
    getNodePathRecursive(nodeId, this.configurationItems, paths)
    return paths
  }

  getNode (nodeId: number): Node | null {
    const getNodeRecursive = (nodeId: number, nodes: Node[]): Node | null => {
      for (const node of nodes) {
        if (node.id === nodeId) {
          return node
        }
        if (!node.canHaveChildren()) {
          continue
        }
        const found = getNodeRecursive(nodeId, (node as PlatformNode).getChildren())
        if (!found) {
          continue
        }
        return found
      }
      return null
    }
    return getNodeRecursive(nodeId, this.configurationItems)
  }

  @Watch('selectedConfigurationItemId')
  onItemSelect (val: number[]) {
    if (val.length) {
      const node: Node | null = this.getNode(val[0])
      this.selectedPlatform = node ? node.unpack() as Platform : null
    } else {
      this.selectedPlatform = null
    }
  }
}
</script>
