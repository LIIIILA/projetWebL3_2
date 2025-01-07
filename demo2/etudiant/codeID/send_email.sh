#!/usr/bin/env bash

SERVER='smtp.office365.com'            # Remplacez par le serveur SMTP
PORT='587'                         # Typiquement 465 pour SSL
USER='fragrand.dream@outlook.be'   # Votre adresse Gmail
PASS='M.zdx521'    # Remplacez par un mot de passe d'application
SENDER_ADDRESS="$1"                # Adresse de l'expéditeur passée comme argument
SENDER_NAME='SENDER'
RECIPIENT_NAME='ESTELHU'
RECIPIENT_ADDRESS='ESTELLE.HU2004@GMAIL.COM'
SUBJECT='TESTE PROJET SI'
MESSAGE="Votre code usage unique : hello world"  # Contenu du mail

# Connexion SMTP avec authentification et envoi du mail
curl -v --url "smtp://smtp.office365.com:587" \
    --user "$USER:$PASS" \
    --mail-from "$SENDER_ADDRESS" \
    --mail-rcpt "$RECIPIENT_ADDRESS" \
    --header "Subject: $SUBJECT" \
    --header "From: $SENDER_NAME <$SENDER_ADDRESS>" \
    --header "To: $RECIPIENT_NAME <$RECIPIENT_ADDRESS>" \
    --data-binary "$MESSAGE"
