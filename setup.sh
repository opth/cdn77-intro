#!/bin/bash -eu
RED='\033[1;31m'
GREEN='\033[1;32m'
NC='\033[0m' # No Color

IPS=(
	"172.77.0.2"  # web
	"172.77.0.3"  # monitoring
	"172.77.0.10" # etcd00
	"172.77.0.11" # etcd01
	"172.77.0.12" # etcd02
)

KNOWN_HOSTS="$HOME/.ssh/known_hosts"
PYTHON_EXECUTABLE="/usr/bin/python3"

exit_msg() {
	echo -e "${RED}====== ERROR ======"
	echo -e "$1"
	echo -e "===================${NC}"
	exit $2
}

check_projet_dir() {
	if [[ ! "$PWD" =~ "cdn77-intro" ]]; then
		exit_msg "Current directory is not projet root: 'cd77-intro'." 1
	fi
}

register_known_hosts() {
	check_projet_dir

	mkdir -p ~/.ssh
	touch ~/.ssh/known_hosts

	echo "========== Importing ssh pubkey fingerprints =========="
	if [ ! -w "$KNOWN_HOSTS" ]; then
		exit_msg "$KNOWN_HOSTS does not exist or is unwritable." 1
	fi

	chmod 700 .ssh
	chmod 600 .ssh/ansible
	chmod 644 .ssh/ansible

	for host in "${IPS[@]}"; do
		if ! ping -c 1 -W 0.5 $host 1>/dev/null; then
			echo -e "${RED}X: $host is unreachable.${NC}" 1>&2
			echo
			continue
		fi

		sed -i '/${host}/d' ~/.ssh/known_hosts

		ssh-keyscan $host 2>/dev/null >>"$KNOWN_HOSTS"

		echo -e "${GREEN}✓ Imported $host${NC}"
		echo
	done

}

build_docker_image() {

	check_projet_dir

	echo "========== Building docker image =========="
	docker image rm -f mydebian-ssh:latest 2>/dev/null

	docker build -t mydebian-ssh ./docker

	echo "========== Preparing docker containers =========="
	docker-compose -f docker/docker-compose.yaml up -d
}

check_ansible_ping() {
	check_projet_dir
	(ansible all -i inventory -m ping) || exit_msg "Could not reach all containers from ansible." 1
}

success_msg() {
	echo -e "${GREEN}\n\n✓ Successfully preared all containers for you."
	echo -e "Now you can execute ansible playbooks${NC}"
	echo -e "For example: ansible-playbook web_playbook.yaml"
}

check_python_and_docker() {
	if ! command -v ansible >/dev/null; then
		exit_msg "Ansible not found." 1
	fi
	
	if [[ ! -x "$PYTHON_EXECUTABLE" ]]; then
		exit_msg "Python3 not found at ${PYTHON_EXECUTABLE}" 1
	fi

	if [[ ! -f /var/run/docker.pid ]]; then
		exit_msg "Docker is not running." 1
	fi

	if (! docker version ); then
		exit_msg "Cannot access docker engine." 1
	fi

	if ! command -v docker-compose >/dev/null; then
		exit_msg "docker-compose is not accessible." 1
	fi
}

check_python_and_docker

build_docker_image

register_known_hosts

check_ansible_ping

success_msg
