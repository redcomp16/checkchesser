const minInput = document.querySelector('.min-input');
const maxInput = document.querySelector('.max-input');
const range1 = document.querySelector('#range1');
const range2 = document.querySelector('#range2');

const filterBtn = document.querySelector('.dropbtn');
const dropdownMenu = document.querySelector('.dropdown-content');

function updateRange() {
    let minVal = parseInt(minInput.value);
    let maxVal = parseInt(maxInput.value);


    if (minVal > maxVal) {
        let TempValue = maxInput.value

        minInput.value = maxVal 
        maxInput.value = minVal
    }

    range1.textContent = minInput.value;
    range2.textContent = maxInput.value;

}

filterBtn.addEventListener('click', () => {
    dropdownMenu.classList.toggle('show');
});

minInput.addEventListener('input', updateRange);
maxInput.addEventListener('input', updateRange);
    
async function loadPlayers(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`http://127.0.0.1:8000/api/players/?${params}`);

    const tableBody = document.getElementById('leaderboard-body');
    tableBody.innerHTML = '';

    playerData.forEach((player, index) => {
        const row = document.createElement('tr');
        row.classList.add('Player');

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${player.name}</td>
            <td>${player.school}</td>
            <td>${player.grade}</td>
            <td>${player.official_rating}</td>
            <td>${player.live_rating}</td>
            <td>${player.delta_live_rating}</td>
        `;

        tableBody.appendChild(row);
    });

}

loadPlayers();
