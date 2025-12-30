const sliderWrapper = document.querySelector('.slider-wrapper'); 

const minInput = document.querySelector('#rating-slider1');
const maxInput = document.querySelector('#rating-slider2');
const range1 = document.querySelector('#range1');
const range2 = document.querySelector('#range2');
const filterBtn = document.querySelector('.dropbtn');
const dropdownMenu = document.querySelector('.dropdown-content');

function updateRange() {
    let minVal = parseInt(minInput.value);
    let maxVal = parseInt(maxInput.value);

    if (minVal > maxVal) {
        let temp = minVal;
        minVal = maxVal;
        maxVal = temp;
    }

    range1.textContent = minVal;
    range2.textContent = maxVal;


    const minPercent = (minVal / minInput.max) * 100;
    const maxPercent = (maxVal / maxInput.max) * 100;

    sliderWrapper.style.background = `linear-gradient(
        to right, 
        #C9B79C ${minPercent}%, 
        #71816D ${minPercent}%, 
        #71816D ${maxPercent}%, 
        #C9B79C ${maxPercent}%
    )`;
}



async function loadPlayers(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`http://127.0.0.1:8000/api/players/?${params}`);
    if (!response.ok) {
        console.error("Failed to fetch players");
        return;
    }
    const data = await response.json();
    renderLeaderboard(data);



}


async function renderLeaderboard(playerData) {
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
        `;

        tableBody.appendChild(row);

    });

}

/*            <td>${player.delta_live_rating}</td> */

function getFilters() {
    const filters = {};

    const searchValue = document.getElementById('searchBar').value.trim();
    if (searchValue !== '') {
        filters.name = searchValue;
    }

    const minVal = Math.min(
        parseInt(minInput.value),
        parseInt(maxInput.value)
    );
    const maxVal = Math.max(
        parseInt(minInput.value),
        parseInt(maxInput.value)
    );

    filters.min_rating = minVal;
    filters.max_rating = maxVal;

    const schoolCheckboxes = document.querySelectorAll(
        '.SchoolCheck input[type="checkbox"]'
    );

    for (const cb of schoolCheckboxes) {
        if (cb.checked) {
            filters.school = cb.nextElementSibling.textContent;
            break;
        }
    }

    const gradeCheckboxes = document.querySelectorAll(
        '#g9, #g10, #g11, #g12'
    );

    for (const cb of gradeCheckboxes) {
        if (cb.checked) {
            filters.grade = cb.id.replace('g', '');
            break;
        }
    }

    return filters;
}

function applyFilters() {
    const filters = getFilters();
    console.log(filters)
    loadPlayers(filters);
}

minInput.addEventListener('input', () => {
    updateRange();
    applyFilters();
});

maxInput.addEventListener('input', () => {
    updateRange();
    applyFilters();
});

filterBtn.addEventListener('click', () => {
    dropdownMenu.classList.toggle('show');
});

const searchBar = document.getElementById('searchBar');

searchBar.addEventListener('input', () => {
    applyFilters();
});

const allCheckboxes = document.querySelectorAll(
    '.checkbox-grid input[type="checkbox"]'
);

allCheckboxes.forEach(cb => {
    cb.addEventListener('change', () => {
        applyFilters();
    });
});

updateRange();
loadPlayers();

