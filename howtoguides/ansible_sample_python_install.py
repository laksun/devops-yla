---
- name: Deploy Python Application to Amazon Linux 2 and RedHat 9
  hosts: all
  become: yes
  vars:
    # Default variables for RedHat 9
    python_pkg: "python3"
    pip_pkg: "python3-pip"
    python_bin: "/usr/bin/python3"
    venv_path: "/opt/myapp/venv"
    app_dir: "/opt/myapp"
    app_user: "myappuser"
    app_group: "myappgroup"
    service_name: "myapp"
  tasks:
    - name: Set variables for Amazon Linux 2
      set_fact:
        python_pkg: "python38"
        pip_pkg: "python38-pip"
        python_bin: "/usr/bin/python3.8"
      when: ansible_distribution == "Amazon"

    - name: Install Python 3
      package:
        name: "{{ python_pkg }}"
        state: present

    - name: Install pip
      package:
        name: "{{ pip_pkg }}"
        state: present

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
