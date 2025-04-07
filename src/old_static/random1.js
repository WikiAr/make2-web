function randomCategory() {
    const categoryInput = document.getElementById('category');
    $("#category").removeClass("alert-danger");
    const loadingSpinner = document.getElementById('autocomplete_loading');

    // Show loading spinner
    loadingSpinner.style.display = 'inline-block';

    // Wikipedia API endpoint
    const apiUrl = 'https://en.wikipedia.org/w/api.php';

    // API parameters
    const params = {
        action: 'query',
        format: 'json',
        list: 'random',
        rnnamespace: '14', // 14 is for Category namespace
        rnlimit: '1',
        origin: '*' // Required for CORS
    };

    // Build URL with parameters
    const queryString = Object.keys(params)
        .map(key => `${key}=${encodeURIComponent(params[key])}`)
        .join('&');

    // Make the API request
    fetch(`${apiUrl}?${queryString}`)
        .then(response => response.json())
        .then(data => {
            const randomTitle = data.query.random[0].title;
            // Remove "Category:" prefix as we'll add it later
            const title = randomTitle.replace(/^Category:/, '');
            categoryInput.value = `Category:${title}`;
        })
        .catch(error => {
            console.error('Error fetching random category:', error);
            categoryInput.value = 'Error fetching random category';
        })
        .finally(() => {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
        });
}
