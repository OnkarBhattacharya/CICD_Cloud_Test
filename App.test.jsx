/**
 * Frontend Tests for User Management App
 * Demonstrates frontend testing in cloud applications
 */
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest'
import App from '../App'

// Mock fetch globally
global.fetch = vi.fn()

describe('User Management App', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the app title and description', () => {
    // Mock empty users response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    })

    render(<App />)
    
    expect(screen.getByText('Cloud Testing PoC - User Management')).toBeInTheDocument()
    expect(screen.getByText('Demonstration of testing strategies for cloud applications')).toBeInTheDocument()
  })

  it('displays loading state initially', () => {
    // Mock delayed response
    fetch.mockImplementationOnce(() => new Promise(() => {}))

    render(<App />)
    
    expect(screen.getByText('Loading users...')).toBeInTheDocument()
  })

  it('displays empty state when no users exist', async () => {
    // Mock empty users response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    })

    render(<App />)
    
    await waitFor(() => {
      expect(screen.getByText('No users found. Add your first user above.')).toBeInTheDocument()
    })
  })

  it('displays users when they exist', async () => {
    // Mock users response
    const mockUsers = [
      { id: 1, username: 'testuser1', email: 'test1@example.com' },
      { id: 2, username: 'testuser2', email: 'test2@example.com' }
    ]

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers
    })

    render(<App />)
    
    await waitFor(() => {
      expect(screen.getByText('testuser1')).toBeInTheDocument()
      expect(screen.getByText('test1@example.com')).toBeInTheDocument()
      expect(screen.getByText('testuser2')).toBeInTheDocument()
      expect(screen.getByText('test2@example.com')).toBeInTheDocument()
      expect(screen.getByText('Users (2)')).toBeInTheDocument()
    })
  })

  it('handles form submission for creating a new user', async () => {
    // Mock initial empty users response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    })

    // Mock create user response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, username: 'newuser', email: 'new@example.com' })
    })

    // Mock updated users response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [{ id: 1, username: 'newuser', email: 'new@example.com' }]
    })

    render(<App />)
    
    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('No users found. Add your first user above.')).toBeInTheDocument()
    })

    // Fill out the form
    const usernameInput = screen.getByPlaceholderText('Enter username')
    const emailInput = screen.getByPlaceholderText('Enter email')
    const submitButton = screen.getByText('Add User')

    fireEvent.change(usernameInput, { target: { value: 'newuser' } })
    fireEvent.change(emailInput, { target: { value: 'new@example.com' } })
    fireEvent.click(submitButton)

    // Verify API call was made
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'newuser', email: 'new@example.com' })
      })
    })
  })

  it('validates form fields before submission', async () => {
    // Mock initial empty users response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    })

    render(<App />)
    
    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('No users found. Add your first user above.')).toBeInTheDocument()
    })

    // Try to submit empty form
    const submitButton = screen.getByText('Add User')
    fireEvent.click(submitButton)

    // Should show validation error
    await waitFor(() => {
      expect(screen.getByText('Please fill in all fields')).toBeInTheDocument()
    })

    // Verify no API call was made for user creation
    expect(fetch).toHaveBeenCalledTimes(1) // Only the initial fetch
  })

  it('handles edit user functionality', async () => {
    // Mock initial users response
    const mockUsers = [
      { id: 1, username: 'testuser', email: 'test@example.com' }
    ]

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers
    })

    render(<App />)
    
    // Wait for users to load
    await waitFor(() => {
      expect(screen.getByText('testuser')).toBeInTheDocument()
    })

    // Click edit button (using simpler approach)
    const buttons = screen.getAllByRole('button')
    // The edit button should be the first button in the user row (before delete)
    const editButton = buttons.find(button => {
      const svg = button.querySelector('svg')
      return svg && svg.classList.toString().includes('edit')
    })
    
    if (!editButton) {
      // Fallback: find by position (edit is typically before delete)
      const userRow = screen.getByText('testuser').closest('div')
      const rowButtons = userRow.querySelectorAll('button')
      fireEvent.click(rowButtons[0]) // First button should be edit
    } else {
      fireEvent.click(editButton)
    }

    // Verify form is populated with user data
    expect(screen.getByDisplayValue('testuser')).toBeInTheDocument()
    expect(screen.getByDisplayValue('test@example.com')).toBeInTheDocument()
    expect(screen.getByText('Edit User')).toBeInTheDocument()
    expect(screen.getByText('Update User')).toBeInTheDocument()
  })

  it('handles delete user functionality', async () => {
    // Mock initial users response
    const mockUsers = [
      { id: 1, username: 'testuser', email: 'test@example.com' }
    ]

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers
    })

    // Mock window.confirm
    window.confirm = vi.fn(() => true)

    // Mock delete response
    fetch.mockResolvedValueOnce({
      ok: true
    })

    // Mock updated empty users response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    })

    render(<App />)
    
    // Wait for users to load
    await waitFor(() => {
      expect(screen.getByText('testuser')).toBeInTheDocument()
    })

    // Click delete button (using more specific selector)
    const deleteButtons = screen.getAllByRole('button')
    const deleteButton = deleteButtons.find(button => 
      button.querySelector('svg[class*="trash"]') || 
      button.querySelector('svg[class*="lucide-trash"]')
    )
    expect(deleteButton).toBeTruthy()
    fireEvent.click(deleteButton)

    // Verify confirmation was shown
    expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to delete this user?')

    // Verify delete API call was made
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/users/1', { method: 'DELETE' })
    })
  })

  it('handles API errors gracefully', async () => {
    // Mock failed API response
    fetch.mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    
    // Should display error message
    await waitFor(() => {
      expect(screen.getByText(/Failed to load users: Network error/)).toBeInTheDocument()
    })
  })

  it('handles cancel edit functionality', async () => {
    // Mock initial users response
    const mockUsers = [
      { id: 1, username: 'testuser', email: 'test@example.com' }
    ]

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers
    })

    render(<App />)
    
    // Wait for users to load
    await waitFor(() => {
      expect(screen.getByText('testuser')).toBeInTheDocument()
    })

    // Click edit button (using simpler approach)
    const buttons = screen.getAllByRole('button')
    // The edit button should be the first button in the user row (before delete)
    const editButton = buttons.find(button => {
      const svg = button.querySelector('svg')
      return svg && svg.classList.toString().includes('edit')
    })
    
    if (!editButton) {
      // Fallback: find by position (edit is typically before delete)
      const userRow = screen.getByText('testuser').closest('div')
      const rowButtons = userRow.querySelectorAll('button')
      fireEvent.click(rowButtons[0]) // First button should be edit
    } else {
      fireEvent.click(editButton)
    }

    // Verify we're in edit mode
    expect(screen.getByText('Edit User')).toBeInTheDocument()

    // Click cancel button
    const cancelButton = screen.getByText('Cancel')
    fireEvent.click(cancelButton)

    // Verify we're back to add mode
    expect(screen.getByText('Add New User')).toBeInTheDocument()
    expect(screen.getByText('Add User')).toBeInTheDocument()
    
    // Verify form is cleared
    expect(screen.getByPlaceholderText('Enter username')).toHaveValue('')
    expect(screen.getByPlaceholderText('Enter email')).toHaveValue('')
  })
})

