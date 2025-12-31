+++
date = '2025-02-09T20:37:31+08:00'
draft = false
title = 'Understanding the ABAC Access Control Model'
tags = ["Information Security"]
+++

## Evolution of Access Control (AC)

Access Control (Access Control, AC) is an important mechanism for protecting system resources, determining "who" can access "which" resources and execute "which operations." Its core goal is to prevent unauthorized access and malicious operations, thereby ensuring system security and data confidentiality. The history of access control technology dates back to the 1960s and 1970s, almost synchronized with the birth of computers. After decades of development, access control models have evolved from MAC (Mandatory Access Control) to ABAC (Attribute-Based Access Control), with each stage having its own characteristics and suitable application scenarios.

### AC Evolution Stages

The development of access control technology has gone through the following key stages:

1. **MAC (Mandatory Access Control)**
    - **Features**: The earliest access control model, where the system uniformly manages permissions, and users cannot modify their own permissions.
    - **Pros**: High security, suitable for high-security environments like military and government.
    - **Cons**: Low flexibility, difficult to adapt to enterprise or commercial applications.

2. **DAC (Discretionary Access Control)**
    - **Features**: Resource owners can assign permissions themselves, such as a file owner deciding who can read or modify it.
    - **Pros**: High flexibility, easy to implement, suitable for personal computers, file systems, etc.
    - **Cons**: Fragmented permission management, lack of uniformity, potentially leading to security vulnerabilities.

3. **RBAC (Role-Based Access Control)**
    - **Features**: Users are assigned roles, and permissions are bound to roles. Users inherit permissions from roles rather than having permissions directly assigned.
    - **Pros**: Simplifies permission management, especially suitable for enterprise and organizational management, reducing manual management complexity.
    - **Cons**:
        - Limited fine-grained control capability, difficult to meet complex permission requirements.
        - "Role Explosion" problem: As organizational scale increases, the number of roles may surge, complicating management.

4. **ABAC (Attribute-Based Access Control)**
    - **Features**: Dynamically calculates access permissions based on attributes of users, resources, and environment, rather than fixed role assignments.
    - **Pros**:
        - More flexible, supporting complex permission requirements, suitable for cloud computing, large enterprises, cross-organizational cooperation, etc.
        - Dynamic permission adjustment based on real-time factors (e.g., access time, location, device).
    - **Cons**: High management complexity, requiring stronger policy management capabilities and computing resources.

### AC Development Trends

Overall, access control technology is evolving from static, coarse-grained control toward dynamic, fine-grained management to adapt to increasingly complex IT environments and security needs.

- Early MAC emphasized security and uniform management but lacked flexibility.
- DAC and RBAC improved flexibility and manageability, especially RBAC, which remains the primary mode for many enterprises today.
- ABAC takes flexibility to a new level, achieving finer-grained permission management through attribute combinations, suitable for cloud computing and enterprises with complex security needs.

Although RBAC is currently the mainstream for enterprise access control, ABAC is increasingly adopted due to its powerful flexibility, especially in scenarios requiring dynamic permission adjustment and fine-grained control. In the future, a hybrid RBAC and ABAC model (RBAC-ABAC) may become a new trend—where RBAC manages basic permissions and ABAC handles fine-grained control, ensuring both management simplicity and improved system security and flexibility.

## Overview of ABAC

ABAC (Attribute-Based Access Control) is a dynamic, fine-grained access control method. Unlike traditional RBAC (Role-Based Access Control) and ACL (Access Control List), ABAC does not rely on predefined roles or permissions but instead calculates access permissions in real-time based on attributes of users, resources, and environment. Compared to fixed permission models like RBAC, ABAC provides stronger flexibility, allowing permissions to be adjusted dynamically based on different attributes.

🔹 **Example Comparison:**
- **RBAC Rule:**
    - "Only Managers (role) can access customer personal information."
    - **Problem:** Cannot restrict access based on time or network environment.
- **ABAC Rule:**
    - "Managers can access customer personal information only when using the Company Network (environment attribute) + during Business Day hours (environment attribute)."
    - **Advantage:** Finer permission control, enhancing system security and preventing unauthorized access.

ABAC can be used independently or as a supplementary model to RBAC and ACL, providing finer-grained access control capabilities in an enterprise security architecture.

**Terminology:** Multiple terms are involved in the ABAC system, with several key concepts:

1. **Subject**: The user or program requesting access to a resource, e.g., a doctor, an automated system.
2. **Object**: The protected resource, e.g., a file, database, API, application.
3. **Attributes**: Characteristics used to describe a subject, object, or environment, such as:
    - User attributes: A doctor's "title," an employee's "security level."
    - Object attributes: A file's "classification," a database record's "owner."
4. **Policy**: Decision rules for access permissions, for example:
    - "Only cardiologists can view patient records for heart disease."
    - "Only finance managers can access company financial reports at the end of a quarter."
5. **Environment Conditions**: Dynamic factors affecting access permissions, such as:
    - Time (business day, weekend, off-hours).
    - Location (office, remote VPN, overseas access).
    - Device (PC, phone, personal device, company device).
6. **NPE (Non-Person Entity)**: Non-human entities needing resource access, such as:
    - Programs, automated systems, cameras, printers, IoT devices, etc.

## Competitive Advantages of ABAC

In RBAC (Role-Based Access Control) or ACL (Access Control List) systems, administrators need to define all users who may need access and manually configure their permissions for resources. This static authorization approach has several issues:

1. **Cumbersome permission management and low flexibility**: Administrators must manually establish links between resources and access subjects. When users, resources, or access needs change, permission configurations must be adjusted, leading to high maintenance costs.
2. **Difficult to adapt to dynamic environments**: If a user has not been pre-configured with permissions, they cannot access required resources and must wait for an administrator to manually grant them, as shown below:

**RBAC/ACL Static Access Control Issues**

![image-20250203194643576](https://s2.loli.net/2025/02/09/tVOQpPan9Srdw7X.png)

Under this model:
1. User of Organization A requests access to Organization B's resources.
2. Organization B must first create an account for the user and manually configure access permissions.
3. The user can access resources only after permission configuration is complete.

**Problem:** This method relies on static permission management, leading to cumbersome authorization processes and difficulty adapting to frequently changing business needs.

Compared to RBAC and ACL, ABAC improves system security and management efficiency through dynamic calculation of access permissions, primarily in the following aspects:

### Avoiding Role Explosion

**RBAC Limitations:**
- In the RBAC system, if finer-grained permission control is needed, additional roles are often required, easily leading to "role explosion," where the number of roles increases sharply, raising management complexity.
- For example, in a hospital system, multiple roles might need to be created for ICU doctors, ICU nurses, general doctors, and chief doctors to distinguish locations and their permissions.

**ABAC Advantages:**
- ABAC allows adding environment attributes (location, time, device, etc.) on top of RBAC to dynamically decide access permissions.
- Attributes can be combined freely, avoiding role explosion while providing more precise and flexible access control policies.

🔹 **Example: Hospital Access Control**
- Under RBAC, if a hospital adds an ICU case type and stipulates that only medical staff in the ICU ward can view ICU cases, the following roles must be added:
    - ICU Nurse
    - ICU General Doctor
    - ICU Chief Doctor
- This leads to a role surge and requires manual management of doctor role changes (e.g., when a doctor rotates).

✅ **ABAC Solution:**
- Just define one access policy:
    - "If the doctor's location attribute is 'ICU Ward' and the patient belongs to 'ICU', allow access to patient cases."
- No need to create extra roles; permissions adjust automatically with environmental changes.

### Supporting Dynamic Authorization

In the traditional RBAC model, users must be granted roles beforehand to access resources. For example:
- Only after an administrator manually grants a "Manager" role can a user access financial data.
- If a user is promoted to manager but permissions are not updated in time, they will be unable to access relevant data until the administrator adjusts the role.

✅ **ABAC Improvement:**
- No need for prior permission assignment; as long as a user meets specific attribute conditions, they automatically gain access.
- For example:
    - "If Title = Manager, allow access to financial data."
    - "If Access Device = Company Laptop and Network Environment = Internal Network, allow access to company confidential documents."
- Automated authorization reduces manual management costs, particularly suitable for permission management in large, multi-level organizations, improving authorization efficiency.

**Summary of ABAC Advantages**

| Feature | RBAC/ACL (Manual Method) | ABAC (Attribute-Based Automatic) |
| :--- | :--- | :--- |
| **Permission Config** | Manual role/permission assignment required | Access permissions dynamically calculated based on attributes |
| **Management Cost** | Manual adjustment when resources/users change | Permissions automatically adapt to environment changes |
| **Flexibility** | Static permission binding, hard to adapt to dynamic needs | Supports multi-factor decision-making (environment, time, device, etc.) |
| **Fine-grained Control** | Difficult fine-grained control, prone to role explosion | More fine-grained and flexible permission management |

🔹 **Conclusion:** ABAC makes permission management more efficient, precise, and secure through complex authorization policies. It overcomes the limitations of RBAC/ACL and is especially suitable for cloud computing, large enterprises, and cross-organizational collaboration where fine-grained permission control is needed. In the future, a hybrid RBAC + ABAC mode (RBAC-ABAC) may become mainstream, retaining RBAC's management convenience while integrating ABAC's dynamic decision-making capabilities for an optimal access control solution.

## Working Logic of ABAC

Running an ABAC system requires the following core components:

1. **Attributes**: Characteristics of subjects, objects, or environmental conditions, usually provided as key-value pairs (name-value).
2. **Subject**: The user or device requesting access to resources, typically representing human users or non-person entities (NPE). Subjects can be assigned multiple attributes.
3. **Object**: The protected resource managed by ABAC, such as applications, functions, data, or networks.
4. **Operation**: Execution of functions on the subject, e.g., read, modify, delete.
5. **Policy**: Expression of access rules, usually preset, determining the access logic (allow or deny) between subject and object.
6. **Environment Conditions**: Additional contextual information, such as time, location, device type, etc., used in Policy access control decisions.

The overall working flow of ABAC can refer to the following process:

![image-20250204174348369](https://s2.loli.net/2025/02/09/Qty4r1wugTkRWO2.png)

The ABAC decision process is as follows:
1. User (subject) initiates an access request for a resource (object).
2. The ABAC Access Control Mechanism (ACM) considers the following factors to make a decision:
    1. **Access Control Policy (2a)**: Fetch preset rules, e.g., "Only doctors can view medical records" or "Only accessible within the hospital."
    2. **Subject Attributes (2b)**: Fetch user attributes (position, department, level, etc.).
    3. **Resource (Object) Attributes (2c)**: Fetch attributes of the accessed resource, e.g., which department the record belongs to, its classification, etc.
    4. **Environmental Condition Factors (2d)**: Fetch current situation, e.g., doctor's location, whether it is working hours, and whether the device is trusted.
3. Make a decision, allowing or denying access.
    1. If all conditions match the policy, allow access.
    2. If not, deny access.

Through this example, we understand that ABAC controls access by assigning "attributes" to users and resources, and then using policies. Objects (resources) have attributes (e.g., classification, department, creator). Subjects (users) have attributes (e.g., position, organization, security level). The environment also has attributes (e.g., access time, device, location). The system uses policy rules to decide if a user has permission to access a resource, rather than setting permissions for users individually, making the entire access control system more flexible and efficient.

## Usage Principles of ABAC

### No Individual User Permission Setting

In the ABAC system, access permissions are automatically calculated based on "Policy Rules" rather than manually assigned to users. These rules are usually expressed in two ways:

1. **Boolean conditions**
    - Example: "If user role is Doctor and access object is MedicalRecord, allow access."
    - Such rules directly decide if access is allowed based on user and resource attributes.

2. **Relations**
    - Example: "Nurses can only access patient records of their own department."
    - Rules here are based on relationships between users and resources rather than static assignment.

This means the ABAC system does not need to manually set permissions for each user but dynamically matches user attributes to decide access. This mechanism has higher flexibility and automation capability than traditional role or ACL management.

✅ **Example: New Employee Automatically Gaining Permissions**
- **Scenario:** A hospital adds a new nurse assigned to the Cardiology department.
- **RBAC Method:** Administrator must manually assign access permissions to her.
- **ABAC Method:** As long as the nurse's attributes include "Cardiology Nurse," she can automatically access cardiology cases without extra authorization.

**Advantages:**
- **Reduced administrator workload**: No manual permission updates needed; permissions adapt automatically as user attributes change.
- **Improved security**: Avoids over-authorization or missing permissions.
- **Adaptability to organizational changes**: When departments or personnel change, no re-configuration is needed; ABAC takes effect automatically.

---

### No Attributes for Operations

In the ABAC system, attributes apply only to Subjects and Objects, not to Operations.

🚫 **Wrong Practice (not according to ABAC specifications):**
- Assigning attributes to a "read" operation, for example:
    - ❌ `read = all` (Wrong: Operations should not be assigned values directly)

✅ **Correct Practice:**
- Defining "who can execute an operation," for example:
    - "Doctors can read medical records." (✅ Correct)
    - "Nurses can modify nursing records." (✅ Correct)

**Why should operations not be assigned attributes?**
- **Avoid rule confusion**: Permissions should be based on user and resource attributes rather than assigned to operations, otherwise management becomes difficult.
- **Ensure system clarity and maintainability**: If operations also have attributes, access control logic becomes complex and hard to understand.

---

**Summary:** In ABAC, user permissions don't need manual assignment; the system matches them automatically based on attributes, reducing management costs and increasing flexibility. Operations should not be assigned attributes; instead, permissions are decided based on subject and object attributes, ensuring clarity. These principles make ABAC a dynamic, efficient, and scalable access control solution, especially suitable for large enterprises and cloud environments.

## Enterprise Application of ABAC

In large enterprises, access control is often more complex. The scale is huge, many systems exist, and data is highly sensitive, involving numerous users, resources, environmental attributes, and policies, making traditional RBAC or ACL difficult to meet needs.

Many enterprises already have employee Identity Management Systems storing information like name, ID, position, and rank ("subject attributes"). Furthermore, internal access rules often exist, such as:
- "Finance employees can access financial reports."
- "Senior management can view annual profit data."

However, these rules are often documented business regulations that computers cannot directly understand or execute. ABAC needs to convert these rules into computer-parsable formats (like code or policy configs) and store them in a unified policy repository for the ACM to resolve and execute.

To run ABAC efficiently in an enterprise environment, three core management systems are usually needed:

1. **Subject Attributes Management**: Stores employee department, rank, levels, etc., in a unified Identity System, ensuring all business systems can access these attributes.
2. **Object Attributes Management**: Every file, database, or application system needs correctly marked attributes, e.g.:
    - "Classification: High"
    - "Department: Finance"
    - "Data Category: Customer Information"
    - These attributes are bound to resources themselves, ensuring the ABAC mechanism can evaluate permissions based on rules.
3. **ABAC Access Control Mechanism (ACM)**
    - Deploy a system that dynamically calculates access permissions based on subject, object, and environment attributes, without manual configuration for each user.
    - The system should calculate permissions in real-time, ensuring users matching policies can access resources while others are denied.

✅ **Example: Enterprise ABAC Application Scenario**
When a new employee joins the Finance department, no manual permission assignment is needed. As long as their identity attribute includes "Finance Department," the ABAC mechanism automatically allows them to access financial reports without administrator intervention.

The diagram below shows the complete workflow of enterprise ABAC, involving identity management, policy checks, permission calculation, and final access decisions:

![image-20250207060614809](https://s2.loli.net/2025/02/09/5lMkYrqEnc9mTWD.png)

Main steps of the enterprise-grade ABAC Access Control Mechanism (ACM):

1. **User Identity Management**: User (Subject) authenticates through the Enterprise Identity/Credential Manager and gets access credentials (Credential Issuance). These credentials contain attributes like name, role, organization, and rank, and are stored in the Local Subject Attribute Repository.
2. **Access Request**: User tries to access a resource (Object) and submits a request to the ABAC ACM.
3. **Policy Check**: The ABAC ACM fetches access policies from the Local Access Control Policy Repository. These policies are set by the Enterprise Access Control Policy Administration Point and can be distributed hierarchically to sub-organizations to ensure consistency.
4. **Permission Calculation via Attribute Matching**: The ABAC ACM calculates permissions based on three key factors:
    1. **a) Subject Attributes**: From Local Subject Attribute Repository (e.g., `Title = Finance Manager`, `Level = Confident Access`).
    2. **b) Object Attributes**: From Object Attribute Repository (e.g., `File Type = Finance Data`, `Classification = High`).
    3. **c) Environment Conditions**: Environmental factors (e.g., `Time = Business Day`, `Location = Internal Network`, `Device = Trusted`).
5. **Decision & Execution**:
    1. If all attributes match policies, access is allowed; otherwise, denied.
    2. The result is returned to the user and logged for audit purposes.

From the enterprise ACM mechanism, we can see that access control is dynamically calculated based on multiple attributes. ABAC manages employee and resource attributes uniformly and controls permissions dynamically based on computer-readable rules. It moves away from traditional manual assignment, making management more flexible, efficient, and secure. It is especially suitable for large organizations, significantly improving security and efficiency when sharing information across departments and systems.

### Enterprise Control Strategies

In an enterprise, we need rules to control who can access what under what circumstances. Initially, we use Natural Language Policies (NLPs) to describe these rules, such as:
- Only authenticated doctors can view patient records.
- Finance employees can access financial reports but only read, not modify.
- Senior management can access data from all departments.

These rules are easy for humans to understand but not for computers. Converting NLPs into computer-executable commands is a key problem for ABAC.

To automate access control, we need to convert NLP to Digital Policy (DP). DP features:
- Rules must be directly compiled and executed by computers.
- DP must specify Subject and Object attributes, environment conditions, and allowed operations.

For example, "Only doctors can see medical records" might become:
```xml
<Rule>
    <SubjectAttribute>Role = Doctor</SubjectAttribute>
    <ObjectAttribute>Type = MedicalRecord</ObjectAttribute>
    <Action>Read</Action>
    <Condition>Authenticated = True</Condition>
</Rule>
```
This rule indicates:
- Subject Role must be Doctor.
- Object Type must be MedicalRecord.
- Action is limited to Read.
- Environment Condition requires Authentication.

#### Resolving Policy Conflicts with MP

In enterprise access control, there are often many rules that might overlap or conflict. For example:
- **Rule A**: Doctors can access all medical records.
- **Rule B**: Patients can restrict which doctors view their records.
- **Rule C**: Interns cannot access records of VIP patients.

Which rule takes precedence? Metapolicy (MP) resolves such conflicts in ABAC by:
- Defining rule priorities to ensure high-priority rules are not overwritten.
- Resolving contradictions between different policies.
- Maintaining compliance with security requirements and laws.

For example, a reasonable MP priority might be:
1. Highest priority: Patient's personal privacy settings (patient decides who views their record).
2. Next: Government or industry regulations (e.g., HIPAA).
3. Lowest: Hospital internal policies (e.g., "doctors can access all records").

MP coordinates DP rules, keeping the system flexible yet secure and compliant. Once NLP is converted to DP and managed by MP, an enterprise can build a complete Digital Policy Management (DPM) system. DPM allows flexible adjustment of permissions without manual modification, ensuring compliance and efficiency.

Finally, control strategies help ABAC balance security and flexibility, achieving efficient and secure information sharing.

### Enterprise Attribute Management

ABAC relies on attributes of Subject, Object, and Environment. If attributes are unclear or incomplete, the system fails. For example, if a user's attributes are unknown, the system cannot judge their permissions. If attributes differ across organizations, consistency is lost. Therefore, a complete management mechanism is needed. Key principles:

##### Clear Definition of Attributes
Every attribute must have a clear name, definition, and range.
1. **User attributes**: Position, Department, Clearance, etc.
2. **Resource attributes**: Type, Classification, Owner, etc.
3. **Environment attributes**: Time, Location, etc.

##### Maintenance of Subject Attributes
Different departments manage different attributes to ensure accuracy:
1. Security departments manage Clearance.
2. HR departments manage Name, Title, etc.

This ensured authoritative and reliable data.

##### Maintenance of Object Attributes
Every resource must be correctly assigned attributes to ensure rules execute correctly.
1. Objects are tagged to support access control.
2. Standardized attributes ensure cross-system compatibility.
3. Prevent tampering with object attributes.
4. Ensure no gaps due to missing or wrong data.

Without clear object attributes, ABAC is like a city without house numbers—unable to distinguish where who should enter, leading to vulnerabilities.

##### Metaattributes
When managing tens of thousands of attributes, how do we track them? Are they reliable? Are they up to date? ABAC introduces **Metaattributes** ("attributes about attributes"). They include:
* Records of creation/update time.
* Reliability assessments (e.g., verified by HR vs. self-reported).
* Usage scope (e.g., only for a specific department).

Metaattributes ensure the ACM runs stably and intelligently. They are like "manufacturing dates" or "origins" on food packaging, helping the system manage data correctly.

### ABAC Attribute Management (Summary)

ABAC dynamically decides permissions based on attributes. If data is incomplete or inconsistent, it fails.
- **Clear definition**: Attributes like Position, Classification, and Time must be precise.
- **Subject maintenance**: Departments like HR and Security ensure data authoritative and consistent.
- **Object maintenance**: Resources like files and apps must be correctly tagged; unauthorized modification must be prevented.
- **Metaattributes**: Metadata about attributes (reliability, staleness, scope) ensures intelligent and secure decisions.

In conclusion, ABAC depends on accurate attribute management. Standardized and uniformly managed attributes, along with metaattributes, provide a smart, flexible, and secure solution for complex enterprise IT environments.

### Enterprise-level Distributed ACM (Access Control Mechanism)

In small systems, access control is centralized. However, in large enterprises, this leads to performance bottlenecks and single-point failures. Enterprises adopt a **Distributed Access Control Mechanism (ACM)** for availability, reliability, and scalability. Based on needs, ACM can be centralized, distributed, or hybrid.

#### Key Challenges of Distributed ABAC
- How are decisions made? (Who judges permissions?)
- Who executes control? (Who intercepts requests?)
- How are policies managed? (Writing, storing, updating rules)
- How to optimize? (Ensuring efficiency in high-concurrency environments)

To solve these, ABAC ACM is divided into core components, each handling different tasks.

#### Components of Distributed ACM
The four key components of enterprise-grade ABAC are:

1. **PEP (Policy Enforcement Point)**: Intercepts user requests and enforces Allow/Deny decisions made by PDP. It is the "frontline guard."
2. **PDP (Policy Decision Point)**: The "Brain" that calculates permissions based on policies and attributes. It relies on Policy Repository and PIP.
3. **PIP (Policy Information Point)**: Provides necessary user, object, and environment attributes to the PDP.
4. **PAP (Policy Administration Point)**: Where administrators define, manage, and update policies stored in the Policy Repository for PDP access.

#### Distributed ACM Running Flow
How do these components collaborate?

![Enterprise ACM Interaction Flow](https://s2.loli.net/2025/02/09/uFOC2YVIbA8ZPiG.png)

1. **PEP**: Intercepts the request and sends it to PDP. If PDP allows, PEP executes the access; otherwise, it denies.
2. **PDP**: Receives request, fetches information from Policy Repository and PIP, evaluates compliance, and returns the result to PEP.
3. **PIP**: Fills gaps in attributes by querying Attribute Repository and Environment Conditions upon PDP request.
4. **PAP**: Administrators use it to manage policies in the repository accessed by PDP.

In summary, while small systems can be centralized, large enterprises need a distributed ACM. ABAC components (PEP, PDP, PIP, PAP) ensure requests are dynamically evaluated based on real-time attributes. This allows flexible, cross-system, and cross-organizational access control, making it a mainstream solution for enterprise security.

## References

1. Hu V C, Ferraiolo D, Kuhn R, et al. Guide to Attribute Based Access Control (ABAC) Definition and Considerations NIST SP 800-162. National Institute of Standards and Technology, 2014. [NIST SP 800-162](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-162.pdf)
2. Attribute-based access control. In: Wikipedia. 2024
