<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/platforms/' + platformId + '/parameters'"
          @save="save"
        />
        <v-btn
          class="ml-1"
          color="accent darken-3"
          small
          @click="saveAndRedirectToAddValue"
        >
          Add & Set Value
        </v-btn>
      </v-card-actions>
      <v-card-text>
        <parameter-form
          ref="parameterForm"
          v-model="value"
          :units="units"
          auto-completion-endpoint="platform-parameter-labels"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <SaveAndCancelButtons
          save-btn-text="Add"
          :to="'/platforms/' + platformId + '/parameters'"
          @save="save"
        />
        <v-btn
          class="ml-1"
          color="accent darken-3"
          small
          @click="saveAndRedirectToAddValue"
        >
          Add & Set Value
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-subheader
      v-if="platformParametersSortedAlphabetically.length > 0"
    >
      Existing parameters
    </v-subheader>
    <BaseList
      :list-items="platformParametersSortedAlphabetically"
    >
      <template #list-item="{item,index}">
        <ParameterListItem
          :value="item"
          :index="index"
          :parameter-change-actions="platformParameterChangeActions"
        />
      </template>
    </BaseList>
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import {
  AddPlatformParameterAction,
  PlatformsState,
  LoadPlatformParametersAction, SetPlatformPresetParameterAction, SetChosenKindOfPlatformActionAction
} from '@/store/platforms'
import { VocabularyState } from '@/store/vocabulary'

import { Parameter } from '@/models/Parameter'

import BaseList from '@/components/shared/BaseList.vue'
import ParameterForm from '@/components/shared/ParameterForm.vue'
import ParameterListItem from '@/components/shared/ParameterListItem.vue'
import { SetLoadingAction } from '@/store/progressindicator'
import SaveAndCancelButtons from '@/components/shared/SaveAndCancelButtons.vue'
import { platformParameterChangeActionOption } from '@/models/ActionKind'

@Component({
  middleware: ['auth'],
  components: {
    BaseList,
    ParameterForm,
    ParameterListItem,
    SaveAndCancelButtons
  },
  computed: {
    ...mapState('vocabulary', ['units']),
    ...mapState('platforms', ['platformParameterChangeActions']),
    ...mapGetters('platforms', ['platformParametersSortedAlphabetically'])
  },
  methods: {
    ...mapActions('platforms', ['addPlatformParameter', 'loadPlatformParameters', 'setPlatformPresetParameter', 'setChosenKindOfPlatformAction']),
    ...mapActions('progressindicator', ['setLoading'])
  },
  scrollToTop: true
})
export default class ParametersAddPage extends mixins(CheckEditAccess) {
  private value: Parameter = new Parameter()

  // vuex definition for typescript check
  units!: VocabularyState['units']
  platformParametersSortedAlphabetically!: PlatformsState['platformParameters']
  platformParameterChangeActions!: PlatformsState['platformParameterChangeActions']
  addPlatformParameter!: AddPlatformParameterAction
  loadPlatformParameters!: LoadPlatformParametersAction
  setLoading!: SetLoadingAction
  setPlatformPresetParameter!: SetPlatformPresetParameterAction
  setChosenKindOfPlatformAction!: SetChosenKindOfPlatformActionAction

  mounted () {
    (this.$refs.parameterForm as ParameterForm).focus()
  }

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/platforms/' + this.platformId + '/parameters'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this platform.'
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  private async _save (callback: (newParameter: Parameter) => void | (() => void)) {
    if (!(this.$refs.parameterForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }

    try {
      this.setLoading(true)
      const newParameter = await this.addPlatformParameter({
        platformId: this.platformId,
        parameter: this.value
      })

      this.$store.commit('snackbar/setSuccess', 'New parameter has been added')

      callback(newParameter)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to save parameter')
    } finally {
      this.setLoading(false)
    }
  }

  save () {
    this._save(() => {
      this.loadPlatformParameters(this.platformId)
      this.$router.push('/platforms/' + this.platformId + '/parameters')
    })
  }

  saveAndRedirectToAddValue () {
    this._save(
      (newParameter: Parameter) => {
        this.setPlatformPresetParameter(newParameter)
        this.setChosenKindOfPlatformAction(platformParameterChangeActionOption)
        this.$router.push('/platforms/' + this.platformId + '/actions/new/parameter-change-actions')
      }
    )
  }
}
</script>
