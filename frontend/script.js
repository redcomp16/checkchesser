const sliderWrapper = document.querySelector('.slider-wrapper'); 

const minInput = document.querySelector('#rating-slider1');
const maxInput = document.querySelector('#rating-slider2');
const range1 = document.querySelector('#range1');
const range2 = document.querySelector('#range2');
const filterBtn = document.querySelector('.dropbtn');
const dropdownMenu = document.querySelector('.dropdown-content');
let ratingType = "Live";

const PAGE_SIZE = 25;
let currentPage = 1;
let currentData = [];

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


const tableBody = document.getElementById("leaderboard-body");

let officialAsc = false;
let liveAsc = false;

document.getElementById("OfficialRating").addEventListener("click", () => {
    ratingType = "Official";
    applyFilters();
});

document.getElementById("LiveRating").addEventListener("click", () => {
    ratingType = "Live";
    applyFilters();
});

function isMobile() {
    return window.innerWidth <= 900; 
}

const ratingHeaders = document.querySelectorAll(".RatingSort");

ratingHeaders.forEach(header => {
    header.addEventListener("click", () => {
        ratingType = header.dataset.sort;

        ratingHeaders.forEach(h => h.classList.remove("active"));

        header.classList.add("active");

        applyFilters();
    });
});

async function loadPlayers(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`https://redcomp16.pythonanywhere.com/api/players/?${params}`);
    if (!response.ok) {
        console.error("Failed to fetch players");
        return;
    }
    const data = await response.json();
    renderLeaderboard(data);
}

async function loadPlayers(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`https://redcomp16.pythonanywhere.com/api/players/?${params}`);

    if (!response.ok) {
        console.error("Failed to fetch players");
        return;
    }

    currentData = await response.json();
    currentPage = 1;
    renderPage();
    renderPaginationControls();
}

function renderPage() {
    const tableBody = document.getElementById('leaderboard-body');
    tableBody.innerHTML = '';

    const start = (currentPage - 1) * PAGE_SIZE;
    const end = start + PAGE_SIZE;
    const pageData = currentData.slice(start, end);
    const mobile = isMobile();

    pageData.forEach((player, index) => {
        const delta = player.delta_live_rating ?? 0;
        const deltaClass = delta > 0 ? "delta-up" : delta < 0 ? "delta-down" : "delta-neutral";
        const arrow = delta > 0 ? "▲" : delta < 0 ? "▼" : "";

        const row = document.createElement('tr');
        row.classList.add('Player');
        if (mobile) {
            row.innerHTML = `
            <td>${start + index + 1}</td>
            <td>${player.name}</td>
            <td>${player.school}</td>
            <td>${player.grade}</td>
            <td>${player.official_rating}</td>
            <td class="live-rating">
                ${player.live_rating}
                <span class="delta ${deltaClass}">
                    ${arrow}${Math.abs(delta)}
                </span>
            </td>
        `;
        }  else {
             row.innerHTML = `
            <td>${start + index + 1}</td>
            <td>${player.name}</td>
            <td>${player.school} HS</td>
            <td>${player.grade}</td>
            <td>${player.official_rating}</td>
            <td class="live-rating">
                ${player.live_rating}
                <span class="delta ${deltaClass}">
                    ${arrow}${Math.abs(delta)}
                </span>
            </td>
        `;
        }

       

        row.style.cursor = "pointer";
        row.addEventListener("click", () => {
            window.open(
                `https://ratings.uschess.org/player/${player.uscf_id}`,
                "_blank",
                "noopener,noreferrer"
            );
        });

        tableBody.appendChild(row);
    });
}

function renderPaginationControls() {
    const totalPages = Math.ceil(currentData.length / PAGE_SIZE);
    const pageInfo = document.getElementById("pageInfo");

    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

    document.getElementById("prevPage").disabled = currentPage === 1;
    document.getElementById("nextPage").disabled = currentPage === totalPages;
}

function scrollTableToTop() {
    const table = document.querySelector('.leaderboard-table') 
        || document.querySelector('table');

    table.scrollIntoView({ behavior: "instant", block: "start" });
}

document.getElementById("prevPage").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        renderPage();
        renderPaginationControls();
        scrollTableToTop();
    }
});

document.getElementById("nextPage").addEventListener("click", () => {
    const totalPages = Math.ceil(currentData.length / PAGE_SIZE);
    if (currentPage < totalPages) {
        currentPage++;
        renderPage();
        renderPaginationControls();
        scrollTableToTop();
    }
});

/*            <td>${player.delta_live_rating}</td> */

function getFilters() {
    const filters = {};
    const FilteringGrades = [];
    const FilteringSchools = [];
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

    const gradeCheckboxes = document.querySelectorAll(
        '.GradeCheck input[type="checkbox"]'
    );

    for (const cb of schoolCheckboxes) {
        if (cb.checked) {
            FilteringSchools.push(cb.id);
        }
    }

    for (const cb of gradeCheckboxes) {
        if (cb.checked) {
            FilteringGrades.push(cb.id.replace('g', ''));
        }
    }

    filters.school = FilteringSchools;
    filters.grade = FilteringGrades;
    filters.ratingType = ratingType;
    console.log(FilteringGrades);
    console.log(FilteringSchools);

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
    filterBtn.classList.toggle("active")
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

