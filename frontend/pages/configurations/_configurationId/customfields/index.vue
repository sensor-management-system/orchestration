<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions
      v-if="editable"
    >
      <v-spacer />
      <v-btn
        color="primary"
        small
        :to="'/configurations/' + configurationId + '/customfields/new'"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
    <hint-card v-if="configurationCustomFields.length === 0">
      There are no custom fields for this configuration.
    </hint-card>
    <BaseList
      :list-items="configurationCustomFields"
    >
      <template #list-item="{item}">
        <CustomFieldListItem
          :value="item"
          :editable="editable"
          :to="'/configurations/' + configurationId + '/customfields/' + item.id + '/edit'"
        >
          <template #dot-menu-items>
            <DotMenuActionDelete
              :readonly="!editable"
              @click="initDeleteDialog(item)"
            />
          </template>
        </CustomFieldListItem>
      </template>
    </BaseList>
    <v-card-actions
      v-if="configurationCustomFields.length > 3"
    >
      <v-spacer />
      <v-btn
        v-if="editable"
        color="primary"
        small
        :to="'/configurations/' + configurationId + '/customfields/new'"
      >
        Add Custom Field
      </v-btn>
    </v-card-actions>
    <DeleteDialog
      v-if="customFieldToDelete"
      v-model="showDeleteDialog"
      title="Delete Custom Field"
      :disabled="isLoading"
      @cancel="closeDialog"
      @delete="deleteAndCloseDialog"
    >
      Do you really want to delete the field &quot;<em>{{ customFieldToDelete.key | shortenRight }}</em>&quot;?
    </DeleteDialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { DeleteConfigurationCustomFieldAction, ConfigurationsState, LoadConfigurationCustomFieldsAction } from '@/store/configurations'

import { CustomTextField } from '@/models/CustomTextField'

import BaseList from '@/components/shared/BaseList.vue'
import CustomFieldListItem from '@/components/shared/CustomFieldListItem.vue'
import DotMenuActionDelete from '@/components/DotMenuActionDelete.vue'
import DeleteDialog from '@/components/shared/DeleteDialog.vue'
import HintCard from '@/components/HintCard.vue'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  components: { HintCard, DeleteDialog, DotMenuActionDelete, CustomFieldListItem, BaseList },
  computed: {
    ...mapState('configurations', ['configurationCustomFields']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('configurations', ['deleteConfigurationCustomField', 'loadConfigurationCustomFields']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationCustomFieldsShowPage extends Vue {
  @InjectReactive()
    editable!: boolean

  private showDeleteDialog = false
  private customFieldToDelete: CustomTextField | null = null

  // vuex definition for typescript check
  configurationCustomFields!: ConfigurationsState['configurationCustomFields']
  loadConfigurationCustomFields!: LoadConfigurationCustomFieldsAction
  deleteConfigurationCustomField!: DeleteConfigurationCustomFieldAction
  setLoading!: SetLoadingAction

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  initDeleteDialog (customField: CustomTextField) {
    this.showDeleteDialog = true
    this.customFieldToDelete = customField
  }

  closeDialog () {
    this.showDeleteDialog = false
    this.customFieldToDelete = null
  }

  async deleteAndCloseDialog () {
    if (this.customFieldToDelete === null || this.customFieldToDelete.id === null) {
      return
    }
    try {
      this.setLoading(true)
      await this.deleteConfigurationCustomField(this.customFieldToDelete.id)
      this.loadConfigurationCustomFields(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Custom field deleted')
    } catch (_error) {
      this.$store.commit('snackbar/setError', 'Failed to delete custom field')
    } finally {
      this.setLoading(false)
      this.closeDialog()
    }
  }
}
</script>
