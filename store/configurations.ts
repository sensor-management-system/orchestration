import { ActionContext } from 'vuex/types'
import { Configuration } from '@/models/Configuration'
import { Project } from '@/models/Project'

export interface ConfigurationsStoreState {
  configuration: Configuration,
  projects: Project[],
  configurationStates: string[]
}

export const state = (): ConfigurationsStoreState => {
  return {
    configuration: new Configuration(),
    projects: [],
    configurationStates: []
  }
}

export const mutations = {
  setConfiguration (state: ConfigurationsStoreState, configuration: Configuration) {
    state.configuration = configuration
  },
  setProjects (state: ConfigurationsStoreState, projects: Project[]) {
    state.projects = projects
  },
  setConfigurationsStates (state: ConfigurationsStoreState, configurationStates: string[]) {
    state.configurationStates = configurationStates
  }
}

export const actions = {
  async loadProjects (context: ActionContext<ConfigurationsStoreState, ConfigurationsStoreState>) {
    // @ts-ignore
    const projects = await this.$api.projects.findAll()
    context.commit('setProjects', projects)
  },
  async loadConfigurationsStates (context: ActionContext<ConfigurationsStoreState, ConfigurationsStoreState>) {
    // @ts-ignore
    const configurationStates = await this.$api.configurationStates.findAll()
    context.commit('setConfigurationsStates', configurationStates)
  },
  async loadConfigurationById (context: ActionContext<ConfigurationsStoreState, ConfigurationsStoreState>, id:string) {
    // @ts-ignore
    const configuration = await this.$api.configurations.findById(id)
    context.commit('setConfiguration', configuration)
  },
  async saveConfiguration (context: ActionContext<ConfigurationsStoreState, ConfigurationsStoreState>) {
    // @ts-ignore
    const configuration = await this.$api.configurations.save(context.state.configuration)
    context.commit('setConfiguration', configuration)
  }
}

export const getters = {
  projectNames: (state: ConfigurationsStoreState) => {
    return state.projects.map((p:Project) => p.name)
  }
}
