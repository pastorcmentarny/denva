function displayIntermittentFastingInfo() {
    const date = new Date();
    let currentHour = date.getHours();
    if (currentHour === 19) {
        document.write('<span class="warn">' + "LAST HOUR BEFORE INTERMITTENT FASTING PERIOD" + '</span>');
    } else if (currentHour === 10) {
        document.write('<span class="warn">' + "ALMOST FOOD TIME" + '</span>');
    } else if (currentHour < 19 && currentHour >= 11) {
        document.write('<span class="good">' + "FOOD TIME :)" + '</span>');
    } else {
        document.write('<span class="bad">' + "NO FOOD" + '</span> (INTERMITTENT FASTING PERIOD)');
    }
}
