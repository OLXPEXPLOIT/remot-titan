#!/data/data/com.termux/files/usr/bin/bash
# Titan Remote Control Installer

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════╗"
echo "║         TITAN REMOTE CONTROL INSTALLER           ║"
echo "║        Attack on Titan Themed Remote Control     ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${RED}[!] This script must be run in Termux${NC}"
    exit 1
fi

# Update packages
echo -e "${YELLOW}[*] Updating packages...${NC}"
pkg update -y && pkg upgrade -y

# Install dependencies
echo -e "${YELLOW}[*] Installing dependencies...${NC}"
pkg install -y python git curl wget nmap termux-api
pkg install -y python-pip python-numpy python-pillow
pip install requests colorama

# Install Termux API
echo -e "${YELLOW}[*] Setting up Termux API...${NC}"
pkg install -y termux-api
termux-setup-storage

# Download main script
echo -e "${YELLOW}[*] Downloading Titan Remote Control...${NC}"
curl -L -o /data/data/com.termux/files/home/titan_remote.py https://raw.githubusercontent.com/example/titan-remote/main/titan_remote.py

# Make executable
chmod +x /data/data/com.termux/files/home/titan_remote.py

# Create shortcut command
echo 'alias titan="python /data/data/com.termux/files/home/titan_remote.py"' >> /data/data/com.termux/files/home/.bashrc
echo 'alias titan-server="python /data/data/com.termux/files/home/titan_remote.py 1"' >> /data/data/com.termux/files/home/.bashrc
echo 'alias titan-client="python /data/data/com.termux/files/home/titan_remote.py 2"' >> /data/data/com.termux/files/home/.bashrc

# Create config directory
mkdir -p /data/data/com.termux/files/home/.titan

# Create startup service
cat > /data/data/com.termux/files/home/.titan/start.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Titan Auto-start Script

echo "[*] Starting Titan Remote Control..."
python /data/data/com.termux/files/home/titan_remote.py
EOF

chmod +x /data/data/com.termux/files/home/.titan/start.sh

# Create uninstall script
cat > /data/data/com.termux/files/home/.titan/uninstall.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Titan Uninstaller

echo "[!] Uninstalling Titan Remote Control..."
rm -f /data/data/com.termux/files/home/titan_remote.py
rm -rf /data/data/com.termux/files/home/.titan
sed -i '/alias titan/d' /data/data/com.termux/files/home/.bashrc
echo "[+] Uninstallation complete!"
EOF

chmod +x /data/data/com.termux/files/home/.titan/uninstall.sh

# Create client script
cat > /data/data/com.termux/files/home/titan_client.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Titan Client Quick Script

if [ -z "$1" ]; then
    echo "Usage: ./titan_client.sh [SERVER_IP]"
    echo "Example: ./titan_client.sh 192.168.1.100"
    exit 1
fi

python /data/data/com.termux/files/home/titan_remote.py 2
EOF

chmod +x /data/data/com.termux/files/home/titan_client.sh

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════╗"
echo "║          INSTALLATION COMPLETE!                  ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${CYAN}[+] Titan Remote Control installed successfully!${NC}"
echo -e "${CYAN}[+] Available commands:${NC}"
echo -e "${YELLOW}  titan        - Start Titan Control${NC}"
echo -e "${YELLOW}  titan-server - Start as Server${NC}"
echo -e "${YELLOW}  titan-client - Start as Client${NC}"
echo -e "${CYAN}[+] Grant permissions to Termux API app${NC}"
echo -e "${CYAN}[+] Run 'titan' to start the system${NC}"
echo -e "${RED}[!] Shinzo wo Sasageyo!${NC}"

# Reload bashrc
source /data/data/com.termux/files/home/.bashrc