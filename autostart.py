import argparse
import json
import os
import subprocess
from crontab import CronTab

CLASH_SERVICE_FILE = '/lib/systemd/system/clash@.service'
CONFIG_JSON_FILE = 'config.json'

def is_clash_service_running():
    username = get_current_username()
    command = ['systemctl', 'is-active', f'clash@{username}']
    result = subprocess.run(command, capture_output=True, text=True)
    return 'active' in result.stdout

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

def restart_clash_service():
    username = get_current_username()
    command = ['systemctl', 'restart', f'clash@{username}']
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
        url = data['configUrl']
    
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
        if is_clash_service_running():
            print('正在重启 Clash 服务以使新的配置文件生效...')
            restart_clash_service()
        else:
            print('Clash 服务当前未运行，不进行重启')
    except subprocess.CalledProcessError:
        print('更新 Clash 配置文件失败，请检查您的 URL 是否正确')

def create_cron_job():
    with open(CONFIG_JSON_FILE) as json_file:
        data = json.load(json_file)
        cron_setting = data['cronJob']
    cron = CronTab(user=True)
    command = f'{cron_setting["interpreter"]} {cron_setting["script"]} {cron_setting["argument"]}'
    job = cron.new(command=command)
    job.setall(cron_setting['cron'])
    cron.write()
    print('已设置 cron 任务')

def view_cron_jobs():
    cron = CronTab(user=True)
    for job in cron:
        print(job)

def get_current_username():
    return os.getlogin()

def prompt_menu():
    while True:
        print('请选择操作：')
        print('1. 安装 Clash 服务')
        print('2. 重新加载 systemd')
        print('3. 启动 Clash 服务')
        print('4. 停止 Clash 服务')
        print('5. 重启 Clash 服务')
        print('6. 查看 Clash 服务')
        print('7. 设置开机自启动')
        print('8. 更新 Clash 配置')
        print('9. 设置 cron 任务')
        print('10. 查看 cron 任务')
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
            restart_clash_service()
        elif choice == '6':
            get_clash_service_status()
        elif choice == '7':
            enable_autostart()
        elif choice == '8':
            update_config()
        elif choice == '9':
            create_cron_job()
        elif choice == '10':
            view_cron_jobs()
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?', default='')
    args = parser.parse_args()
    if args.command == 'update_config':
        update_config()
    elif args.command == 'restart':
        restart_clash_service()
    else:
        prompt_menu()

if __name__ == '__main__':
    main()