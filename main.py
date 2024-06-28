import subprocess

def get_wifi_password():
    # Получаем профили Wi-Fi
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('cp866').split('n')
    profiles = [i.split(":")[1][1:-1] for i in profiles_data if "Все профили пользователей" in i]

    if len(profiles) > 0:
        # Перебираем все профили и ищем пароль
        for profile in profiles:
            # Пытаемся извлечь детали профиля, включая пароль
            try:
                wifi_details = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('cp866').split('n')
                # Ищем строку с ключом безопасности
                password = [b.split(":")[1][1:-1] for b in wifi_details if "Содержимое ключа" in b]
                if password:
                    print(f'Profile: {profile}nPassword: {password[0]}n')
                else:
                    print(f'Profile: {profile}nPassword: Cannot be retrievedn')
            except subprocess.CalledProcessError as e:
                print(f'Error retrieving information for profile {profile}. Error code: {e.returncode}')
    else:
        print("No profiles found. Are you connected to a wifi network?")

if __name__ == "__main__":
    get_wifi_password()
