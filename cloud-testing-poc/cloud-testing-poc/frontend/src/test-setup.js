import '@testing-library/jest-dom'

// Mock window.confirm for tests
Object.defineProperty(window, 'confirm', {
  writable: true,
  value: vi.fn(() => true),
})

