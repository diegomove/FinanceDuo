/* Nuestras Finanzas — Chart.js dashboard charts */

document.addEventListener("DOMContentLoaded", () => {
    const dataEl = document.getElementById("chart-data");
    if (!dataEl) return;

    const data = JSON.parse(dataEl.textContent);

    /* Color palette matching our CSS variables */
    const terracotta = "#c4704b";
    const sage = "#7d9a7e";
    const sand = "#e6ddd3";
    const blush = "#e8c4b8";
    const charcoal = "#2d2a26";
    const stone = "#8a8279";

    const pieColors = [
        "#c4704b", "#7d9a7e", "#e8c4b8", "#e6ddd3",
        "#a8c4a9", "#e8956f", "#c45c5c", "#5c9a6e",
        "#d4a574", "#8fa4b0", "#b8a090", "#9cb89e",
        "#d4937a", "#a0b4a4",
    ];

    /* Shared font settings */
    const fontFamily = "'DM Sans', sans-serif";

    Chart.defaults.font.family = fontFamily;
    Chart.defaults.color = stone;

    /* Bar Chart: Expected vs Actual */
    const barCtx = document.getElementById("barChart");
    if (barCtx && data.bar.labels.length > 0) {
        new Chart(barCtx, {
            type: "bar",
            data: {
                labels: data.bar.labels,
                datasets: [
                    {
                        label: barCtx.dataset.labelBudgeted || "Budgeted",
                        data: data.bar.expected,
                        backgroundColor: sand,
                        borderColor: stone,
                        borderWidth: 1,
                        borderRadius: 4,
                    },
                    {
                        label: barCtx.dataset.labelActual || "Actual",
                        data: data.bar.actual,
                        backgroundColor: terracotta,
                        borderColor: terracotta,
                        borderWidth: 1,
                        borderRadius: 4,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "top",
                        labels: { usePointStyle: true, padding: 20 },
                    },
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { maxRotation: 45 },
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: "rgba(0,0,0,0.05)" },
                        ticks: {
                            callback: (v) => v + " \u20ac",
                        },
                    },
                },
            },
        });
    }

    /* Pie Chart: Spending Breakdown */
    const pieCtx = document.getElementById("pieChart");
    if (pieCtx && data.pie.labels.length > 0) {
        new Chart(pieCtx, {
            type: "doughnut",
            data: {
                labels: data.pie.labels,
                datasets: [
                    {
                        data: data.pie.values,
                        backgroundColor: pieColors.slice(0, data.pie.labels.length),
                        borderWidth: 2,
                        borderColor: getComputedStyle(document.documentElement).getPropertyValue("--color-cream").trim() || "#faf7f2",
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { usePointStyle: true, padding: 12, font: { size: 11 } },
                    },
                },
                cutout: "55%",
            },
        });
    }
});
