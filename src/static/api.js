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
                if (data.result == "") {
                    $resultInput.attr("placeholder", "لا يوجد نتيجة");
                    $resultInput.addClass("alert-danger");
                } else {
                    $resultInput.val(data.result);
                    // ---
                    let random_id = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
                    // ---
                    // add result to results with copy button
                    $resultsTable.append(`
                        <tr>
                            <td class="ltr_left">
                                <span class="ltr_left">
                                    ${category}
                                </span>
                            </td>
                            <td>
                                <span id="${random_id}">
                                    ${data.result}
                                </span>
                                <!-- <div class="d-flex justify-content-between align-items-center">
                                    <input type="text" id="${random_id}" readonly class="form-control input-group-input" value="${data.result}">
                                    <button type="button" class="btn btn-sm btn-outline-secondary"
                                        onclick="copyResult('${random_id}', event)">
                                        <i class="bi bi-clipboard"></i>
                                    </button>
                                </div> -->
                            </td>
                        </tr>
                    `);
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
                // إخفاء "جاري التحميل" بعد الانتهاء
                $loadingDiv.hide();
                $notLoadingDiv.show();
            }
        });
    });
});
