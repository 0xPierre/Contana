import currency from 'currency.js'

export const fullNameToText = (fullName: string) => {
  const [firstName, lastName] = fullName.split(' ')
  return `${firstName[0]}${lastName[0]}`
}

export const euro = (value: string | number): currency =>
  currency(value, {
    symbol: '',
    decimal: ',',
    separator: ' ',
    precision: 2
  })
