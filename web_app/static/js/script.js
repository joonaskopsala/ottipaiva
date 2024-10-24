let currentDay = 0;

const forecastData = JSON.parse(document.getElementById("forecast-data").value);

if (!Array.isArray(forecastData) || forecastData.length === 0) {
    console.error("Kävi virhe. Yritä uudelleen myöhemmin.")
}

function changeDay(direction) {
    currentDay += direction
    if (currentDay < 0) currentDay = forecastData.length - 1
    if (currentDay >= forecastData.length) currentDay = 0

    updateNavigationButtons()
    updateForecast()
}

function updateForecast() {
    const prevButton = document.getElementById("prev-day")
    const nextButton = document.getElementById("next-day")
    const forecastDisplay = document.getElementById("forecast-display")
    forecastDisplay.innerHTML = ''

    const dayElement = document.querySelector(".day")

    if (forecastData[currentDay]) {
        const currentForecast = forecastData[currentDay][0];
        const formattedDate = new Date(currentForecast.date * 1000).toLocaleDateString('fi-FI', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })

        dayElement.innerHTML = formattedDate;

        forecastData[currentDay].forEach(item => {
            forecastDisplay.innerHTML += `
                <div class="forecast-item">
                    <p>🕓 ${(new Date(item.date * 1000).toLocaleTimeString('fi-FI', { hour: '2-digit', minute: '2-digit' })).replace(".",":")}</p>
                    <p>💨: ${Math.round(item.wind_speed)} m/s</p>
                    <p>🌡️: ${Math.round(item.temp)} °C</p>
                    <p>${item.prediction}</p>
                    <img src="/static/icons/${item.fisherman_icon}" alt="Fishing Success">
                </div>
            `
        });
    } else {
        prevButton.style.visibility = "hidden"
        nextButton.style.visibility = "hidden"
        forecastDisplay.innerHTML += `
            <div class="forecast-item">
                <p>Kaupunkia ei löytynyt 😪</p>
            </div>
        `;
    }
}

function updateNavigationButtons() {
    const prevButton = document.getElementById("prev-day")
    const nextButton = document.getElementById("next-day")

    prevButton.style.visibility = currentDay === 0 ? 'hidden' : 'visible'

    nextButton.style.visibility = currentDay === forecastData.length - 1 ? 'hidden' : 'visible'
}

updateNavigationButtons()
updateForecast()
