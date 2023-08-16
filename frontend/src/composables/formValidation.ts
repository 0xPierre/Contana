import { reactive } from 'vue'
// @ts-ignore
import { useVuelidate } from '@vuelidate/core'

interface Rules {
  [key: string]: any
}

const useFormValidation = <T extends Object>(state: T, rules: Rules) => {
  const formState = reactive({ ...state })

  const v$ = useVuelidate(rules, formState)

  const reset = () => {
    Object.assign(formState, state)
    v$.value.$reset()
  }

  return {
    formState,
    v$,
    reset
  }
}
export { useFormValidation }
