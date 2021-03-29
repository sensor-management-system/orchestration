<template>
  <div>
    <ProgressIndicator
      v-model="isLoading"
      dark
    />
    <v-card
      flat
    >
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="isLoggedIn"
          small
          text
          nuxt
          to="/search/platforms"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="isLoggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          create
        </v-btn>
      </v-card-actions>
      <PlatformBasicDataForm
        ref="basicForm"
        v-model="platform"
      />
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-if="isLoggedIn"
          small
          text
          nuxt
          to="/search/platforms"
        >
          cancel
        </v-btn>
        <v-btn
          v-if="isLoggedIn"
          color="green"
          small
          @click="onSaveButtonClicked"
        >
          create
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { Platform } from '@/models/Platform'

import ProgressIndicator from '@/components/ProgressIndicator.vue'
import PlatformBasicDataForm from '@/components/PlatformBasicDataForm.vue'

@Component({
  components: {
    PlatformBasicDataForm,
    ProgressIndicator
  }
})
// @ts-ignore
export default class PlatformNewPage extends mixins(Rules) {
  private numberOfTabs: number = 1

  private platform: Platform = new Platform()
  private isLoading: boolean = false

  mounted () {
    this.initializeAppBar()
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }

  onSaveButtonClicked (): void {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    if (!this.isLoggedIn) {
      this.$store.commit('snackbar/setError', 'You need to be logged in to save the platform')
      return
    }
    this.isLoading = true
    this.$api.platforms.save(this.platform).then((savedPlatform) => {
      this.isLoading = false
      this.$store.commit('snackbar/setSuccess', 'Platform created')
      this.$router.push('/platforms/' + savedPlatform.id + '')
    }).catch((_error) => {
      this.isLoading = false
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  initializeAppBar () {
    this.$store.dispatch('appbar/init', {
      tabs: [
        {
          to: '/platforms/new',
          name: 'Basic Data'
        },
        {
          name: 'Contacts',
          disabled: true
        },
        {
          name: 'Attachments',
          disabled: true
        }
      ],
      title: 'Add Platform'
    })
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }
}
</script>
