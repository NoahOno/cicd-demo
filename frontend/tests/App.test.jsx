import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi, afterEach } from 'vitest'
import App from '../src/App'

afterEach(() => {
  vi.restoreAllMocks()
})

describe('App', () => {
  it('renders the title', () => {
    global.fetch = vi.fn().mockResolvedValue({ json: vi.fn().mockResolvedValue([]) })
    render(<App />)
    expect(screen.getByText('Todo App')).toBeInTheDocument()
  })

  it('renders the input and add button', () => {
    global.fetch = vi.fn().mockResolvedValue({ json: vi.fn().mockResolvedValue([]) })
    render(<App />)
    expect(screen.getByPlaceholderText('Add a todo...')).toBeInTheDocument()
    expect(screen.getByText('Add')).toBeInTheDocument()
  })
})
