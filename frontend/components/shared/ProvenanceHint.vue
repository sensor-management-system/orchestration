<!--
SPDX-FileCopyrightText: 2023 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <p class="text-caption">
    To fill out the provenance please note the origin of the term.
    Perhaps there is a relevant vocabulary
    (<a href="http://vocab.nerc.ac.uk/" target="_blank">NERC</a>,
    <a href="http://vocabulary.odm2.org/" target="_blank">ODM2</a>,
    <a href="https://en.wikipedia.org/" target="_blank">Wiki</a>, etc.) that contains the term.
    If it's a term used in your scientific discipline, you can note that as well.
    In the field <em>Provenance URI</em> you can enter the link to the origin of the term.
  </p>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class ProvenanceHint extends Vue {
}
</script>
