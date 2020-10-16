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
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <h1>Welcome to the Sensor Management System</h1>
        <p>The purpose of this application is to help scientists and technicans to...</p>
        <p>
          If you don't have an account, you can browse and view all datasets.<br>
          If you're already registered, you can login below
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="2">
        <v-text-field
          label="username"
        />
      </v-col>
      <v-col cols="12" md="2">
        <v-text-field
          label="password"
          type="password"
        />
      </v-col>
      <v-col cols="12" md="2">
        <v-btn color="primary">
          Login
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
