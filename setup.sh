#!/bin/bash -eu
RED='\033[1;31m'
GREEN='\033[1;32m'
NC='\033[0m' # No Color

IPS=(
	"172.77.0.2"	# web
	"172.77.0.3"	# monitoring
	"172.77.0.10"	# etcd00
	"172.77.0.11"	# etcd01
	"172.77.0.12"	# etcd02
)

KNOWN_HOSTS="$HOME/.ssh/known_hosts"

exit_msg() {
	echo "$1"
	exit $2
}

if [ ! -w "$KNOWN_HOSTS" ]
then
	exit_msg "$KNOWN_HOSTS does not exist or is unwritable." 1
fi

for host in "${IPS[@]}"
do
	if ! ping -c 1 -W 0.5 $host 1>/dev/null
	then
		echo -e "${RED}X: $host is unreachable.${NC}" 1>&2
		echo
		continue
	fi

	sed -i '/${host}/d' ~/.ssh/known_hosts

	ssh-keyscan $host 2>/dev/null >> "$KNOWN_HOSTS"

	echo -e "${GREEN}✓ Imported $host${NC}"
	echo
done
