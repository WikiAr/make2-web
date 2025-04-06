function randomCategory() {
    const $categoryInput = $("#category");
    const $loadingSpinner = $("#autocomplete_loading");

    $categoryInput.removeClass("alert-danger");

    // Show loading spinner
    $loadingSpinner.show();

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
    $.ajax({
        url: `${apiUrl}?${queryString}`,
        method: 'GET',
        dataType: 'json'
    })
        .done(function (data) {
            const randomTitle = data.query.random[0].title;
            // Remove "Category:" prefix as we'll add it later
            const title = randomTitle.replace(/^Category:/, '');
            $categoryInput.val(`Category:${title}`);
        })
        .fail(function (error) {
            console.error('Error fetching random category:', error);
            $categoryInput.val('Error fetching random category');
        })
        .always(function () {
            // Hide loading spinner
            $loadingSpinner.hide();
        });
}
