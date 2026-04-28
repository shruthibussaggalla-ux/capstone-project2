/**
 * Dashboard Module
 * Main dashboard functionality
 */

let currentPage = 'dashboard';
let pomodoroTimer = null;
let pomodoroTime = 25 * 60; // 25 minutes in seconds
let isTimerRunning = false;

document.addEventListener('DOMContentLoaded', function () {
    initializeDashboard();
});

function initializeDashboard() {
    // Check authentication
    if (!api.isAuthenticated()) {
        window.location.href = '/frontend/auth.html';
        return;
    }

    // Set user name
    if (api.user) {
        document.getElementById('userName').textContent = api.user.username;
    }

    // Initialize navigation
    initializeNavigation();

    // Initialize logout
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);

    // Initialize modals
    initializeModals();

    // Load dashboard data
    loadDashboardData();

    // Load page content
    document.getElementById('addNewBtn').addEventListener('click', handleAddNew);
}

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            navigateToPage(page);
        });
    });
}

function navigateToPage(page) {
    // Hide all pages
    document.querySelectorAll('.page-section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active class from nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-page') === page) {
            link.classList.add('active');
        }
    });

    // Show selected page
    document.getElementById(`${page}-page`).classList.add('active');

    // Update page title
    const titles = {
        'dashboard': 'Dashboard',
        'courses': 'My Courses',
        'planner': 'Study Planner',
        'tasks': 'Study Tasks',
        'schedule': 'Study Schedule',
        'analytics': 'Analytics & Progress',
        'recommendations': 'Smart Recommendations',
        'profile': 'User Profile',
    };
    document.getElementById('pageTitle').textContent = titles[page] || 'Dashboard';

    currentPage = page;

    // Load page-specific data
    loadPageData(page);
}

function loadPageData(page) {
    switch (page) {
        case 'courses':
            loadCoursesPage();
            break;
        case 'planner':
            loadPlannerPage();
            break;
        case 'tasks':
            loadTasksPage();
            break;
        case 'schedule':
            loadSchedulePage();
            break;
        case 'analytics':
            loadAnalyticsPage();
            break;
        case 'recommendations':
            loadRecommendationsPage();
            break;
        case 'profile':
            loadProfilePage();
            break;
    }
}

async function loadDashboardData() {
    try {
        const data = await api.getDashboard();

        // Update stats
        document.getElementById('totalStudyHours').textContent = data.total_study_hours.toFixed(1);
        document.getElementById('tasksCompleted').textContent = data.tasks_completed;
        document.getElementById('avgProductivity').textContent = data.average_productivity.toFixed(1);
        document.getElementById('streakDays').textContent = data.streak_days;
        document.getElementById('activeCourses').textContent = data.courses_active;
        document.getElementById('pendingTasks').textContent = data.tasks_pending;

        // Calculate completion rate
        const completionRate = data.tasks_completed + data.tasks_pending > 0
            ? Math.round((data.tasks_completed / (data.tasks_completed + data.tasks_pending)) * 100)
            : 0;
        document.getElementById('completionRate').textContent = completionRate + '%';

        // Populate upcoming tasks
        displayUpcomingTasks(data.upcoming_tasks);

        // Populate today's schedule
        displayTodaySchedule(data.today_sessions);

        // Populate recommendations
        displayRecommendations(data.recommendations);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function displayUpcomingTasks(tasks) {
    const container = document.getElementById('upcomingTasks');
    container.innerHTML = '';

    if (tasks.length === 0) {
        container.innerHTML = '<p class="empty-state">No upcoming tasks</p>';
        return;
    }

    tasks.forEach(task => {
        const daysUntilDue = task.days_until_due;
        let statusClass = '';
        if (daysUntilDue < 0) statusClass = 'overdue';
        else if (daysUntilDue <= 3) statusClass = 'due-soon';

        const html = `
            <div class="task-item ${statusClass}">
                <div class="task-item-header">
                    <div>
                        <div class="task-title">${escapeHtml(task.title)}</div>
                        <div class="task-meta">${escapeHtml(task.course_name)}</div>
                    </div>
                    <span class="task-priority priority-${task.priority.toLowerCase()}">${task.priority}</span>
                </div>
                <div class="task-meta">Due: ${formatDate(task.due_date)}</div>
            </div>
        `;
        container.innerHTML += html;
    });
}

function displayTodaySchedule(sessions) {
    const container = document.getElementById('todaySchedule');
    container.innerHTML = '';

    if (sessions.length === 0) {
        container.innerHTML = '<p class="empty-state">No sessions scheduled for today</p>';
        return;
    }

    sessions.forEach(session => {
        const html = `
            <div class="session-item">
                <div class="session-time">${session.scheduled_time}</div>
                <div class="session-title">${escapeHtml(session.title)}</div>
                <div class="session-duration">Duration: ${session.duration_minutes} minutes</div>
                <div class="task-meta">${escapeHtml(session.course_name)}</div>
            </div>
        `;
        container.innerHTML += html;
    });
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '';

    if (recommendations.length === 0) {
        container.innerHTML = '<p class="empty-state">No new recommendations</p>';
        return;
    }

    recommendations.slice(0, 3).forEach(rec => {
        const html = `
            <div class="recommendation-item">
                <h4>${escapeHtml(rec.title)}</h4>
                <p>${escapeHtml(rec.description)}</p>
                ${rec.action_item ? `<p><strong>Action:</strong> ${escapeHtml(rec.action_item)}</p>` : ''}
            </div>
        `;
        container.innerHTML += html;
    });
}

async function loadCoursesPage() {
    try {
        const data = await api.getCourses();
        const courses = data.results || data;
        const container = document.getElementById('coursesList');
        container.innerHTML = '';

        if (courses.length === 0) {
            container.innerHTML = '<p class="empty-state">No courses yet. Add one to get started!</p>';
            return;
        }

        courses.forEach(course => {
            const html = `
                <div class="course-card" style="border-top: 4px solid ${course.color}">
                    <div class="course-header" style="background: linear-gradient(135deg, ${course.color} 0%, ${course.color}dd 100%)">
                        <div class="course-code">${escapeHtml(course.code)}</div>
                        <h3 class="course-name">${escapeHtml(course.name)}</h3>
                    </div>
                    <div class="course-body">
                        <div class="course-info">
                            <div class="course-info-item">
                                <span class="course-info-label">Instructor:</span>
                                <span class="course-info-value">${escapeHtml(course.instructor || 'N/A')}</span>
                            </div>
                            <div class="course-info-item">
                                <span class="course-info-label">Credit Hours:</span>
                                <span class="course-info-value">${course.credit_hours}</span>
                            </div>
                            <div class="course-info-item">
                                <span class="course-info-label">Semester:</span>
                                <span class="course-info-value">${escapeHtml(course.semester)}</span>
                            </div>
                            <div class="course-info-item">
                                <span class="course-info-label">Tasks:</span>
                                <span class="course-info-value">${course.task_count}</span>
                            </div>
                        </div>
                        <button class="btn btn-sm btn-primary" onclick="editCourse('${course.id}')">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteCourse('${course.id}')">Delete</button>
                    </div>
                </div>
            `;
            container.innerHTML += html;
        });
    } catch (error) {
        console.error('Error loading courses:', error);
    }
}

async function loadTasksPage() {
    try {
        const data = await api.getTasks();
        const tasks = data.results || data;
        const container = document.getElementById('allTasksList');

        renderTasks(tasks);

        // Add filter functionality
        document.getElementById('taskFilter').addEventListener('change', function () {
            const filter = this.value;
            if (filter) {
                const filtered = tasks.filter(task => {
                    if (filter === 'CRITICAL' || filter === 'HIGH') {
                        return task.priority === filter;
                    }
                    return task.status === filter;
                });
                renderTasks(filtered);
            } else {
                renderTasks(tasks);
            }
        });
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

function renderTasks(tasks) {
    const container = document.getElementById('allTasksList');
    container.innerHTML = '';

    if (tasks.length === 0) {
        container.innerHTML = '<p class="empty-state">No tasks to display</p>';
        return;
    }

    tasks.forEach(task => {
        const html = `
            <div class="task-item">
                <div class="task-item-header">
                    <div>
                        <div class="task-title">${escapeHtml(task.title)}</div>
                        <div class="task-meta">${escapeHtml(task.course_name)}</div>
                    </div>
                    <span class="task-priority priority-${task.priority.toLowerCase()}">${task.priority}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${Math.min(task.actual_hours / task.estimated_hours * 100, 100)}%">
                        ${Math.round(Math.min(task.actual_hours / task.estimated_hours * 100, 100))}%
                    </div>
                </div>
                <div class="task-meta">Due: ${formatDate(task.due_date)} | Status: ${task.status}</div>
            </div>
        `;
        container.innerHTML += html;
    });
}

async function loadSchedulePage() {
    try {
        const data = await api.getSessions();
        const sessions = data.results || data;
        const container = document.getElementById('sessionsList');
        container.innerHTML = '';

        if (sessions.length === 0) {
            container.innerHTML = '<p class="empty-state">No sessions scheduled</p>';
            return;
        }

        sessions.forEach(session => {
            const html = `
                <div class="session-card">
                    <div class="session-time">${session.scheduled_time}</div>
                    <div class="session-title">${escapeHtml(session.title)}</div>
                    <div class="session-duration">Duration: ${session.duration_minutes} minutes</div>
                    <div class="task-meta">${escapeHtml(session.course_name)} | ${formatDate(session.scheduled_date)}</div>
                </div>
            `;
            container.innerHTML += html;
        });
    } catch (error) {
        console.error('Error loading schedule:', error);
    }
}

async function loadPlannerPage() {
    try {
        const data = await api.getPlans();
        const plans = data.results || data;
        const container = document.getElementById('plansList');
        container.innerHTML = '';

        if (plans.length === 0) {
            container.innerHTML = '<p class="empty-state">No study plans yet. Create one to organize your learning!</p>';
            return;
        }

        plans.forEach(plan => {
            const progressPercent = Math.min(Math.round(plan.actual_hours / plan.estimated_hours * 100), 100);
            const html = `
                <div class="goal-card">
                    <div class="goal-header">
                        <div>
                            <div class="goal-title">${escapeHtml(plan.title)}</div>
                            <div class="task-meta">${escapeHtml(plan.goal_title)}</div>
                        </div>
                        <span class="goal-badge ${plan.status === 'COMPLETED' ? 'completed' : 'in-progress'}">${plan.status}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${progressPercent}%">${progressPercent}%</div>
                    </div>
                    <div class="task-meta">From ${formatDate(plan.start_date)} to ${formatDate(plan.end_date)}</div>
                </div>
            `;
            container.innerHTML += html;
        });
    } catch (error) {
        console.error('Error loading plans:', error);
    }
}

async function loadAnalyticsPage() {
    try {
        const data = await api.getWeeklyProgress();
        const logs = data.results || data;

        // Prepare data for charts
        const dates = logs.map(log => formatDate(log.date));
        const studyHours = logs.map(log => log.study_hours_today);
        const productivity = logs.map(log => log.average_productivity_score);

        // Weekly chart
        if (document.getElementById('weeklyChart')) {
            new Chart(document.getElementById('weeklyChart'), {
                type: 'bar',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Study Hours',
                        data: studyHours,
                        backgroundColor: '#3498db',
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                        }
                    }
                }
            });
        }

        // Productivity chart
        if (document.getElementById('productivityChart')) {
            new Chart(document.getElementById('productivityChart'), {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Productivity Score',
                        data: productivity,
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        fill: true,
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10,
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

async function loadRecommendationsPage() {
    try {
        const data = await api.getRecommendations();
        const recommendations = data.results || data;
        const container = document.getElementById('allRecommendations');
        container.innerHTML = '';

        if (recommendations.length === 0) {
            container.innerHTML = '<p class="empty-state">No recommendations available</p>';
            return;
        }

        recommendations.forEach(rec => {
            const html = `
                <div class="recommendation-item">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                        <div>
                            <h4>${escapeHtml(rec.title)}</h4>
                            <span class="task-meta">${rec.recommendation_type}</span>
                        </div>
                        <span class="stat-value" style="font-size: 1rem;">${(rec.confidence_score * 100).toFixed(0)}%</span>
                    </div>
                    <p>${escapeHtml(rec.description)}</p>
                    ${rec.action_item ? `<p><strong>Action:</strong> ${escapeHtml(rec.action_item)}</p>` : ''}
                </div>
            `;
            container.innerHTML += html;
        });
    } catch (error) {
        console.error('Error loading recommendations:', error);
    }
}

async function loadProfilePage() {
    try {
        const data = await api.getProfile();
        if (data.results) {
            const profile = data.results[0];
            document.getElementById('learningStyle').value = profile.learning_style;
            document.getElementById('dailyGoal').value = profile.daily_study_goal_hours;
            document.getElementById('preferredTime').value = profile.preferred_study_time;
            document.getElementById('notificationEnabled').checked = profile.notification_enabled;
            document.getElementById('weeklyReportEnabled').checked = profile.weekly_report_enabled;
        }

        document.getElementById('profileForm').addEventListener('submit', handleProfileUpdate);
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

async function handleProfileUpdate(e) {
    e.preventDefault();

    const profileData = {
        learning_style: document.getElementById('learningStyle').value,
        daily_study_goal_hours: parseFloat(document.getElementById('dailyGoal').value),
        preferred_study_time: document.getElementById('preferredTime').value,
        notification_enabled: document.getElementById('notificationEnabled').checked,
        weekly_report_enabled: document.getElementById('weeklyReportEnabled').checked,
    };

    try {
        await api.updateProfile(profileData);
        alert('Profile updated successfully!');
    } catch (error) {
        alert('Error updating profile: ' + error.message);
    }
}

function initializeModals() {
    const courseModal = document.getElementById('courseModal');
    const courseForm = document.getElementById('courseForm');
    const modalCloses = document.querySelectorAll('.modal-close');

    document.getElementById('addCourseBtn').addEventListener('click', function () {
        courseModal.classList.add('show');
    });

    modalCloses.forEach(close => {
        close.addEventListener('click', function () {
            this.closest('.modal').classList.remove('show');
        });
    });

    window.addEventListener('click', function (event) {
        if (event.target.classList.contains('modal')) {
            event.target.classList.remove('show');
        }
    });

    courseForm.addEventListener('submit', handleAddCourse);
}

async function handleAddCourse(e) {
    e.preventDefault();

    const courseData = {
        name: document.querySelector('#courseForm input[name="name"]').value,
        code: document.querySelector('#courseForm input[name="code"]').value,
        credit_hours: parseInt(document.querySelector('#courseForm input[name="credit_hours"]').value),
        instructor: document.querySelector('#courseForm input[name="instructor"]').value,
        semester: document.querySelector('#courseForm input[name="semester"]').value,
        color: document.querySelector('#courseForm input[name="color"]').value,
    };

    try {
        await api.createCourse(courseData);
        alert('Course added successfully!');
        document.getElementById('courseModal').classList.remove('show');
        document.getElementById('courseForm').reset();
        loadCoursesPage();
    } catch (error) {
        alert('Error adding course: ' + error.message);
    }
}

function handleAddNew() {
    if (currentPage === 'courses') {
        document.getElementById('courseModal').classList.add('show');
    }
}

async function handleLogout() {
    try {
        await api.logout();
        window.location.href = '/frontend/auth.html';
    } catch (error) {
        console.error('Error logging out:', error);
    }
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
