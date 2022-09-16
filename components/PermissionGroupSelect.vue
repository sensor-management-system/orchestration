<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
    <v-select
      v-model="entityPermissionGroups"
      :items="items"
      :readonly="readonly"
      :disabled="readonly"
      :label="label"
      chips
      :deletable-chips="multiple"
      :multiple="multiple"
      :hint="hint"
      persistent-hint
      :rules="[...rules]"
      :class="{ required: required }"
    >
      <template #selection="data">
        <v-chip
          v-bind="data.attrs"
          :close="!multiple ? false : isRemoveable(data.item.value)"
          @click:close="removeItem(data.item.value)"
        >
          {{ data.item.text }}
        </v-chip>
      </template>
      <template #item="{ item, on, attrs }">
        <v-list-item v-slot="{ active }" v-bind="attrs" v-on="on">
          <v-list-item-action v-if="multiple">
            <v-checkbox :input-value="active" :disabled="!isRemoveable(item.value)" />
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title
              :class="getClass(item.value)"
            >
              {{ item.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-select>
  </div>
</template>
<script lang="ts">
import { Component, Prop, Watch, Vue } from 'nuxt-property-decorator'

import { mapState, mapGetters } from 'vuex'

import { PermissionsState, UserGroupsGetter } from '@/store/permissions'

import { IPermissionGroup, PermissionGroup } from '@/models/PermissionGroup'
import { IGenericSelectItem } from '@/models/GenericSelectItem'

import { pluralize } from '@/utils/stringHelpers'

type ruleFunction = ((value: string) => string | boolean)

@Component({
  computed: {
    ...mapState('permissions', ['permissionGroups', 'userInfo']),
    ...mapGetters('permissions', ['userGroups'])
  }

})
export default class PermissionGroupSelect extends Vue {
  private initialPermissionGroups!: PermissionGroup[] | undefined

  // vuex definition for typescript check
  userGroups!: UserGroupsGetter
  permissionGroups!: PermissionsState['permissionGroups']
  userInfo!: PermissionsState['userInfo']

  /**
   * the permission groups of the entity
   */
  @Prop({
    required: false,
    type: [Array, Object]
  })
  readonly value!: PermissionGroup[] | PermissionGroup | null

  /**
   * the name of the entity that provides the permission groups
   * (eg. 'device' or 'platform' or 'configuration'
   */
  @Prop({
    default: 'entity',
    required: false,
    type: String
  })
  readonly entityName!: string

  /**
   * an array of validation rules
   */
  @Prop({
    default: () => [],
    type: Array
  })
  readonly rules!: ruleFunction[]

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: () => false,
    type: Boolean
  })
  readonly readonly!: boolean

  @Prop({
    default: () => true,
    type: Boolean
  })
  readonly multiple!: boolean

  @Prop({
    default: 'Permission groups',
    required: false,
    type: String
  })
  readonly label!: string

  /**
   * whether the component is in required mode or not
   */
  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  readonly required!: boolean

  created () {
    // copy the initial value so that we can check which of the groups are new
    this.initialPermissionGroups = this.valueArray.map(i => i)
  }

  get valueArray (): PermissionGroup[] {
    if (Array.isArray(this.value)) {
      return this.value
    } else {
      return (this.value !== null) ? [this.value] : []
    }
  }

  get entityPermissionGroups (): PermissionGroup[] | PermissionGroup | null {
    return this.value
  }

  set entityPermissionGroups (groups: PermissionGroup[] | PermissionGroup | null) {
    if (Array.isArray(groups)) {
      this.$emit('input', [...groups])
    } else {
      this.$emit('input', groups)
    }
  }

  get items (): IGenericSelectItem<IPermissionGroup>[] {
    const items = [
      // all groups the user is member or admin of
      // if the user is not admin of the group and has not just added the
      // group, it is disabled so that it can't be removed
      ...this.userGroups.map(group => ({
        text: group.name,
        value: group,
        disabled: !this.isRemoveable(group)
      })),
      // all groups of the entity, the user is not in
      ...this.valueArray.filter(group => !this.userGroups.find(userGroup => userGroup.equals(group))).map(i => ({
        text: i.name,
        value: i,
        disabled: true
      }))
    ]
    return items
  }

  /**
   * removes a permission group from the device
   *
   * @param {PermissionGroup} item - the group to remove
   */
  removeItem (item: PermissionGroup): void {
    const index = this.valueArray.findIndex(group => group.id === item.id)
    const groups = [...this.valueArray]
    if (index > -1) {
      groups.splice(index, 1)
    }
    this.entityPermissionGroups = groups
  }

  /**
   * checks if a permissiongroup can be removed
   * the group can be removed if:
   * - the user is a super user
   * - the user is an admin of the group
   * - the user is a simple member but has just added the group without saving
   *   the entity
   *
   * @param {PermissionGroup} group - the group to check
   * @returns {boolean} true when the group is removeable, otherwise false
   */
  isRemoveable (group: PermissionGroup): boolean {
    if ((this.userInfo && this.userInfo.isAdminOf(group)) || (this.userInfo && this.userInfo.isSuperUser)) {
      return true
    }
    if (this.initialPermissionGroups?.find(i => i.equals(group)) === undefined) {
      return true
    }
    return false
  }

  getClass (group: PermissionGroup): string {
    if (!this.isRemoveable(group)) {
      return 'text--secondary'
    }
    return ''
  }

  /**
   * Displays a custom hint if the user is not an admin of a group or a
   * superuser and the group is not part of the initial groups
   *
   * @return {string} either a warning if a group will not be removable after saving, or the default hint text
   */
  get hint (): string {
    const groups = this.valueArray.filter((group) => {
      return (this.initialPermissionGroups?.find(i => i.equals(group)) === undefined)
    })
    const nonRemovable = groups.filter((group) => {
      if (this.userInfo && this.userInfo.isSuperUser) {
        return false
      }
      if (this.userInfo && this.userInfo.isAdminOf(group)) {
        return false
      }
      return true
    })

    if (nonRemovable.length > 0) {
      return `You will not be able to remove the ${pluralize(nonRemovable.length, 'group')} "${nonRemovable.map(group => group.name).join(', ')}" after saving the ${this.entityName} because you are not an admin of this group.`
    }

    return `You must specify the ${pluralize(this.multiple ? 2 : 1, 'group')} that ${pluralize(this.multiple ? 2 : 1, 'is', 'are')} allowed to modify this ` + this.entityName + '.'
  }

  @Watch('value')
  permissionGroupsUpdated (newVal: PermissionGroup[]) {
    if (typeof this.initialPermissionGroups === 'undefined') {
      this.initialPermissionGroups = newVal.map(i => i)
    }
  }
}
</script>
