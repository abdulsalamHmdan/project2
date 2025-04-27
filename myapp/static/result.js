const xValues = ["مصاب", "سليم"];
const yValues = [prediction, 100 - prediction];
const barColors = [
    "#b91d47",
    "#1e7145"
];

new Chart("myChart", {
    type: "doughnut",
    data: {
        labels: xValues,
        datasets: [{
            backgroundColor: barColors,
            data: yValues
        }]
    },
    options: {
        animation: {
            onComplete: () => {
                delayed = true;
            },
            delay: (context) => {
                let delay = 0;
                if (context.type === 'data' && context.mode === 'default' && !delayed) {
                    delay = context.dataIndex * 300 + context.datasetIndex * 100;
                }
                return delay;
            },
        },
        title: {
            display: false,
            // text: "نسبة اصابتك بمرض السكري هي " + prediction,
        }
    }

}
);