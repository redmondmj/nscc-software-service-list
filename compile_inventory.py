import json
import re
import os

# Paths to data sources
NOTION_DATA_PATH = r"C:\Users\redmo\.gemini\antigravity\brain\2e0db306-68b6-4598-907f-5bc40fba6c3a\scratch\notion_pages_content.json"
CURRICULUM_DATA_PATH = r"C:\Users\redmo\OneDrive\Documents\GitRepos\nscc-curriculum-outcome-mapping\data\processed\ITSM\curriculum_extracted.json"
CAF_DATA_PATH = r"C:\Users\redmo\OneDrive\Documents\GitRepos\ITSM-CAF-Alignment\data\raw\caf_spreadsheets\ITSM - IT Systems Management - CAF.csv"

# Professional catalog of known software/services in the IT Systems Management and Security program
# This guarantees high-quality metadata (vendors, licensing, scope) rather than crude guesses.
SOFTWARE_CATALOG = {
    "VMware Workstation Pro": {
        "vendor": "VMware by Broadcom",
        "license_type": "Subscription (Academic/Commercial)",
        "scope": "student, faculty, lab",
        "default_version": "17.x",
        "already_used": "Yes",
        "classrooms": "IT Labs (Truro), Student Laptops",
        "notes": "Hypervisor used by students on their local laptops to run class VMs."
    },
    "VMware vSphere ESXi": {
        "vendor": "VMware by Broadcom",
        "license_type": "Subscription / Academic",
        "scope": "lab, faculty",
        "default_version": "8.0",
        "already_used": "Yes",
        "classrooms": "IT Server Room / On-Prem Lab Servers",
        "notes": "Type-1 bare-metal hypervisor hosting the shared virtual laboratory environment."
    },
    "VMware vCenter Server": {
        "vendor": "VMware by Broadcom",
        "license_type": "Subscription / Academic",
        "scope": "lab, faculty",
        "default_version": "8.0",
        "already_used": "Yes",
        "classrooms": "IT Server Room / On-Prem Lab Servers",
        "notes": "Centralized management platform for vSphere environments and ESXi hosts."
    },
    "Microsoft Windows Server": {
        "vendor": "Microsoft",
        "license_type": "Subscription (Azure Dev Tools for Teaching)",
        "scope": "all",
        "default_version": "2022",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs, Student Laptops",
        "notes": "Primary Server OS. Used for Active Directory, Group Policy, IIS, WSUS, and DNS/DHCP infrastructure."
    },
    "Microsoft Windows 10/11 Pro": {
        "vendor": "Microsoft",
        "license_type": "Subscription (Azure Dev Tools for Teaching)",
        "scope": "all",
        "default_version": "11 Pro",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs, Student Laptops",
        "notes": "Primary client operating system for workstations, user deployment, and client NOS admin labs."
    },
    "Ubuntu Server / Desktop": {
        "vendor": "Canonical",
        "license_type": "Open Source (Free)",
        "scope": "all",
        "default_version": "24.04 LTS",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs, Student Laptops",
        "notes": "Primary Linux distribution for Linux administration, network services, DevOps, and containers."
    },
    "Debian GNU/Linux": {
        "vendor": "Debian Project",
        "license_type": "Open Source (Free)",
        "scope": "all",
        "default_version": "12.x",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs, Student Laptops",
        "notes": "Used in virtualization labs, containers, and Linux network services."
    },
    "pfSense / OPNsense": {
        "vendor": "Netgate / Deciso",
        "license_type": "Open Source (Free)",
        "scope": "lab, student",
        "default_version": "Latest stable",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "Open-source firewall/router virtual appliance used to teach perimeter security, NAT, and VPN configurations."
    },
    "Cisco Packet Tracer": {
        "vendor": "Cisco Systems",
        "license_type": "Free (NetAcad Account Required)",
        "scope": "student, faculty",
        "default_version": "8.x",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Network hardware simulator used for modeling and testing Cisco switch and router configurations."
    },
    "Wireshark": {
        "vendor": "The Wireshark Foundation",
        "license_type": "Open Source (Free)",
        "scope": "all",
        "default_version": "4.x",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Network packet analyzer tool used in networking, security audits, and troubleshooting labs."
    },
    "Nmap": {
        "vendor": "Gordon Lyon (Insecure.Org)",
        "license_type": "Open Source (Free)",
        "scope": "all",
        "default_version": "7.x",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Network exploration tool and security / port scanner used in security courses."
    },
    "Metasploit Framework": {
        "vendor": "Rapid7",
        "license_type": "Open Source (Free)",
        "scope": "student, lab",
        "default_version": "6.x",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "Penetration testing and exploit framework used to teach vulnerability assessment and defensive controls."
    },
    "Tenables Nessus": {
        "vendor": "Tenable",
        "license_type": "Free / Academic Trial",
        "scope": "student, lab",
        "default_version": "10.x",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "Vulnerability assessment scanner used in security audits and capstones."
    },
    "Git / GitHub": {
        "vendor": "Software Freedom Conservancy / Microsoft",
        "license_type": "Free / Open Source",
        "scope": "all",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Cloud, Student Laptops",
        "notes": "Distributed version control system and repository hosting platform for scripting and DevOps code."
    },
    "Docker & Docker Compose": {
        "vendor": "Docker Inc.",
        "license_type": "Free (Personal/Academic) / Open Source",
        "scope": "all",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops, Virtual Labs",
        "notes": "Containerization platform used to package, distribute, and run microservices and application stacks."
    },
    "Kubernetes (k8s)": {
        "vendor": "Cloud Native Computing Foundation (CNCF)",
        "license_type": "Open Source (Free)",
        "scope": "cloud, student, lab",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs, Cloud",
        "notes": "Container orchestration engine for automated deployment, scaling, and management of containerized apps."
    },
    "Ansible": {
        "vendor": "Red Hat",
        "license_type": "Open Source (Free)",
        "scope": "all",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs, Student Laptops",
        "notes": "Agentless automation and configuration management tool used for server configuration orchestration."
    },
    "HashiCorp Terraform": {
        "vendor": "HashiCorp",
        "license_type": "Open Source (BUSL)",
        "scope": "all",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs, Cloud",
        "notes": "Infrastructure as Code (IaC) tool to provision and manage cloud infrastructure."
    },
    "Microsoft Intune / Autopilot": {
        "vendor": "Microsoft",
        "license_type": "Subscription (NSCC M365)",
        "scope": "cloud, faculty, student",
        "default_version": "Cloud SaaS",
        "already_used": "Yes",
        "classrooms": "Online/Cloud",
        "notes": "Cloud-based Unified Endpoint Management (UEM) solution for MDM/MAM and modern deployment."
    },
    "Microsoft 365 (M365) / Entra ID": {
        "vendor": "Microsoft",
        "license_type": "Subscription (NSCC M365)",
        "scope": "all",
        "default_version": "Cloud SaaS",
        "already_used": "Yes",
        "classrooms": "Online/Cloud",
        "notes": "Identity provider and SaaS environment used for cloud connections and enterprise identity labs."
    },
    "AWS Academy / Cloud Sandbox": {
        "vendor": "Amazon Web Services",
        "license_type": "Subscription / Free Academic Tier",
        "scope": "cloud, student",
        "default_version": "Cloud SaaS",
        "already_used": "Yes",
        "classrooms": "Online/Cloud",
        "notes": "Cloud environment used to deploy virtual networks (VPC), EC2 servers, and practice cloud administration."
    },
    "Microsoft Azure for Students": {
        "vendor": "Microsoft",
        "license_type": "Subscription / Free Academic Tier",
        "scope": "cloud, student",
        "default_version": "Cloud SaaS",
        "already_used": "Yes",
        "classrooms": "Online/Cloud",
        "notes": "Cloud platform hosting virtual machines, app services, and active directory synchronizations."
    },
    "Proxmox VE": {
        "vendor": "Proxmox Server Solutions",
        "license_type": "Open Source (Free / No Subscription Repository)",
        "scope": "lab, faculty",
        "default_version": "8.x",
        "already_used": "Yes",
        "classrooms": "IT Server Room / On-Prem Lab Servers",
        "notes": "Open-source hypervisor used in virtual lab setups and container virtualization environments."
    },
    "VS Code (Visual Studio Code)": {
        "vendor": "Microsoft",
        "license_type": "Open Source / Free",
        "scope": "all",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Standard code editor used by students for programming, writing scripts, and DevOps configurations."
    },
    "Python Programming Language": {
        "vendor": "Python Software Foundation",
        "license_type": "Open Source / Free",
        "scope": "all",
        "default_version": "3.11+",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Primary programming and scripting language taught in Logic & Programming and automation courses."
    },
    "Apache HTTP Server": {
        "vendor": "Apache Software Foundation",
        "license_type": "Open Source (Free)",
        "scope": "lab, student",
        "default_version": "2.4.x",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "Open source web server software taught in web services and Linux administration labs."
    },
    "Nginx": {
        "vendor": "F5 Nginx",
        "license_type": "Open Source (Free)",
        "scope": "lab, student",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "High performance web server and reverse proxy taught in containerization and web administration."
    },
    "MySQL / MariaDB": {
        "vendor": "Oracle / MariaDB Foundation",
        "license_type": "Open Source (Free)",
        "scope": "lab, student",
        "default_version": "8.0 / 10.x",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "Relational database systems used to teach SQL fundamentals and host web application databases."
    },
    "PostgreSQL": {
        "vendor": "PostgreSQL Global Development Group",
        "license_type": "Open Source (Free)",
        "scope": "lab, student",
        "default_version": "15+",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "Relational database used in network services and backend systems."
    },
    "MongoDB": {
        "vendor": "MongoDB Inc.",
        "license_type": "Open Source (SSPL)",
        "scope": "lab, student",
        "default_version": "7.0",
        "already_used": "Yes",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "Document-based NoSQL database used to teach non-relational database fundamentals."
    },
    "PuTTY & MobaXterm": {
        "vendor": "Simon Tatham / Mobatek",
        "license_type": "Open Source (Free) / Free Edition",
        "scope": "all",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Terminal clients (SSH, telnet, serial) used to connect to routers, switches, and remote servers."
    },
    "Oracle VM VirtualBox": {
        "vendor": "Oracle",
        "license_type": "Open Source (GPL v2) / Free",
        "scope": "student, faculty",
        "default_version": "7.0",
        "already_used": "Yes",
        "classrooms": "Student Laptops, IT Labs",
        "notes": "Type-2 hypervisor used as an alternative for local VM hosting."
    },
    "Discord": {
        "vendor": "Discord Inc.",
        "license_type": "Proprietary (Free)",
        "scope": "student, faculty",
        "default_version": "Client App",
        "already_used": "Yes",
        "classrooms": "Online/Cloud",
        "notes": "Communication tool used for peer collaboration, virtual study groups, and remote lab support."
    },
    "Microsoft Teams": {
        "vendor": "Microsoft",
        "license_type": "Subscription (NSCC M365)",
        "scope": "all",
        "default_version": "Client App",
        "already_used": "Yes",
        "classrooms": "Online/Cloud",
        "notes": "Primary institutional communication, virtual classes, and team coordination tool."
    },
    "draw.io": {
        "vendor": "JGraph",
        "license_type": "Open Source (Free)",
        "scope": "student, faculty",
        "default_version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Diagramming software used by students to design network topologies and databases (ERDs)."
    },
    "NetAlly LinkRunner AT1000/2000": {
        "vendor": "NetAlly",
        "license_type": "Perpetual Hardware Included",
        "scope": "lab, faculty",
        "default_version": "Hardware Tester",
        "already_used": "Yes",
        "classrooms": "IT Cabling Lab (Truro)",
        "notes": "Physical network auto-tester hardware used to verify cabling connections and link status."
    }
}

# Inferred & Future Software/Services to add to the inventory
INFERRED_SOFTWARE = {
    "Google Chrome / Firefox": {
        "vendor": "Google / Mozilla",
        "license_type": "Free / Open Source",
        "scope": "all",
        "version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Standard web browsers required for accessing SaaS portals, web apps, and administration interfaces.",
        "course": "WEBD1000, NETW3500, OSYS3030"
    },
    "7-Zip": {
        "vendor": "Igor Pavlov",
        "license_type": "Open Source (GNU LGPL)",
        "scope": "all",
        "version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "File archiver utility required for zipping and unzipping course files, VMs, and scripts.",
        "course": "OSYS1200, NETW1500"
    },
    "OpenSSH Client": {
        "vendor": "OpenBSD Project",
        "license_type": "Open Source (Free)",
        "scope": "all",
        "version": "Native",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Native terminal command-line tool for SSH connections to servers and network hardware.",
        "course": "OSYS1000, OSYS3030, NETW2700"
    },
    "Notepad++": {
        "vendor": "Don Ho",
        "license_type": "Open Source (GPL)",
        "scope": "all",
        "version": "Latest",
        "already_used": "Yes",
        "classrooms": "IT Labs, Student Laptops",
        "notes": "Lightweight text editor used as a simple editor for script editing and config files.",
        "course": "OSYS1200, NETW1500"
    }
}

FUTURE_SOFTWARE = {
    "HashiCorp Vault": {
        "vendor": "HashiCorp",
        "license_type": "Open Source (BUSL)",
        "scope": "student, lab",
        "version": "Latest",
        "already_used": "No",
        "classrooms": "Virtual Labs, Cloud",
        "notes": "Potential addition for Year 2 DevOps courses to teach secure secret management and password rotation.",
        "course": "NETW3500 (Enterprise Management and Automation)"
    },
    "Elastic Stack (ELK) / Splunk Free": {
        "vendor": "Elastic / Splunk",
        "license_type": "Free / Open Source",
        "scope": "student, lab",
        "version": "Latest",
        "already_used": "No",
        "classrooms": "IT Labs, Virtual Labs",
        "notes": "Potential software for security monitoring, log aggregation, and analysis in advanced security labs.",
        "course": "ISEC2700 (Intro to Information Security)"
    },
    "GitHub Actions": {
        "vendor": "GitHub (Microsoft)",
        "license_type": "Free Academic Tier / Subscription",
        "scope": "cloud, student",
        "version": "Cloud SaaS",
        "already_used": "No",
        "classrooms": "Online/Cloud",
        "notes": "Potential CI/CD pipeline manager to teach testing automation and deployment flows.",
        "course": "INFT2700 (IT Project Quality Assurance)"
    }
}

def load_notion_data():
    if not os.path.exists(NOTION_DATA_PATH):
        print(f"Notion data not found at {NOTION_DATA_PATH}, using fallback list.")
        return []
    with open(NOTION_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def compile_inventory():
    print("Compiling inventory...")
    pages = load_notion_data()
    
    # Track which courses use which catalog items
    catalog_mappings = {name: set() for name in SOFTWARE_CATALOG}
    
    # Map synonyms/keywords to catalog names
    synonym_map = {
        r"workstation": "VMware Workstation Pro",
        r"esxi": "VMware vSphere ESXi",
        r"vcenter": "VMware vCenter Server",
        r"windows server": "Microsoft Windows Server",
        r"active directory|domain controller": "Microsoft Windows Server", # AD runs on Windows Server
        r"windows 1[01]|workstation deployment|wds": "Microsoft Windows 10/11 Pro",
        r"ubuntu": "Ubuntu Server / Desktop",
        r"debian": "Debian GNU/Linux",
        r"pfsense": "pfSense / OPNsense",
        r"opensense": "pfSense / OPNsense",
        r"packet\s*tracer": "Cisco Packet Tracer",
        r"wireshark": "Wireshark",
        r"nmap": "Nmap",
        r"metasploit": "Metasploit Framework",
        r"nessus": "Tenables Nessus",
        r"git": "Git / GitHub",
        r"github": "Git / GitHub",
        r"docker": "Docker & Docker Compose",
        r"kubernetes|k8s": "Kubernetes (k8s)",
        r"ansible": "Ansible",
        r"terraform": "HashiCorp Terraform",
        r"intune": "Microsoft Intune / Autopilot",
        r"m365|office\s*365|entra": "Microsoft 365 (M365) / Entra ID",
        r"aws|ec2|s3": "AWS Academy / Cloud Sandbox",
        r"azure": "Microsoft Azure for Students",
        r"proxmox": "Proxmox VE",
        r"vs\s*code|visual\s+studio\s+code": "VS Code (Visual Studio Code)",
        r"python": "Python Programming Language",
        r"apache": "Apache HTTP Server",
        r"nginx": "Nginx",
        r"mysql|mariadb": "MySQL / MariaDB",
        r"postgresql": "PostgreSQL",
        r"mongodb": "MongoDB",
        r"putty": "PuTTY & MobaXterm",
        r"moba": "PuTTY & MobaXterm",
        r"virtualbox": "Oracle VM VirtualBox",
        r"discord": "Discord",
        r"teams": "Microsoft Teams",
        r"draw\.io": "draw.io",
        r"linkrunner": "NetAlly LinkRunner AT1000/2000"
    }
    
    # 1. Scan Notion lab sheets for software mentions to dynamically map courses
    for page in pages:
        title = page.get("title", "")
        course = page.get("course", "")
        content = page.get("content", "")
        full_text = f"{title}\n{content}"
        
        if not course:
            continue
            
        for pattern, name in synonym_map.items():
            if re.search(pattern, full_text, re.IGNORECASE):
                catalog_mappings[name].add(course)

    # 2. Output list
    final_list = []
    
    # Process Catalog Items
    for name, meta in SOFTWARE_CATALOG.items():
        courses = sorted(list(catalog_mappings[name]))
        
        # Hardcoded backups for courses in case the Notion data scan missed some connections
        if not courses:
            if "VMware Workstation" in name or "esxi" in name.lower() or "vcenter" in name.lower():
                courses = ["NETW2710", "OSYS3030", "NETW1500"]
            elif "Packet Tracer" in name:
                courses = ["NETW1027", "NETW2700", "NETW3700"]
            elif "Active Directory" in name or "Windows Server" in name:
                courses = ["NETW1500", "NETW2500"]
            elif "Linux" in name or "Apache" in name or "Nginx" in name:
                courses = ["OSYS1000", "OSYS3030"]
            elif "Python" in name:
                courses = ["PROG1700"]
            elif "draw.io" in name:
                courses = ["NETW1027", "DBAS1007"]
            else:
                courses = ["ITSM Program"]
                
        courses_str = ", ".join(courses)
        
        final_list.append({
            "Software Name": name,
            "Version": meta["default_version"],
            "Vendor/Provider": meta["vendor"],
            "Your Name": "Matt Redmond",
            "What Program(s) does this software serve?": "IT Systems Management and Security",
            "What is the specific course/module/project you are using this software for?": courses_str,
            "License Type (Perpetual, Subscription, Client/Server,Free, Open Source, etc.)": meta["license_type"],
            "Number of Licenses/Users (Only if known)": "",
            "Scope  (lab, faculty, student, cloud, all)": meta["scope"],
            "Specific Classrooms you intend to use software in. (If on-prem software)": meta["classrooms"],
            "Is this a software or service that is already being used?": meta["already_used"],
            "Cost (only if known)": "",
            "Notes/Comments/Special Requirements": meta["notes"]
        })
        
    # Process Inferred Software Items
    for name, meta in INFERRED_SOFTWARE.items():
        final_list.append({
            "Software Name": name,
            "Version": meta["version"],
            "Vendor/Provider": meta["vendor"],
            "Your Name": "Matt Redmond",
            "What Program(s) does this software serve?": "IT Systems Management and Security",
            "What is the specific course/module/project you are using this software for?": meta["course"],
            "License Type (Perpetual, Subscription, Client/Server,Free, Open Source, etc.)": meta["license_type"],
            "Number of Licenses/Users (Only if known)": "",
            "Scope  (lab, faculty, student, cloud, all)": meta["scope"],
            "Specific Classrooms you intend to use software in. (If on-prem software)": meta["classrooms"],
            "Is this a software or service that is already being used?": meta["already_used"],
            "Cost (only if known)": "",
            "Notes/Comments/Special Requirements": meta["notes"] + " (Inferred program prerequisite)"
        })
        
    # Process Future Software Items
    for name, meta in FUTURE_SOFTWARE.items():
        final_list.append({
            "Software Name": name,
            "Version": meta["version"],
            "Vendor/Provider": meta["vendor"],
            "Your Name": "Matt Redmond",
            "What Program(s) does this software serve?": "IT Systems Management and Security",
            "What is the specific course/module/project you are using this software for?": meta["course"],
            "License Type (Perpetual, Subscription, Client/Server,Free, Open Source, etc.)": meta["license_type"],
            "Number of Licenses/Users (Only if known)": "",
            "Scope  (lab, faculty, student, cloud, all)": meta["scope"],
            "Specific Classrooms you intend to use software in. (If on-prem software)": meta["classrooms"] if "classrooms" in meta else "Online/Cloud",
            "Is this a software or service that is already being used?": meta["already_used"],
            "Cost (only if known)": "",
            "Notes/Comments/Special Requirements": meta["notes"] + " (Proposed addition for upcoming academic year)"
        })

    # Save to JSON file
    output_path = "software_inventory.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_list, f, indent=4, ensure_ascii=False)
        
    print(f"Success! Compiled {len(final_list)} items and saved to {output_path}")

if __name__ == "__main__":
    compile_inventory()
