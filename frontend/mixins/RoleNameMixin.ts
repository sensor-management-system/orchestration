/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Vue, Component } from 'nuxt-property-decorator'
import { ContactRole } from '@/models/ContactRole'
import { CvContactRole } from '@/models/CvContactRole'

@Component
export class RoleNameMixin extends Vue {
  roleName (role: ContactRole, cvContactRoles: CvContactRole[]): string {
    const idx = cvContactRoles.findIndex(cv => cv.uri === role.roleUri)
    if (idx > -1) {
      return cvContactRoles[idx].name
    }
    return role.roleName
  }
}
