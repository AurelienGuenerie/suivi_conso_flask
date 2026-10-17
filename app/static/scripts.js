// static/scripts.js

document.addEventListener('DOMContentLoaded', () => {

    // --- Graphique Chart.js ---
    const container = document.getElementById('chart-container');
    if (container) {
        const historiqueData = JSON.parse(container.dataset.historique);

        const dates = Object.keys(historiqueData);
        const consommations = dates.map(date => historiqueData[date].consommation);
        const prix = dates.map(date =>
            historiqueData[date].prix ? parseFloat(historiqueData[date].prix) : null
        );

        const ctx = document.getElementById('consoChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'L/100',
                        data: consommations,
                        borderColor: 'rgb(220, 53, 69)',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        tension: 0.1,
                        fill: true,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Prix (€)',
                        data: prix,
                        borderColor: 'rgb(13, 110, 253)',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        tension: 0.1,
                        fill: false,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { type: 'linear', display: true, position: 'left', beginAtZero: true },
                    y1: {
                        type: 'linear', display: true, position: 'right', beginAtZero: true,
                        grid: { drawOnChartArea: false }
                    }
                }
            }
        });
    }

    // --- Pré-remplissage de la modale de modification ---
    const editModal = document.getElementById('editEntryModal');
    if (editModal) {
        editModal.addEventListener('show.bs.modal', (event) => {
            const bouton = event.relatedTarget;
            const form = document.getElementById('editEntryForm');
            form.action = bouton.dataset.editUrl;
            document.getElementById('editOriginalDate').value = bouton.dataset.editDate;
            document.getElementById('editDate').value = bouton.dataset.editDate;
            document.getElementById('editPlein').value = bouton.dataset.editPlein;
            document.getElementById('editCompteur').value = bouton.dataset.editCompteur;
            document.getElementById('editPrix').value = bouton.dataset.editPrix;
            document.getElementById('editCarburant').value = bouton.dataset.editCarburant;
        });
    }

    // --- Date du jour par défaut ---
    const dateInput = document.getElementById('date');
    if (dateInput) {
        dateInput.valueAsDate = new Date();
    }
});