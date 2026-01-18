// Configuration - Update this to match your deployed backend URL
const API_BASE_URL = 'http://localhost:8000'; // Change to your deployed URL in production
const API_KEY = 'supersecret123'; // API key for protected endpoints

// Utility function for API calls
async function apiCall(endpoint, options = {}) {
    try {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        // Add API key for PUT requests
        if (options.method === 'PUT') {
            headers['X-API-Key'] = API_KEY;
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers,
            ...options
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('API key required for this operation');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Load and display profile
async function loadProfile() {
    const profileContent = document.getElementById('profile-content');
    
    try {
        const profile = await apiCall('/profile');
        
        profileContent.innerHTML = `
            <h3>${profile.name}</h3>
            <p><strong>Email:</strong> ${profile.email}</p>
            <p><strong>Education:</strong> ${profile.education || 'Not specified'}</p>
            <p><strong>Bio:</strong> ${profile.bio || 'No bio available'}</p>
            <div class="links">
                ${profile.github ? `<a href="${profile.github}" target="_blank">GitHub</a>` : ''}
                ${profile.linkedin ? `<a href="${profile.linkedin}" target="_blank">LinkedIn</a>` : ''}
                ${profile.portfolio ? `<a href="${profile.portfolio}" target="_blank">Portfolio</a>` : ''}
            </div>
        `;
    } catch (error) {
        profileContent.innerHTML = `<div class="error">Failed to load profile: ${error.message}</div>`;
    }
}

// Load and display top skills
async function loadTopSkills() {
    const skillsContent = document.getElementById('skills-content');
    
    try {
        const skills = await apiCall('/skills/top');
        
        if (skills.length === 0) {
            skillsContent.innerHTML = '<p>No skills found.</p>';
            return;
        }
        
        const skillsHtml = skills.map(skill => 
            `<span class="skill-tag">${skill.name} (${skill.level})</span>`
        ).join('');
        
        skillsContent.innerHTML = skillsHtml;
    } catch (error) {
        skillsContent.innerHTML = `<div class="error">Failed to load skills: ${error.message}</div>`;
    }
}

// Load and display projects
let currentOffset = 0;
const PROJECTS_PER_PAGE = 3;
let allProjects = [];
let hasMoreProjects = true;

async function loadProjects(loadMore = false, skillFilter = null) {
    const projectsContent = document.getElementById('projects-content');
    
    try {
        if (!loadMore) {
            currentOffset = 0;
            allProjects = [];
            hasMoreProjects = true;
            projectsContent.innerHTML = '<p class="loading">Loading projects...</p>';
        }
        
        const params = new URLSearchParams({
            limit: PROJECTS_PER_PAGE.toString(),
            offset: currentOffset.toString()
        });
        
        if (skillFilter) {
            params.append('skill', skillFilter);
        }
        
        const endpoint = `/projects?${params.toString()}`;
        const projects = await apiCall(endpoint);
        
        if (!loadMore && projects.length === 0) {
            projectsContent.innerHTML = '<p>No projects found.</p>';
            return;
        }
        
        if (projects.length < PROJECTS_PER_PAGE) {
            hasMoreProjects = false;
        }
        
        allProjects = loadMore ? [...allProjects, ...projects] : projects;
        
        const projectsHtml = allProjects.map(project => {
            const skillsHtml = project.skills.map(skill => 
                `<span class="skill-tag">${skill.name}</span>`
            ).join('');
            
            const linksHtml = [];
            if (project.github_url) {
                linksHtml.push(`<a href="${project.github_url}" target="_blank">GitHub</a>`);
            }
            if (project.live_url) {
                linksHtml.push(`<a href="${project.live_url}" target="_blank">Live Demo</a>`);
            }
            
            return `
                <div class="project-card">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <div style="margin: 10px 0;">${skillsHtml}</div>
                    ${linksHtml.length > 0 ? `<div class="links">${linksHtml.join(' | ')}</div>` : ''}
                </div>
            `;
        }).join('');
        
        // Add load more button if there are more projects
        const loadMoreHtml = hasMoreProjects ? `
            <div style="margin-top: 20px; text-align: center;">
                <button onclick="loadMoreProjects('${skillFilter || ''}')" 
                        style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Load More Projects
                </button>
            </div>
        ` : '';
        
        projectsContent.innerHTML = projectsHtml + loadMoreHtml;
        currentOffset += PROJECTS_PER_PAGE;
    } catch (error) {
        projectsContent.innerHTML = `<div class="error">Failed to load projects: ${error.message}</div>`;
    }
}

// Helper function for load more button
function loadMoreProjects(skillFilter = null) {
    loadProjects(true, skillFilter);
}

// Search functionality
async function performSearch(query) {
    const searchResults = document.getElementById('search-results');
    
    if (!query.trim()) {
        searchResults.innerHTML = '';
        return;
    }
    
    searchResults.innerHTML = '<p class="loading">Searching...</p>';
    
    try {
        const results = await apiCall(`/search?q=${encodeURIComponent(query)}`);
        
        if (results.length === 0) {
            searchResults.innerHTML = '<p>No results found.</p>';
            return;
        }
        
        const resultsHtml = results.map(result => `
            <div class="search-result">
                <div class="search-result-type">${result.type}</div>
                <h4>${result.title}</h4>
                <p>${result.description}</p>
            </div>
        `).join('');
        
        searchResults.innerHTML = resultsHtml;
    } catch (error) {
        searchResults.innerHTML = `<div class="error">Search failed: ${error.message}</div>`;
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Load initial data
    loadProfile();
    loadTopSkills();
    loadProjects();
    
    // Setup search functionality
    const searchInput = document.getElementById('search-input');
    let searchTimeout;
    
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value;
        
        // Debounce search to avoid too many API calls
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Check API health
    apiCall('/health').catch(error => {
        console.error('API health check failed:', error);
        document.body.insertAdjacentHTML('afterbegin', 
            '<div class="error" style="position: fixed; top: 10px; right: 10px; z-index: 1000;">' +
            'Warning: Cannot connect to API. Make sure the backend is running.' +
            '</div>'
        );
    });
});
