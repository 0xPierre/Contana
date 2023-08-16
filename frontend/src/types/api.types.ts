export interface ApiResponse<T = void> {
  status: 'success' | 'failed'
  data: T extends undefined ? never : T
  error?: string
  errors?: {
    [key: string]: string[]
  }
}

export interface ApiPaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
