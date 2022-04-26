<template>
<div>
  <v-card-actions>
    <v-spacer />
    <v-btn
      v-if="$auth.loggedIn"
      small
      text
      nuxt
      :to="'/configurations/' + configurationId + '/platforms-and-devices'"
    >
      cancel
    </v-btn>
  </v-card-actions>
  <v-row justify="center">
      <v-col cols="12" md="6">
        <DateTimePicker
          v-model="selectedDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Configuration at date"
        />
      </v-col>
  </v-row>
  <v-row justify="center">
    <v-col cols="12" md="4">
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
    <v-col cols="12" md="8">
      <v-row>
        <v-col>
          <v-card>
            <v-toolbar
              color="grey"
              dark
              flat
            >
              <v-spacer></v-spacer>
              <v-toolbar-title>Search</v-toolbar-title>

              <v-spacer></v-spacer>

              <template v-slot:extension>
                <v-tabs
                  v-model="tab"
                  centered
                  slider-color="yellow"
                >
                  <v-tab>Platform</v-tab>
                  <v-tab>Device</v-tab>
                </v-tabs>
              </template>
            </v-toolbar>

            <v-tabs-items v-model="tab">
              <v-tab-item>
                <v-card>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          v-model="searchTextPlatforms"
                          label="Name"
                          placeholder="Name of platform"
                          hint="Please enter at least 3 characters"
                          @keydown.enter="searchPlatformsForMount"
                        />
                      </v-col>
                      <v-col
                        cols="12"
                        md="7"
                        align-self="center"
                      >
                        <v-btn
                          color="primary"
                          small
                          @click="searchPlatformsForMount"
                        >
                          Search
                        </v-btn>
                        <v-btn
                          text
                          small
                          @click="clearBasicSearchPlatforms"
                        >
                          Clear
                        </v-btn>
                      </v-col>
                    </v-row>
                    <div v-if="platforms.length>0">
                      <v-subheader>
                        <template v-if="platforms.length == 1">
                          1 device found
                        </template>
                        <template v-else>
                          {{ platforms.length }} platforms found
                        </template>
                        <v-spacer />
                      </v-subheader>
                      <BaseList
                        :list-items="platforms"
                      >
                        <template v-slot:list-item="{item}">
                          <PlatformMountListItem
                            :key="item.id"
                            :platform="item"
                          >
                            <template #mount>
                              <ConfigurationsPlatformDeviceMountForm
                                data-role-btn="add-platform"
                                :readonly="false"
                                :contacts="contacts"
                                :current-user-mail="currentUserMail"
                                @add="mountPlatform(item, $event)"
                              />
                            </template>
                          </PlatformMountListItem>
                        </template>
                      </BaseList>
                    </div>

                  </v-container>
                </v-card>
              </v-tab-item>
              <v-tab-item>
                <v-card>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          v-model="searchTextDevices"
                          label="Name"
                          placeholder="Name of device"
                          hint="Please enter at least 3 characters"
                          @keydown.enter="searchDevicesForMount"
                        />
                      </v-col>
                      <v-col
                        cols="12"
                        md="7"
                        align-self="center"
                      >
                        <v-btn
                          color="primary"
                          small
                          @click="searchDevicesForMount"
                        >
                          Search
                        </v-btn>
                        <v-btn
                          text
                          small
                          @click="clearBasicSearchDevices"
                        >
                          Clear
                        </v-btn>
                      </v-col>
                    </v-row>
                    <div v-if="devices.length>0">
                      <v-subheader>
                        <template v-if="devices.length == 1">
                          1 device found
                        </template>
                        <template v-else>
                          {{ devices.length }} devices found
                        </template>
                        <v-spacer />
                      </v-subheader>
                      <BaseList
                        :list-items="devices"
                      >
                        <template v-slot:list-item="{item}">
                          <DevicesMountListItem
                            :key="item.id"
                            :device="item"
                          >
                            <template #mount>
                              <ConfigurationsPlatformDeviceMountForm
                                data-role-btn="add-device"
                                :readonly="false"
                                :contacts="contacts"
                                :current-user-mail="currentUserMail"
                                @add="mountDevice(item, $event)"
                              />
                            </template>
                          </DevicesMountListItem>
                        </template>
                      </BaseList>
                    </div>
                  </v-container>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { DateTime } from 'luxon'
import { buildConfigurationTree, mountDevice } from '@/modelUtils/mountHelpers'
import { mapActions, mapGetters, mapState } from 'vuex'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'
import BaseList from '@/components/shared/BaseList.vue'
import DevicesListItem from '@/components/devices/DevicesListItem.vue'
import DevicesMountListItem from '@/components/devices/DevicesMountListItem.vue'
import ConfigurationsPlatformDeviceMountForm from '@/components/ConfigurationsPlatformDeviceMountForm.vue'
import { Device } from '@/models/Device'
import { Contact } from '@/models/Contact'
import { Configuration } from '@/models/Configuration'
import { Platform } from '@/models/Platform'
import { DeviceMountAction, IDeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import PlatformMountListItem from '@/components/platforms/PlatformMountListItem.vue'
import { PlatformMountAction } from '@/models/PlatformMountAction'

@Component({
  components: { PlatformMountListItem, ConfigurationsPlatformDeviceMountForm, DevicesMountListItem, DevicesListItem, BaseList, DateTimePicker, ConfigurationsTreeView },
  middleware:['auth'],
  computed:{
    ...mapGetters('configurations',['mountingActionsDates']),
    ...mapState('configurations',['configuration']),
    ...mapState('devices',['devices']),
    ...mapState('platforms',['platforms']),
    ...mapState('contacts',['contacts'])
  },
  methods:{
    ...mapActions('devices',['searchDevices']),
    ...mapActions('platforms',['searchPlatforms']),
    ...mapActions('configurations',['addDeviceMountAction','addPlatformMountAction','loadConfiguration']),
    ...mapActions('contacts',['loadAllContacts'])
  }
})
export default class ConfigurationAddPlatformsAndDevicesPage extends Vue {
  private loading = false
  private tab= null

  private searchTextPlatforms:string|null = null
  private searchTextDevices:string|null = null
  private selectedType:string|null =null
  private selectedNode: ConfigurationsTreeNode | null = null
  private selectedDate = DateTime.utc()

  async created(){
    await this.loadAllContacts()
  }

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
  get currentUserMail (): string | null {
    if (this.$auth.user && this.$auth.user.email) {
      return this.$auth.user.email as string
    }
    return null
  }


  setSelectedNode (node: ConfigurationsTreeNode) {
    this.selectedNode = node
  }
  clearBasicSearchPlatforms(){
    this.searchTextPlatforms=null
  }
  clearBasicSearchDevices(){
    this.searchTextPlatforms=null
  }

  async searchDevicesForMount(){
      await this.searchDevices({ searchText: this.searchTextDevices })
  }
  async searchPlatformsForMount(){
      await this.searchPlatforms({ searchText: this.searchTextPlatforms })
  }

  mountDevice(device,mountInfo){
    try {

      let parentPlatform = null;

      if(this.selectedNode && !this.selectedNode.canHaveChildren()){
        this.$store.commit('snackbar/setError', 'Selected node-type cannot have children')
        return
      }

      if (this.selectedNode && this.selectedNode.canHaveChildren()) {
        parentPlatform = (this.selectedNode as PlatformNode).unpack().platform
      }

      const newDeviceMountAction = DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform: parentPlatform,
        date: this.selectedDate,
        offsetX: mountInfo.offsetX,
        offsetY: mountInfo.offsetY,
        offsetZ: mountInfo.offsetZ,
        contact: mountInfo.contact,
        description: mountInfo.description
      })

      this.addDeviceMountAction({
        configurationId: this.configurationId,
        deviceMountAction: newDeviceMountAction
      })
      this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add device mount action')
    }
  }

  async mountPlatform(platform,mountInfo){
    try {

      let parentPlatform = null;

      if(this.selectedNode && !this.selectedNode.canHaveChildren()){
        this.$store.commit('snackbar/setError', 'Selected node-type cannot have children')
        return
      }

      if (this.selectedNode && this.selectedNode.canHaveChildren()) {
        parentPlatform = (this.selectedNode as PlatformNode).unpack().platform
      }

      const newPlatformMountAction = PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform: parentPlatform,
        date: this.selectedDate,
        offsetX: mountInfo.offsetX,
        offsetY: mountInfo.offsetY,
        offsetZ: mountInfo.offsetZ,
        contact: mountInfo.contact,
        description: mountInfo.description
      })

      await this.addPlatformMountAction({
        configurationId: this.configurationId,
        platformMountAction: newPlatformMountAction
      })
      this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add platform mount action')
    }
  }
}
</script>

<style scoped>

</style>
