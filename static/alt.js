const imgLink = 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/';
const raceLink = 'https://www.formula1.com/en/racing/2025/'
const circuitToCountry = {
    // Primary circuit names from the JSON
    "Melbourne": "Australia",
    "Shanghai": "China",
    "Suzuka": "Japan",
    "Sakhir": "Bahrain",
    "Jeddah": "Saudi_Arabia",
    "Miami": "Miami",
    "Imola": "Emilia_Romagna",
    "Monte Carlo": "Monaco",
    "Barcelona": "Spain",
    "Montreal": "Canada",
    "Spielberg": "Austria",
    "Silverstone": "United_Kingdom",
    "Spa-Francorchamps": "Belgium",
    "Budapest": "Hungary",
    "Zandvoort": "Netherlands",
    "Monza": "Italy",
    "Baku": "Azerbaijan",
    "Marina Bay": "Singapore",
    "Austin": "United_States",
    "Mexico City": "Mexico",
    "Sao Paulo": "Brazil",
    "Las Vegas": "United_States",
    "Lusail": "Qatar",
    "Yas Marina": "United_Arab_Emirates"
};

const getData = () => {
    let pos = 1;
    const tableElement = document.getElementById("pos-table-body");
    const tableContainer = document.getElementById('pos-table-container');
    const circuitName = document.getElementById('circuit-name').children[0];
    const imageContainer = document.getElementById('circuit-link');
    fetch('/api/predict')
        .then(res => res.json())
        .then(data => {
            imageContainer.removeChild(imageContainer.firstChild)
            const htmlData = data.map((element) => {
                return `<tr class="posRow"><td class="posElement">${pos++}</td><td class="posElement">${element.Driver}</td><td class="posElement">${element.Team}</td></tr>`;
            });
            //const tableHead = '<thead><tr class="posRow"><th class="posHead">POS</th><th class="posHead">DRIVER</th><th class="posHead">TEAM</th></tr></thead>';
            console.log(data);
            tableElement.innerHTML = htmlData.join('');
            tableContainer.style.height = tableContainer.scrollHeight + "px";
            const rows = document.querySelectorAll('#pos-table tr');
            rows.forEach((row, index) => {
                if (index === 0)
                    return
                row.classList.add('row-animate-in');
                row.style.animationDelay = `${(index - 1) * 0.08}s`
            });

            circuitName.innerHTML = data[0].Circuit
            let imagePath = imgLink + circuitToCountry[data[0].Circuit] + "_Circuit";

            let imageElement = document.createElement('img');
            console.log(imagePath)

            imageContainer.href = raceLink + fixLink(circuitToCountry[data[0].Circuit]).replace("_", "-").toLowerCase();
            imageElement.src = imagePath;
            imageElement.alt = "Circuit";
            imageContainer.appendChild(imageElement);
        });
}


function fixLink(circuit) {
    if (circuit === "Emilia_Romagna") return "EmiliaRomagna"
    else return circuit
}

// DYNAMICALLY FETCH CIRCUITS!!