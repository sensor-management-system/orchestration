<!--
SPDX-FileCopyrightText: 2026
- Nils Brinckmann <nils.brinckmann@gfz.de>
- GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <nuxt-child
        v-if="organization"
      />
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, ProvideReactive, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { LoadOrganizationAction, OrganizationsState } from '@/store/organizations'
import { SetLoadingAction } from '@/store/progressindicator'
import { SetShowBackButtonAction, SetTabsAction, SetTitleAction } from '@/store/appbar'
import { CanDeleteOrganizationGetter, CanModifyOrganizationGetter } from '@/store/permissions'

@Component({
  computed: {
    ...mapState('organizations', ['organization']),
    ...mapGetters('permissions', ['canModifyOrganization', 'canDeleteOrganization'])
  },
  methods: {
    ...mapActions('organizations', ['loadOrganization']),
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('appbar', ['setShowBackButton', 'setTabs', 'setTitle'])
  }
})
export default class OrganizationPage extends Vue {
  @ProvideReactive()
    editable: boolean = false

  @ProvideReactive()
    deletable: boolean = false

  organization!: OrganizationsState['organization']
  loadOrganization!: LoadOrganizationAction
  setLoading!: SetLoadingAction
  setShowBackButton!: SetShowBackButtonAction
  setTabs!: SetTabsAction
  setTitle!: SetTitleAction
  canModifyOrganization!: CanModifyOrganizationGetter
  canDeleteOrganization!: CanDeleteOrganizationGetter

  mounted () {
    this.initializeAppBar()
  }

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await this.loadOrganization({ organizationId: this.organizationId })
      this.updatePermissions(this.organization)
      if (this.isBasePath()) {
        this.$router.replace('/organizations/' + this.organizationId + '/basic')
      }
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading of organization failed')
    } finally {
      this.setLoading(false)
    }
  }

  get organizationId (): string {
    return this.$route.params.organizationId
  }

  isBasePath () {
    return this.$route.path === '/organizations/' + this.organizationId || this.$route.path === '/organizations/' + this.organizationId + '/'
  }

  initializeAppBar () {
    if ('from' in this.$route.query && this.$route.query.from === 'searchResult') {
      this.setShowBackButton(true)
    }
    this.setTabs([])
    if (this.organization) {
      this.setTitle(this.organization.name)
    }
  }

  updatePermissions (organization: OrganizationsState['organization']) {
    if (organization) {
      this.editable = this.canModifyOrganization(organization)
      this.deletable = this.canDeleteOrganization(organization)
    }
  }

  @Watch('organization', { immediate: true, deep: true })
  onOrganizationChange (val: OrganizationsState['organization']) {
    if (val) {
      this.setTitle(val.name)
      this.updatePermissions(val)
    }
  }
}
</script>
