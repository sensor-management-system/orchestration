<template>
  <div>
    <ProgressIndicator
      v-model="isInProgress"
      :dark="isSaving"
    />
    <v-card-actions>
      <v-spacer/>
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
            <v-card>
              <v-card-title>Submit unmount form</v-card-title>
              <v-container>
                <ConfigurationsSelectedItemUnmountForm
                  v-if="selectedNode"
                  :node="selectedNode"
                  :contacts="contacts"
                  :current-user-mail="currentUserMail"
                  @unmount="unmount"
                />
              </v-container>
            </v-card>
          </div>
        </v-slide-x-reverse-transition>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { DateTime } from 'luxon'
import DateTimePicker from '@/components/DateTimePicker.vue'
import { mapActions, mapGetters, mapState } from 'vuex'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { buildConfigurationTree } from '@/modelUtils/mountHelpers'
import ConfigurationsTreeView from '@/components/ConfigurationsTreeView.vue'
import ConfigurationsSelectedItemUnmountForm from '@/components/ConfigurationsSelectedItemUnmountForm.vue'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { Device } from '@/models/Device'
import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
@Component({
  components: { ProgressIndicator, ConfigurationsSelectedItemUnmountForm, ConfigurationsTreeView, DateTimePicker },
  middleware:['auth'],
  computed:{
    ...mapGetters('configurations',['mountingActionsDates']),
    ...mapState('configurations',['configuration']),
    ...mapState('contacts',['contacts'])
  },
  methods:{
    ...mapActions('contacts',['loadAllContacts']),
    ...mapActions('configurations',['addDeviceUnMountAction','addPlatformUnMountAction','loadConfiguration'])
  }
})
export default class ConfigurationUnMountPlatformsAndDevicesPage extends Vue {
  private selectedDate = DateTime.utc()
  private selectedNode: ConfigurationsTreeNode | null = null

  private isSaving = false
  private isLoading = false

  async created(){
    try {
      this.isLoading=true
      await this.loadAllContacts()
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch contacts')
    } finally {
      this.isLoading=false
    }
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
    return tree.toArray()
  }

  get isInProgress (): boolean {
    return this.isLoading || this.isSaving
  }

  get currentUserMail (): string | null {
    if (this.$auth.user && this.$auth.user.email) {
      return this.$auth.user.email as string
    }
    return null
  }

  unmount({contact,description}){
    if(!this.selectedNode || !this.selectedDate){
      return
    }

    if(this.selectedNode.isDevice()){
      this.unmountDevice(this.selectedNode.unpack().device,contact,description)
    }
    if(this.selectedNode.isPlatform()){
      this.unmountPlatform(this.selectedNode.unpack().platform,contact,description)
    }
  }

  async unmountDevice(device:Device,contact:Contact,description:string){
    const newDeviceUnmountAction = DeviceUnmountAction.createFromObject({
      id: '',
      device: device,
      date: this.selectedDate,
      contact: contact,
      description: description
    })

    try {
      this.isSaving=true
      await this.addDeviceUnMountAction({
        configurationId: this.configurationId,
        deviceUnMountAction: newDeviceUnmountAction
      })
      this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add device unmount action')
    }finally {
      this.isSaving=false
    }
  }
  async unmountPlatform(platform:Platform,contact:Contact,description:string){
    const newPlatformUnmountAction = PlatformUnmountAction.createFromObject({
      id: '',
      platform: platform,
      date: this.selectedDate,
      contact: contact,
      description: description
    })

    try {
      this.isSaving=true
      await this.addPlatformUnMountAction({
        configurationId: this.configurationId,
        platformUnMountAction: newPlatformUnmountAction
      })
      this.loadConfiguration(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Save successful')
      this.$router.push('/configurations/' + this.configurationId + '/platforms-and-devices')
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to add device unmount action')
    }finally {
      this.isSaving=true
    }
  }
}
</script>

<style scoped>

</style>
