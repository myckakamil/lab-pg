<?php
// Obsługuje zapytanie OPTIONS (preflight request)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    // Wysyła odpowiedź bez treści
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type');
    http_response_code(204); // Brak treści w odpowiedzi
    exit;
}

// Nagłówki CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Kontynuacja działania skryptu dla metod POST/GET
session_start();
header('Content-Type: application/json; charset=utf-8');

// Kontynuacja działania skryptu dla metod POST/GET
session_start();
header('Content-Type: application/json; charset=utf-8');

$users = [
    'student' => 'pg',
    'test' => 'test'
];

$input = file_get_contents('php://input');
$data = json_decode($input, true);

$user = $data['user'];
$net = $data['net'];
$nonce = $data['nonce'];

$password = $users[$user];

function calculateNet($password, $nonce) {
    return md5(md5($password) . $nonce);
}

$expectedNet = calculateNet($password, $nonce);

if ($net === $expectedNet) {
    echo json_encode(['code' => 'OK', 'message' => 'Authentication successful']);
} else {
    echo json_encode(['code' => 'ERROR', 'message' => 'Authentication failed']);
}
?>
