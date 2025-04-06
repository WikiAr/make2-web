async function sendCategories() {
    const titles = document.getElementById('titles').value.trim();
    const resultBox = document.getElementById('result');
    const loading = document.getElementById('loading');
    const notloading = document.getElementById('notloading');

    if (!titles) return;

    loading.style.display = 'inline-block';
    notloading.style.display = 'none';
    resultBox.textContent = '';

    try {
        const titles_list = titles.split('\n').filter(t => t.trim() !== "");
        // ---
        var timestart = new Date().getTime();
        const response = await fetch("/api/list", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ titles: titles_list })
        });

        const data = await response.json();
        // const time = data.time;
        // ---
        var timeend = new Date().getTime();
        var time = (timeend - timestart) / 1000;
        // ---
        $("#time").text("(" + time.toFixed(2) + " ثانية)");
        // ---
        resultBox.textContent = JSON.stringify(data.results, null, 2);
    } catch (error) {
        resultBox.textContent = "حدث خطأ أثناء الاتصال بالخادم.";
        console.error(error);
    } finally {
        loading.style.display = 'none';
        notloading.style.display = 'inline';
    }
}
