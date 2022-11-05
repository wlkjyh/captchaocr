<?php
while (true) {
    file_put_contents('c.png', file_get_contents('https://qlnote.sylu.edu.cn/check_code/'));
    $url = 'http://127.0.0.1:5000/ocr';
    $postdata = [
        'file' => new CURLFile('c.png'),
    ];
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postdata);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);
    echo $response."\n";
}
