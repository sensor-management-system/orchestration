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
      <p>
        This internet presence was developed within the DataHub initiative of the Helmholtz Association of German
        Research Centres.
      </p>
    </section>
    <section>
      <h2>Provider of this website</h2>
      <p>
        Team <a href="https://www.ufz.de/index.php?en=48474">Research Data Management (RDM)</a><br>
        <a href="mailto:sms-administration@ufz.de">sms-administration@ufz.de</a>
      </p>
      <p>
        at the<br>
        Helmholtz-Zentrum für Umweltforschung GmbH - UFZ<br>
        Permoserstraße 15<br>
        04318 Leipzig, Germany<br>
        <a href="mailto:info@ufz.de">info@ufz.de</a><br>
        Tel.: +49 341 / 235-0<br>
        Website: <a href="https://www.ufz.de">www.ufz.de</a>
      </p>
    </section>
    <section>
      <h2>Legal form</h2>
      <p>
        The Helmholtz-Zentrum für Umweltforschung GmbH - UFZ is a limited liability company (“Gesellschaft mit
        beschränkter Haftung“ incorporated under German law). Company shareholders are the Federal Republic of Germany,
        the Free State of Saxony and the Federal State Saxony-Anhalt. The UFZ is member of the <a
          href="https://www.helmholtz.de"
        >Helmholtz-Gemeinschaft Deutscher Forschungszentren e.V. (Helmholtz Association of German Research Centres)</a>.
      </p>
      <p>
        Registration court: Amtsgericht (local court) Leipzig<br>
        Register number: HRB 4703<br>
        Value added tax identification number: DE 141507065
      </p>
    </section>
    <section>
      <h2>Authorized representatives</h2>
      <p>
        The UFZ is legally represented by Prof. Dr. Rolf Altenburger (Scientific Director) and Dr. Sabine König
        (Administrative Director).
      </p>
    </section>
    <section>
      <h2>Chairwoman of Supervisory Board</h2>
      <p>MinDirig´in Oda Keppler</p>
    </section>
    <section>
      <h2>Responsibility for the content of the website</h2>
      <p>
        Dr.-Ing. Jan Bumberger (Head of <a href="https://www.ufz.de/index.php?en=48474">Research Data Management
          (RDM)</a>)<br>
        Permoserstr. 15, 04318 Leipzig, Germany<br>
        E-Mail: <a href="mailto:jan.bumberger@ufz.de">jan.bumberger@ufz.de</a>
      </p>
    </section>
    <section>
      <h2>
        Content management, conception, coordination
      </h2>
      <p>
        Daniel Sielaff (<a href="https://www.ufz.de/index.php?en=48474">Research Data Management
          (RDM)</a>)<br>
        Permoserstr. 15, 04318 Leipzig, Germany<br>
        E-Mail: <a href="mailto:daniel.sielaff@ufz.de">daniel.sielaff@ufz.de</a>
      </p>
    </section>
    <section>
      <h2>Technical Realization and support</h2>
      <p>
        Responsible for the technical implementation is the <a href="https://www.ufz.de/index.php?en=45348">Research
          Data Management (RDM)</a><br>
        E-Mail: <a href="mailto:sms-administration@ufz.de">sms-administration@ufz.de</a>
      </p>
    </section>
    <section>
      <h2>Copyright</h2>
      <p>
        The texts and images on this website are protected by copyright. Copying these files or printing the
        publications is only permitted for private use. All other uses, such as duplication, alteration or use of these
        graphics, recordings, video sequences or texts on this websites in further electronic or printed publications
        for non-commercial and commercial purposes are not permitted without the explicit consent of the copyright
        holder - even if they are not labelled as a copyright protected document.
      </p>
      <p>
        This site uses cookies to ensure technical functionality. To read more about what we store in the cookies, have
        a look at our <nuxt-link to="/info/privacy-policy">
          Privacy Policy
        </nuxt-link>. By using
        this service, I also accept the <nuxt-link to="/info/terms-of-use">
          Terms of
          Use
        </nuxt-link>.
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
