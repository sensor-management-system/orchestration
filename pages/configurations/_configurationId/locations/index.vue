<template>
  <div>
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
          v-model="selectedAction"
          :item-text="(x) => x.text"
          :items="locationActionsDates"
          label="Dates defined by actions"
          hint="The referenced time zone is UTC."
          @input="updateDate"
          return-object
          persistent-hint
        />
      </v-col>
    </v-row>
    <v-row v-if="selectedAction && selectedAction.value">
      <v-col>
        <v-card>
          <v-container>
            <ConfigurationStaticLocationBeginActionData
              v-if="isStaticLocationStartAction"
              :value="selectedAction.value"
              :elevation-data="[]"
              :epsg-codes="[]"
            />
            <ConfigurationStaticLocationEndActionData
              v-if="isStaticLocationEndAction"
              :value="selectedAction.value"
            />
            <ConfigurationDynamicLocationBeginActionData
              v-if="isDynamicLocationStartAction"
              :value="selectedAction.value"
              :epsg-codes="[]"
              :elevation-data="[]"
              :devices="[]"
            />
            <ConfigurationDynamicLocationEndActionData
              v-if="isDynamicLocationEndAction"
              :value="selectedAction.value"
            />
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { LocationTypes } from '@/store/configurations'
import { Component, Vue } from 'vue-property-decorator'
import { mapGetters } from 'vuex'
import { DateTime } from 'luxon'
import DateTimePicker from '@/components/DateTimePicker.vue'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'
import ConfigurationStaticLocationBeginActionData
  from '@/components/configurations/ConfigurationStaticLocationBeginActionData.vue'
import ConfigurationStaticLocationEndActionData
  from '@/components/configurations/ConfigurationStaticLocationEndActionData.vue'
import ConfigurationDynamicLocationBeginActionData
  from '@/components/configurations/ConfigurationDynamicLocationBeginActionData.vue'
import ConfigurationDynamicLocationEndActionData
  from '@/components/configurations/ConfigurationDynamicLocationEndActionData.vue'

@Component({
  components: { ConfigurationDynamicLocationEndActionData, ConfigurationDynamicLocationBeginActionData, ConfigurationStaticLocationEndActionData, ConfigurationStaticLocationBeginActionData, DateTimePicker },
  computed:mapGetters('configurations',['locationActionsDates'])
})
export default class ConfigurationShowLocationPage extends Vue {
  private selectedDate = DateTime.utc()

  private selectedAction:StaticLocationBeginAction|StaticLocationEndAction|DynamicLocationBeginAction|DynamicLocationEndAction|null=null

  updateDate(val){
    this.selectedDate=val.date;
  }

  get isStaticLocationStartAction(){
    if(this.selectedAction && this.selectedAction.type){
      return this.selectedAction.type === LocationTypes.staticStart
    }
    return false
  }
  get isStaticLocationEndAction(){
    if(this.selectedAction && this.selectedAction.type){
      return this.selectedAction.type === LocationTypes.staticEnd
    }
    return false
  }
  get isDynamicLocationStartAction(){
    if(this.selectedAction && this.selectedAction.type){
      return this.selectedAction.type === LocationTypes.dynamicStart
    }
    return false
  }
  get isDynamicLocationEndAction(){
    if(this.selectedAction && this.selectedAction.type){
      return this.selectedAction.type === LocationTypes.dynamicEnd
    }
    return false
  }
}
</script>

<style scoped>

</style>
