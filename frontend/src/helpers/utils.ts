export const fullNameToText = (fullName: string) => {
  const [firstName, lastName] = fullName.split(' ')
  return `${firstName[0]}${lastName[0]}`
}
