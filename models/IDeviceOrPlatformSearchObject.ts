import { PlatformOrDeviceType } from '../enums/PlatformOrDeviceType'

export interface IDeviceOrPlatformSearchObject {
  id: number | null,
  name: string,
  type: string,
  searchType: PlatformOrDeviceType,
  project: string,
  status: string
}
