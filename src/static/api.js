$(document).ready(function () {
    const $startButton = $("button[type='submit']");
    const $categoryInput = $("#category");
    const $resultInput = $("#result");
    const $loadingDiv = $("#loading");
    const $notLoadingDiv = $("#notloading");

    $startButton.on("click", function (e) {
        e.preventDefault();
        $notLoadingDiv.hide();

        const category = $.trim($categoryInput.val());
        if (!category) {
            // alert("يرجى إدخال العنوان أولاً.");
            return;
        }

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
                $resultInput.val(data.result);
                var timeend = new Date().getTime();
                var time = (timeend - timestart) / 1000;
                $("#time").text("(" + time.toFixed(2) + " ثانية)");
            },
            error: function (xhr, status, error) {
                $resultInput.val("فشل في جلب البيانات");
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
