import SamplingMedia from '@/models/SamplingMedia'

import { removeBaseUrl } from '@/utils/urlHelpers'

export default class StatusSerializer {
    private cvBaseUrl: string | undefined

    constructor (cvBaseUrl: string | undefined) {
      this.cvBaseUrl = cvBaseUrl
    }

    convertJsonApiObjectListToModelList (jsonApiObjectList: any): SamplingMedia[] {
      return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
    }

    convertJsonApiDataToModel (jsonApiData: any): SamplingMedia {
      const id = jsonApiData.id
      const name = jsonApiData.attributes.name
      const url = removeBaseUrl(jsonApiData.links.self, this.cvBaseUrl)

      return SamplingMedia.createWithData(id, name, url)
    }
}
