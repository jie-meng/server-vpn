import json
import os
import subprocess

CLASH_SERVICE_FILE = '/lib/systemd/system/clash@.service'
CONFIG_JSON_FILE = 'config.json'

def reload_systemd():
    command = ['systemctl', 'daemon-reload']
    print(f'执行命令: {" ".join(command)}')
    subprocess.run(command)

def start_clash_service():
    username = get_current_username()
    command = ['systemctl', 'start', f'clash@{username}']
    print(f'执行命令: {" ".join(command)}')
    subprocess.run(command)

def stop_clash_service():
    username = get_current_username()
    command = ['systemctl', 'stop', f'clash@{username}']
    print(f'执行命令: {" ".join(command)}')
    subprocess.run(command)

def get_clash_service_status():
    username = get_current_username()
    command = ['systemctl', 'status', f'clash@{username}']
    print(f'执行命令: {" ".join(command)}')
    subprocess.run(command)

def enable_autostart():
    username = get_current_username()
    command = ['systemctl', 'enable', f'clash@{username}']
    print(f'执行命令: {" ".join(command)}')
    subprocess.run(command)
    print(f'已设置 Clash 服务在开机时自启动')

def update_config():
    with open(CONFIG_JSON_FILE) as json_file:
        data = json.load(json_file)
        url = data['config_url']
    
    if url == '':
        print('您的配置文件 url 为空，无法更新 Clash 配置文件')
        return

    config_path = os.path.join(os.path.expanduser('~'), '.config/clash')
    new_config_path = os.path.join(config_path, 'config_new.yaml')
    old_config_path = os.path.join(config_path, 'config.yaml')
    command = ['wget', '-O', new_config_path, url]
    print(f'执行命令: {" ".join(command)}')
    try:
        subprocess.run(command, check=True)
        if os.path.exists(old_config_path):
            os.remove(old_config_path)
        os.rename(new_config_path, old_config_path)
        print('成功更新 Clash 配置文件')
    except subprocess.CalledProcessError:
        print('更新 Clash 配置文件失败，请检查您的 URL 是否正确')

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
        print('7. 更新 Clash 配置')
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
        elif choice == '7':
            update_config()
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
