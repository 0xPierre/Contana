export const useInputImageRenderer = (inputEl: any, callback: any) => {
  const inputImageRenderer = () => {
    const file = inputEl.value.files[0]
    const reader = new FileReader()

    reader.addEventListener(
      'load',
      () => {
        callback(reader.result)
      },
      false
    )

    if (file) {
      reader.readAsDataURL(file)
    }
  }
  return {
    inputImageRenderer
  }
}
