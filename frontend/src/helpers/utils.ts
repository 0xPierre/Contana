import currency from 'currency.js'
import strftime from 'strftime'

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

// @ts-ignore
export const strftimeFR = strftime.localizeByIdentifier('fr_FR')
