#!/usr/bin/env python3
import argparse
import re
import sys
import logging
from airportcli import get_available_networks, get_current_connection

# Set up logging
logger = logging.getLogger('airportcli')
logger.setLevel(logging.INFO)  # Default level
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global verbose flag
verbose = False

def display_networks(xml_format=False):
    """Display available networks in a tabular format similar to airport -s"""
    logger.debug("Fetching available networks...")
    networks = get_available_networks()
    if not networks:
        logger.warning("No networks found.")
        print("No networks found.")
        return
    
    logger.debug(f"Found {len(networks)} networks")
    
    if xml_format:
        # Generate XML output
        logger.debug("Generating XML output")
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<airport>')
        print('  <networks>')
        for network in networks:
            try:
                ssid = network.get("_name", "")
                bssid = network.get("spairport_bssid", "")
                signal_noise = network.get("spairport_signal_noise", "")
                rssi_match = re.search(r'(-\d+)\s*dBm', signal_noise)
                rssi = rssi_match.group(1) if rssi_match else ""
                channel_info = network.get("spairport_network_channel", "")
                channel_match = re.search(r'(\d+(?:,\s*-?\d+)?)', channel_info)
                channel = channel_match.group(1) if channel_match else ""
                ht = "Y" if network.get("spairport_ht_capable", False) else "N"
                cc = network.get("spairport_country_code", "--")
                security_mode = network.get("spairport_security_mode", "")
                security = parse_security_mode(security_mode)
                
                logger.debug(f"Processing network: {ssid}")
                
                print(f'    <network>')
                print(f'      <ssid>{ssid}</ssid>')
                print(f'      <bssid>{bssid}</bssid>')
                print(f'      <rssi>{rssi}</rssi>')
                print(f'      <channel>{channel}</channel>')
                print(f'      <ht>{ht}</ht>')
                print(f'      <cc>{cc}</cc>')
                print(f'      <security>{security}</security>')
                print(f'    </network>')
            except Exception as e:
                logger.error(f"Error processing network: {e}")
                continue
        print('  </networks>')
        print('</airport>')
    else:
        # Print header with indentation
        logger.debug("Generating tabular output")
        print("    SSID                      BSSID             RSSI CHANNEL HT CC SECURITY (auth/unicast/group)")
        
        # Print each network
        for network in networks:
            try:
                ssid = network.get("_name", "")
                bssid = network.get("spairport_bssid", "")
                
                # Extract RSSI from signal noise string (remove dBm)
                signal_noise = network.get("spairport_signal_noise", "")
                rssi_match = re.search(r'(-\d+)\s*dBm', signal_noise)
                rssi = rssi_match.group(1) if rssi_match else ""
                
                # Extract channel information
                channel_info = network.get("spairport_network_channel", "")
                # Extract just the channel number
                channel_match = re.search(r'(\d+(?:,\s*-?\d+)?)', channel_info)
                channel = channel_match.group(1) if channel_match else ""
                
                # Other information
                ht = "Y" if network.get("spairport_ht_capable", False) else "N"
                cc = network.get("spairport_country_code", "--")
                
                # Parse security mode
                security_mode = network.get("spairport_security_mode", "")
                security = parse_security_mode(security_mode)
                
                logger.debug(f"Network: SSID={ssid}, BSSID={bssid}, RSSI={rssi}, Channel={channel}, Security={security}")
                
                # Format the output with proper spacing and indentation
                print(f"    {ssid:<25} {bssid:<18} {rssi:<4} {channel:<7} {ht:<2} {cc:<2} {security}")
            except Exception as e:
                logger.error(f"Error formatting network: {e}")
                continue

def display_current_connection(xml_format=False):
    """Display information about the current wireless connection"""
    logger.debug("Fetching current connection information...")
    connection = get_current_connection()
    if not connection:
        logger.warning("Not connected to any wireless network.")
        print("Not connected to any wireless network.")
        return
    
    logger.debug("Processing connection details")
    
    # Extract signal and noise levels from signal_noise string
    signal_noise = connection.get("spairport_signal_noise", "")
    signal_match = re.search(r'(-\d+)\s*dBm', signal_noise)
    noise_match = re.search(r'/ (-\d+)\s*dBm', signal_noise)
    
    signal_level = signal_match.group(1) if signal_match else "0"
    noise_level = noise_match.group(1) if noise_match else "0"
    
    logger.debug(f"Signal level: {signal_level} dBm, Noise level: {noise_level} dBm")
    
    # Get other connection details
    bssid = connection.get("spairport_bssid", "")
    ssid = connection.get("_name", "")
    security_mode = connection.get("spairport_security_mode", "")
    security = parse_security_mode(security_mode)
    tx_rate = connection.get("spairport_network_rate", "0")
    
    # Get channel and band information
    channel_info = connection.get("spairport_network_channel", "")
    channel_match = re.search(r'(\d+)', channel_info)
    channel = channel_match.group(1) if channel_match else ""
    
    # Get phy mode
    phy_mode = connection.get("spairport_network_phymode", "")
    
    logger.debug(f"SSID: {ssid}, BSSID: {bssid}, Channel: {channel}, Security: {security}, TX Rate: {tx_rate}")
    
    # Define the fields and values with the correct key names
    fields = {
        "agrCtlRSSI": signal_level,
        "agrCtlNoise": noise_level,
        "state": "running",
        "op mode": "station",
        "lastTxRate": str(tx_rate),
        "maxRate": str(tx_rate),
        "802.11 auth": phy_mode,
        "link auth": security,
        "BSSID": bssid,
        "SSID": ssid,
        "channel": channel
    }
    
    if xml_format:
        # Generate XML output
        logger.debug("Generating XML output for current connection")
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<airport>')
        print('  <current_network>')
        for field, value in fields.items():
            # Convert field names to valid XML tags (replace spaces with underscores)
            field_tag = field.replace(" ", "_").replace(".", "_")
            print(f'    <{field_tag}>{value}</{field_tag}>')
        print('  </current_network>')
        print('</airport>')
    else:
        # Find the longest field name to determine proper alignment
        max_field_length = max(len(field) for field in fields.keys())
        
        logger.debug("Displaying formatted connection information")
        # Print each field with proper alignment
        for field, value in fields.items():
            # Right-align the key, left-align the value with a space after the colon
            print(f"{field:>{max_field_length}}: {value}")

def parse_security_mode(security_mode):
    """Parse security mode into auth/unicast/group format"""
    if not security_mode:
        return "none"
    
    # Handle the raw security mode strings from the output
    if security_mode == "spairport_security_mode_wpa2_personal":
        return "WPA2(PSK/AES/AES)"
    elif security_mode == "spairport_security_mode_wpa2_enterprise":
        return "WPA2(802.1X/AES/AES)"
    elif security_mode == "spairport_security_mode_wpa3_personal":
        return "WPA3(SAE/AES/AES)"
    elif security_mode == "spairport_security_mode_wpa_personal":
        return "WPA(PSK/TKIP/TKIP)"
    elif security_mode == "spairport_security_mode_wpa_enterprise":
        return "WPA(802.1X/TKIP/TKIP)"
    elif security_mode == "spairport_security_mode_none" or "Open" in security_mode:
        return "none"
    else:
        # Return the raw mode if no specific pattern matches
        return security_mode

def display_ssid():
    """Display only the SSID of the current connection"""
    logger.debug("Fetching SSID of current connection...")
    connection = get_current_connection()
    if not connection:
        logger.warning("Not connected to any wireless network.")
        print("Not connected to any wireless network.")
        return
    
    ssid = connection.get("_name", "")
    logger.debug(f"Current SSID: {ssid}")
    print(ssid)

def display_quality():
    """Display the wireless quality as a percentage"""
    logger.debug("Calculating wireless quality percentage...")
    connection = get_current_connection()
    if not connection:
        logger.warning("Not connected to any wireless network.")
        print("Not connected to any wireless network.")
        return
    
    # Extract signal and noise levels from signal_noise string
    signal_noise = connection.get("spairport_signal_noise", "")
    signal_match = re.search(r'(-\d+)\s*dBm', signal_noise)
    
    if signal_match:
        signal_level = int(signal_match.group(1))
        # Convert dBm to percentage (typical range: -30 dBm to -90 dBm)
        # -30 dBm or better = 100%, -90 dBm or worse = 0%
        quality = max(0, min(100, (signal_level + 90) * (100 / 60)))
        logger.debug(f"Signal level: {signal_level} dBm, Calculated quality: {int(quality)}%")
        print(f"{int(quality)}%")
    else:
        logger.error("Unable to determine signal quality - no signal level found.")
        print("Unable to determine signal quality.")

def cli():
    """Main CLI entry point with the new command structure"""
    global verbose
    # Define version
    version = "1.0.0"
    
    # If no arguments provided or help requested, show help
    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        return
    
    # Check for verbose flag in any position
    if '-v' in sys.argv or '--verbose' in sys.argv:
        verbose = True
        # Remove the verbose flag from argv to not interfere with command processing
        if '-v' in sys.argv:
            sys.argv.remove('-v')
        if '--verbose' in sys.argv:
            sys.argv.remove('--verbose')
        # Set logger to DEBUG level
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    # If after removing verbose flag, no arguments left, show help
    if len(sys.argv) == 1:
        print_help()
        return
    
    # Handle version request
    if sys.argv[1] == '--version':
        logger.debug("Displaying version information")
        print(f"airportcli version {version}")
        print("A replacement for the deprecated 'airport' utility removed in macOS Sonoma 14.4")
        return
    
    # Process commands
    command = sys.argv[1].lower()
    logger.debug(f"Processing command: {command}")
    
    # Handle command aliases
    if command in ['info', '-i', '-getinfo']:
        logger.debug("Executing info command")
        # Check for long option
        long_format = False
        if len(sys.argv) > 2 and sys.argv[2] in ['-l', '--long']:
            long_format = True
            logger.debug("Long format enabled")
            
        if long_format:
            # Show detailed information
            display_current_connection(xml_format=False)
        else:
            # Show only SSID and quality percentage
            connection = get_current_connection()
            if not connection:
                print("Not connected to any wireless network.")
                return
                
            # Get SSID
            ssid = connection.get("_name", "")
            
            # Get quality percentage
            signal_noise = connection.get("spairport_signal_noise", "")
            signal_match = re.search(r'(-\d+)\s*dBm', signal_noise)
            
            if signal_match:
                signal_level = int(signal_match.group(1))
                # Convert dBm to percentage (typical range: -30 dBm to -90 dBm)
                # -30 dBm or better = 100%, -90 dBm or worse = 0%
                quality = max(0, min(100, (signal_level + 90) * (100 / 60)))
                quality_str = f"{int(quality)}%"
            else:
                quality_str = "Unknown"
                
            logger.debug(f"Displaying basic info - SSID: {ssid}, Quality: {quality_str}")
            print(f"SSID: {ssid}")
            print(f"Quality: {quality_str}")
    
    elif command in ['scan', '-s']:
        logger.debug("Executing scan command")
        # Optional query parameter not implemented yet
        display_networks(xml_format=False)
    
    elif command == 'ssid':
        logger.debug("Executing ssid command")
        display_ssid()
    
    elif command == 'quality':
        logger.debug("Executing quality command")
        display_quality()
    
    elif command in ['off', 'on', 'join']:
        logger.warning(f"Command 'airportcli {command}' is deprecated and not implemented.")
        print(f"Command 'airportcli {command}' is deprecated and not implemented.")
    
    else:
        logger.warning(f"Unknown command: {command}")
        print(f"Unknown command: {command}")
        print_help()

def print_help():
    """Print the help information in the exact format requested"""
    help_text = """Usage:
  airportcli info [-l|--long]
  airportcli -I | -getinfo [-l|--long]
  airportcli join <SSID>
  airportcli quality
  airportcli off
  airportcli on
  airportcli scan [<query>]
  airportcli -s [<query>]
  airportcli ssid
  airportcli -h | --help | help
  airportcli --version
  
  Add -v or --verbose to any command for detailed logging output.

Subcommands:
  info, -I, -getinfo  Print the current network SSID and quality percentage. Use the -l or --long
                      options to print detailed information about the connection.
  join                Join the specified network. (deprecated)
  quality             Show the wireless quality as a percentage.
  off                 Turn wireless off. (deprecated)
  on                  Turn wireless on. (deprecated)
  scan, -s            Perform a scan for wireless networks.
  ssid                Print the current network's SSID.
  help                Display this help information.

Options:
  -h --help           Display this help information.
  --version           Display version information.
  -v --verbose        Enable verbose logging output.

Note: This tool is designed to replace the functionality of the deprecated
      'airport' utility that was removed in macOS Sonoma 14.4."""
    logger.debug("Displaying help information")
    print(help_text)

if __name__ == "__main__":
    cli()
