

let rawData = [];
function resetFilters() {
    document.getElementById('monthSelect').value = 'all';
    document.getElementById('yearSelect').value = 'all';
    // document.getElementById('dateStart').value = 'all';
    // document.getElementById('dateEnd').value = 'all';
    // updateDateOptions();
    populateMonthYearFilters(rawData);
    renderCharts(rawData);
}

function fetchData() {
    return fetch('/api/logs_by_day')
        .then(response => response.json())
        .then(data => {
            rawData = data;
            populateMonthYearFilters(data);
            renderCharts(data);
        });
}

function populateMonthYearFilters(data) {
    const days = new Set();
    const months = new Set();
    const years = new Set();

    data.forEach(item => {
        const [year, month] = item.day.split('-');
        days.add(item.day);
        months.add(month);
        years.add(year);
    });

    const monthSelect = document.getElementById('monthSelect');
    const yearSelect = document.getElementById('yearSelect');
    const dateStart = document.getElementById('dateStart');
    const dateEnd = document.getElementById('dateEnd');

    // Reset options
    monthSelect.innerHTML = '';
    yearSelect.innerHTML = '';
    dateStart.innerHTML = '';
    dateEnd.innerHTML = '';

    // Add "All" option
    monthSelect.innerHTML += '<option value="all">All</option>';
    yearSelect.innerHTML += '<option value="all">All</option>';
    // dateStart.innerHTML += '<option value="all">All</option>';
    // dateEnd.innerHTML += '<option value="all">All</option>';

    // Sort and populate months
    Array.from(months).sort().forEach(m => {
        const option = document.createElement('option');
        option.value = m;
        option.text = new Date(0, m - 1).toLocaleString('en', { month: 'long' });
        monthSelect.appendChild(option);
    });

    // Sort and populate years
    Array.from(years).sort().forEach(y => {
        const option = document.createElement('option');
        option.value = y;
        option.text = y;
        yearSelect.appendChild(option);
    });

    // Add event listeners to update date options when month/year changes
    monthSelect.addEventListener('change', updateDateOptions);
    yearSelect.addEventListener('change', updateDateOptions);

    // Initial population of date options
    updateDateOptions();

    function updateDateOptions() {
        const selectedMonth = monthSelect.value;
        const selectedYear = yearSelect.value;

        // Reset date options
        dateStart.innerHTML = '';
        dateEnd.innerHTML = '';

        // Filter and add dates based on selected month/year
        const filteredDates = Array.from(days)
            .filter(d => {
                const [year, month] = d.split('-');
                const matchMonth = (selectedMonth === 'all') || (month === selectedMonth);
                const matchYear = (selectedYear === 'all') || (year === selectedYear);
                return matchMonth && matchYear;
            })
            .sort();

        filteredDates.forEach(d => {
            const option1 = document.createElement('option');
            option1.value = d;
            option1.text = d;
            dateStart.appendChild(option1);

            const option2 = document.createElement('option');
            option2.value = d;
            option2.text = d;
            dateEnd.appendChild(option2);
        });

        // Set default dates when specific month is selected
        if (
            // selectedMonth !== 'all' &&
            filteredDates.length > 0) {
            // Set start date to first day of month
            dateStart.value = filteredDates[0];

            // Set end date to last day of month
            dateEnd.value = filteredDates[filteredDates.length - 1];
        }
    }

}

function filterByMonthYear() {
    const selectedMonth = document.getElementById('monthSelect').value;
    const selectedYear = document.getElementById('yearSelect').value;
    const selectedStartDate = document.getElementById('dateStart').value;
    const selectedEndDate = document.getElementById('dateEnd').value;

    const filtered = rawData.filter(item => {
        // Fallback to month and year filtering
        const [year, month] = item.day.split('-');
        const matchYear = (selectedYear === 'all') || (year === selectedYear);
        const matchMonth = (selectedMonth === 'all') || (month === selectedMonth);
        return matchYear && matchMonth;
    });

    const filtered2 = filtered.filter(item => {
        // Handle date range filtering
        if (selectedStartDate !== 'all' || selectedEndDate !== 'all') {
            // Only start date is specified
            if (selectedStartDate !== 'all' && selectedEndDate === 'all') {
                return item.day >= selectedStartDate;
            }
            // Only end date is specified
            if (selectedStartDate === 'all' && selectedEndDate !== 'all') {
                return item.day <= selectedEndDate;
            }
            // Both dates are specified
            return item.day >= selectedStartDate && item.day <= selectedEndDate;
        }
        return true;
    });

    renderCharts(filtered2);
}


let totalChart, resultsChart;

function renderCharts(data) {
    const labels = data.map(item => item.day);
    const totalCounts = data.map(item => item.total || 0);
    const categoryCounts = data.map(item => item.results.Category || 0);
    const noResultCounts = data.map(item => item.results.no_result || 0);
    const categoryRatios = data.map(item =>
        item.total ? ((item.results.Category || 0) / item.total * 100).toFixed(2) : 0
    );
    const noResultRatios = data.map(item =>
        item.total ? ((item.results.no_result || 0) / item.total * 100).toFixed(2) : 0
    );

    if (totalChart) totalChart.destroy();
    if (resultsChart) resultsChart.destroy();

    const totalCtx = document.getElementById('totalLineChart').getContext('2d');
    totalChart = new Chart(totalCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total',
                data: totalCounts,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.3
            }, {
                label: 'Category Count',
                data: categoryCounts,
                backgroundColor: 'rgba(255, 99, 132, 0.6)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'No Result Count',
                data: noResultCounts,
                backgroundColor: 'rgba(255, 206, 86, 0.6)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: false, text: 'Total per Day' },
                tooltip: {
                    callbacks: {
                        label: (context) => `Total: ${context.parsed.y}`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: false, text: 'Total' }
                },
                x: {
                    title: { display: false, text: 'Day' }
                }
            }
        }
    });
    /*
    const resultsCtx = document.getElementById('resultsBarChart').getContext('2d');
    resultsChart = new Chart(resultsCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Category Count',
                    data: categoryCounts,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'No Result Count',
                    data: noResultCounts,
                    backgroundColor: 'rgba(255, 206, 86, 0.6)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                },
                {
                    label: '% Category of Total',
                    data: categoryRatios,
                    type: 'line',
                    yAxisID: 'percentage',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.3,
                    fill: false
                },
                {
                    label: '% No Result of Total',
                    data: noResultRatios,
                    type: 'line',
                    yAxisID: 'percentage',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    tension: 0.3,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: 'Category & No Result with Percentages' },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.dataset.label || '';
                            const value = context.parsed.y;
                            return label.includes('%') ? `${label}: ${value}%` : `${label}: ${value}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Counts' }
                },
                percentage: {
                    position: 'right',
                    beginAtZero: true,
                    min: 0,
                    max: 100,
                    title: { display: false, text: 'Percentage (%)' },
                    grid: { drawOnChartArea: false }
                },
                x: {
                    title: { display: false, text: 'Day' }
                }
            }
        }
    });
    */
}
