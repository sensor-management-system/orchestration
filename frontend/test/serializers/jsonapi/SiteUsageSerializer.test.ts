/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { SiteUsage } from '@/models/SiteUsage'
import { SiteUsageSerializer } from '@/serializers/jsonapi/SiteUsageSerializer'

describe('SiteUsageSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: 'Foo Bar',
            note: null,
            provenance: '',
            provenance_uri: null,
            status: 'ACCEPTED',
            term: 'Agricultural areas'
          },
          id: '1',
          links: {
            self: 'https://localhost.localdomain/cv/api/v1/siteusages/1/'
          },
          relationships: {
            global_provenence: {
              data: null
            }
          },
          type: 'SiteUsage'
        }, {
          attributes: {
            category: 'category',
            definition: 'Foo Bar Baz',
            note: 'note',
            provenance: 'Originally from CUAHSI HIS GeneralCategoryCV.',
            provenance_uri: 'uri',
            status: 'ACCEPTED',
            term: 'Body of standing water'
          },
          id: '2',
          links: {
            self: 'https://localhost.localdomain/cv/api/v1/siteusages/5/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '2',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'SiteUsage'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedSiteUsage1 = SiteUsage.createFromObject({
        id: '1',
        name: 'Agricultural areas',
        uri: 'https://localhost.localdomain/cv/api/v1/siteusages/1/',
        definition: 'Foo Bar',
        category: '',
        note: '',
        provenance: '',
        provenanceUri: '',
        globalProvenanceId: null
      })
      const expectedSiteUsage2 = SiteUsage.createFromObject({
        id: '2',
        name: 'Body of standing water',
        uri: 'https://localhost.localdomain/cv/api/v1/siteusages/5/',
        definition: 'Foo Bar Baz',
        category: 'category',
        note: 'note',
        provenance: 'Originally from CUAHSI HIS GeneralCategoryCV.',
        provenanceUri: 'uri',
        globalProvenanceId: '2'
      })

      const serializer = new SiteUsageSerializer()

      const siteUsages = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(siteUsages)).toBeTruthy()
      expect(siteUsages.length).toEqual(2)
      expect(siteUsages[0]).toEqual(expectedSiteUsage1)
      expect(siteUsages[1]).toEqual(expectedSiteUsage2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const siteUsage = SiteUsage.createFromObject({
        id: '2',
        name: 'Body of standing water',
        uri: 'https://localhost.localdomain/cv/api/v1/siteusages/5/',
        definition: 'Foo Bar Baz',
        category: 'category',
        note: 'note',
        provenance: 'Originally from CUAHSI HIS GeneralCategoryCV.',
        provenanceUri: 'uri',
        globalProvenanceId: '2'
      })

      const expectedResult = {
        id: '2',
        type: 'SiteUsage',
        attributes: {
          term: 'Body of standing water',
          definition: 'Foo Bar Baz',
          category: 'category',
          note: 'note',
          provenance: 'Originally from CUAHSI HIS GeneralCategoryCV.',
          provenance_uri: 'uri'
        },
        relationships: {
          global_provenance: {
            data: {
              id: '2',
              type: 'GlobalProvenance'
            }
          }
        }
      }

      const serializer = new SiteUsageSerializer()
      const result = serializer.convertModelToJsonApiData(siteUsage)

      expect(result).toEqual(expectedResult)
    })
  })
})
