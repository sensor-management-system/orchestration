/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Vue, Component } from 'nuxt-property-decorator'
import { protocolsInUrl } from '@/utils/urlHelpers'

@Component
export class ExternalUrlLinkMixin extends Vue {
  ensureHttpOrHttpsPrefix (website: string) {
    if (!protocolsInUrl(['http', 'https', 'ftp'], website)) {
      return 'http://' + website
    }
    return website
  }
}
