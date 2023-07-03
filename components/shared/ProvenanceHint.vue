<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

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
