<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

function http_ping($serwer) {
    $czas = microtime(true);
    file('http://' . $serwer);
    return microtime(true) - $czas;
}

$serwery = array('192.168.122.253', '192.168.122.28');
$opoznienie = array();

foreach ($serwery as $serwer) {
    $opoznienie[$serwer] = http_ping($serwer);
}

asort($opoznienie); // Sortowanie serwerów według opóźnienia rosnąco

$najlepszy_serwer = key($opoznienie); // Pobranie serwera z najmniejszym opóźnieniem

echo json_encode(['server' => $najlepszy_serwer]);

?>
