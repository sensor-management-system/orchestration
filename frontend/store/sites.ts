/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2024
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */

import { Commit, GetterTree, ActionTree, Dispatch } from 'vuex'

// import { DateTime } from 'luxon'
import { RootState } from '@/store'

import { Attachment } from '@/models/Attachment'
import { Image } from '@/models/Image'
import { Site } from '@/models/Site'
import { ISiteSearchParams } from '@/modelUtils/SiteSearchParams'
import { IncludedRelationships } from '@/services/sms/SiteApi'
import { Configuration } from '@/models/Configuration'
import { ContactRole } from '@/models/ContactRole'
import { getLastPathElement } from '@/utils/urlHelpers'
import { ContactWithRoles } from '@/models/ContactWithRoles'

const PAGE_SIZES = [
  25,
  50,
  100
]

export interface SitesState {
  sites: Site[],
  site: Site | null,
  siteContactRoles: ContactRole[],
  siteConfigurations: Configuration[],
  siteAttachments: Attachment[],
  siteAttachment: Attachment | null,
  pageNumber: number,
  pageSize: number,
  totalPages: number,
  totalCount: number
}

const state = (): SitesState => ({
  sites: [],
  site: null,
  siteContactRoles: [],
  siteConfigurations: [],
  siteAttachments: [],
  siteAttachment: null,
  pageNumber: 1,
  pageSize: PAGE_SIZES[0],
  totalPages: 1,
  totalCount: 0
})

export type PageSizesGetter = number[]

const getters: GetterTree<SitesState, RootState> = {
  pageSizes: (): number[] => {
    return PAGE_SIZES
  },
  contactsWithRoles: (state: SitesState): ContactWithRoles[] => {
    const result: ContactWithRoles[] = []
    for (const contactRole of state.siteContactRoles) {
      const contact = contactRole.contact
      const contactId = contact?.id
      if (contact && contactId) {
        const foundIndex = result.findIndex(c => c.contact?.id === contact.id)
        if (foundIndex > -1) {
          result[foundIndex].roles.push(contactRole)
        } else {
          result.push(new ContactWithRoles(contact, [contactRole]))
        }
      }
    }
    return result
  }
}

export type LoadSiteAction = (params: { siteId: string } & IncludedRelationships) => Promise<void>
export type SearchSitesAction = () => Promise<void>
export type SearchSitesPaginatedAction = (searchParams: ISiteSearchParams) => Promise<void>
export type LoadSiteConfigurationsAction = (id: string) => Promise<void>
export type LoadSiteContactRolesAction = (id: string) => Promise<void>
export type AddSiteContactRoleAction = (params: { siteId: string, contactRole: ContactRole }) => Promise<void>
export type RemoveSiteContactRoleAction = (params: { siteContactRoleId: string }) => Promise<void>
export type AddSiteAttachmentAction = (params: { siteId: string, attachment: Attachment }) => Promise<Attachment>
export type DeleteSiteAttachmentAction = (attachmentId: string) => Promise<void>
export type DeleteSiteImageAction = (imageId: string) => Promise<void>
export type UpdateSiteAttachmentAction = (params: { siteId: string, attachment: Attachment }) => Promise<Attachment>
export type LoadSiteAttachmentsAction = (id: string) => Promise<void>
export type LoadSiteAttachmentAction = (id: string) => Promise<void>
export type DownloadAttachmentAction = (attachmentUrl: string) => Promise<Blob>
export type ClearSiteAttachmentsAction = () => void
export type SaveSiteAction = (site: Site) => Promise<Site>
export type SaveSiteImagesAction = (params: {siteId: string, siteImages: Image[], siteCopyImages: Image[]}) => Promise<Image[]>
export type CopySiteAction = (params: {site: Site, copyContacts: boolean, copyAttachments: boolean, originalSiteId: string}) => Promise<string>
export type DeleteSiteAction = (id: string) => Promise<void>
export type ArchiveSiteAction = (id: string) => Promise<void>
export type RestoreSiteAction = (id: string) => Promise<void>
export type SetPageNumberAction = (newPageNumber: number) => void
export type SetPageSizeAction = (newPageSize: number) => void
export type ReplaceSiteInSitesAction = (newSite: Site) => void
export type ExportAsSensorMLAction = (id: string) => Promise<Blob>
export type GetSensorMLUrlAction = (id: string) => Promise<string>

const actions: ActionTree<SitesState, RootState> = {
  async searchSitesPaginated ({
    commit,
    state
  }: { commit: Commit, state: SitesState }, searchParams: ISiteSearchParams): Promise<void> {
    let userId = null
    if (searchParams.onlyOwnSites) {
      userId = this.getters['permissions/userId']
    }

    const {
      elements,
      totalCount
    } = await this.$api.sites
      .setSearchText(searchParams.searchText)
      .setSearchedPermissionGroups(searchParams.permissionGroups)
      .setSearchedCreatorId(userId)
      .setSearchedSiteUsages(searchParams.siteUsages)
      .setSearchedSiteTypes(searchParams.siteTypes)
      .setSearchIncludeArchivedSites(searchParams.includeArchivedSites)
      .searchPaginated(
        state.pageNumber,
        state.pageSize,
        {
          includeCreatedBy: true
        }
      )
    commit('setSites', elements)

    const totalPages = Math.ceil(totalCount / state.pageSize)
    commit('setTotalPages', totalPages)
    commit('setTotalCount', totalCount)
  },
  async searchSites ({ commit }: { commit: Commit }, searchText: string = ''): Promise<void> {
    const sites = await this.$api.sites
      .setSearchText(searchText)
      // In order to not use pre-assigned filters, we need to remove them.
      .setSearchedPermissionGroups([])
      .setSearchedCreatorId(null)
      .setSearchedSiteUsages([])
      .setSearchedSiteTypes([])
      .setSearchIncludeArchivedSites(false)
      .searchAll()
    commit('setSites', sites)
  },
  async loadSite ({ commit }: { commit: Commit },
    {
      siteId,
      includeContacts,
      includeCreatedBy,
      includeUpdatedBy,
      includeImages
    }: { siteId: string } & IncludedRelationships
  ): Promise<void> {
    const site = await this.$api.sites.findById(siteId, {
      includeContacts,
      includeCreatedBy,
      includeUpdatedBy,
      includeImages
    })
    const configurations = await this.$api.sites.findRelatedConfigurations(site.id)
    commit('setSite', site)
    commit('setSiteConfigurations', configurations)
  },
  async loadSiteConfigurations ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const siteConfigurations = await this.$api.sites.findRelatedConfigurations(id)
    commit('setSiteConfigurations', siteConfigurations)
  },

  deleteSiteImage (_, imageId: string): Promise<void> {
    return this.$api.siteImages.deleteById(imageId)
  },
  updateSiteImage (_, {
    siteId,
    siteImage
  }: { siteId: string, siteImage: Image }): Promise<Image> {
    return this.$api.siteImages.update(siteId, siteImage)
  },
  addSiteImage (_, {
    siteId,
    siteImage
  }: { siteId: string, siteImage: Image }): Promise<Image> {
    return this.$api.siteImages.add(siteId, siteImage)
  },
  async saveSiteImages (
    { dispatch }: { dispatch: Dispatch }, {
      siteId,
      siteImages,
      siteCopyImages
    }: {siteId: string, siteImages: Image[], siteCopyImages: Image[]}): Promise<Image[]> {
    const imagesToDelete = siteImages.filter(el => !siteCopyImages.map(i => i.id).includes(el.id))
    imagesToDelete.forEach(async (siteImage) => {
      await dispatch('deleteSiteImage', siteImage.id)
    })
    const images = siteCopyImages
    for (const i in images) {
      const imageId = images[i].id
      if (!imageId) {
        images[i].id = (await dispatch('addSiteImage', { siteId, siteImage: images[i] })).id
      } else if (siteImages.find(i => i.id === imageId)?.orderIndex !== images[i].orderIndex) {
        images[i].id = (await dispatch('updateSiteImage', { siteId, siteImage: images[i] })).id
      }
    }

    return images
  },

  saveSite (_, site: Site): Promise<Site> {
    return this.$api.sites.save(site)
  },

  async copySite (
    { dispatch }: { dispatch: Dispatch },
    { site, copyContacts, copyAttachments, originalSiteId }:
      {site: Site, copyContacts: boolean, copyAttachments: boolean, originalSiteId: string}
  ): Promise<string> {
    const savedSite = await dispatch('saveSite', site)
    const savedSiteId = savedSite.id!
    const related: Promise<any>[] = []

    if (copyContacts) {
      const sourceContactRoles = await this.$api.sites.findRelatedContactRoles(originalSiteId)
      const freshCreatedContactRoles = await this.$api.sites.findRelatedContactRoles(savedSiteId)
      const contactRolesToSave = sourceContactRoles.filter(c => freshCreatedContactRoles.findIndex((ec: ContactRole) => { return ec.contact!.id === c.contact!.id && ec.roleUri === c.roleUri }) === -1)

      for (const contactRole of contactRolesToSave) {
        const contactRoleToSave = ContactRole.createFromObject(contactRole)
        contactRoleToSave.id = null
        related.push(dispatch('addSiteContactRole', {
          siteId: savedSiteId,
          contactRole: contactRoleToSave
        }))
      }
    }

    const siteImages = site.images.map(Image.createFromObject)
    const siteAttachments = await this.$api.sites.findRelatedSiteAttachments(originalSiteId)
    for (const attachment of siteAttachments) {
      // copy if attachments should be copied or copied images include attachment
      if (!copyAttachments && !siteImages.map(i => i.attachment?.id).includes(attachment.id)) {
        continue
      }

      const oldAttachmentId = attachment.id
      attachment.id = null

      if (attachment.isUpload) {
        const blob = await dispatch('downloadAttachment', attachment.url)
        const filename = getLastPathElement(attachment.url)
        const uploadResult = await dispatch('files/uploadBlob', { blob, filename }, { root: true })
        const newUrl = uploadResult.url
        attachment.url = newUrl
      }
      const savedAttachment = await dispatch('addSiteAttachment', { siteId: savedSiteId, attachment })

      const siteImageToCopy = siteImages.find(i => i.attachment?.id && i.attachment.id === oldAttachmentId)
      if (!siteImageToCopy) { continue }
      const siteImage = Image.createFromObject(siteImageToCopy)
      siteImage.id = ''
      siteImage.attachment = savedAttachment
      related.push(dispatch('addSiteImage', { siteId: savedSiteId, siteImage }))
    }

    await Promise.all(related)
    return savedSiteId
  },

  async deleteSite (_, id: string): Promise<void> {
    await this.$api.sites.deleteById(id)
  },
  async archiveSite (_, id: string): Promise<void> {
    await this.$api.sites.archiveById(id)
  },
  async restoreSite (_, id: string): Promise<void> {
    await this.$api.sites.restoreById(id)
  },
  async loadSiteContactRoles ({ commit }: { commit: Commit }, id: string): Promise<void> {
    const siteContactRoles = await this.$api.sites.findRelatedContactRoles(id)
    commit('setSiteContactRoles', siteContactRoles)
  },
  addSiteContactRole (_, {
    siteId,
    contactRole
  }: { siteId: string, contactRole: ContactRole }): Promise<string> {
    return this.$api.sites.addContact(siteId, contactRole)
  },
  async loadSiteAttachments ({ commit }: {commit: Commit}, id: string): Promise<void> {
    const siteAttachments = await this.$api.sites.findRelatedSiteAttachments(id)
    commit('setSiteAttachments', siteAttachments)
  },
  async loadSiteAttachment ({ commit }: {commit: Commit}, id: string): Promise<void> {
    const siteAttachment = await this.$api.siteAttachments.findById(id)
    commit('setSiteAttachment', siteAttachment)
  },
  async addSiteAttachment (_, { siteId, attachment }: { siteId: string, attachment: Attachment }): Promise<Attachment> {
    return await this.$api.siteAttachments.add(siteId, attachment)
  },
  async updateSiteAttachment (_, { siteId, attachment }: { siteId: string, attachment: Attachment }): Promise<Attachment> {
    return await this.$api.siteAttachments.update(siteId, attachment)
  },
  async deleteSiteAttachment (_, attachmentId: string): Promise<void> {
    return await this.$api.siteAttachments.deleteById(attachmentId)
  },
  async downloadAttachment (_, attachmentUrl: string): Promise<Blob> {
    return await this.$api.siteAttachments.getFile(attachmentUrl)
  },
  removeSiteContactRole (_, {
    siteContactRoleId
  }: { siteContactRoleId: string }): Promise<void> {
    return this.$api.sites.removeContact(siteContactRoleId)
  },
  setPageNumber ({ commit }: { commit: Commit }, newPageNumber: number) {
    commit('setPageNumber', newPageNumber)
  },
  setPageSize ({ commit }: { commit: Commit }, newPageSize: number) {
    commit('setPageSize', newPageSize)
  },
  replaceSiteInSites ({ commit, state }: {commit: Commit, state: SitesState}, newSite: Site) {
    const result = []
    for (const oldSite of state.sites) {
      if (oldSite.id !== newSite.id) {
        result.push(oldSite)
      } else {
        result.push(newSite)
      }
    }
    commit('setSites', result)
  },
  getSensorMLUrl (_, id: string): string {
    return this.$api.sites.getSensorMLUrl(id)
  },
  async exportAsSensorML (_, id: string): Promise<Blob> {
    return await this.$api.sites.getSensorML(id)
  },
  clearSiteAttachments ({ commit }: { commit: Commit }): void {
    commit('setSiteAttachments', [])
  }
}

const mutations = {
  setSites (state: SitesState, sites: Site[]) {
    state.sites = sites
  },
  setSite (state: SitesState, site: Site) {
    state.site = site
  },
  setSiteConfigurations (state: SitesState, configurations: Configuration[]) {
    state.siteConfigurations = configurations
  },
  setSiteAttachments (state: SitesState, attachments: Attachment[]) {
    state.siteAttachments = attachments
  },
  setSiteAttachment (state: SitesState, attachment: Attachment) {
    state.siteAttachment = attachment
  },
  setPageNumber (state: SitesState, newPageNumber: number) {
    state.pageNumber = newPageNumber
  },
  setPageSize (state: SitesState, newPageSize: number) {
    state.pageSize = newPageSize
  },
  setTotalPages (state: SitesState, count: number) {
    state.totalPages = count
  },
  setTotalCount (state: SitesState, count: number) {
    state.totalCount = count
  },
  setSiteContactRoles (state: SitesState, contactRoles: ContactRole[]) {
    state.siteContactRoles = contactRoles
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
