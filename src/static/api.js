const main_table = new DataTable('#main_table', {
    paging: false,
    info: false,
    searching: false
});

$(document).ready(function () {
    const $startButton = $("button[type='submit']");
    const $categoryInput = $("#category");
    const $resultInput = $("#result");
    const $loadingDiv = $("#loading");
    const $notLoadingDiv = $("#notloading");

    $startButton.on("click", function (e) {
        e.preventDefault();

        const category = $.trim($categoryInput.val());
        if (!category) {
            $categoryInput.attr("placeholder", "يرجى إدخال العنوان");
            $categoryInput.addClass("alert-danger");
            return;
        }

        $categoryInput.removeClass("alert-danger");
        $resultInput.removeClass("alert-danger");

        $notLoadingDiv.hide();

        const encodedCategory = encodeURIComponent(category);

        // إظهار "جاري التحميل"
        $loadingDiv.show();
        $resultInput.val("");
        var timestart = new Date().getTime();
        $.ajax({
            url: `api/${encodedCategory}`,
            method: "GET",
            dataType: "json",
            success: function (data) {
                // ---
                if (data.error) {
                    console.error(data.error);
                    return;
                }
                // ---
                if (data.result == "") {
                    $resultInput.attr("placeholder", "لا يوجد نتيجة");
                    $resultInput.addClass("alert-danger");
                } else {
                    $resultInput.val(data.result);
                    // ---
                    main_table.row.add([category, data.result]).draw();
                    // ---
                }
                // ---
                var timeend = new Date().getTime();
                var time = (timeend - timestart) / 1000;
                $("#time").text("(" + time.toFixed(2) + " ثانية)");
            },
            error: function (xhr, status, error) {
                $resultInput.val("فشل في جلب البيانات");
                $resultInput.addClass("alert-danger");
                console.error("Error:", error);
            },
            complete: function () {
                $loadingDiv.hide();
                $notLoadingDiv.show();
            }
        });
    });
});
