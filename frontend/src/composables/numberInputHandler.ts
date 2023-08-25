import { ref } from 'vue'

/**
 * Composable function to handle number input for currency
 * @param callback Function to be called when the input value changes
 * @param precision Number of decimal places to round the input value to (default: 2)
 * @param factor Factor to multiply the input value by (default: 100)
 */
export const useNumberInputHandler = (
  defaultVal: number = 0,
  callback: (value: number) => void = () => {},
  precision: number = 2,
  factor: number = 1
) => {
  let formattedValue = ref(defaultVal)
  const inputHandler = (event: Event) => {
    const inputValue = (event.target as HTMLInputElement).value
    const parsedValue = parseFloat(inputValue)

    if (isNaN(parsedValue)) {
      return
    }

    const value =
      Math.abs(parseFloat(parsedValue.toFixed(precision))) * factor
    formattedValue.value = value / factor
    callback(value)
  }
  return {
    formattedValue,
    inputHandler
  }
}
