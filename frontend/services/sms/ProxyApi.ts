/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export class ProxyApi {
  private baseUrl: string

  constructor (baseUrl: string) {
    this.baseUrl = baseUrl
  }

  getUrlViaProxy (url: string): string {
    return this.baseUrl + '/proxy?url=' + encodeURIComponent(url)
  }
}
