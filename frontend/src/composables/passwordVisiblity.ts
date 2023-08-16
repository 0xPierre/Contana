import { ref, computed } from 'vue'

const usePasswordVisibility = () => {
  const passwordFieldType = ref('password')

  const togglePasswordVisibility = () => {
    if (passwordFieldType.value === 'password') {
      passwordFieldType.value = 'text'
    } else {
      passwordFieldType.value = 'password'
    }
  }
  const passwordIcon = computed(() => {
    if (passwordFieldType.value === 'password') {
      return 'eye'
    } else {
      return 'eye-off'
    }
  })

  return {
    passwordFieldType,
    togglePasswordVisibility,
    passwordIcon
  }
}

export { usePasswordVisibility }
