$(function () {
    $("#category").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "https://en.wikipedia.org/w/api.php",
                timeout: 5000,
                beforeSend: function () {
                    $("#autocomplete_loading").show();
                },
                error: function (xhr, status, error) {
                    console.error("API request failed:", error.toString().replace(/[<>'"]/g, ''));
                    response([]);
                },
                complete: function () {
                    $("#autocomplete_loading").hide();
                },
                dataType: "jsonp",
                data: {
                    action: "opensearch",
                    format: "json",
                    search: request.term
                },
                success: function (data) {
                    response(data[1]); // قائمة العناوين المقترحة
                }
            });
        },
        minLength: 2 // يبدأ الإكمال بعد إدخال حرفين على الأقل
    });
});
