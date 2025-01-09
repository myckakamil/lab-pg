<?php
session_start();

// Ścieżka do pliku cache
$cacheFile = './nonce_cache.json';

// Sprawdzanie, czy plik istnieje i czy zawartość jest aktualna
if (file_exists($cacheFile)) {
    $cacheData = json_decode(file_get_contents($cacheFile), true);
    if ($cacheData && (time() - $cacheData['timestamp']) <= 10) {
        // Jeśli klucz jest aktualny, użyj go
        $nonce = $cacheData['nonce'];
    } else {
        // Jeśli klucz wygasł, generuj nowy
        $nonce = sha1(uniqid());
        $expiresIn = 10;
        file_put_contents($cacheFile, json_encode(['nonce' => $nonce, 'timestamp' => time()]));
    }
} else {
    // Jeśli plik nie istnieje, generuj nowy klucz
    $nonce = sha1(uniqid());
    file_put_contents($cacheFile, json_encode(['nonce' => $nonce, 'timestamp' => time()]));
}

// Zapamiętanie klucza w sesji
$_SESSION['nonce'] = $nonce;

// Wysyłanie klucza w formacie JSON
$result['nonce'] = $nonce;
header('Content-Type: application/json; charset=utf8');
header('Access-Control-Allow-Origin: *');
print(json_encode($result));
?>