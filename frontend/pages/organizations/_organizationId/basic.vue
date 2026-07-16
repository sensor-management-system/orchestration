<!--
SPDX-FileCopyrightText: 2026
- Nils Brinckmann <nils.brinckmann@gfz.de>
- GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <NuxtChild />
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class OrganizationBasicPage extends Vue {
  head () {
    return {
      titleTemplate: 'Basic Data - %s'
    }
  }
}
</script>
