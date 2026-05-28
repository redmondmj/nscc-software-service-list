# IT Systems Management & Security (ITSYSSEC) Program - Software & Service Report

This report compiles all the software tools, cloud services, and hardware utilities used in the two-year **IT Systems Management and Security** diploma program at NSCC. It maps each software to its target courses and details licensing types, usage scope, and deployment settings.

## Core Software & Service Catalog

### Virtualization & Hypervisors
| Software/Service Name | Courses Used In | License Type | Scope | Notes |
| --- | --- | --- | --- | --- |
| **VMware Workstation Pro** | ISEC2700, ISEC3700, NETW2710, OSYS1200, OSYS3030 | Subscription (Academic/Commercial) | *student, faculty, lab* | Hypervisor used by students on their local laptops to run class VMs. |
| **VMware vSphere ESXi** | ISEC2700, NETW1500, NETW2710, OSYS3030 | Subscription / Academic | *lab, faculty* | Type-1 bare-metal hypervisor hosting the shared virtual laboratory environment. |
| **VMware vCenter Server** | ISEC2700, NETW2710 | Subscription / Academic | *lab, faculty* | Centralized management platform for vSphere environments and ESXi hosts. |
| **Proxmox VE** | ISEC2700, NETW1500, NETW2710, OSYS3030 | Open Source (Free / No Subscription Repository) | *lab, faculty* | Open-source hypervisor used in virtual lab setups and container virtualization environments. |
| **Oracle VM VirtualBox** | ISEC3700, OSYS3030 | Open Source (GPL v2) / Free | *student, faculty* | Type-2 hypervisor used as an alternative for local VM hosting. |
| **VirtViewer** | NETW2710, OSYS3030 | Open Source (Free) | *student, faculty, lab* | Spice protocol client for high-performance remote console access to virtual machines. |

### Cloud Computing Platforms
| Software/Service Name | Courses Used In | License Type | Scope | Notes |
| --- | --- | --- | --- | --- |
| **AWS Academy / Cloud Sandbox** | ISEC2700, ISEC3700, NETW1500, NETW2710, OSYS3030 | Subscription / Free Academic Tier | *cloud, student* | Cloud environment used to deploy virtual networks (VPC), EC2 servers, and practice cloud administration. |
| **Microsoft Azure for Students** | ISEC2700, ISEC3700, NETW1027, NETW1500, NETW2710, NETW3500, OSYS1200, OSYS3030 | Subscription / Free Academic Tier | *cloud, student* | Cloud platform hosting virtual machines, app services, and active directory synchronizations. |

### Operating Systems (Server & Client)
| Software/Service Name | Courses Used In | License Type | Scope | Notes |
| --- | --- | --- | --- | --- |
| **Microsoft Windows Server** | ISEC2700, ISEC3700, NETW1500, NETW2710, NETW3500, OSYS1200, OSYS3030 | Subscription (Azure Dev Tools for Teaching) | *all* | Primary Server OS. Used for Active Directory, Group Policy, IIS, WSUS, and DNS/DHCP infrastructure. |
| **Microsoft Windows 10/11 Pro** | ISEC2700, ISEC3700, NETW1500, NETW3500, OSYS1200 | Subscription (Azure Dev Tools for Teaching) | *all* | Primary client operating system for workstations, user deployment, and client NOS admin labs. |
| **Debian GNU/Linux** | ISEC2700, NETW2710, OSYS3030 | Open Source (Free) | *all* | Used in virtualization labs, containers, and Linux network services. |
| **Windows ADK** | NETW1500, NETW3500 | Free | *student, faculty, lab* | Set of tools used to customize Windows images for large-scale deployment and to test system performance. |
| **Windows Subsystem for Linux** | ISEC2700, NETW2710, OSYS3030 | Free | *student, faculty, lab* | Compatibility layer for running Linux binary executables natively on Windows 10/11, vital for container, Docker, and DevOps labs. |
| **Windows PE (Preinstallation Environment)** | NETW1500, NETW3500 | Free | *student, faculty, lab* | Lightweight operating system used for preparing PCs for Windows installation and deployment (MCM dependency). |
| **Windows Recovery Environment (WinRE)** | OSYS1200, NETW1500 | Free (OS Native) | *student, faculty, lab* | Recovery environment used to troubleshoot, recover, or restore Windows installations. |
| **DISM** | NETW1500, NETW3500 | Free (OS Native) | *student, faculty, lab* | Command-line tool used to service Windows images (.wim, .vhd) prior to deployment. |
| **Rufus** | OSYS1200, NETW1500 | Open Source (Free) | *student, faculty, lab* | Utility that helps format and create bootable USB flash drives for OS installation. |

### Network Services & Infrastructure
| Software/Service Name | Courses Used In | License Type | Scope | Notes |
| --- | --- | --- | --- | --- |
| **Apache HTTP Server** | ISEC2700, ISEC3700, OSYS3030 | Open Source (Free) | *lab, student* | Open source web server software taught in web services and Linux administration labs. |
| **Nginx** | ISEC2700, OSYS3030 | Open Source (Free) | *lab, student* | High performance web server and reverse proxy taught in containerization and web administration. |
| **NetAlly LinkRunner AT1000/2000** | ITSM Program | Perpetual Hardware Included | *lab, faculty* | Physical network auto-tester hardware used to verify cabling connections and link status. |
| **Tftpd64** | NETW1500, NETW3500 | Open Source (Free) | *student, faculty, lab* | A lightweight IPv6-ready TFTP server and client utility used for network device firmware updates and PXE network booting. |
| **WiFiman Desktop** | NETW1027, NETW1500 | Free | *student, faculty, lab* | Network diagnostics tool providing Wi-Fi discovery, device scanning, and link speed analysis. |

### DevOps & Automation Tools
| Software/Service Name | Courses Used In | License Type | Scope | Notes |
| --- | --- | --- | --- | --- |
| **Git / GitHub** | ISEC2700, NETW1500, NETW2710, OSYS1200, OSYS3030 | Free / Open Source | *all* | Distributed version control system and repository hosting platform for scripting and DevOps code. |
| **Docker & Docker Compose** | ISEC2700, ISEC3700, OSYS1200, OSYS3030 | Free (Personal/Academic) / Open Source | *all* | Containerization platform used to package, distribute, and run microservices and application stacks. |
| **Kubernetes (k8s)** | NETW3500 | Open Source (Free) | *cloud, student, lab* | Container orchestration engine for automated deployment, scaling, and management of containerized apps. |
| **Ansible** | ITSM Program | Open Source (Free) | *all* | Agentless automation and configuration management tool used for server configuration orchestration. |
| **HashiCorp Terraform** | ITSM Program | Open Source (BUSL) | *all* | Infrastructure as Code (IaC) tool to provision and manage cloud infrastructure. |
| **Microsoft Endpoint Configuration Manager (MCM / SCCM)** | NETW3500 (Enterprise Management and Automation) | Subscription / Client/Server (Academic License) | *lab, faculty, student* | Enterprise systems management software for managing large groups of Windows-based computers. |
| **Ninite** | OSYS1200, NETW1500 | Free / Proprietary | *student, faculty, lab* | Package management utility to install and update multiple applications automatically. |
| **Puppet** | NETW3500 (Enterprise Management and Automation) | Open Source / Free | *student, lab* | Configuration management utility to automate provisioning and compliance management (taught alongside Ansible). |
| **Chef** | NETW3500 (Enterprise Management and Automation) | Open Source / Free | *student, lab* | Infrastructure automation platform used to define infrastructure as code (taught alongside Ansible). |

### Security & Penetration Testing Tools
| Software/Service Name | Courses Used In | License Type | Scope | Notes |
| --- | --- | --- | --- | --- |
| **pfSense / OPNsense** | ISEC3700 | Open Source (Free) | *lab, student* | Open-source firewall/router virtual appliance used to teach perimeter security, NAT, and VPN configurations. |
| **Wireshark** | ISEC2700, ISEC3700, OSYS1200 | Open Source (Free) | *all* | Network packet analyzer tool used in networking, security audits, and troubleshooting labs. |
| **Nmap** | ISEC2700, ISEC3700, OSYS3030 | Open Source (Free) | *all* | Network exploration tool and security / port scanner used in security courses. |
| **Metasploit Framework** | ISEC2700 | Open Source (Free) | *student, lab* | Penetration testing and exploit framework used to teach vulnerability assessment and defensive controls. |
| **Tenables Nessus** | ISEC2700, ISEC3700 | Free / Academic Trial | *student, lab* | Vulnerability assessment scanner used in security audits and capstones. |

### Development & Programming Utilities
| Software/Service Name | Courses Used In | License Type | Scope | Notes |
| --- | --- | --- | --- | --- |
| **VS Code (Visual Studio Code)** | ISEC2700, NETW1500, OSYS1200, OSYS3030 | Open Source / Free | *all* | Standard code editor used by students for programming, writing scripts, and DevOps configurations. |
| **Python Programming Language** | ISEC2700 | Open Source / Free | *all* | Primary programming and scripting language taught in Logic & Programming and automation courses. |
| **MySQL / MariaDB** | ISEC2700, OSYS1200, OSYS3030 | Open Source (Free) | *lab, student* | Relational database systems used to teach SQL fundamentals and host web application databases. |
| **PostgreSQL** | OSYS3030 | Open Source (Free) | *lab, student* | Relational database used in network services and backend systems. |
| **MongoDB** | ITSM Program | Open Source (SSPL) | *lab, student* | Document-based NoSQL database used to teach non-relational database fundamentals. |
| **PuTTY & MobaXterm** | NETW3500 | Open Source (Free) / Free Edition | *all* | Terminal clients (SSH, telnet, serial) used to connect to routers, switches, and remote servers. |
| **draw.io** | NETW1027, DBAS1007 | Open Source (Free) | *student, faculty* | Diagramming software used by students to design network topologies and databases (ERDs). |
| **Sysinternals Suite** | OSYS1200, OSYS3030, ISEC2700 | Free | *student, faculty, lab* | Advanced system diagnostics utilities (Procmon, Process Explorer, Autoruns) for Windows troubleshooting. |
| **Windows Admin Center** | OSYS1200, OSYS3030 | Free (Windows Server License Required) | *student, faculty, lab* | Browser-based management tool for administering Windows Server, clusters, and hyper-converged infrastructure. |
| **Tera Term** | NETW1027, NETW1500 | Open Source (Free) | *student, faculty, lab* | A terminal emulator program supporting serial port, SSH, and telnet connections for managing switch/router consoles. |
| **Ollama** | ITSM Program | Open Source (Free) | *student, faculty, lab* | Local execution environment for large language models, allowing AI integration in developer tools and terminal setups. |
| **WinDirStat** | OSYS1200 | Open Source (Free) | *student, faculty, lab* | Disk usage statistics viewer and cleanup tool, helping visualize storage consumption. |
| **Microsoft SQL Server** | NETW3500 (Enterprise Management and Automation), DBAS1007 | Subscription / Client/Server (Academic License / Developer Edition) | *lab, faculty, student* | Relational database management server, serving as the backend database host for Configuration Manager (MCM). |

### Collaboration & Productivity Services
| Software/Service Name | Courses Used In | License Type | Scope | Notes |
| --- | --- | --- | --- | --- |
| **Ubuntu Server / Desktop** | ISEC2700, ISEC3700, NETW2710, NETW3500, OSYS3030 | Open Source (Free) | *all* | Primary Linux distribution for Linux administration, network services, DevOps, and containers. |
| **Cisco Packet Tracer** | ISEC3700 | Free (NetAcad Account Required) | *student, faculty* | Network hardware simulator used for modeling and testing Cisco switch and router configurations. |
| **Microsoft Intune / Autopilot** | NETW1500, NETW3500 | Subscription (NSCC M365) | *cloud, faculty, student* | Cloud-based Unified Endpoint Management (UEM) solution for MDM/MAM and modern deployment. |
| **Microsoft 365 (M365) / Entra ID** | ISEC2700, ISEC3700, NETW1500, NETW2710, NETW3500, OSYS1200, OSYS3030 | Subscription (NSCC M365) | *all* | Identity provider and SaaS environment used for cloud connections and enterprise identity labs. |
| **Discord** | OSYS1200 | Proprietary (Free) | *student, faculty* | Communication tool used for peer collaboration, virtual study groups, and remote lab support. |
| **Microsoft Teams** | ISEC2700, ISEC3700, NETW1500, NETW2710, NETW3500, OSYS1200, OSYS3030 | Subscription (NSCC M365) | *all* | Primary institutional communication, virtual classes, and team coordination tool. |

## Inferred Software & assumed Prerequisites
These tools are essential prerequisites and daily administrative utilities assumed for coursework but not explicitly registered in standard syllabus documents:
| Software Name | Vendor | Usage & Assumptions | Courses |
| --- | --- | --- | --- |
| **Google Chrome / Firefox** | Google / Mozilla | Standard web browsers required for accessing SaaS portals, web apps, and administration interfaces. | WEBD1000, NETW3500, OSYS3030 |
| **7-Zip** | Igor Pavlov | File archiver utility required for zipping and unzipping course files, VMs, and scripts. | OSYS1200, NETW1500 |
| **OpenSSH Client** | OpenBSD Project | Native terminal command-line tool for SSH connections to servers and network hardware. | OSYS1000, OSYS3030, NETW2700 |
| **Notepad++** | Don Ho | Lightweight text editor used as a simple editor for script editing and config files. | OSYS1200, NETW1500 |

## Future Software Requirements (Next 12 Months)
These technologies are proposed for integration into the curriculum over the next academic year to keep pace with industry developments in DevSecOps and cloud automation:
| Software Name | Vendor | Rationale for Curriculum Integration | Target Course |
| --- | --- | --- | --- |
| **HashiCorp Vault** | HashiCorp | Potential addition for Year 2 DevOps courses to teach secure secret management and password rotation. | NETW3500 (Enterprise Management and Automation) |
| **Elastic Stack (ELK) / Splunk Free** | Elastic / Splunk | Potential software for security monitoring, log aggregation, and analysis in advanced security labs. | ISEC2700 (Intro to Information Security) |
| **GitHub Actions** | GitHub (Microsoft) | Potential CI/CD pipeline manager to teach testing automation and deployment flows. | INFT2700 (IT Project Quality Assurance) |