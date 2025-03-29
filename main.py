import subprocess
import locale

def get_wifi_password():
    # Определяем язык системы
    lang = locale.getencoding()

    # Устанавливаем ключевые фразы для разных языков
    if lang.startswith("ru"):
        profile_keyword = "Все профили пользователей"
        key_content_keyword = "Содержимое ключа"
    else:
        profile_keyword = "All User Profile"
        key_content_keyword = "Key Content"

    # Получаем профили Wi-Fi
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode('cp866', errors='ignore').split('\n')
    profiles = [i.split(":")[1].strip() for i in profiles_data if profile_keyword in i]

    if profiles:
        # Перебираем все профили и ищем пароль
        for profile in profiles:
            try:
                wifi_details = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('cp866', errors='ignore').split('\n')
                # Ищем строку с ключом безопасности
                password = [b.split(":")[1].strip() for b in wifi_details if key_content_keyword in b]
                if password:
                    print(f'Profile: {profile}\nPassword: {password[0]}\n')
                else:
                    print(f'Profile: {profile}\nPassword: Cannot be retrieved\n')
            except subprocess.CalledProcessError as e:
                print(f'Error retrieving information for profile {profile}. Error code: {e.returncode}')
    else:
        print("No profiles found. Are you connected to a Wi-Fi network?")

if __name__ == "__main__":
    get_wifi_password()
