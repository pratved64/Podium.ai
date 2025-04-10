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
        })
        .catch(error => console.error(error));
}

const circuitImg = document.getElementById('circuit-img');
const imgLink = 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/';
const circuitName = 'Japan_Circuit';

circuitImg.innerHTML = `<img src='${imgLink + circuitName}' alt='${circuitName}' class='circuit-Img'>`

/*
TODO:
1. Get Circuit dynamically, add functionality to automatically change current
2. Add team colour for driver
 */