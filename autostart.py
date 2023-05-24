import subprocess

CLASH_SERVICE_FILE = '/lib/systemd/system/clash@.service'

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

def start_clash_service():
    subprocess.run(['systemctl', 'start', 'clash'])

def stop_clash_service():
    subprocess.run(['systemctl', 'stop', 'clash'])

def get_clash_service_status():
    subprocess.run(['systemctl', 'status', 'clash'])

def display_clash_service_log():
    process = subprocess.Popen(['journalctl', '-u', 'clash', '-f'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for line in iter(process.stdout.readline, b''):
            print(line.decode().strip())
    except KeyboardInterrupt:
        process.terminate()

def prompt_menu():
    while True:
        print('请选择操作：')
        print('1. 安装 Clash 服务')
        print('2. 启动 Clash 服务')
        print('3. 停止 Clash 服务')
        print('4. 查看 Clash 服务状态')
        print('5. 查看 Clash 服务日志')
        print('0. 退出')
        choice = input('输入你的选择：')
        if choice == '1':
            install_clash_service()
        elif choice == '2':
            start_clash_service()
        elif choice == '3':
            stop_clash_service()
        elif choice == '4':
            get_clash_service_status()
        elif choice == '5':
            display_clash_service_log()
        elif choice == '0':
            break
        else:
            print('无效的选择')

if __name__ == '__main__':
    prompt_menu()
