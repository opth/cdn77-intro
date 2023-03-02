#!/bin/bash -eu

ips=(
	"172.77.0.2"	# web
	"172.77.0.3"	# monitoring
	"172.77.0.10"	# etcd00
	"172.77.0.11"	# etcd01
	"172.77.0.12"	# etcd02
)

known_hosts_path="$HOME/.ssh/known_hosts"

exit_msg() {
	echo "$1"
	exit $2
}

if [ ! -w "$known_hosts_path" ]
then
	exit_msg "$known_hosts_path does not exist or is unwritable." 1
fi

for host in "${ips[@]}"
do
	if ping -c 1 $host &>/dev/null
	then
		echo "$host is unreachable."
		break
	fi

	sed -i '/${host}/d' ~/.ssh/known_hosts

	echo "==== Importing ssh pubkey fingerpring for $host ===="
	ssh-keyscan $host >> "$known_hosts_path"
done
