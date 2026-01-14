let countFormLogin = -1
let countFormLoginVerified = -1

let bucketsLogin = null
let bucketsScanQr = null
let bucketsScanUrl = null

function bucketByHour(arr) {
    const map = new Map();
    if (!arr || arr.length === 0) {
        return []
    }
    arr.forEach(ts => {
        const d = new Date(ts)
        d.setMinutes(0, 0, 0)
        const key = d.toISOString()
        map.set(key, (map.get(key) || 0) + 1)

    })
    return [...map.entries()]
        .sort((a, b) => new Date(a[0]) - new Date(b[0]))
        .map(([k, v]) => ({ hour : k, count : v }))
};

function bucketByHourOfDay(arr) {
    const hourlyCounts = Array(24).fill(0);
    if (!arr || arr.length === 0) {
        return hourlyCounts;
    }

    arr.forEach(ts => {
        const hour = new Date(ts).getHours();
        if (hour >= 0 && hour < 24) {
            hourlyCounts[hour]++;
        }
    });
    return hourlyCounts;
}

function generateHourlyLabels(startDate, endDate) {
    const labels = [];
    let currentDate = new Date(startDate);
    currentDate.setMinutes(0, 0, 0);

    while (currentDate <= endDate) {
        labels.push(currentDate.toISOString());
        currentDate.setHours(currentDate.getHours() + 1);
    }

    return labels;
}

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const currentValue = Math.floor(progress * (end - start) + start);
        element.textContent = currentValue.toLocaleString('fr-FR');
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}


window.addEventListener('load', async function() {

    // try {
    //     fetch("http://127.0.0.1:8000/generate_test_data", {
    //         method: 'POST'
    //     });
    // } catch (error) {
    //     console.error(error)
    // }

    try{
        const response = await fetch('http://127.0.0.1:8000/stats', {
            method: 'GET'
        });
        if (response.ok){
            const data = await response.json()
            console.log(data)
            const dataStats = data.dataStats
            countFormLogin = dataStats.count_form_login
            countFormLoginVerified = dataStats.count_form_login_verified

            const dataVisits = data.dataVisits
            const loginTime = dataVisits.loginTime
            const scanTimeQr = dataVisits.scanTimeQr
            const scanTimeUrl = dataVisits.scanTimeUrl

            // Animation des KPIs
            const countScanQr = scanTimeQr?.length || 0;
            const countScanUrl = scanTimeUrl?.length || 0;
            const totalScans = countScanQr + countScanUrl;
            animateValue(document.getElementById('countScanQr'), 0, countScanQr, 1500);
            animateValue(document.getElementById('countScanUrl'), 0, countScanUrl, 1500);
            animateValue(document.getElementById('countTotalScans'), 0, totalScans, 1500);
            animateValue(document.getElementById('countFormLogin'), 0, countFormLogin || 0, 1500);
            animateValue(document.getElementById('countFormLoginVerified'), 0, countFormLoginVerified || 0, 1500);



            bucketsLogin   = bucketByHour(loginTime);
            bucketsScanQr  = bucketByHour(scanTimeQr);
            bucketsScanUrl = bucketByHour(scanTimeUrl);

            const hourlyLogins = bucketByHourOfDay(loginTime);
            const hourlyScanQr = bucketByHourOfDay(scanTimeQr);
            const hourlyScanUrl = bucketByHourOfDay(scanTimeUrl);

            const hoursOfDayLabels = Array.from({ length: 24 }, (_, i) => `${i.toString().padStart(2, '0')}h`);

            // Chart pour les logins
            const loginCtx = document.getElementById('loginChart').getContext('2d');
            new Chart(loginCtx, {
                type: 'bar',
                data: {
                    labels: hoursOfDayLabels,
                    datasets: [{
                        label: 'Nombre de connexions',
                        data: hourlyLogins,
                        backgroundColor: 'rgba(52, 152, 219, 0.6)',
                        borderColor: 'rgba(52, 152, 219, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });

            // Chart pour la comparaison des scans
            const scanCtx = document.getElementById('scanChart').getContext('2d');
            new Chart(scanCtx, {
                type: 'bar',
                data: {
                    labels: hoursOfDayLabels,
                    datasets: [{
                        label: 'Scans QR Code',
                        data: hourlyScanQr,
                        backgroundColor: 'rgba(231, 76, 60, 0.6)',
                        borderColor: 'rgba(231, 76, 60, 1)',
                        borderWidth: 1
                    }, {
                        label: 'Scans URL',
                        data: hourlyScanUrl,
                        backgroundColor: 'rgba(26, 188, 156, 0.6)',
                        borderColor: 'rgba(26, 188, 156, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });

            // --- GRAPHIQUES CHRONOLOGIQUES (INCHANGÉS) ---

            const startDate = new Date('2025-11-19T00:00:00.000Z');
            const endDate = new Date();
            const timelineLabels = generateHourlyLabels(startDate, endDate);

            // Préparez les données pour la chronologie
            const bucketsLoginMap = new Map(bucketsLogin.map(item => [item.hour, item.count]));
            const bucketsScanQrMap = new Map(bucketsScanQr.map(item => [item.hour, item.count]));
            const bucketsScanUrlMap = new Map(bucketsScanUrl.map(item => [item.hour, item.count]));

            const loginTimelineData = timelineLabels.map(hour => bucketsLoginMap.get(hour) || 0);
            const scanQrTimelineData = timelineLabels.map(hour => bucketsScanQrMap.get(hour) || 0);
            const scanUrlTimelineData = timelineLabels.map(hour => bucketsScanUrlMap.get(hour) || 0);

            const formattedTimelineLabels = timelineLabels.map(h => new Date(h).toLocaleString('fr-FR', { day: '2-digit', month: '2-digit', hour: '2-digit' }) + 'h');

            // Chart chronologique pour les logins
            const loginTimelineCtx = document.getElementById('loginTimelineChart').getContext('2d');
            new Chart(loginTimelineCtx, {
                type: 'line', // 'line' est plus adapté pour une longue chronologie
                data: {
                    labels: formattedTimelineLabels,
                    datasets: [{
                        label: 'Nombre de connexions',
                        data: loginTimelineData,
                        backgroundColor: 'rgba(52, 152, 219, 0.2)',
                        borderColor: 'rgba(52, 152, 219, 1)',
                        borderWidth: 1,
                        fill: true,
                        tension: 0.3 // Rend la ligne plus lisse
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });

            // Chart chronologique pour la comparaison des scans
            const scanTimelineCtx = document.getElementById('scanTimelineChart').getContext('2d');
            new Chart(scanTimelineCtx, {
                type: 'line',
                data: {
                    labels: formattedTimelineLabels,
                    datasets: [{
                        label: 'Scans QR Code',
                        data: scanQrTimelineData,
                        backgroundColor: 'rgba(231, 76, 60, 0.2)',
                        borderColor: 'rgba(231, 76, 60, 1)',
                        borderWidth: 1,
                        fill: true,
                        tension: 0.3
                    }, {
                        label: 'Scans URL',
                        data: scanUrlTimelineData,
                        backgroundColor: 'rgba(26, 188, 156, 0.2)',
                        borderColor: 'rgba(26, 188, 156, 1)',
                        borderWidth: 1,
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: { scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } }
            });
        }


    } catch(error){
        console.error(error)
    }
});