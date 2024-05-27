<!--
SPDX-FileCopyrightText: 2021 - 2024
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Norman Ziegner <norman.ziegner@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->

# Vuex + TypeScript

To ensure type compatibility when using `state`, `actions` and `getters` from
the store in custom components, you have to define and export the types
explicitly in the store modules as shown in the following sections.

Some more details can be found at
<https://typescript.nuxtjs.org/cookbook/store#vanilla>.

## State

Either explicitly describe the type of the state:

```typescript
export interface MyState {
  foo: string
}
const state = (): MyState => ({
  foo: 'bar'
})

export default {
  state
}
```

or export the type of the state implicitly:

```typescript
const state = () => ({
  foo: 'bar'
})
export type MyState = ReturnType<typeof state>

export default {
  state
}
```

In a component the type of the state can be ensured as follows:

```typescript
import { mapState } from 'vuex'
import { MyState } from '@/store/my.ts'

@Component({
  computed: {
    ...mapState('my', ['foo'])
  }
})
class MyComponent extends Vue {
  // explicitly use the type of the state to satisfy the TypeScript Compiler
  foo!: MyState['foo']
}
```

## Getters

Also the type of the getters has to be exported:

```typescript
import { GetterTree } from 'vuex'
import { RootState } from '@/store'

export type FooGetter = string

const getters: GetterTree<MyState, RootState> = {
  foo: (state: MyState): string => state.foo.replace('r', 'z')
}
```

In a component the type of the state can be ensured as follows:

```typescript
import { mapGetters } from 'vuex'
import { FooGetter } from '@/store/my.ts'

@Component({
  computed: {
    ...mapGetters('my', ['foo'])
  }
})
class MyComponent extends Vue {
  // explicitly use the type of the getter to satisfy the TypeScript Compiler
  foo!: FooGetter

  mounted () {
    const bar: string = this.foo // no type error
  }
}
```

## Actions

As the actions are functions which expose the second parameter and up, the whole
function definition has to be exported as a type:

```typescript
import { ActionTree } from 'vuex'
import { RootState } from '@/store'

export type LoadAction = (id: number) => Promise<void>

const actions: ActionTree<MyState, RootState> = {
  async load ({ commit }: { commit: Commit }, id: number): Promise<void> {
    const result = someApi.load(id) // load the entity
    commit('setResult', result)
  }
}
```

As with the getters, the type of the action can now be used in the component:

```typescript
import { mapActions } from 'vuex'
import { LoadAction } from '@/store/my.ts'

@Component({
  methods: {
    ...mapActions('my', ['load'])
  }
})
class MyComponent extends Vue {
  // explicitly use the type of the action to satisfy the TypeScript Compiler
  load!: LoadAction

  async fetch (): Promise<void> {
    await this.load(123) // no type error and full LSP support
  }
}
```

## Remarks

I've played around by defining the types of the getters and actions by reusing
the types from the function definition with the help of TypeScript utility
types, which would be much more flexible. The idea was to use
`ReturnType` and `Parameters`, eg.:

```typescript
import { ActionTree } from 'vuex'
import { RootState } from '@/store'

const actions: ActionTree<MyState, RootState> = {
  async load ({ commit }: { commit: Commit }, id: number): Promise<void> {
    const result = someApi.load(id) // load the entity
    commit('setResult', result)
  }
}

export type LoadAction = (params: Parameters<typeof actions['load']>[1]) => ReturnType<typeof actions['load']>
```

But unfortunately this produces the following TypeScript error:

```
Type 'Action<MyState, {}>' does not satisfy the constraint '(...args: any) => any'.
  Type 'ActionObject<MyState, {}>' is not assignable to type '(...args: any) => any'.
    Type 'ActionObject<MyState, {}>' provides no match for the signature '(...args: any): any'.
```

