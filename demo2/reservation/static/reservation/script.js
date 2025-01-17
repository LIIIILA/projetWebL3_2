document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // Mois au format "MM"
    const dd = String(today.getDate()).padStart(2, '0'); // Jour au format "DD"
    const limitDate = new Date(today.getFullYear(), 6, 19); // 19 juillet de l'année en cours
    
    // Initialiser Flatpickr
    flatpickr("#reservation-date", {
        minDate: `${yyyy}-${mm}-${dd}`, // La date minimale sera aujourd'hui
        disable: [
            function(date) {
                return date.getDay() === 0 || date.getDay() === 6 || date > limitDate; // Désactiver les week-ends et après le 19 juillet
            }
        ],
        altInput: true,
        altFormat: "d-m-Y", // Format utilisé pour le champ visible
        dateFormat: "d-m-Y", // Le format de date d'affichage
    });


    


    
});
document.querySelectorAll('.hour-btn').forEach(function(button) {
    button.addEventListener('click', function() {      
        if (button.hasAttribute('disabled')) {
            return; // Empêcher toute action si le bouton est désactivé
        }

        // Récupérer l'heure et l'ID de la box
        const selectedHour = button.getAttribute('data-hour');
        const boxId = button.getAttribute('data-box-id');
       
       
        // Mettre à jour le champ caché pour cette box
        document.getElementById(`selected-hour-${boxId}`).value = selectedHour;

        // Désélectionner les autres boutons pour cette box
        document.querySelectorAll(`.hour-btn[data-box-id="${boxId}"]`).forEach(function(btn) {
            btn.classList.remove('selected');
        });
        button.classList.add('selected');

        // Activer ou désactiver le bouton de réservation de la box
        toggleReserveButton(boxId);
    });
});

// Fonction pour activer/désactiver le bouton de réservation en fonction de l'heure sélectionnée
function toggleReserveButton(boxId) {
    var selectedHour = document.getElementById(`selected-hour-${boxId}`).value;
    var reserveButton = document.getElementById(`reserve-button-${boxId}`);
    
    // Si une heure est sélectionnée, activer le bouton "Réserver"
    if (selectedHour) {
        reserveButton.disabled = false;
    } else {
        reserveButton.disabled = true;
    }
}
