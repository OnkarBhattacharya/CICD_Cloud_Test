import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Trash2, Edit, Plus, Users } from 'lucide-react'
import './App.css'

function App() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({ username: '', email: '' })
  const [editingUser, setEditingUser] = useState(null)

  // Fetch users from API
  const fetchUsers = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/users')
      if (!response.ok) throw new Error('Failed to fetch users')
      const data = await response.json()
      setUsers(data)
      setError('')
    } catch (err) {
      setError('Failed to load users: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  // Create or update user
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.username || !formData.email) {
      setError('Please fill in all fields')
      return
    }

    setLoading(true)
    try {
      const url = editingUser ? `/api/users/${editingUser.id}` : '/api/users'
      const method = editingUser ? 'PUT' : 'POST'
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      
      if (!response.ok) throw new Error('Failed to save user')
      
      setFormData({ username: '', email: '' })
      setEditingUser(null)
      setError('')
      await fetchUsers()
    } catch (err) {
      setError('Failed to save user: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  // Delete user
  const handleDelete = async (userId) => {
    if (!confirm('Are you sure you want to delete this user?')) return
    
    setLoading(true)
    try {
      const response = await fetch(`/api/users/${userId}`, { method: 'DELETE' })
      if (!response.ok) throw new Error('Failed to delete user')
      
      setError('')
      await fetchUsers()
    } catch (err) {
      setError('Failed to delete user: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  // Start editing user
  const handleEdit = (user) => {
    setEditingUser(user)
    setFormData({ username: user.username, email: user.email })
  }

  // Cancel editing
  const handleCancel = () => {
    setEditingUser(null)
    setFormData({ username: '', email: '' })
  }

  // Load users on component mount
  useEffect(() => {
    fetchUsers()
  }, [])

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-2 mb-2">
          <Users className="h-8 w-8" />
          Cloud Testing PoC - User Management
        </h1>
        <p className="text-gray-600">
          Demonstration of testing strategies for cloud applications
        </p>
      </div>

      {error && (
        <Alert className="mb-6 border-red-200 bg-red-50">
          <AlertDescription className="text-red-800">{error}</AlertDescription>
        </Alert>
      )}

      {/* User Form */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Plus className="h-5 w-5" />
            {editingUser ? 'Edit User' : 'Add New User'}
          </CardTitle>
          <CardDescription>
            {editingUser ? 'Update user information' : 'Create a new user account'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Username</label>
                <Input
                  type="text"
                  placeholder="Enter username"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  disabled={loading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <Input
                  type="email"
                  placeholder="Enter email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  disabled={loading}
                />
              </div>
            </div>
            <div className="flex gap-2">
              <Button type="submit" disabled={loading}>
                {loading ? 'Saving...' : (editingUser ? 'Update User' : 'Add User')}
              </Button>
              {editingUser && (
                <Button type="button" variant="outline" onClick={handleCancel}>
                  Cancel
                </Button>
              )}
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Users List */}
      <Card>
        <CardHeader>
          <CardTitle>Users ({users.length})</CardTitle>
          <CardDescription>Manage your user accounts</CardDescription>
        </CardHeader>
        <CardContent>
          {loading && users.length === 0 ? (
            <p className="text-center py-8 text-gray-500">Loading users...</p>
          ) : users.length === 0 ? (
            <p className="text-center py-8 text-gray-500">No users found. Add your first user above.</p>
          ) : (
            <div className="space-y-3">
              {users.map((user) => (
                <div key={user.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium">{user.username}</h3>
                    <p className="text-sm text-gray-600">{user.email}</p>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleEdit(user)}
                      disabled={loading}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDelete(user.id)}
                      disabled={loading}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default App
