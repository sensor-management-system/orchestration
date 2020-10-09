import Manufacturer from '@/models/Manufacturer'

import { removeBaseUrl } from '@/utils/urlHelpers'

export default class ManufacturerSerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: any): Manufacturer[] {
      return jsonApiObjectList.data.map((x: any) => this.convertJsonApiDataToModel(x))
    }

    convertJsonApiDataToModel (jsonApiData: any): Manufacturer {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return Manufacturer.createWithData(id, name, url)
    }
}
