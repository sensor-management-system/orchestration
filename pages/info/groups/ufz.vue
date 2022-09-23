<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
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
    <v-card flat>
      <v-card-title>Group management</v-card-title>
      <v-card-text>
        <p>
          Groups and roles are handled using the <b>Data Projects</b>.
          You can access them at <a href="https://webapp.ufz.de/dataprojects" target="_blank" style="text-decoration: none">
            <strong>UFZ DPVM</strong>
            <v-icon small>
              mdi-open-in-new
            </v-icon>
          </a>.
        </p>
      </v-card-text>
    </v-card>
    <v-card flat class="pb-0">
      <v-card-title>Roles</v-card-title>
      <v-card-text>
        <p class="mb-0">
          We have five roles with their permissions in the groups:
        </p>
      </v-card-text>
    </v-card>
    <div class="ml-4">
      <v-card flat class>
        <v-card-subtitle class="pt-0">
          Anonymous
        </v-card-subtitle>
        <v-card-text>
          <v-row>
            <v-col>
              <permission-info :value="true" label="view" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="create" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="edit" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="archive" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="restore" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="delete" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <v-card flat>
        <v-card-subtitle>Logged in</v-card-subtitle>
        <v-card-text>
          <v-row>
            <v-col>
              <permission-info :value="true" label="view" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="create" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="edit" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="archive" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="restore" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="delete" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <v-card flat>
        <v-card-subtitle>Group member</v-card-subtitle>
        <v-card-text>
          <v-row>
            <v-col>
              <permission-info :value="true" label="view" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="create" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="edit" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="archive" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="restore" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="delete" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <v-card flat>
        <v-card-subtitle>Group admin</v-card-subtitle>
        <v-card-text>
          <v-row>
            <v-col>
              <permission-info :value="true" label="view" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="create" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="edit" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="archive" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="restore" />
            </v-col>
            <v-col>
              <permission-info :value="false" label="delete" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <v-card flat>
        <v-card-subtitle>Super user</v-card-subtitle>
        <v-card-text>
          <v-row>
            <v-col>
              <permission-info :value="true" label="view" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="create" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="edit" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="archive" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="restore" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="delete" />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>
    <v-card flat>
      <v-card-title>Visibility</v-card-title>
      <v-card-text>
        <p>
          There are three visibility states for
          devices/platforms/configurations.
        </p>
        <v-row>
          <v-col>
            <code>Private</code>
          </v-col>
          <v-col>
            <code>Internal</code>
          </v-col>
          <v-col>
            <code>Public</code>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            Only the owner can view, edit or delete the entity.
          </v-col>
          <v-col>
            The user must be loggin in to see the entity. Edit and delete permissions are handled by the role memberships of the associated groups.
          </v-col>
          <v-col>
            The entity is visible for everyone. Edit and delete permissions are handled by the role memberships of the associated groups (similar to <code>Internal</code>).
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import PermissionInfo from '@/components/PermissionInfo.vue'

@Component({
  components: {
    PermissionInfo
  }
})
export default class GfzGroupInfoPage extends Vue {
  created () {
    this.$store.dispatch('appbar/setDefaults')
    this.$store.commit('appbar/setTitle', 'Group information')
  }

  beforeDestroy () {
    this.$store.dispatch('appbar/setDefaults')
  }
}
</script>
