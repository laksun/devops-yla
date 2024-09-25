---
- name: Deploy Python Application to Multiple Distributions
  hosts: all
  become: yes
  vars:
    # Default variables for RedHat 9 and Amazon Linux 2023
    python_pkg: "python3.11"
    pip_pkg: "python3-pip"
    python_bin: "/usr/bin/python3.11"
    venv_path: "/opt/myapp/venv"
    app_dir: "/opt/myapp"
    app_user: "myappuser"
    app_group: "myappgroup"
    service_name: "myapp"
    epel_release_pkg: "epel-release"
    epel_repo_url: "https://dl.fedoraproject.org/pub/epel/epel-release-latest-{{ ansible_distribution_major_version }}.noarch.rpm"
  tasks:
    - name: Set variables for Amazon Linux 2
      set_fact:
        python_pkg: "python38"
        pip_pkg: "python38-pip"
        python_bin: "/usr/bin/python3.8"
      when: ansible_distribution == "Amazon" and ansible_distribution_major_version == "2"

    - name: Set variables for Amazon Linux 2023
      set_fact:
        python_pkg: "python3.11"
        pip_pkg: "python3-pip"
        python_bin: "/usr/bin/python3.11"
      when: ansible_distribution == "Amazon" and ansible_distribution_major_version == "2023"

    - name: Set variables for RedHat 8
      set_fact:
        python_pkg: "python3.11"
        pip_pkg: "python3-pip"
        python_bin: "/usr/bin/python3.11"
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "8"

    - name: Set variables for RedHat 7
      set_fact:
        python_pkg: "python3.11"
        pip_pkg: "pip3.11"
        python_bin: "/usr/local/bin/python3.11"
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "7"

    - name: Install EPEL repository on RedHat 8
      yum:
        name: "{{ epel_release_pkg }}"
        state: present
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "8"

    - name: Install EPEL repository on RedHat 7
      yum:
        name: "{{ epel_repo_url }}"
        state: present
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "7"

    - name: Install Python 3 on RedHat 8
      yum:
        name: "{{ python_pkg }}"
        enablerepo: "epel"
        state: present
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "8"

    - name: Install development tools on RedHat 7
      yum:
        name:
          - gcc
          - openssl-devel
          - bzip2-devel
          - libffi-devel
          - zlib-devel
        state: present
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "7"

    - name: Download Python 3.11 source code on RedHat 7
      get_url:
        url: "https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz"
        dest: "/usr/src/Python-3.11.0.tgz"
        mode: '0644'
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "7"

    - name: Extract Python 3.11 source code on RedHat 7
      unarchive:
        src: "/usr/src/Python-3.11.0.tgz"
        dest: "/usr/src/"
        remote_src: yes
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "7"

    - name: Compile and install Python 3.11 on RedHat 7
      shell: |
        cd /usr/src/Python-3.11.0
        ./configure --enable-optimizations
        make altinstall
      args:
        creates: "/usr/local/bin/python3.11"
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "7"

    - name: Install pip on RedHat 7
      get_url:
        url: https://bootstrap.pypa.io/get-pip.py
        dest: /tmp/get-pip.py
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "7"

    - name: Install pip3.11 on RedHat 7
      shell: "{{ python_bin }} /tmp/get-pip.py"
      args:
        creates: "/usr/local/bin/pip3.11"
      when: ansible_distribution == "RedHat" and ansible_distribution_major_version == "7"

    - name: Install pip package on other systems
      package:
        name: "{{ pip_pkg }}"
        state: present
      when: not (ansible_distribution == "RedHat" and ansible_distribution_major_version == "7")

    - name: Create application user
      user:
        name: "{{ app_user }}"
        group: "{{ app_group }}"
        create_home: no
        shell: /sbin/nologin
        system: yes

    - name: Create application directory
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
        mode: '0755'

    - name: Create virtual environment
      command: "{{ python_bin }} -m venv {{ venv_path }}"
      args:
        creates: "{{ venv_path }}/bin/activate"
      become_user: "{{ app_user }}"

    - name: Copy application code
      copy:
        src: /local/path/to/application/
        dest: "{{ app_dir }}/"
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
        mode: '0755'
        recursive: yes

    - name: Install application dependencies
      pip:
        requirements: "{{ app_dir }}/requirements.txt"
        virtualenv: "{{ venv_path }}"
        virtualenv_command: "{{ python_bin }} -m venv"
      become_user: "{{ app_user }}"

    - name: Create systemd service file
      template:
        src: app.service.j2
        dest: "/etc/systemd/system/{{ service_name }}.service"
        mode: '0644'
      notify:
        - Reload systemd
        - Restart application

    - name: Enable and start the application service
      systemd:
        name: "{{ service_name }}"
        enabled: yes
        state: started

  handlers:
    - name: Reload systemd
      command: systemctl daemon-reload

    - name: Restart application
      systemd:
        name: "{{ service_name }}"
        state: restarted
