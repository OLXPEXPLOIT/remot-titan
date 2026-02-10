#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import socket
import threading
import time
import json
import subprocess
import requests
from datetime import datetime
import hashlib
import base64

# Import Termux API
try:
    import termux
    TERMUX_AVAILABLE = True
except ImportError:
    TERMUX_AVAILABLE = False

# Color codes untuk terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Banner Attack on Titan
def display_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║    ████████╗██╗████████╗ █████╗ ███╗   ██╗                      ║
    ║    ╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║                      ║
    ║       ██║   ██║   ██║   ███████║██╔██╗ ██║                      ║
    ║       ██║   ██║   ██║   ██╔══██║██║╚██╗██║                      ║
    ║       ██║   ██║   ██║   ██║  ██║██║ ╚████║                      ║
    ║       ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝                      ║
    ║                                                                  ║
    ║    ██████╗ ███████╗███╗   ███╗ ██████╗ ████████╗███████╗        ║
    ║    ██╔══██╗██╔════╝████╗ ████║██╔═══██╗╚══██╔══╝██╔════╝        ║
    ║    ██████╔╝█████╗  ██╔████╔██║██║   ██║   ██║   █████╗          ║
    ║    ██╔══██╗██╔══╝  ██║╚██╔╝██║██║   ██║   ██║   ██╔══╝          ║
    ║    ██║  ██║███████╗██║ ╚═╝ ██║╚██████╔╝   ██║   ███████╗        ║
    ║    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚══════╝        ║
    ║                                                                  ║
    ║                SURVEY CORPS REMOTE CONTROL SYSTEM               ║
    ║                 Version 2.0 - Multi-Feature                      ║
    ╚══════════════════════════════════════════════════════════════════╝
{Colors.END}
    {Colors.YELLOW}[!] Shinzo wo Sasageyo! Dedikasikan Hatimu!{Colors.END}
    {Colors.CYAN}[!] System Initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}
    """
    print(banner)

class TitanRemoteSystem:
    def __init__(self, host='0.0.0.0', port=6969):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
        self.config = self.load_config()
        self.current_flashlight = False
        self.current_volume = 50
        
    def load_config(self):
        """Load konfigurasi dari file"""
        config = {
            'password': 'titan123',  # Password default
            'max_clients': 5,
            'log_commands': True,
            'auto_start': False,
            'features': {
                'flashlight': True,
                'camera': True,
                'whatsapp': True,
                'youtube': True,
                'volume': True,
                'wifi': True,
                'bluetooth': True,
                'screenshot': True,
                'notification': True,
                'call': True,
                'sms': True
            }
        }
        
        config_path = '/data/data/com.termux/files/home/.titan_remote.json'
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    config.update(user_config)
            except:
                pass
                
        return config
        
    def save_config(self):
        """Simpan konfigurasi ke file"""
        config_path = '/data/data/com.termux/files/home/.titan_remote.json'
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
            
    def get_ip_address(self):
        """Dapatkan IP address perangkat"""
        try:
            # Coba beberapa metode untuk mendapatkan IP
            ip_methods = [
                "ip route get 1 | awk '{print $7}'",
                "ifconfig wlan0 | grep 'inet ' | awk '{print $2}'",
                "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
            ]
            
            for cmd in ip_methods:
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.stdout.strip():
                        return result.stdout.strip()
                except:
                    continue
                    
            # Jika semua gagal, gunakan localhost
            return "127.0.0.1"
        except:
            return "127.0.0.1"
            
    def execute_command(self, command):
        """Eksekusi command di Termux"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def control_flashlight(self, action):
        """Kontrol flashlight (senter)"""
        try:
            if action == "on":
                if TERMUX_AVAILABLE:
                    # Gunakan Termux API jika tersedia
                    os.system("termux-torch on")
                else:
                    # Fallback ke metode lain
                    os.system("echo 'Flashlight ON'")
                self.current_flashlight = True
                return f"{Colors.GREEN}[+] Flashlight ON - Signal Api Menyala!{Colors.END}"
                
            elif action == "off":
                if TERMUX_AVAILABLE:
                    os.system("termux-torch off")
                else:
                    os.system("echo 'Flashlight OFF'")
                self.current_flashlight = False
                return f"{Colors.YELLOW}[-] Flashlight OFF{Colors.END}"
                
            elif action == "blink":
                response = f"{Colors.CYAN}[*] Blinking Flashlight (3x)...{Colors.END}\n"
                for i in range(3):
                    self.control_flashlight("on")
                    time.sleep(0.3)
                    self.control_flashlight("off")
                    time.sleep(0.3)
                    response += f"Blink {i+1}\n"
                return response
                
        except Exception as e:
            return f"{Colors.RED}[!] Error: {str(e)}{Colors.END}"
            
    def open_camera(self, mode="photo"):
        """Buka kamera"""
        try:
            if mode == "photo":
                if TERMUX_AVAILABLE:
                    os.system("termux-camera-photo /data/data/com.termux/files/home/camera_photo.jpg")
                    return f"{Colors.GREEN}[+] Photo taken: /data/data/com.termux/files/home/camera_photo.jpg{Colors.END}"
                else:
                    return f"{Colors.YELLOW}[!] Termux API not available for camera{Colors.END}"
            elif mode == "video":
                return f"{Colors.CYAN}[*] Starting video recording (5 seconds){Colors.END}"
                # Implement video recording here
        except Exception as e:
            return f"{Colors.RED}[!] Camera Error: {str(e)}{Colors.END}"
            
    def open_whatsapp(self, number=None, message=None):
        """Buka WhatsApp"""
        try:
            if number:
                if message:
                    # Buka WhatsApp dengan nomor dan pesan
                    whatsapp_url = f"whatsapp://send?phone={number}&text={message}"
                else:
                    # Buka chat dengan nomor tertentu
                    whatsapp_url = f"whatsapp://send?phone={number}"
            else:
                # Buka WhatsApp biasa
                whatsapp_url = "whatsapp://"
                
            os.system(f"am start -a android.intent.action.VIEW -d '{whatsapp_url}'")
            return f"{Colors.GREEN}[+] Opening WhatsApp...{Colors.END}"
            
        except Exception as e:
            return f"{Colors.RED}[!] WhatsApp Error: {str(e)}{Colors.END}"
            
    def open_youtube(self, video_id=None):
        """Buka YouTube"""
        try:
            if video_id:
                # Buka video tertentu
                youtube_url = f"https://youtube.com/watch?v={video_id}"
                os.system(f"am start -a android.intent.action.VIEW -d '{youtube_url}'")
                return f"{Colors.GREEN}[+] Opening YouTube video: {video_id}{Colors.END}"
            else:
                # Buka YouTube app
                os.system("am start -n com.google.android.youtube/com.google.android.youtube.HomeActivity")
                return f"{Colors.GREEN}[+] Opening YouTube app...{Colors.END}"
                
        except Exception as e:
            return f"{Colors.RED}[!] YouTube Error: {str(e)}{Colors.END}"
            
    def control_volume(self, action, value=None):
        """Kontrol volume"""
        try:
            if action == "set":
                if value:
                    self.current_volume = int(value)
                    os.system(f"termux-volume music {value}")
                    return f"{Colors.GREEN}[+] Volume set to {value}%{Colors.END}"
            elif action == "up":
                self.current_volume = min(100, self.current_volume + 10)
                os.system(f"termux-volume music {self.current_volume}")
                return f"{Colors.GREEN}[+] Volume increased to {self.current_volume}%{Colors.END}"
            elif action == "down":
                self.current_volume = max(0, self.current_volume - 10)
                os.system(f"termux-volume music {self.current_volume}")
                return f"{Colors.GREEN}[+] Volume decreased to {self.current_volume}%{Colors.END}"
            elif action == "mute":
                os.system("termux-volume music 0")
                return f"{Colors.YELLOW}[-] Volume muted{Colors.END}"
                
        except Exception as e:
            return f"{Colors.RED}[!] Volume Error: {str(e)}{Colors.END}"
            
    def send_notification(self, title, message):
        """Kirim notifikasi"""
        try:
            os.system(f'termux-notification --title "{title}" --content "{message}"')
            return f"{Colors.GREEN}[+] Notification sent: {title}{Colors.END}"
        except Exception as e:
            return f"{Colors.RED}[!] Notification Error: {str(e)}{Colors.END}"
            
    def make_call(self, number):
        """Lakukan panggilan telepon"""
        try:
            os.system(f"am start -a android.intent.action.CALL -d tel:{number}")
            return f"{Colors.GREEN}[+] Calling: {number}{Colors.END}"
        except Exception as e:
            return f"{Colors.RED}[!] Call Error: {str(e)}{Colors.END}"
            
    def send_sms(self, number, message):
        """Kirim SMS"""
        try:
            os.system(f'am start -a android.intent.action.SENDTO -d sms:{number} --es sms_body "{message}"')
            return f"{Colors.GREEN}[+] SMS ready to send to {number}{Colors.END}"
        except Exception as e:
            return f"{Colors.RED}[!] SMS Error: {str(e)}{Colors.END}"
            
    def take_screenshot(self):
        """Ambil screenshot"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/data/data/com.termux/files/home/screenshot_{timestamp}.png"
            os.system(f"screencap -p {filename}")
            return f"{Colors.GREEN}[+] Screenshot saved: {filename}{Colors.END}"
        except Exception as e:
            return f"{Colors.RED}[!] Screenshot Error: {str(e)}{Colors.END}"
            
    def get_system_info(self):
        """Dapatkan informasi sistem"""
        try:
            info = {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'battery': subprocess.getoutput("termux-battery-status"),
                'storage': subprocess.getoutput("df -h /data"),
                'memory': subprocess.getoutput("free -h"),
                'wifi': subprocess.getoutput("termux-wifi-connectioninfo")
            }
            
            result = f"{Colors.CYAN}=== SYSTEM INFORMATION ==={Colors.END}\n"
            for key, value in info.items():
                result += f"{Colors.YELLOW}{key.upper()}:{Colors.END}\n{value}\n"
                
            return result
        except Exception as e:
            return f"{Colors.RED}[!] System Info Error: {str(e)}{Colors.END}"
            
    def handle_command(self, client_socket, command, args=None):
        """Handle command dari client"""
        response = ""
        
        # Log command
        if self.config['log_commands']:
            log_msg = f"[{datetime.now()}] Command: {command} | Args: {args}"
            print(f"{Colors.MAGENTA}[LOG] {log_msg}{Colors.END}")
            
        # Process commands
        if command == "HELP":
            response = self.show_help()
            
        elif command == "FLASHLIGHT":
            if args and args[0] in ["on", "off", "blink"]:
                response = self.control_flashlight(args[0])
            else:
                response = f"{Colors.RED}[!] Usage: FLASHLIGHT [on|off|blink]{Colors.END}"
                
        elif command == "CAMERA":
            mode = args[0] if args else "photo"
            response = self.open_camera(mode)
            
        elif command == "WHATSAPP":
            number = args[0] if len(args) > 0 else None
            message = " ".join(args[1:]) if len(args) > 1 else None
            response = self.open_whatsapp(number, message)
            
        elif command == "YOUTUBE":
            video_id = args[0] if args else None
            response = self.open_youtube(video_id)
            
        elif command == "VOLUME":
            if args:
                if args[0] in ["up", "down", "mute"]:
                    response = self.control_volume(args[0])
                elif args[0] == "set" and len(args) > 1:
                    response = self.control_volume("set", args[1])
                else:
                    response = f"{Colors.RED}[!] Usage: VOLUME [up|down|mute|set VALUE]{Colors.END}"
            else:
                response = f"{Colors.YELLOW}[*] Current volume: {self.current_volume}%{Colors.END}"
                
        elif command == "NOTIFY":
            if len(args) >= 2:
                title = args[0]
                message = " ".join(args[1:])
                response = self.send_notification(title, message)
            else:
                response = f"{Colors.RED}[!] Usage: NOTIFY [title] [message]{Colors.END}"
                
        elif command == "CALL":
            if args:
                response = self.make_call(args[0])
            else:
                response = f"{Colors.RED}[!] Usage: CALL [phone_number]{Colors.END}"
                
        elif command == "SMS":
            if len(args) >= 2:
                number = args[0]
                message = " ".join(args[1:])
                response = self.send_sms(number, message)
            else:
                response = f"{Colors.RED}[!] Usage: SMS [number] [message]{Colors.END}"
                
        elif command == "SCREENSHOT":
            response = self.take_screenshot()
            
        elif command == "SYSINFO":
            response = self.get_system_info()
            
        elif command == "REBOOT":
            response = f"{Colors.RED}[!] Rebooting device...{Colors.END}"
            os.system("reboot")
            
        elif command == "SHUTDOWN":
            response = f"{Colors.RED}[!] Shutting down...{Colors.END}"
            os.system("poweroff")
            
        elif command == "PING":
            response = f"{Colors.GREEN}[+] PONG! Titan System Active{Colors.END}"
            
        elif command == "STATUS":
            status_msg = f"""
{Colors.CYAN}=== TITAN SYSTEM STATUS ==={Colors.END}
{Colors.YELLOW}Flashlight:{Colors.END} {'ON' if self.current_flashlight else 'OFF'}
{Colors.YELLOW}Volume:{Colors.END} {self.current_volume}%
{Colors.YELLOW}Connected Clients:{Colors.END} {len(self.clients)}
{Colors.YELLOW}System Time:{Colors.END} {datetime.now().strftime('%H:%M:%S')}
{Colors.YELLOW}Uptime:{Colors.END} {self.get_uptime()}
            """
            response = status_msg
            
        elif command == "EXIT":
            response = f"{Colors.RED}[!] Disconnecting... Shinzo wo Sasageyo!{Colors.END}"
            client_socket.send(response.encode())
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            return
            
        else:
            response = f"{Colors.RED}[!] Unknown command: {command}{Colors.END}"
            
        # Kirim response ke client
        try:
            client_socket.send(response.encode())
        except:
            pass
            
    def show_help(self):
        """Tampilkan help menu"""
        help_text = f"""
{Colors.CYAN}{Colors.BOLD}=== TITAN REMOTE CONTROL - COMMAND LIST ==={Colors.END}

{Colors.YELLOW}{Colors.BOLD}[FLASHLIGHT CONTROLS]{Colors.END}
  FLASHLIGHT on          - Turn flashlight ON
  FLASHLIGHT off         - Turn flashlight OFF  
  FLASHLIGHT blink       - Blink flashlight (3x)

{Colors.YELLOW}{Colors.BOLD}[MEDIA CONTROLS]{Colors.END}
  CAMERA [photo|video]   - Open camera
  YOUTUBE [video_id]     - Open YouTube
  VOLUME up/down/mute    - Control volume
  VOLUME set VALUE       - Set volume (0-100)

{Colors.YELLOW}{Colors.BOLD}[COMMUNICATION]{Colors.END}
  WHATSAPP [number] [msg]- Open WhatsApp
  CALL [number]          - Make a phone call
  SMS [number] [message] - Send SMS
  NOTIFY [title] [msg]   - Send notification

{Colors.YELLOW}{Colors.BOLD}[SYSTEM CONTROLS]{Colors.END}
  SCREENSHOT            - Take screenshot
  SYSINFO               - Show system information
  STATUS                - Show system status
  REBOOT                - Reboot device
  SHUTDOWN              - Shutdown device

{Colors.YELLOW}{Colors.BOLD}[UTILITY]{Colors.END}
  PING                  - Test connection
  HELP                  - Show this help
  EXIT                  - Disconnect

{Colors.GREEN}Example:{Colors.END} FLASHLIGHT on
{Colors.GREEN}Example:{Colors.END} WHATSAPP +628123456789 Hello!
{Colors.GREEN}Example:{Colors.END} YOUTUBE dQw4w9WgXcQ
        """
        return help_text
        
    def get_uptime(self):
        """Dapatkan uptime sistem"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            seconds = int(uptime_seconds % 60)
            
            return f"{hours}h {minutes}m {seconds}s"
        except:
            return "Unknown"
            
    def client_handler(self, client_socket, client_address):
        """Handle koneksi client"""
        print(f"{Colors.GREEN}[+] New connection from {client_address}{Colors.END}")
        self.clients.append(client_socket)
        
        try:
            # Kirim banner welcome
            welcome_msg = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════╗
║      TITAN REMOTE CONTROL SYSTEM CONNECTED       ║
║          Welcome, Survey Corps Member!           ║
╚══════════════════════════════════════════════════╝
{Colors.END}
Type HELP for commands. Type EXIT to disconnect.
            """
            client_socket.send(welcome_msg.encode())
            
            while True:
                # Terima data dari client
                data = client_socket.recv(1024).decode().strip()
                if not data:
                    break
                    
                # Parse command
                parts = data.split()
                if parts:
                    command = parts[0].upper()
                    args = parts[1:] if len(parts) > 1 else None
                    
                    # Handle command
                    self.handle_command(client_socket, command, args)
                    
        except Exception as e:
            print(f"{Colors.RED}[!] Client error: {str(e)}{Colors.END}")
        finally:
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            print(f"{Colors.YELLOW}[-] Client disconnected: {client_address}{Colors.END}")
            
    def start_server(self):
        """Start Titan server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            
            ip_address = self.get_ip_address()
            print(f"{Colors.GREEN}[+] Titan Server started on {ip_address}:{self.port}{Colors.END}")
            print(f"{Colors.GREEN}[+] Waiting for Survey Corps connections...{Colors.END}")
            print(f"{Colors.YELLOW}[!] Type 'stop' to shutdown server{Colors.END}")
            
            # Thread untuk menerima input server commands
            input_thread = threading.Thread(target=self.server_input_handler)
            input_thread.daemon = True
            input_thread.start()
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    
                    # Start thread baru untuk handle client
                    client_thread = threading.Thread(
                        target=self.client_handler,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except Exception as e:
                    if self.running:
                        print(f"{Colors.RED}[!] Accept error: {str(e)}{Colors.END}")
                        
        except Exception as e:
            print(f"{Colors.RED}[!] Server error: {str(e)}{Colors.END}")
        finally:
            self.stop_server()
            
    def server_input_handler(self):
        """Handle input command untuk server"""
        while self.running:
            try:
                cmd = input(f"{Colors.CYAN}titan-server> {Colors.END}").strip()
                
                if cmd.lower() == "stop":
                    print(f"{Colors.YELLOW}[!] Stopping server...{Colors.END}")
                    self.running = False
                    self.stop_server()
                    break
                    
                elif cmd.lower() == "status":
                    print(f"{Colors.CYAN}[*] Active clients: {len(self.clients)}{Colors.END}")
                    print(f"{Colors.CYAN}[*] Flashlight: {'ON' if self.current_flashlight else 'OFF'}{Colors.END}")
                    print(f"{Colors.CYAN}[*] Server running: {self.running}{Colors.END}")
                    
                elif cmd.lower() == "help":
                    print(f"""
{Colors.YELLOW}Server Commands:{Colors.END}
  status    - Show server status
  stop      - Stop the server
  help      - Show this help
                    """)
                    
                elif cmd:
                    print(f"{Colors.RED}[!] Unknown server command: {cmd}{Colors.END}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Stopping server...{Colors.END}")
                self.running = False
                break
            except Exception as e:
                print(f"{Colors.RED}[!] Input error: {str(e)}{Colors.END}")
                
    def stop_server(self):
        """Stop Titan server"""
        self.running = False
        
        # Tutup semua client connections
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # Tutup server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
                
        print(f"{Colors.RED}[!] Titan Server stopped{Colors.END}")

class TitanClient:
    def __init__(self, server_ip, server_port=6969):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.connected = False
        
    def connect(self):
        """Connect ke Titan server"""
        try:
            print(f"{Colors.CYAN}[*] Connecting to {self.server_ip}:{self.server_port}...{Colors.END}")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.connected = True
            
            # Terima welcome message
            welcome = self.client_socket.recv(4096).decode()
            print(welcome)
            
            # Start receive thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[!] Connection failed: {str(e)}{Colors.END}")
            return False
            
    def receive_messages(self):
        """Terima pesan dari server"""
        while self.connected:
            try:
                data = self.client_socket.recv(4096).decode()
                if not data:
                    break
                print(data)
            except:
                break
                
        print(f"{Colors.RED}[!] Disconnected from server{Colors.END}")
        self.connected = False
        
    def send_command(self, command):
        """Kirim command ke server"""
        if not self.connected:
            print(f"{Colors.RED}[!] Not connected to server{Colors.END}")
            return
            
        try:
            self.client_socket.send(command.encode())
        except Exception as e:
            print(f"{Colors.RED}[!] Send failed: {str(e)}{Colors.END}")
            self.connected = False
            
    def start_interactive(self):
        """Mode interactive client"""
        print(f"{Colors.CYAN}[*] Titan Client Interactive Mode{Colors.END}")
        print(f"{Colors.CYAN}[*] Type 'exit' to quit{Colors.END}")
        print(f"{Colors.CYAN}[*] Type 'help' for command list{Colors.END}")
        
        while self.connected:
            try:
                # Prompt dengan warna
                cmd = input(f"{Colors.GREEN}titan-client> {Colors.END}").strip()
                
                if cmd.lower() == 'exit':
                    self.send_command("EXIT")
                    break
                elif cmd.lower() == 'help':
                    self.send_command("HELP")
                elif cmd:
                    self.send_command(cmd)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Disconnecting...{Colors.END}")
                self.send_command("EXIT")
                break
            except Exception as e:
                print(f"{Colors.RED}[!] Error: {str(e)}{Colors.END}")
                
        if self.client_socket:
            self.client_socket.close()

def install_dependencies():
    """Install dependencies untuk Termux"""
    print(f"{Colors.CYAN}[*] Installing Termux dependencies...{Colors.END}")
    
    commands = [
        "pkg update && pkg upgrade -y",
        "pkg install python -y",
        "pkg install termux-api -y",
        "pip install requests",
        "termux-setup-storage"
    ]
    
    for cmd in commands:
        print(f"{Colors.YELLOW}[>] Executing: {cmd}{Colors.END}")
        os.system(cmd)
        
    print(f"{Colors.GREEN}[+] Installation complete!{Colors.END}")
    print(f"{Colors.GREEN}[+] Please grant all permissions to Termux API{Colors.END}")

def quick_connect_mode():
    """Mode quick connect untuk testing"""
    print(f"{Colors.CYAN}[*] Quick Connect Mode{Colors.END}")
    print(f"{Colors.YELLOW}[!] This will connect to localhost for testing{Colors.END}")
    
    client = TitanClient("127.0.0.1", 6969)
    if client.connect():
        client.start_interactive()

def main():
    """Main function"""
    # Check jika di Termux
    if not os.path.exists('/data/data/com.termux/files/usr/bin/'):
        print(f"{Colors.RED}[!] This script is designed for Termux on Android{Colors.END}")
        print(f"{Colors.RED}[!] Please run it in Termux app{Colors.END}")
        sys.exit(1)
        
    display_banner()
    
    print(f"{Colors.CYAN}[1] Start Titan Server (Be Controlled){Colors.END}")
    print(f"{Colors.CYAN}[2] Connect as Client (Control Remote){Colors.END}")
    print(f"{Colors.CYAN}[3] Install Dependencies{Colors.END}")
    print(f"{Colors.CYAN}[4] Quick Connect Test{Colors.END}")
    print(f"{Colors.CYAN}[5] Exit{Colors.END}")
    
    choice = input(f"{Colors.GREEN}Select option (1-5): {Colors.END}").strip()
    
    if choice == "1":
        port = input(f"{Colors.GREEN}Enter port (default 6969): {Colors.END}").strip()
        port = int(port) if port.isdigit() else 6969
        
        server = TitanRemoteSystem(port=port)
        server.start_server()
        
    elif choice == "2":
        server_ip = input(f"{Colors.GREEN}Enter server IP: {Colors.END}").strip()
        port = input(f"{Colors.GREEN}Enter port (default 6969): {Colors.END}").strip()
        port = int(port) if port.isdigit() else 6969
        
        client = TitanClient(server_ip, port)
        if client.connect():
            client.start_interactive()
            
    elif choice == "3":
        install_dependencies()
        
    elif choice == "4":
        quick_connect_mode()
        
    elif choice == "5":
        print(f"{Colors.YELLOW}[!] Exiting... Shinzo wo Sasageyo!{Colors.END}")
        sys.exit(0)
        
    else:
        print(f"{Colors.RED}[!] Invalid choice{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Program terminated by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] Fatal error: {str(e)}{Colors.END}")