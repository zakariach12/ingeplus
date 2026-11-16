<?php
/**
 * INGEPLUS — traitement du formulaire de contact
 * Fonctionne sur tout hébergement PHP (mail() activé).
 * Pour un envoi plus fiable, configurer un SMTP (ex. PHPMailer) chez l'hébergeur.
 */
header('Content-Type: application/json; charset=utf-8');

$TO      = 'contact@ingeplus.ma';          // destinataire des demandes
$FROM    = 'no-reply@ingeplus.ma';         // adresse d'envoi (doit appartenir au domaine)
$SUBJECT = 'Nouvelle demande via ingeplus.ma';

function fail($msg, $code = 400) { http_response_code($code); echo json_encode(['ok' => false, 'error' => $msg]); exit; }
function clean($v) { return trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', strip_tags((string)$v))); }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Méthode non autorisée.', 405);

// Anti-spam : champ piège + délai minimal entre deux envois par session
if (!empty($_POST['website'])) { echo json_encode(['ok' => true]); exit; }
session_start();
if (isset($_SESSION['last_submit']) && time() - $_SESSION['last_submit'] < 30) fail('Merci de patienter quelques secondes avant un nouvel envoi.', 429);

$nom     = clean($_POST['nom'] ?? '');
$societe = clean($_POST['societe'] ?? '');
$email   = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$tel     = clean($_POST['tel'] ?? '');
$ville   = clean($_POST['ville'] ?? '');
$service = clean($_POST['service'] ?? '');
$message = trim(strip_tags((string)($_POST['message'] ?? '')));
$consent = !empty($_POST['consent']);

if ($nom === '' || !$email || $message === '') fail('Merci de renseigner votre nom, un e-mail valide et votre message.');
if (!$consent) fail('Merci d’accepter l’utilisation de vos données pour traiter votre demande.');
if (mb_strlen($message) > 5000) fail('Votre message est trop long.');

$body  = "Nouvelle demande reçue depuis le site ingeplus.ma\n";
$body .= str_repeat('-', 48) . "\n";
$body .= "Nom        : $nom\nSociété    : " . ($societe ?: '-') . "\nE-mail     : $email\n";
$body .= "Téléphone  : " . ($tel ?: '-') . "\nVille      : " . ($ville ?: '-') . "\nExpertise  : $service\n\n";
$body .= "Message :\n$message\n";

$headers  = "From: INGEPLUS Site <$FROM>\r\n";
$headers .= "Reply-To: $nom <$email>\r\n";
$headers .= "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n";

$subject = '=?UTF-8?B?' . base64_encode("$SUBJECT – $service") . '?=';

if (@mail($TO, $subject, $body, $headers, "-f$FROM")) {
  $_SESSION['last_submit'] = time();
  echo json_encode(['ok' => true]);
} else {
  fail('L’envoi a échoué. Merci de nous écrire directement à ' . $TO . ' ou de nous appeler.', 500);
}
