import subprocess
import re

def get_saved_wifi_passwords():
    # Run command to list Wi-Fi profiles
    profiles_output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
    profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_output)

    wifi_data = []

    for profile in profiles:
        try:
            # Run command to get password for each profile
            profile_info = subprocess.check_output(
                f'netsh wlan show profile name="{profile}" key=clear',
                shell=True, text=True
            )
            password_match = re.search(r"Key Content\s*:\s*(.*)", profile_info)
            password = password_match.group(1) if password_match else "N/A"

            wifi_data.append((profile, password))
        except subprocess.CalledProcessError:
            wifi_data.append((profile, "Error retrieving"))

    return wifi_data


if __name__ == "__main__":
    print("{:<30} | {}".format("SSID", "PASSWORD"))
    print("-" * 50)
    for ssid, password in get_saved_wifi_passwords():
        print("{:<30} | {}".format(ssid, password))
