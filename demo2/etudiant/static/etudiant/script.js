/*document.addEventListener('DOMContentLoaded', function () {
    const reservationForm = document.getElementById('reservation-form');

    reservationForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Empêche le formulaire de soumettre normalement

        // Récupérer les données du formulaire
        const box = document.getElementById('box').value;
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;

        // Créer un objet pour la réservation
        const reservation = {
            box: box,
            date: date,
            time: time
        };

        // Récupérer l'historique existant ou créer un tableau vide
        let historyList = JSON.parse(localStorage.getItem('reservations')) || [];

        // Ajouter la nouvelle réservation à l'historique
        historyList.push(reservation);

        // Sauvegarder à nouveau l'historique dans le localStorage
        localStorage.setItem('reservations', JSON.stringify(historyList));

        // Optionnellement, afficher un message de confirmation ou réinitialiser le formulaire
        alert('Réservation effectuée avec succès !');
        reservationForm.reset(); // Réinitialise le formulaire après soumission
    });
});*/
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Mois au format "MM"
    const dd = String(today.getDate()).padStart(2, '0'); // Jour au format "DD"
    const limitDate = new Date(today.getFullYear(), 6, 19);
    // Initialiser Flatpickr
    flatpickr("#reservation-date", {
        minDate: `${yyyy}-${mm}-${dd}`, // La date minimale sera aujourd'hui
        disable: [
            function(date) {
                // Désactiver les week-ends (samedi = 6, dimanche = 0)
                return date.getDay() === 0 || date.getDay() === 6|| date > limitDate;
            }
        ],
        dateFormat: "d-m-Y", // Format de la date
    });
});