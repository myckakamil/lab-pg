<?php
session_start();
$nonce = sha1(uniqid());
$_SESSION['nonce'] = $nonce;
$result['nonce'] = $nonce;
header('Content-Type: application/json; charset=utf8');
header('Access-Control-Allow-Origin: *');
print(json_encode($result));
