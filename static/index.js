const circuitImg = document.getElementById('circuit-img');
const circuitNameElement = document.getElementById('circuit-name');
const imgLink = 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/';
//const circuitName = 'Saudi_Arabia_Circuit';

const circuitToCountry = {
  // Primary circuit names from the JSON
  "Melbourne": "Australia",
  "Shanghai": "China",
  "Suzuka": "Japan",
  "Sakhir": "Bahrain",
  "Jeddah": "Saudi_Arabia",
  "Miami": "United_States",
  "Imola": "Italy",
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

//circuitImg.innerHTML = `<img src='${imgLink + circuitName}' alt='${circuitName}' class='circuit-Img'>`;


function getCircuit(trackName) {
    return circuitToCountry[trackName]
}


function fetchData() {
    let pos = 1;
    const tableElement = document.getElementById('posTable');
    const tableHead = '<tr> <th>POS</th> <th>DRIVER</th> <th>TEAM</th> </tr>';
    fetch('/api/predict')
        .then(res => res.json())
        .then(data => {
            const htmlData = data.map((element) => {
                return `<tr><td>${pos++}</td><td>${element.Driver}</td><td>${element.Team}</td></tr>`
            });
            console.log(htmlData);
            tableElement.innerHTML = tableHead + htmlData.join('');

            const rows = document.querySelectorAll('#posTable tr');
            rows.forEach((row, index) => {
                row.classList.add('row-animate-in');
                row.style.animationDelay = `${index * 0.05}s`
            });

            const circuitName = getCircuit(data[0].Circuit) + "_Circuit";
            circuitImg.innerHTML = `<img src='${imgLink + circuitName}' alt='${circuitName}' class='circuit-Img'>`;
            circuitNameElement.innerHTML = (data[0].Circuit).toUpperCase()
        })
        .catch(error => console.error(error));
}