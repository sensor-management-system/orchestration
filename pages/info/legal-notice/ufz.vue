<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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
  <div>
    <section>
      <h1>Legal information / Provider Identification</h1>
      <p>Imprint according to § 5 TMG (Tele Media Act) and § 55 RStV (German Interstate Treaty on Broadcasting)</p>
    </section>
    <section>
      <h2>Provider</h2>
      <p>
        The provider of the internet presence <a href="https://rdm-test.intranet.ufz.de/sms">rdm-test.intranet.ufz.de/sms</a> is the <a href="https://www.ufz.de/index.php?en=33573" target="_blank">Helmholtz Centre for Environmental Research UFZ</a>. This internet presence was developed within the DataHub initiative of the Helmholtz Association of German Research Centres.
      </p>
    </section>
    <section>
      <h2>Address</h2>
      <p>
        Helmholtz Centre for Environmental Research UFZ<br>
        Permoserstraße 15<br>
        04318 Leipzig, Germany<br>
        Tel.: +49 341 / 235-0<br>
        Website: <a href="https://www.ufz.de" target="_blank">www.ufz.de</a>
      </p>
    </section>
    <section>
      <h2>Legal form</h2>
      <p>The Helmholtz Centre for Environmental Research UFZ is a Public Law Foundation. The UFZ is member of the <a href="https://www.helmholtz.de" target="_blank">Helmholtz-Gemeinschaft Deutscher Forschungszentren e.V. (Helmholtz Association of German Research Centres)</a>.</p>
    </section>
    <section>
      <h2>Authorized representatives</h2>
      <p>The UFZ is legally represented by Prof. Dr. Rolf Altenburger, Scientific Managing Director and Dr. Sabine König, Administrative Managing Director.</p>
    </section>
    <section>
      <h2>Value Added Tax ID</h2>
      <p>VAT Identification Number according to § 27a VAT Tax Act: DE141507065</p>
    </section>
    <section>
      <h2>Editorial Staff</h2>
      <p>
        Responsible editors for the contents of this internet presence with regard to media law are<br>
        <br>
        Dr.-Ing. Jan Bumberger (Head of <a href="https://www.ufz.de/index.php?en=48474" target="_blank">Research Data Management (RDM)</a>)
        E-Mail: <a href="mailto:jan.bumberger@ufz.de">jan.bumberger@ufz.de</a>
        <br>
        Thomas Schnicke (Head of <a href="https://www.ufz.de/index.php?en=48474" target="_blank">Research Data Management (RDM)</a>)
        E-Mail: <a href="mailto:thomas.schnicke@ufz.de">thomas.schnicke@ufz.de</a>
      </p>
      <p>
        Editor, conception, coordination (<a href="https://rdm-test.intranet.ufz.de/sms">rdm-test.intranet.ufz.de/sms</a>)<br>
        <br>
        Daniel Sielaff (<a href="https://www.ufz.de/index.php?en=48474" target="_blank">Research Data Management (RDM)</a>)
        E-Mail: <a href="mailto:daniel.sielaff@ufz.de">daniel.sielaff@ufz.de</a>
      </p>
    </section>
    <section>
      <h2>Technical Realization and support</h2>
      <p>
        Responsible for the technical implementation is the <a href="https://www.ufz.de/index.php?en=45348" target="_blank">Research Data Management (RDM)</a><br>
        E-Mail: <a href="mailto:sms-administration@ufz.de">sms-administration@ufz.de</a>
      </p>
    </section>
    <section>
      <h2>
        Software licenses
      </h2>
      <p>
        The following third-party software is used within the scope of this web application <br>
        <a href="/info/licenses/">Licenses</a>
      </p>
    </section>
    <section>
      <h2>Copyright</h2>
      <p>
        The texts and images on this website are protected by copyright. Copying these files or printing the publications is only permitted for private use.
        All other uses, such as duplication, alteration or use of these graphics, recordings, video sequences or texts on this websites in further electronic or printed publications for non-commercial and commercial purposes are not permitted without the explicit consent of the copyright holder - even if they are not labelled as a copyright protected document.
      </p>
    </section>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class UfzImprintPage extends Vue {
  created () {
    this.$store.dispatch('appbar/init', { title: 'Legal Notice' })
  }
}
</script>
