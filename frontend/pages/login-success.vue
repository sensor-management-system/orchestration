<!--
SPDX-FileCopyrightText: 2020 - 2024
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div
    class="container d-flex align-items-center justify-content-center flex-column"
  >
    <v-alert
      border="left"
      colored-border
      type="success"
      elevation="2"
    >
      Please wait, you'll be redirected...
    </v-alert>
  </div>
</template>

<script>
import { removeSavedRoute } from '@/utils/loginHelpers'

export default {
  name: 'LoginSuccess',
  mounted () {
    const route = removeSavedRoute() || '/'
    this.$router.replace(route)
  }
}
</script>
