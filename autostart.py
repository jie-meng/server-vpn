import argparse
import json
import os
import subprocess
from crontab import CronTab

CLASH_SERVICE_FILE = '/lib/systemd/system/clash@.service'
CONFIG_JSON_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

class Command:
    def __init__(self, name, function):
        self.name = name
        self.function = function

def is_clash_service_running():
    username = get_current_username()
    result = subprocess.getoutput(f'systemctl is-active clash@{username}')
    return result == 'active'

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

def delete_cron_job():
    with open(CONFIG_JSON_FILE) as json_file:
        data = json.load(json_file)
        cron_setting = data['cronJob']
    cron = CronTab(user=True)
    command = f'{cron_setting["interpreter"]} {cron_setting["script"]} {cron_setting["argument"]}'
    cron.remove_all(command=command)
    cron.write()
    print('已删除指定的 cron 任务')

def get_current_username():
    return os.getlogin()

def prompt_menu():
    commands = [
        Command('安装 Clash 服务', install_clash_service),
        Command('重新加载 systemd', reload_systemd),
        Command('启动 Clash 服务', start_clash_service),
        Command('停止 Clash 服务', stop_clash_service),
        Command('重启 Clash 服务', restart_clash_service),
        Command('查看 Clash 服务', get_clash_service_status),
        Command('设置开机自启动', enable_autostart),
        Command('更新 Clash 配置', update_config),
        Command('设置 cron 任务', create_cron_job),
        Command('查看 cron 任务', view_cron_jobs),
        Command('删除 cron 任务', delete_cron_job),
    ]

    while True:
        print('请选择操作：')
        for i, command in enumerate(commands):
            print(f'{i + 1}. {command.name}')
        print('0. 退出')

        choice = input('输入你的选择：')
        if choice == '0':
            break
        try:
            index = int(choice) - 1
            command = commands[index]
            if command.function is not None:
                command.function()
        except (ValueError, IndexError):
            print('无效的选择，请重新输入。')
        
        print('')


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
