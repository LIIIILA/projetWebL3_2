document.addEventListener('DOMContentLoaded', function () {
    // Vérifier si des réservations sont stockées dans le localStorage
    const historyList = JSON.parse(localStorage.getItem('reservations')) || [];

    const historyContainer = document.getElementById('history-list');
    
    // Si des réservations existent, les afficher dans la liste
    if (historyList.length > 0) {
        historyList.forEach(function (reservation) {
            let listItem = document.createElement('li');
            listItem.textContent = `Box: ${reservation.box}, Date: ${reservation.date}, Heure: ${reservation.time}`;
            historyContainer.appendChild(listItem);
        });
    } else {
        historyContainer.innerHTML = '<li>Aucune réservation précédente.</li>';
    }
});
