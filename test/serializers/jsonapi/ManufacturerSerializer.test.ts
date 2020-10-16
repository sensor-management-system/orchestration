/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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
import Manufacturer from '@/models/Manufacturer'
import { ManufacturerSerializer } from '@/serializers/jsonapi/ManufacturerSerializer'

describe('ManufacturerSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            active: true,
            category: null,
            definition: 'ecoTech Umwelt-Meßsysteme GmbH',
            name: 'Ecotech',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'ecotech'
          },
          id: 'Ecotech',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturer/Ecotech/'
          },
          relationships: {},
          type: 'Manufacturer'
        }, {
          attributes: {
            active: true,
            category: null,
            definition: 'Campbell Scientific Ltd.',
            name: 'Campbell ++',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'campbell'
          },
          id: 'Campbell',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturer/Campbell/'
          },
          relationships: {},
          type: 'Manufacturer'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedManufacturer1 = Manufacturer.createFromObject({
        id: 'Ecotech',
        name: 'Ecotech',
        uri: 'manufacturer/Ecotech'
      })
      const expectedManufacturer2 = Manufacturer.createFromObject({
        id: 'Campbell',
        name: 'Campbell ++',
        uri: 'manufacturer/Campbell'
      })

      const serializer = new ManufacturerSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const manufacturers = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(manufacturers)).toBeTruthy()
      expect(manufacturers.length).toEqual(2)
      expect(manufacturers[0]).toEqual(expectedManufacturer1)
      expect(manufacturers[1]).toEqual(expectedManufacturer2)
    })
  })
})
