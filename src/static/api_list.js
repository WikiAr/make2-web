async function sendCategories() {
    const titles = document.getElementById('titles').value.trim();
    const resultBox = document.getElementById('result');
    const loading = document.getElementById('loading');
    const notloading = document.getElementById('notloading');

    if (!titles) return;

    loading.style.display = 'inline-block';
    notloading.style.display = 'none';
    resultBox.textContent = '';
    // ---
    $("#with_labs").hide();
    $("#no_labs").hide();
    $("#time").hide();
    $("#duplicates").hide();
    // ---
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
        if (data.error) {
            console.error(data.error);
            return;
        }
        // ---
        const with_labs = data.with_labs;
        const no_labs = data.no_labs;
        const duplicates = data.duplicates;
        // ---
        var timeend = new Date().getTime();
        var time = (timeend - timestart) / 1000;
        // ---
        $("#duplicates").text(duplicates);
        $("#duplicates").show();
        // ---
        $("#with_labs").text(with_labs);
        $("#with_labs").show();
        // ---
        $("#no_labs").text(no_labs);
        $("#no_labs").show();
        // ---
        $("#time").text(time.toFixed(2) + " ثانية");
        $("#time").show();
        // ---
        resultBox.textContent = JSON.stringify(data.results, null, 2);
        // ---
    } catch (error) {
        resultBox.textContent = "حدث خطأ أثناء الاتصال بالخادم.";
        console.error(error);
    } finally {
        loading.style.display = 'none';
        notloading.style.display = 'inline';
    }
}
