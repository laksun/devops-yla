To use specific Python versions on Red Hat 9 and Amazon Linux 2, you need to modify the playbook accordingly. You will need to install Python 3.11 on Red Hat 9 and Python 3.7 on Amazon Linux 2, as specified.

Here’s the updated playbook:

```yaml
---
- name: Setup Specific Python Environments on Linux Servers
  hosts: all
  become: yes
  vars:
    project_src: "/path/to/your/project"
    project_dest: "/opt/your_project"
    virtualenv_name: "your_env"
  
  tasks:
    - name: Install Python 3.7 on Amazon Linux 2
      yum:
        name: 
          - "python37"
          - "python37-pip"
          - "python37-virtualenv"
        state: present
      when: ansible_distribution == "Amazon" and ansible_distribution_major_version == "2"

    - name: Install Python 3.11 on Red Hat 9
      dnf:
        name: 
          - "python3.11"
          - "python3.11-pip"
          - "python3.11-virtualenv"
        state: present
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "9"

    - name: Create Python virtual environment on Amazon Linux 2
      command: "/usr/bin/python3.7 -m venv {{ project_dest }}/{{ virtualenv_name }}"
      args:
        creates: "{{ project_dest }}/{{ virtualenv_name }}"
      when: ansible_distribution == "Amazon" and ansible_distribution_major_version == "2"
    
    - name: Create Python virtual environment on Red Hat 9
      command: "/usr/bin/python3.11 -m venv {{ project_dest }}/{{ virtualenv_name }}"
      args:
        creates: "{{ project_dest }}/{{ virtualenv_name }}"
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "9"
    
    - name: Copy project files to server
      copy:
        src: "{{ project_src }}"
        dest: "{{ project_dest }}"
        owner: root
        group: root
        mode: "0755"

    - name: Upgrade pip in virtual environment on Amazon Linux 2
      command: "{{ project_dest }}/{{ virtualenv_name }}/bin/pip install --upgrade pip"
      when: ansible_distribution == "Amazon" and ansible_distribution_major_version == "2"
    
    - name: Upgrade pip in virtual environment on Red Hat 9
      command: "{{ project_dest }}/{{ virtualenv_name }}/bin/pip install --upgrade pip"
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "9"

    - name: Install required Python packages from requirements.txt
      command: "{{ project_dest }}/{{ virtualenv_name }}/bin/pip install -r {{ project_dest }}/requirements.txt"
      args:
        creates: "{{ project_dest }}/requirements.txt"
      ignore_errors: yes  # Skips step if no requirements.txt file is present
```

### Explanation of Changes:
1. **Python 3.7 for Amazon Linux 2**: Installs Python 3.7 and related packages (`python37`, `python37-pip`, `python37-virtualenv`).
2. **Python 3.11 for Red Hat 9**: Installs Python 3.11 and related packages (`python3.11`, `python3.11-pip`, `python3.11-virtualenv`).
3. **Create Virtual Environment**: Uses the appropriate Python version (`/usr/bin/python3.7` or `/usr/bin/python3.11`) to create a virtual environment based on the distribution.

### Usage Notes:
- Make sure the source path (`project_src`) and the destination path (`project_dest`) are properly set.
- This playbook assumes the specific versions of Python (`3.7` for Amazon Linux 2 and `3.11` for Red Hat 9) are available in the repositories. If not, you may need to enable additional repositories or manually install the versions you need.
- Run the playbook using your Ansible command as shown before:

```bash
ansible-playbook -i inventory setup_python_env.yml
```

Let me know if you need further customization or assistance!