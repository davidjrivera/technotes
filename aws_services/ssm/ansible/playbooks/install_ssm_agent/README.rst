install_ssm_agent Ansible Playbook
==================================

This playbook relies on ansible role ansible-aws-ssm from https://github.com/dhoeric/ansible-aws-ssm

Installing ansible-aws-ssm anisible role::

  install_ssm_agent> mkdir roles/
  install_ssm_agent> cd roles/
  install_ssm_agent/roles> git clone https://github.com/dhoeric/ansible-aws-ssm.git
  Cloning into 'ansible-aws-ssm'...
  [cut]
  install_ssm_agent/roles> ll
  drwxrwxr-x. 10 agould agould 4096 Nov  9 10:37 ansible-aws-ssm


Running ansible-playbook::

  ACTIVATION_NAME=ucop_ssm_agents
  ansible-playbook install_ssm_agent.yml \
    -i inventory \
    -e "ssm_param_name=/activation/${ACTIVATION_NAME}"
