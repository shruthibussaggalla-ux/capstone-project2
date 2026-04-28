/**
 * API Service for SmartStudy Planner
 * Handles all API communications with the backend
 */

const API_BASE_URL = 'http://localhost:8000/api';

class APIService {
    constructor() {
        this.token = localStorage.getItem('token');
        this.user = JSON.parse(localStorage.getItem('user')) || null;
    }

    // ============= Authentication =============
    async register(username, email, password, firstName, lastName) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    email,
                    password,
                    first_name: firstName,
                    last_name: lastName,
                }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Registration failed');
            }

            const data = await response.json();
            this.setToken(data.token);
            this.setUser(data.user);
            return data;
        } catch (error) {
            throw error;
        }
    }

    async login(username, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Login failed');
            }

            const data = await response.json();
            this.setToken(data.token);
            this.setUser(data.user);
            return data;
        } catch (error) {
            throw error;
        }
    }

    async logout() {
        try {
            await fetch(`${API_BASE_URL}/auth/logout/`, {
                method: 'POST',
                headers: this.getHeaders(),
            });
        } finally {
            this.clearToken();
            this.clearUser();
        }
    }

    // ============= Token & User =============
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('token');
    }

    setUser(user) {
        this.user = user;
        localStorage.setItem('user', JSON.stringify(user));
    }

    clearUser() {
        this.user = null;
        localStorage.removeItem('user');
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (this.token) {
            headers['Authorization'] = `Token ${this.token}`;
        }
        return headers;
    }

    isAuthenticated() {
        return !!this.token;
    }

    // ============= Dashboard =============
    async getDashboard() {
        return this.get('/dashboard/');
    }

    // ============= Courses =============
    async getCourses(semester = null) {
        if (semester) {
            return this.get(`/courses/by_semester/?semester=${semester}`);
        }
        return this.get('/courses/');
    }

    async createCourse(courseData) {
        return this.post('/courses/', courseData);
    }

    async updateCourse(id, courseData) {
        return this.put(`/courses/${id}/`, courseData);
    }

    async deleteCourse(id) {
        return this.delete(`/courses/${id}/`);
    }

    // ============= Study Goals =============
    async getGoals() {
        return this.get('/goals/');
    }

    async getActiveGoals() {
        return this.get('/goals/active/');
    }

    async createGoal(goalData) {
        return this.post('/goals/', goalData);
    }

    async updateGoal(id, goalData) {
        return this.put(`/goals/${id}/`, goalData);
    }

    async deleteGoal(id) {
        return this.delete(`/goals/${id}/`);
    }

    // ============= Study Plans =============
    async getPlans() {
        return this.get('/plans/');
    }

    async getActivePlans() {
        return this.get('/plans/active/');
    }

    async createPlan(planData) {
        return this.post('/plans/', planData);
    }

    async updatePlan(id, planData) {
        return this.put(`/plans/${id}/`, planData);
    }

    async deletePlan(id) {
        return this.delete(`/plans/${id}/`);
    }

    // ============= Study Sessions =============
    async getSessions() {
        return this.get('/sessions/');
    }

    async getTodaySessions() {
        return this.get('/sessions/today/');
    }

    async getUpcomingSessions() {
        return this.get('/sessions/upcoming/');
    }

    async createSession(sessionData) {
        return this.post('/sessions/', sessionData);
    }

    async updateSession(id, sessionData) {
        return this.put(`/sessions/${id}/`, sessionData);
    }

    async deleteSession(id) {
        return this.delete(`/sessions/${id}/`);
    }

    // ============= Study Tasks =============
    async getTasks() {
        return this.get('/tasks/');
    }

    async getPendingTasks() {
        return this.get('/tasks/pending/');
    }

    async getOverdueTasks() {
        return this.get('/tasks/overdue/');
    }

    async getTasksByPriority(priority) {
        return this.get(`/tasks/by_priority/?priority=${priority}`);
    }

    async createTask(taskData) {
        return this.post('/tasks/', taskData);
    }

    async updateTask(id, taskData) {
        return this.put(`/tasks/${id}/`, taskData);
    }

    async deleteTask(id) {
        return this.delete(`/tasks/${id}/`);
    }

    // ============= User Profile =============
    async getProfile() {
        return this.get('/profile/');
    }

    async updateProfile(profileData) {
        return this.put('/profile/update/', profileData);
    }

    // ============= Progress Logs =============
    async getProgressLogs() {
        return this.get('/progress/');
    }

    async getWeeklyProgress() {
        return this.get('/progress/weekly/');
    }

    async getMonthlyProgress() {
        return this.get('/progress/monthly/');
    }

    // ============= Recommendations =============
    async getRecommendations() {
        return this.get('/recommendations/');
    }

    async markRecommendationAsRead(id) {
        return this.post('/recommendations/mark_as_read/', { id });
    }

    // ============= HTTP Methods =============
    async get(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'GET',
            headers: this.getHeaders(),
        });

        if (response.status === 401) {
            this.clearToken();
            window.location.href = '/frontend/auth.html';
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        }

        return await response.json();
    }

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data),
        });

        if (response.status === 401) {
            this.clearToken();
            window.location.href = '/frontend/auth.html';
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || error.detail || 'Request failed');
        }

        return await response.json();
    }

    async put(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify(data),
        });

        if (response.status === 401) {
            this.clearToken();
            window.location.href = '/frontend/auth.html';
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || error.detail || 'Request failed');
        }

        return await response.json();
    }

    async delete(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'DELETE',
            headers: this.getHeaders(),
        });

        if (response.status === 401) {
            this.clearToken();
            window.location.href = '/frontend/auth.html';
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || error.detail || 'Request failed');
        }

        return response.status === 204 ? null : await response.json();
    }
}

// Create global API instance
const api = new APIService();
