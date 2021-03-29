<template>
  <div>
    <ProgressIndicator
      v-model="isLoading"
      dark
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        :to="'/platforms/' + platformId + '/basic'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click="onSaveButtonClicked"
      >
        apply
      </v-btn>
    </v-card-actions>
    <PlatformBasicDataForm
      ref="basicForm"
      v-model="platformCopy"
    />
    <v-card-actions>
      <v-spacer />
      <v-btn
        v-if="isLoggedIn"
        small
        text
        nuxt
        :to="'/platforms/' + platformId + '/basic'"
      >
        cancel
      </v-btn>
      <v-btn
        v-if="isLoggedIn"
        color="green"
        small
        @click="onSaveButtonClicked"
      >
        apply
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'nuxt-property-decorator'

import PlatformBasicDataForm from '@/components/PlatformBasicDataForm.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'

import { Platform } from '@/models/Platform'

@Component({
  components: {
    PlatformBasicDataForm,
    ProgressIndicator
  }
})
export default class PlatformEditBasicPage extends Vue {
  // we need to initialize the instance variable with an empty Platform instance
  // here, otherwise the form is not reactive
  private platformCopy: Platform = new Platform()

  private isLoading: boolean = false

  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Platform

  created () {
    this.platformCopy = Platform.createFromObject(this.value)
  }

  onSaveButtonClicked () {
    if (!(this.$refs.basicForm as Vue & { validateForm: () => boolean }).validateForm()) {
      this.$store.commit('snackbar/setError', 'Please correct your input')
      return
    }
    this.isLoading = true
    this.save().then((platform) => {
      this.isLoading = false
      this.$emit('input', platform)
      this.$router.push('/platforms/' + this.platformId + '/basic')
    }).catch((_error) => {
      this.isLoading = false
      this.$store.commit('snackbar/setError', 'Save failed')
    })
  }

  save (): Promise<Platform> {
    return new Promise((resolve, reject) => {
      this.$api.platforms.save(this.platformCopy).then((savedPlatform) => {
        resolve(savedPlatform)
      }).catch((_error) => {
        reject(_error)
      })
    })
  }

  get platformId () {
    return this.$route.params.platformId
  }

  get isLoggedIn () {
    return this.$store.getters['oidc/isAuthenticated']
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onPlatformChanged (val: Platform) {
    this.platformCopy = Platform.createFromObject(val)
  }
}
</script>
