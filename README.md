# server-vpn

The "server-vpn" project provides a convenient way to set up a VPN proxy using Clash on a Linux server. It consists of two scripts: `autostart.py` and `install_clash.py`.

## Purpose

The purpose of this project is to simplify the process of installing and managing Clash as a VPN proxy on a Linux server. It offers the following features:

- Installation of Clash service and configuration.
- Automatic startup and shutdown of Clash service.
- Checking the status of the Clash service.
- Viewing real-time logs of the Clash service.
- Enabling Clash service to start automatically on system boot.

## Prerequisites

Before using this project, make sure you have the following:

- A Linux server where you have administrative access.
- Python 3 installed on the server.
- Basic knowledge of working with the command line on Linux.

## Usage

1. Clone or download the "server-vpn" project to your Linux server.

2. Install Clash:
   - Place the Clash binary file in the `clash` directory within the project.
   - Run the `install_clash.py` script to select and install the desired Clash binary.

3. Configure the Clash service:
   - Modify the Clash configuration file located at `/path/to/clash/config` to suit your needs.

4. Start, stop, or check the status of the Clash service:
   - Execute the `autostart.py` script and select the appropriate option from the menu.
   - Option 1: Install Clash service (required only once).
   - Option 2: Reload systemd configuration.
   - Option 3: Start the Clash service.
   - Option 4: Stop the Clash service.
   - Option 5: Check the status of the Clash service.
   - Option 6: Enable Clash service to start on system boot.

5. View Clash logs:
   - Choose option 5 from the menu to view real-time logs of the Clash service.
   - Press `Ctrl-C` to stop viewing the logs.

6. Customize the configuration:
   - Adjust Clash settings, rules, and other configurations in the Clash configuration file.

## Disclaimer

This project assumes that you have the necessary rights and permissions to use a VPN proxy and that you comply with all applicable laws and regulations. Please use this project responsibly and at your own risk.

## License

This project is licensed under the [MIT License](LICENSE).
