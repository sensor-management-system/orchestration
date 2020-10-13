import Property from '@/models/Property'

import { IJsonApiObjectListWithLinks, IJsonApiDataWithIdAndLinks } from '@/serializers/jsonapi/JsonApiTypes'

import { removeBaseUrl } from '@/utils/urlHelpers'

export class PropertySerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectListWithLinks): Property[] {
      return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
    }

    convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithIdAndLinks): Property {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return Property.createWithData(id, name, url)
    }
}
