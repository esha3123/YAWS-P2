document.addEventListener('DOMContentLoaded', () => {
    const compositionData = [
    ];

    const minutesData = [
    ];

    const feedbackData = [
    ];

    const compositionTable = document.getElementById('iqac-composition-table')?.getElementsByTagName('tbody')[0];
    if (compositionTable) {
        compositionData.forEach(item => {
            const row = compositionTable.insertRow();
            row.insertCell(0).textContent = item.year;
            row.insertCell(1).innerHTML = `<a href="${item.link}" class="view-btn" target="_blank"><button>View</button></a>`;
        });
    }

    const minutesTable = document.getElementById('iqac-minutes-table')?.getElementsByTagName('tbody')[0];
    if (minutesTable) {
        minutesData.forEach(item => {
            const row = minutesTable.insertRow();
            row.insertCell(0).textContent = item.date;
            row.insertCell(1).innerHTML = `<a href="${item.minutes}" class="view-btn" target="_blank"><button>View</button></a>`;
            row.insertCell(2).innerHTML = item.atr ? 
                `<a href="${item.atr}" class="view-btn" target="_blank"><button>View</button></a>` : 
                'N/A';
        });
    }

    const feedbackTable = document.getElementById('feedback-table')?.getElementsByTagName('tbody')[0];
    if (feedbackTable) {
        feedbackData.forEach(item => {
            const row = feedbackTable.insertRow();
            row.insertCell(0).textContent = item.year;
            row.insertCell(1).innerHTML = `<a href="${item.link}" class="view-btn" target="_blank"><button>View</button></a>`;
        });
    }

    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
});