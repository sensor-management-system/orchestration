<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 -2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
  <v-container fluid class="pa-0">
    <v-row no-gutters>
      <v-col>
        <v-row class="image-footer elevation-4" :class="{'mb-10' : !isLandingPage, 'pb-16' : $vuetify.breakpoint.smAndDown}">
          <v-col cols="12" md="9">
            <v-row class="d-flex justify-space-around justify-center align-center">
              <v-col cols="3" class="align-self-center">
                <a href="https://www.ufz.de/index.php?en=33573" target="_blank"><v-img contain height="4em" src="logos/UFZ_Logo_CMYK_EN.svg" /></a>
              </v-col>
              <v-col cols="3" class="align-self-center">
                <a href="https://www.ufz.de/index.php?en=45348" target="_blank"><v-img contain height="3em" src="logos/RDM_fullcolor.svg" /></a>
              </v-col>
              <v-col cols="3" class="align-self-center">
                <a href="https://www.gfz-potsdam.de/en/" target="_blank">
                  <v-img contain height="3em" src="logos/GFZ-Logo_eng_RGB.svg" />
                </a>
              </v-col>
              <v-col cols="3" class="align-self-center">
                <a href="https://datahub.erde-und-umwelt.de/en/" target="_blank"><v-img contain height="2.5em" src="logos/datahublogo.svg" /></a>
              </v-col>
            </v-row>
          </v-col>
          <v-col align-self="center" class="body-2 footer-text" cols="12" md="3">
            SMS, developed by <a href="https://www.gfz-potsdam.de/en/" target="_blank">GFZ</a> and <a href="https://www.ufz.de/index.php?en=45348" target="_blank">RDM</a> at <a href="https://www.ufz.de/index.php?en=33573" target="_blank">UFZ</a> as part of the <a href="https://datahub.erde-und-umwelt.de/en/" target="_blank">DataHub</a> initiative.
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
// @ts-ignore
export default class LogoFooter extends Vue {
@Prop({
  default: false
})isLandingPage!: boolean
}
</script>
<style lang="scss">
  @import '~vuetify/src/styles/styles.sass';

  .image-footer {
    position: relative;
    padding: 0;
    margin: 0;
    z-index: 1;
    background-color: rgba(90,105,110,0.2);
    // box-shadow: 0px 0px 3px 0px rgba(0,0,0,0.65) !important;
  }

  .footer-text {
    color: #002864;
    a {
      font-weight: bold;
      color: #002864 !important;
    }
  }

</style>
