#!/usr/bin/env bash

set -euo pipefail

readonly REPORT_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/helsing"
declare -A THREAT_LABELS=(
	[0]="clear"
	[1]="observed"
	[2]="severe"
)

log() {
	local level=$1
	shift
	printf '[%(%H:%M:%S)T] %-8s %s\n' -1 "${THREAT_LABELS[$level]}" "$*"
}

inspect_host() {
	local host=$1
	local response

	if ! response=$(curl --fail --silent --max-time 3 "https://${host}/health"); then
		log 2 "${host} did not answer before sunrise"
		return 1
	fi

	[[ $response == *'"status":"awake"'* ]] && log 1 "${host} requires observation"
}

main() {
	mkdir -p "$REPORT_DIR"

	local host
	for host in "$@"; do
		inspect_host "$host" || printf '%s\n' "$host" >>"${REPORT_DIR}/unreachable.log"
	done
}

[[ ${BASH_SOURCE[0]} == "$0" ]] && main "$@"
