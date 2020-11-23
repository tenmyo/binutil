param(
    [string] $ip='127.0.0.1',
    [int] $port=8080,
    [parameter(mandatory)][string] $fpath
)

Set-StrictMode -Version Latest
[byte[]]$data = [System.IO.File]::ReadAllBytes($fpath)
$sock = New-Object System.Net.Sockets.UdpClient
$sock.Send($data, $data.Length, $ip, $port)
$sock.Close()
