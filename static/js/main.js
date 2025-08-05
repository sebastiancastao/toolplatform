// Main JavaScript file for Flask App

document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask App loaded successfully!');
    
    // Initialize API test buttons
    initializeApiTests();
    
    // Add smooth scrolling to all anchor links
    addSmoothScrolling();
    
    // Initialize tooltips if Bootstrap is loaded
    initializeTooltips();
});

function initializeApiTests() {
    const testApiBtn = document.getElementById('testApiBtn');
    const testEchoBtn = document.getElementById('testEchoBtn');
    const searchKeywordBtn = document.getElementById('searchKeywordBtn');
    const useSheetKeyword = document.getElementById('useSheetKeyword');
    const useCustomKeyword = document.getElementById('useCustomKeyword');
    const customKeywordInput = document.getElementById('customKeywordInput');
    
    if (testApiBtn) {
        testApiBtn.addEventListener('click', function() {
            testApiHello();
        });
    }
    
    if (testEchoBtn) {
        testEchoBtn.addEventListener('click', function() {
            testEchoApi();
        });
    }
    
    if (searchKeywordBtn) {
        searchKeywordBtn.addEventListener('click', function() {
            searchKeywords();
        });
    }
    
    // Handle radio button changes
    if (useSheetKeyword && useCustomKeyword && customKeywordInput) {
        useSheetKeyword.addEventListener('change', function() {
            if (this.checked) {
                customKeywordInput.disabled = true;
                customKeywordInput.value = '';
            }
        });
        
        useCustomKeyword.addEventListener('change', function() {
            if (this.checked) {
                customKeywordInput.disabled = false;
                customKeywordInput.focus();
            }
        });
    }
}

async function testApiHello() {
    const responseDiv = document.getElementById('apiResponse');
    const button = document.getElementById('testApiBtn');
    
    try {
        // Show loading state
        button.innerHTML = '<span class="loading"></span> Testing...';
        button.disabled = true;
        responseDiv.className = '';
        responseDiv.innerHTML = 'Making API request...';
        
        const response = await fetch('/api/hello');
        const data = await response.json();
        
        if (response.ok) {
            responseDiv.className = 'success';
            responseDiv.innerHTML = `
                <h5>✅ Success!</h5>
                <p><strong>Message:</strong> ${data.message}</p>
                <p><strong>Status:</strong> ${data.status}</p>
                <small>Response received at: ${new Date().toLocaleTimeString()}</small>
            `;
        } else {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
    } catch (error) {
        responseDiv.className = 'error';
        responseDiv.innerHTML = `
            <h5>❌ Error!</h5>
            <p><strong>Error:</strong> ${error.message}</p>
            <small>Error occurred at: ${new Date().toLocaleTimeString()}</small>
        `;
    } finally {
        // Reset button state
        button.innerHTML = 'Test API Hello';
        button.disabled = false;
    }
}

async function testEchoApi() {
    const responseDiv = document.getElementById('apiResponse');
    const button = document.getElementById('testEchoBtn');
    
    try {
        // Show loading state
        button.innerHTML = '<span class="loading"></span> Testing...';
        button.disabled = true;
        responseDiv.className = '';
        responseDiv.innerHTML = 'Making API request...';
        
        const testData = {
            message: 'Hello from the frontend!',
            timestamp: new Date().toISOString(),
            randomNumber: Math.floor(Math.random() * 1000)
        };
        
        const response = await fetch('/api/echo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            responseDiv.className = 'success';
            responseDiv.innerHTML = `
                <h5>✅ Echo Success!</h5>
                <p><strong>Status:</strong> ${data.status}</p>
                <p><strong>Received Data:</strong></p>
                <pre class="bg-light p-2 rounded">${JSON.stringify(data.received, null, 2)}</pre>
                <small>Response received at: ${new Date().toLocaleTimeString()}</small>
            `;
        } else {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
    } catch (error) {
        responseDiv.className = 'error';
        responseDiv.innerHTML = `
            <h5>❌ Error!</h5>
            <p><strong>Error:</strong> ${error.message}</p>
            <small>Error occurred at: ${new Date().toLocaleTimeString()}</small>
        `;
    } finally {
        // Reset button state
        button.innerHTML = 'Test Echo API';
        button.disabled = false;
    }
}

function addSmoothScrolling() {
    // Add smooth scrolling to all links with hash
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Utility functions
function showNotification(message, type = 'info') {
    // Simple notification function
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

async function searchKeywords() {
    const resultsDiv = document.getElementById('searchResults');
    const progressDiv = document.getElementById('searchProgress');
    const button = document.getElementById('searchKeywordBtn');
    const useCustom = document.getElementById('useCustomKeyword').checked;
    const customKeyword = document.getElementById('customKeywordInput').value.trim();
    
    try {
        // Validate input
        if (useCustom && !customKeyword) {
            resultsDiv.className = 'error';
            resultsDiv.innerHTML = `
                <h5>❌ Validation Error</h5>
                <p>Please enter a keyword or select "Use keyword from Google Sheets".</p>
            `;
            return;
        }
        
        // Show loading state
        button.innerHTML = '<span class="loading"></span> Searching...';
        button.disabled = true;
        progressDiv.style.display = 'block';
        resultsDiv.className = '';
        resultsDiv.innerHTML = '';
        
        const requestData = {
            use_custom: useCustom,
            keyword: customKeyword
        };
        
        const response = await fetch('/api/search-keyword', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        const data = await response.json();
        
        if (response.ok && data.status === 'success') {
            resultsDiv.className = 'success';
            const results = data.results;
            
            let urlsList = '';
            if (results.urls_with_keyword && results.urls_with_keyword.length > 0) {
                urlsList = `
                    <h6>URLs with keyword:</h6>
                    <ul class="list-group list-group-flush">
                        ${results.urls_with_keyword.map(url => 
                            `<li class="list-group-item"><a href="${url}" target="_blank">${url}</a></li>`
                        ).join('')}
                    </ul>
                `;
            }
            
            resultsDiv.innerHTML = `
                <h5>✅ Search Completed!</h5>
                <p><strong>Message:</strong> ${data.message}</p>
                <div class="row">
                    <div class="col-md-4">
                        <div class="text-center">
                            <h6>Keyword Searched</h6>
                            <span class="badge bg-primary fs-6">${results.keyword}</span>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center">
                            <h6>Total URLs</h6>
                            <span class="badge bg-info fs-6">${results.total_urls}</span>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center">
                            <h6>Matches Found</h6>
                            <span class="badge bg-success fs-6">${results.matches_found}</span>
                        </div>
                    </div>
                </div>
                ${urlsList}
                <div class="alert alert-info mt-3">
                    <small><strong>Note:</strong> Results have been updated in your Google Sheets (Column C). Search completed at: ${new Date().toLocaleTimeString()}</small>
                </div>
            `;
            
            showNotification(`Search completed! Found ${results.matches_found} matches out of ${results.total_urls} URLs.`, 'success');
        } else {
            throw new Error(data.message || 'Unknown error occurred');
        }
    } catch (error) {
        resultsDiv.className = 'error';
        resultsDiv.innerHTML = `
            <h5>❌ Search Error</h5>
            <p><strong>Error:</strong> ${error.message}</p>
            <div class="alert alert-warning">
                <small><strong>Common issues:</strong></small>
                <ul>
                    <li>Google Sheets credentials file not found</li>
                    <li>No internet connection</li>
                    <li>Invalid spreadsheet ID or permissions</li>
                    <li>No URLs found in column A</li>
                </ul>
            </div>
            <small>Error occurred at: ${new Date().toLocaleTimeString()}</small>
        `;
        
        showNotification('Search failed. Please check the error details above.', 'danger');
    } finally {
        // Reset button and hide progress
        button.innerHTML = '<i class="fas fa-search"></i> Start Search';
        button.disabled = false;
        progressDiv.style.display = 'none';
    }
}

// Export functions for global use
window.FlaskApp = {
    testApiHello,
    testEchoApi,
    searchKeywords,
    showNotification
};