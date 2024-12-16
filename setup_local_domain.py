import os
import subprocess
 

def print_welcome_message(): 
    print("\n" + "="*50)
    print("     Welcome to the Local Domain Setup Tool!")
    print("          Created with ❤️ by Mostafa")
    print("="*50 + "\n")

def create_local_domain(domain_name, document_root): 
    print_welcome_message()
 
    hosts_file = "/etc/hosts"
    apache_sites_available = f"/etc/apache2/sites-available/{domain_name}.conf"
 
    try:
        print(f"Adding {domain_name} to {hosts_file}...")
        with open(hosts_file, "r") as file:
            if domain_name in file.read():
                print(f"{domain_name} already exists in {hosts_file}.")
            else:
                with open(hosts_file, "a") as hosts:
                    hosts.write(f"127.0.0.1 {domain_name}\n")
                print(f"{domain_name} added to {hosts_file}.")
    except PermissionError:
        print(f"Permission denied. Please run the script with sudo.")
        return
 
    apache_config = f"""<VirtualHost *:80>
    ServerName {domain_name}
    DocumentRoot {document_root}

    <Directory {document_root}>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog /var/log/apache2/{domain_name}_error.log
    CustomLog /var/log/apache2/{domain_name}_access.log combined
</VirtualHost>
"""
    
    try:
        print(f"Creating Apache configuration file at {apache_sites_available}...")
        with open(apache_sites_available, "w") as conf_file:
            conf_file.write(apache_config)
        print("Configuration file created.")
    except PermissionError:
        print("Permission denied. Please run the script with sudo.")
        return
 
    try:
        print("Enabling site and restarting Apache...")
        subprocess.run(["a2ensite", domain_name], check=True)
        subprocess.run(["systemctl", "reload", "apache2"], check=True)
        print(f"Site {domain_name} is enabled and Apache has been restarted.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return

if __name__ == "__main__":
    print_welcome_message()
    domain = input("Enter the local domain name (e.g., mysite.local): ")
    root = input("Enter the document root path (e.g., /var/www/html/mysite): ")

    if not os.path.isdir(root):
        print(f"The document root {root} does not exist. Please create it first.")
    else:
        create_local_domain(domain, root)
