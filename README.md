# Automated IT Audit & GRC Framework

A comprehensive, Python-based IT General Controls (ITGC) and ISO 27001:2022 automated audit framework. This tool streamlines the extraction, analysis, and reporting of Active Directory vulnerabilities and Windows Security Event Logs.

## 1. Project Overview
This framework was developed in an isolated enterprise virtual laboratory environment (Windows Server 2022 Domain Controller) to automate the manual audit procedures for ITGC and ISO 27001 compliance. It directly addresses the following ISO 27001:2022 controls:
* **A.5.15 & A.5.18:** Access Control & Access Rights (Inactive accounts, password policies)
* **A.8.2:** Privileged Access Rights (Domain Admin monitoring)
* **A.8.5:** Secure Authentication (Password never expires detection)
* **A.12.4.1:** Event Logging (Brute-force detection via Windows Event Logs)

## 2. Architecture & Lab Environment
The tool was tested in a custom-built hypervisor environment simulating a corporate infrastructure:
* **Hypervisor:** VirtualBox (Internal Network Subnet: 192.168.X.0/24)
* **Domain Controller:** Windows Server 2022 (Active Directory Domain Services)
* **Development Environment:** Python 3.11+, Linux & Windows environments.

## 3. Core Features
* **Active Directory Auditor (ad_auditor.py):** Queries LDAP to detect dormant accounts (>90 days), accounts with non-expiring passwords, and high-privilege group members.
* **Security Log Auditor (log_auditor.py):** Parses Windows Security.evtx logs to detect brute-force attempts (Event ID 4625) and unauthorized group modifications (Event ID 4728).
* **Automated Workpaper Engine (workpaper_engine.py):** Converts raw audit findings into color-coded, professional Excel audit workpapers using Pandas and OpenPyXL.
* **Executive PDF Reporting (pdf_report_engine.py):** Generates management-ready executive summary PDFs highlighting critical risks.

## 4. Installation & Configuration

Clone the repository and configure your target environment:

    git clone https://github.com/Wildrdon/Automated-IT-Audit-Framework.git
    cd Automated-IT-Audit-Framework
    pip install pandas openpyxl reportlab ldap3 colorama tabulate pywin32

Edit the config/config.json file with your Domain Controller IP and audit thresholds before execution.

## 5. Usage

Run the modules individually based on the audit scope:

    # Execute Active Directory Vulnerability Scan
    python src/ad_auditor.py

    # Execute Windows Event Log Analysis
    python src/log_auditor.py

    # Generate Excel Audit Workpaper
    python src/workpaper_engine.py

## 6. Sample Output
[IT_Audit_Executive_Report.pdf](https://github.com/user-attachments/files/31622994/IT_Audit_Executive_Report.pdf)
[IT_Audit_Workpaper.xlsx](https://github.com/user-attachments/files/31622995/IT_Audit_Workpaper.xlsx)

*Disclaimer: This tool is developed strictly for authorized IT auditing and educational purposes.*

