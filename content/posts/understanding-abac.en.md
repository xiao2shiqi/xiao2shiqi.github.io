+++
date = '2025-02-09T20:37:31+08:00'
draft = false
title = 'Understanding Attribute-Based Access Control (ABAC)'
tags = ["Information Security"]
+++

## 1. Evolution of Access Control (AC)

Access Control determines **who** can access **what** and perform **which operations**. 

### The Key Phases:
1. **MAC (Mandatory Access Control)**: Fixed centralized management. High security, low flexibility (e.g., military).
2. **DAC (Discretionary Access Control)**: Owner-based sharing. High flexibility, low consistency (e.g., file systems).
3. **RBAC (Role-Based Access Control)**: Permissions mapped to roles. Simplifies management for enterprise structures.
4. **ABAC (Attribute-Based Access Control)**: Permissions calculated dynamically based on attributes of users, resources, and environment.

**Trend**: Moving from static/coarse-grained to dynamic/fine-grained control. **Hybrid RBAC-ABAC** is the current industry trend.

## 2. What is ABAC?

ABAC doesn't use hardcoded roles. It evaluates **Attributes** in real-time.
- **Subject Attributes**: Title, department, security clearance.
- **Object Attributes**: Sensitivity level, owner, file type.
- **Environment Attributes**: Time of day, IP location, device health.

**Example**:
*   **RBAC**: "Managers can view files."
*   **ABAC**: "Managers from the Finance Dept can view 'Sealed' files only on workdays from the office VPN."

## 3. Why ABAC?

### Avoiding Role Explosion
In RBAC, adding granularity (e.g., "ICU Nurse" vs "ER Nurse") requires new roles. In ABAC, you keep the "Nurse" role and add an `Environment.Location` attribute to the policy.

### Dynamic Authorization
No need for manual provisioning. If a user’s department attribute changes in the central HR system, their access updates instantly across the ecosystem based on policies.

## 4. Enterprise-Grade Implementation

In large organizations, ABAC requires three pillars:
- **Centralized Identity**: A source for Subject Attributes (HR/Identity system).
- **Tagged Resources**: Objects must have metadata (Object Attributes).
- **Policy Engine**: A system to calculate permissions on the fly.

### The Architecture (NIST Standard):
1. **PEP (Policy Enforcement Point)**: Intercepts requests.
2. **PDP (Policy Decision Point)**: The brain that evaluates policies.
3. **PIP (Policy Information Point)**: Fetches missing attributes.
4. **PAP (Policy Administration Point)**: Where admins write and deploy policies.

## 5. Decision Logic (NLP -> DP -> MP)

1. **NLP (Natural Language Policy)**: "Only doctors can see patient records."
2. **DP (Digital Policy)**: Machine-readable version (e.g., XML/JSON).
3. **MP (Metapolicy)**: Rules to handle conflicts when multiple policies apply (e.g., "Deny-Override" strategy).

## 6. Summary

ABAC provides the precision and flexibility needed for modern, scale-out cloud environments. While it takes more effort to define attributes and policies compared to simple RBAC, it significantly reduces long-term maintenance costs and security risks in complex organizations.
