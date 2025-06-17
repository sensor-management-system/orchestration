/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2025
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { ReleaseNotesSerializer } from '@/serializers/custom/ReleaseNotesSerializer'
import { Release } from '@/models/ReleaseNotes'
import { ProxyApi } from '@/services/sms/ProxyApi'

export class ReleaseNotesApi {
  private axiosApi: AxiosInstance
  private proxyApi: ProxyApi
  readonly repositoryChangelogFilePath: string
  private serializer: ReleaseNotesSerializer

  constructor (axiosApi: AxiosInstance, proxyApi: ProxyApi, repositoryChangelogFilePath: string) {
    this.axiosApi = axiosApi
    this.proxyApi = proxyApi
    this.repositoryChangelogFilePath = repositoryChangelogFilePath
    this.serializer = new ReleaseNotesSerializer()
  }

  async findAllReleases (): Promise<Release[]> {
    const response = await this.axiosApi.get(this.proxyApi.getUrlViaProxy(this.repositoryChangelogFilePath))
    return this.serializer.convertChangelogTextToModel(response.data)
  }
}
