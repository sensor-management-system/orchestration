<!--
SPDX-FileCopyrightText: 2022 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <v-card-title>Group management</v-card-title>
      <v-card-text>
        <p>
          Groups and roles are handled using the <b>HIFIS virtual organizations</b>.
          You have an overview at
          <a
            target="_blank"
            style="text-decoration: none"
            href="https://hifis.net/doc/helmholtz-aai/list-of-vos/"
          >
            https://hifis.net/doc/helmholtz-aai/list-of-vos/
            <v-icon small>
              mdi-open-in-new
            </v-icon>
          </a>.
        </p>
        <p>
          Administrators can manage them on <a
            target="_blank"
            style="text-decoration: none"
            href="https://login.helmholtz.de/upman/"
          >
            https://login.helmholtz.de/upman/
            <v-icon small>
              mdi-open-in-new
            </v-icon>
          </a>.
          Please note that you need to have <b>two-factor-authentification</b> activated to access this page. You can do so on <a
            target="_blank"
            style="text-decoration: none"
            href="https://login.helmholtz.de"
          >
            https://login.helmholtz.de
            <v-icon small>
              mdi-open-in-new
            </v-icon>
          </a> in the Credentials tab.
        </p>
        <p>
          You can use any group that you create there in the SMS.
        </p>
      </v-card-text>
    </v-card>
    <v-card flat class="pb-0">
      <v-card-title>Roles</v-card-title>
      <v-card-text>
        <p class="mb-0">
          We have four roles with their permissions in the groups:
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
              <permission-info :value="true" label="archive" />
            </v-col>
            <v-col>
              <permission-info :value="true" label="restore" />
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
          devices, platforms, configurations and sites/labs.
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
        <p />
        <p>Visibility handling is inspired by Gitlab.</p>
      </v-card-text>
    </v-card>
    <v-card flat>
      <v-card-title>Sub-groups</v-card-title>
      <v-card-text>
        <p>
          You can also use sub-groups for even finer granularity:
          <v-treeview open-all dense :items="exampletreeview">
            <template #prepend="{ item }">
              <v-icon v-if="item.icon">
                {{ item.icon }}
              </v-icon>
            </template>
          </v-treeview>
        </p>
        <p>
          This will make the <code>Moses:HydrEx</code> group available in the Sensor Management System.
        </p>
      </v-card-text>
    </v-card>
    <v-card flat>
      <v-card-title>GFZ specific</v-card-title>
      <v-card-text>
        <p>
          Additional to the pure HIFIS VO way of handling groups, you can also use
          <a
            target="_blank"
            style="text-decoration: none"
            href="https://myprofile.gfz.de/"
          >
            MyProfile groups
            <v-icon small>
              mdi-open-in-new
            </v-icon>
          </a>
          for the group management
          in the Sensor Management System.
        </p>
        <p>
          However, there is a precondition that the group can be used for external systems. To do so, you need
          administration permissions for the myprofile group itself - or you must ask your group administrator
          to make the changes.
        </p>
        <p>
          To allow external usage of a group, you need to
          <ol>
            <li>
              Open
              <a
                target="_blank"
                style="text-decoration: none"
                href="https://myprofile.gfz.de/"
              >
                MyProfile
                <v-icon small>
                  mdi-open-in-new
                </v-icon>
              </a>
            </li>
            <li>Go to the <code>Groups</code>tab</li>
            <li>Click to open the <code>Management</code> sub tab</li>
            <li>Select the group you want to use</li>
            <li>Activate the checkbox for <code>External use</code></li>
          </ol>
        </p>
        <p>
          All members of those groups will have the <code>member</code> role in
          the Sensor Management System.
        </p>
        <p>
          Please note that section groups are exposed by default, so that you can use those without
          further adjustments.
        </p>
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

  get exampletreeview (): any {
    return [
      {
        id: 1,
        name: 'Moses',
        icon: 'mdi-account-group',
        children: [
          {
            id: 2,
            name: 'HydrEx',
            icon: 'mdi-account-group',
            children: [
              {
                id: 4,
                name: 'User A',
                icon: 'mdi-account'
              },
              {
                id: 6,
                name: 'User B',
                icon: 'mdi-account'
              }
            ]
          }
        ]
      }
    ]
  }
}
</script>
