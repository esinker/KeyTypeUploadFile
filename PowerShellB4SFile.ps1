
$from_file  = "base64str.txt"
$to_file    =  "recoverfile.zip"
$b64        = Get-Content $from_file
$bytes      = [Convert]::FromBase64String($b64)
[IO.File]::WriteAllBytes($to_file, $bytes)