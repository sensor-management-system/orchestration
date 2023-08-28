<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <v-dialog
    v-if="!isLoading"
    v-model="showDialog"
    max-width="600px"
    persistent
  >
    <v-card>
      <v-card-title class="headline">
        User agreement
      </v-card-title>
      <v-card-text>
        <p>
          To be able to contribute to the Sensor Management System, we
          need to know that you agree to our Terms Of Use and that you read the
          Privacy Statement.
          Please check all of the points below to proceed:
        </p>
        <v-checkbox v-model="willAcceptTermsOfUse" dense>
          <template #label>
            I agree to the&nbsp;
            <a href="/info/terms-of-use" target="_blank" @click.stop>
              Terms of Use
            </a>.
          </template>
        </v-checkbox>
        <v-checkbox v-model="willAcceptPrivacyPolicy" dense>
          <template #label>
            I read the&nbsp;
            <a href="/info/privacy-policy" target="_blank" @click.stop>
              Privacy Statement
            </a>.
          </template>
        </v-checkbox>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="logout">
          Logout
        </v-btn>
        <v-btn color="primary" :disabled="!acceptAll" @click="sendAccept">
          OK
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'

import { SetLoadingAction } from '@/store/progressindicator'

import { AcceptTermsOfUseAction } from '@/store/permissions'

@Component({
  computed: {
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('permissions', ['acceptTermsOfUse']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class TermsOfUseAcceptanceDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  private willAcceptTermsOfUse = false
  private willAcceptPrivacyPolicy = false

  get acceptAll (): boolean {
    return this.willAcceptTermsOfUse && this.willAcceptPrivacyPolicy
  }

  acceptTermsOfUse!: AcceptTermsOfUseAction
  setLoading!: SetLoadingAction

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (newValue: boolean) {
    this.$emit('input', newValue)
  }

  async sendAccept () {
    this.setLoading(true)
    this.showDialog = false
    try {
      await this.acceptTermsOfUse()
      this.$store.commit('snackbar/setSuccess', 'Accepted the terms of use.')
    } catch {
      this.$store.commit('snackbar/setError', 'Accepting the terms of use failed.')
    } finally {
      this.setLoading(false)
    }
  }

  logout () {
    this.showDialog = false
    this.$emit('logout')
  }

  routerLink (internalLink: string) {
    this.$router.getRoutes()
    return (this.$router.options.base || '/') + internalLink
  }
}
</script>
