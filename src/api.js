const API_BASE_URL = 'http://localhost:5000';

export async function loginUser(credentials) {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'PUT', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(credentials), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Login failed');
    }

    return response.status;
}

export async function registerUser(credentials) {
    const response = await fetch(`${API_BASE_URL}/signup`, {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        }, body: JSON.stringify(credentials), credentials: 'include',
    });

    if (!response.ok) {
        throw new Error('Login failed');
    }
    return response.status;
}
