#!/bin/bash

# Send DST_DIR to 1st parameter of this shellcode
# Send Cluster name to 2nd param, default to MyDediServer
# Send INSTALL_TEMP_DIR to 3rd param

DST_DIR=$1
cluster_name=$2
INSTALL_TEMP_DIR=$3

steamcmd_dir="$INSTALL_TEMP_DIR/steamcmd"
install_dir="$INSTALL_TEMP_DIR/dontstarvetogether_dedicated_server"
#cluster_name="MyDediServer"
dontstarve_dir="$DST_DIR/DoNotStarveTogether"

function fail()
{
	echo Error: "$@" >&2
	exit 1
}

function check_for_file()
{
	if [ ! -e "$1" ]; then
		fail "Missing file: $1"
	fi
}

cd "$steamcmd_dir" || fail "Missing $steamcmd_dir directory!"

check_for_file "steamcmd.sh"
check_for_file "$dontstarve_dir/$cluster_name/cluster.ini"
check_for_file "$dontstarve_dir/$cluster_name/cluster_token.txt"
check_for_file "$dontstarve_dir/$cluster_name/Master/server.ini"
check_for_file "$dontstarve_dir/$cluster_name/Caves/server.ini"

## validate section, we will backup mod file first
echo "Backup mods..."
cp $INSTALL_TEMP_DIR/dontstarvetogether_dedicated_server/mods/dedicated_server_mods_setup.lua $INSTALL_TEMP_DIR/dedicated_server_mods_setup.lua

echo "Validating game..."
./steamcmd.sh +force_install_dir "$install_dir" +login anonymous +app_update 343050 validate +quit

echo "Restore mods"
cp $INSTALL_TEMP_DIR/dedicated_server_mods_setup.lua $INSTALL_TEMP_DIR/dontstarvetogether_dedicated_server/mods/dedicated_server_mods_setup.lua

# start game

check_for_file "$install_dir/bin64"

cd "$install_dir/bin64" || fail

run_shared=(./dontstarve_dedicated_server_nullrenderer_x64)
run_shared+=(-console)
run_shared+=(-cluster "$cluster_name")
run_shared+=(-monitor_parent_process $$)

"${run_shared[@]}" -shard Caves  | sed 's/^/Caves:  /' &
"${run_shared[@]}" -shard Master | sed 's/^/Master: /'

