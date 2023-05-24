import os
import subprocess

CLASH_SERVICE_FILE = '/lib/systemd/system/clash@.service'

def reload_systemd():
    subprocess.run(['systemctl', 'daemon-reload'])

def start_clash_service():
    username = get_current_username()
    subprocess.run(['systemctl', 'start', f'clash@{username}'])

def stop_clash_service():
    username = get_current_username()
    subprocess.run(['systemctl', 'stop', f'clash@{username}'])

def get_clash_service_status():
    username = get_current_username()
    subprocess.run(['systemctl', 'status', f'clash@{username}'])

def enable_autostart():
    username = get_current_username()
    subprocess.run(['systemctl', 'enable', f'clash@{username}'])
    print(f'已设置 Clash 服务在开机时自启动')

def get_current_username():
    return os.getlogin()

def prompt_menu():
    while True:
        print('请选择操作：')
        print('1. 安装 Clash 服务')
        print('2. 重新加载 systemd')
        print('3. 启动 Clash 服务')
        print('4. 停止 Clash 服务')
        print('5. 查看 Clash 服务')
        print('6. 设置开机自启动')
        print('0. 退出')
        choice = input('输入你的选择：')
        if choice == '1':
            install_clash_service()
        elif choice == '2':
            reload_systemd()
        elif choice == '3':
            start_clash_service()
        elif choice == '4':
            stop_clash_service()
        elif choice == '5':
            get_clash_service_status()
        elif choice == '6':
            enable_autostart()
        elif choice == '0':
            break
        else:
            print('无效的选择')

def install_clash_service():
    service_content = '''
[Unit]
Description=A rule based proxy in Go for %i.
After=network.target

[Service]
Type=simple
User=%i
Restart=on-abort
ExecStart=/usr/bin/clash

[Install]
WantedBy=multi-user.target
'''
    with open(CLASH_SERVICE_FILE, 'w') as f:
        f.write(service_content)
    print(f'Clash 服务已成功安装到 {CLASH_SERVICE_FILE}')

if __name__ == '__main__':
    prompt_menu()
