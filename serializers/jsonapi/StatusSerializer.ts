import Status from '@/models/Status'

import { removeBaseUrl } from '@/utils/urlHelpers'

export default class StatusSerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: any): Status[] {
      return jsonApiObjectList.data.map((x: any) => this.convertJsonApiDataToModel(x))
    }

    convertJsonApiDataToModel (jsonApiData: any): Status {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return Status.createWithData(id, name, url)
    }
}
