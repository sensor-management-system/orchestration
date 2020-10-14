import Manufacturer from '@/models/Manufacturer'

import { IJsonApiObjectListWithLinks, IJsonApiDataWithIdAndLinks } from '@/serializers/jsonapi/JsonApiTypes'

import { removeBaseUrl } from '@/utils/urlHelpers'

export class ManufacturerSerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectListWithLinks): Manufacturer[] {
      return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
    }

    convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithIdAndLinks): Manufacturer {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return Manufacturer.createWithData(id, name, url)
    }
}
