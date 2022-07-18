<?php

$encrypted = "173ca059bf5d2027251c499b87ca1806b6c6c304153d203b38";
$encrypted  = str_split($encrypted, 2);

$flag_part = str_split("}ecsc{");
$checks = [];

for ($i = 0; $i < 4; $i++) {
    array_push($checks, [ord($flag_part[$i]) % 32, hexdec($encrypted[$i]) ^ ord($flag_part[$i + 1]) ^ ord($flag_part[$i + 2])]);
}

$keys = [];

for ($i = 2 ** 29; $i < 2 ** 32; $i++) {
    $key_attempt = ($i) << 32 | $i;

    $correct = true;

    foreach ($checks as $x) {
        if ((($key_attempt >> $x[0]) & 255) != $x[1]) {
            $correct = false;
            break;
        }
    }

    if ($correct)
        array_push($keys, $key_attempt);
}

foreach ($keys as $key) {
    $key = ($key) << 32 | $key;
    
    $flag = "ec";
    
    for ($i = 1; $i < count($encrypted) - 1; $i++) {
        $next = chr(ord($flag[$i]) ^ hexdec($encrypted[$i]) ^ (($key >> (ord($flag[$i - 1]) % 32)) & 255));
        $flag .= $next;
    }
    
    if (mb_detect_encoding($flag, 'ASCII', true))
        echo $flag . ' ';
}

?>