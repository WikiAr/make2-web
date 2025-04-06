$(document).ready(function () {
    const $startButton = $("button[type='submit']");
    const $categoryInput = $("#category");
    const $resultInput = $("#result");
    const $loadingDiv = $("#loading");
    const $notLoadingDiv = $("#notloading");
    const $resultsTable = $("#results_table");

    $startButton.on("click", function (e) {
        e.preventDefault();

        const category = $.trim($categoryInput.val());
        if (!category) {
            $categoryInput.attr("placeholder", "يرجى إدخال العنوان");
            $categoryInput.addClass("alert-danger");
            // alert("يرجى إدخال العنوان أولاً.");
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
                $resultInput.val(data.result);
                // ---
                // add result to results
                $resultsTable.append(`
                    <tr>
                        <td>${category}</td>
                        <td>
                        ${data.result}
                        </td>
                    </tr>
                    `);
                // ---
                if (data.result == "") {
                    // $resultInput.val();
                    $resultInput.attr("placeholder", "لا يوجد نتيجة");
                    $resultInput.addClass("alert-danger");
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
                // إخفاء "جاري التحميل" بعد الانتهاء
                $loadingDiv.hide();
                $notLoadingDiv.show();
            }
        });
    });
});
