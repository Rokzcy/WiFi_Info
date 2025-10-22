# List all saved Wi-Fi profiles and their passwords
$profiles = netsh wlan show profiles | Select-String "All User Profile" | ForEach-Object {
    ($_ -split ":")[1].Trim()
}

foreach ($profile in $profiles) {
    $wifi = netsh wlan show profile name="$profile" key=clear | Select-String "Key Content"
    if ($wifi) {
        $password = ($wifi -split ":")[1].Trim()
    } else {
        $password = "N/A"
    }
    [PSCustomObject]@{
        SSID     = $profile
        Password = $password
    }
} | Format-Table -AutoSize
