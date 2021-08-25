import { Project } from '@/models/Project'

export interface IConfigurationSearchOption{
  searchText: string
  selectedConfigurationStates: Array<string>,
  selectedLocationTypes: Array<string>
  selectedProjects: Project[]
}
