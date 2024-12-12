<?php
header('Content-Type: application/json; charset=utf-8');

$users = [
    'student' => 'pg'
];

$input = file_get_contents('php://input');
$data = json_decode($input, true);

$user = $data['user'];
$net = $data['net'];
$nonce = $data['nonce'];

$password = $users[$user];

function calculateNet($password, $nonce) {
    return base64_encode(base64_encode($password) . $nonce); 
}

$expectedNet = calculateNet($password, $nonce);

if ($net === $expectedNet) {
    echo json_encode(['code' => 'OK', 'message' => 'Authentication successful']);
} else {
    echo json_encode(['code' => 'ERROR', 'message' => 'Authentication failed']);
}
?>