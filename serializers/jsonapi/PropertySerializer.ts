import Property from '@/models/Property'

import { removeBaseUrl } from '@/utils/urlHelpers'

export default class PropertySerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: any): Property[] {
      return jsonApiObjectList.data.map((x: any) => this.convertJsonApiDataToModel(x))
    }

    convertJsonApiDataToModel (jsonApiData: any): Property {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return Property.createWithData(id, name, url)
    }
}
