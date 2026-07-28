/**
 * Fetch API Consumer — Module 08 Code Snap
 *
 * This file shows how to consume a REST API (Django DRF / FastAPI)
 * from a JavaScript frontend using the Fetch API.
 *
 * Usage:
 *   1. Start your backend server (Django or FastAPI)
 *   2. Include this script in your HTML: <script src="code-fetch-api-consumer.js"></script>
 *   3. Make sure CORS is enabled on your backend
 *
 * All examples use TechPath Institute student data.
 */

// ============================================================
// CONFIG — Change this to match your backend
// ============================================================
const API_BASE = 'http://localhost:8000/api';
let authToken = null;  // JWT token (set after login)


// ============================================================
// 1. GET — Fetch All Students (with pagination)
// ============================================================
async function getStudents(page = 1) {
    try {
        const response = await fetch(`${API_BASE}/students/?page=${page}`);

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Students:', data);

        // DRF returns: { count, next, previous, results }
        // FastAPI returns: { success, data, total }
        const students = data.results || data.data || data;

        // Render to page
        const container = document.getElementById('studentList');
        if (container) {
            container.innerHTML = students.map((s, i) => `
                <tr>
                    <td>${i + 1}</td>
                    <td>${s.name}</td>
                    <td>${s.email}</td>
                    <td>${s.city}</td>
                    <td>${s.marks}</td>
                    <td>
                        <button onclick="deleteStudent(${s.id})" class="btn btn-sm btn-danger">
                            Delete
                        </button>
                    </td>
                </tr>
            `).join('');
        }

        return students;
    } catch (error) {
        console.error('Failed to fetch students:', error);
        showError('Could not load students. Is your API running?');
        return [];
    }
}


// ============================================================
// 2. GET — Fetch Single Student by ID
// ============================================================
async function getStudent(id) {
    try {
        const response = await fetch(`${API_BASE}/students/${id}/`);

        if (response.status === 404) {
            showError(`Student with ID ${id} not found`);
            return null;
        }

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        console.log('Student detail:', data);
        return data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}


// ============================================================
// 3. GET — Search & Filter
// ============================================================
async function searchStudents(query) {
    const params = new URLSearchParams();

    // Add search term
    if (query) params.set('search', query);

    // You can also add filters:
    // params.set('city', 'Bhopal');
    // params.set('course', '1');
    // params.set('ordering', '-marks');

    const url = `${API_BASE}/students/?${params.toString()}`;
    console.log('Fetching:', url);

    const response = await fetch(url);
    const data = await response.json();
    return data.results || data;
}


// ============================================================
// 4. POST — Create a New Student
// ============================================================
async function createStudent(studentData) {
    try {
        const response = await fetch(`${API_BASE}/students/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Include JWT token if your API requires authentication
                ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
            },
            body: JSON.stringify(studentData),
        });

        if (response.status === 201) {
            const created = await response.json();
            console.log('Created:', created);
            showSuccess(`Student "${created.name}" created successfully!`);
            getStudents();  // Reload the list
            return created;
        }

        if (response.status === 401) {
            showError('You must be logged in to create students.');
            return null;
        }

        if (response.status === 400 || response.status === 422) {
            const errors = await response.json();
            console.error('Validation errors:', errors);
            showError('Invalid data: ' + JSON.stringify(errors));
            return null;
        }

        throw new Error(`Unexpected response: ${response.status}`);
    } catch (error) {
        console.error('Create failed:', error);
        showError('Failed to create student.');
        return null;
    }
}


// ============================================================
// 5. PUT — Update a Student (full update)
// ============================================================
async function updateStudent(id, updatedData) {
    try {
        const response = await fetch(`${API_BASE}/students/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
            },
            body: JSON.stringify(updatedData),
        });

        if (response.ok) {
            const updated = await response.json();
            console.log('Updated:', updated);
            showSuccess(`Student "${updated.name}" updated!`);
            return updated;
        }

        throw new Error(`Update failed: ${response.status}`);
    } catch (error) {
        console.error('Update failed:', error);
        return null;
    }
}


// ============================================================
// 6. PATCH — Partial Update (change only some fields)
// ============================================================
async function patchStudent(id, partialData) {
    // Example: patchStudent(1, { marks: 90 })
    // Only sends the fields you want to change
    try {
        const response = await fetch(`${API_BASE}/students/${id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
            },
            body: JSON.stringify(partialData),
        });

        if (response.ok) {
            const updated = await response.json();
            console.log('Patched:', updated);
            return updated;
        }

        throw new Error(`Patch failed: ${response.status}`);
    } catch (error) {
        console.error('Patch failed:', error);
        return null;
    }
}


// ============================================================
// 7. DELETE — Remove a Student
// ============================================================
async function deleteStudent(id) {
    if (!confirm('Are you sure you want to delete this student?')) return;

    try {
        const response = await fetch(`${API_BASE}/students/${id}/`, {
            method: 'DELETE',
            headers: {
                ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
            },
        });

        if (response.status === 204 || response.ok) {
            console.log(`Student ${id} deleted`);
            showSuccess('Student deleted successfully!');
            getStudents();  // Reload the list
            return true;
        }

        if (response.status === 401) {
            showError('You must be logged in to delete students.');
            return false;
        }

        throw new Error(`Delete failed: ${response.status}`);
    } catch (error) {
        console.error('Delete failed:', error);
        return false;
    }
}


// ============================================================
// 8. JWT Authentication — Login
// ============================================================
async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE}/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const tokens = await response.json();
            authToken = tokens.access;

            // Store token (for page refresh persistence)
            localStorage.setItem('access_token', tokens.access);
            localStorage.setItem('refresh_token', tokens.refresh);

            console.log('Logged in successfully');
            showSuccess('Login successful!');
            return true;
        }

        showError('Invalid username or password');
        return false;
    } catch (error) {
        console.error('Login failed:', error);
        return false;
    }
}


// ============================================================
// 9. JWT Token Refresh
// ============================================================
async function refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return false;

    try {
        const response = await fetch(`${API_BASE}/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh }),
        });

        if (response.ok) {
            const data = await response.json();
            authToken = data.access;
            localStorage.setItem('access_token', data.access);
            return true;
        }

        // Refresh token expired — must login again
        logout();
        return false;
    } catch (error) {
        console.error('Token refresh failed:', error);
        return false;
    }
}

function logout() {
    authToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    console.log('Logged out');
}


// ============================================================
// 10. Form Submission Handler
// ============================================================
function setupForm() {
    const form = document.getElementById('studentForm');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const studentData = {
            name: formData.get('name'),
            email: formData.get('email'),
            city: formData.get('city') || 'Bhopal',
            course: parseInt(formData.get('course')) || 1,
            marks: parseInt(formData.get('marks')) || 0,
        };

        const result = await createStudent(studentData);
        if (result) {
            form.reset();
        }
    });
}


// ============================================================
// 11. Live Search with Debounce
// ============================================================
let searchTimeout;
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    searchInput.addEventListener('input', (event) => {
        // Debounce: wait 300ms after user stops typing
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(async () => {
            const query = event.target.value.trim();
            if (query.length >= 2) {
                const results = await searchStudents(query);
                renderStudentList(results);
            } else if (query.length === 0) {
                getStudents();
            }
        }, 300);
    });
}

function renderStudentList(students) {
    const container = document.getElementById('studentList');
    if (!container) return;

    container.innerHTML = students.map((s, i) => `
        <tr>
            <td>${i + 1}</td>
            <td>${s.name}</td>
            <td>${s.email}</td>
            <td>${s.city}</td>
            <td>${s.marks}</td>
        </tr>
    `).join('');
}


// ============================================================
// 12. Streaming AI Response (SSE — Server-Sent Events)
// ============================================================
async function streamAIResponse(prompt) {
    const outputDiv = document.getElementById('aiOutput');
    if (!outputDiv) return;

    outputDiv.textContent = '';
    outputDiv.style.opacity = '1';

    try {
        const response = await fetch(
            `${API_BASE}/chat/stream?prompt=${encodeURIComponent(prompt)}`
        );

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const word = line.slice(6).trim();
                    if (word === '[DONE]') {
                        console.log('Stream complete');
                        return;
                    }
                    outputDiv.textContent += word + ' ';
                }
            }
        }
    } catch (error) {
        console.error('Streaming failed:', error);
        outputDiv.textContent = 'Error: Could not connect to AI endpoint.';
    }
}


// ============================================================
// Helper Functions
// ============================================================
function showSuccess(message) {
    const alertDiv = document.getElementById('alertArea');
    if (alertDiv) {
        alertDiv.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>`;
    }
    console.log('SUCCESS:', message);
}

function showError(message) {
    const alertDiv = document.getElementById('alertArea');
    if (alertDiv) {
        alertDiv.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>`;
    }
    console.error('ERROR:', message);
}


// ============================================================
// Initialize on Page Load
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    // Restore token from localStorage
    authToken = localStorage.getItem('access_token');

    // Setup event listeners
    setupForm();
    setupSearch();

    // Load students
    getStudents();

    console.log('TechPath API Consumer loaded');
    console.log('API Base:', API_BASE);
    console.log('Auth:', authToken ? 'Logged in' : 'Not logged in');
});
