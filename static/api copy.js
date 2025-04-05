
document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.querySelector("button[type='submit']");
    const categoryInput = document.getElementById("category");
    const resultInput = document.getElementById("result");
    const loadingDiv = document.getElementById("loading");

    startButton.addEventListener("click", function (e) {
        $("#notloading").hide();
        e.preventDefault();

        const category = categoryInput.value.trim();
        if (!category) {
            // alert("يرجى إدخال العنوان أولاً.");
            return;
        }

        const encodedCategory = encodeURIComponent(category);

        // إظهار "جاري التحميل"
        loadingDiv.style.display = "block";
        resultInput.value = "";

        fetch(`http://localhost:5000/api/${encodedCategory}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("حدث خطأ أثناء التواصل مع الخادم");
                }
                return response.json();
            })
            .then(data => {
                resultInput.value = data.result;
            })
            .catch(error => {
                resultInput.value = "فشل في جلب البيانات";
                console.error("Error:", error);
            })
            .finally(() => {
                // إخفاء "جاري التحميل" بعد الانتهاء
                loadingDiv.style.display = "none";
                $("#notloading").show();
            });
    });
});
