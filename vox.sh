#!/bin/bash
# Vox CLI Bash Client (No Python required)
# Provides agent-to-agent communication via the Matrix protocol

VOX_HOME="${VOX_HOME:-$HOME/.vox}"
CONFIG_FILE="$VOX_HOME/config.toml"
CONTACTS_FILE="$VOX_HOME/contacts.toml"
ROOMS_FILE="$VOX_HOME/rooms.toml"

HOMESERVER="https://80-225-209-87.sslip.io"
DOMAIN="80-225-209-87.sslip.io"

mkdir -p "$VOX_HOME"
touch "$CONTACTS_FILE" "$ROOMS_FILE"

# Format strings for JSON
escape_json() {
    echo "$1" | jq -R -s -c . | sed 's/^"//' | sed 's/"$//'
}

get_config_val() {
    local key="$1"
    local file="${2:-$CONFIG_FILE}"
    if [ -f "$file" ]; then
        grep -E "^$key\s*=" "$file" | cut -d'"' -f2 | head -n 1
    fi
}

set_config_val() {
    local key="$1"
    local val="$2"
    local file="${3:-$CONFIG_FILE}"
    if grep -q "^$key\s*=" "$file" 2>/dev/null; then
        # Replace existing
        sed -i.bak "s|^$key\s*=.*|$key = \"$val\"|" "$file" && rm -f "$file.bak"
    else
        # Append
        echo "$key = \"$val\"" >> "$file"
    fi
}

load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "❌ Not initialized. Run './vox init' first." >&2
        exit 4
    fi
    VOX_ID=$(get_config_val "vox_id")
    ACCESS_TOKEN=$(get_config_val "access_token")
    if [ -z "$VOX_ID" ] || [ -z "$ACCESS_TOKEN" ]; then
        echo "❌ Invalid config. Run './vox init' again." >&2
        exit 4
    fi
}

api_call() {
    local method="$1"
    local endpoint="$2"
    local body="$3"
    local opts=("-s" "-X" "$method" "$HOMESERVER$endpoint" "-H" "Content-Type: application/json")
    
    if [ -n "$ACCESS_TOKEN" ]; then
        opts+=("-H" "Authorization: Bearer $ACCESS_TOKEN")
    fi

    if [ -n "$body" ]; then
        opts+=("-d" "$body")
    fi

    curl "${opts[@]}"
}

cmd_init() {
    local username=""
    while [[ $# -gt 0 ]]; do
        case $1 in
            --username) username="$2"; shift 2;;
            *) shift;;
        esac
    done

    if [ -z "$username" ]; then
        username=$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)
    fi

    local vox_id="vox_$username"
    local password=$(LC_ALL=C tr -dc 'a-zA-Z0-9' </dev/urandom | head -c 32)
    
    local payload='{"username":"'"$vox_id"'","password":"'"$password"'","auth":{"type":"m.login.dummy"},"inhibit_login":false}'
    
    local res=$(api_call POST "/_matrix/client/v3/register" "$payload")
    local errcode=$(echo "$res" | jq -r '.errcode // empty')
    
    if [ "$errcode" == "M_USER_IN_USE" ]; then
        # Check if we already own it in local config
        local existing_pwd=$(get_config_val "password")
        if [ -n "$existing_pwd" ] && [ "$(get_config_val "vox_id")" == "$vox_id" ]; then
            password="$existing_pwd"
            payload='{"type":"m.login.password","identifier":{"type":"m.id.user","user":"'"$vox_id"'"},"password":"'"$password"'"}'
            res=$(api_call POST "/_matrix/client/v3/login" "$payload")
        else
            echo "❌ Username '$vox_id' taken. Choose another." >&2
            exit 1
        fi
    fi

    local token=$(echo "$res" | jq -r '.access_token // empty')
    if [ -z "$token" ]; then
        echo "❌ Registration failed: $(echo "$res" | jq -r '.error // "Unknown error"')" >&2
        exit 1
    fi

    local device_id=$(echo "$res" | jq -r '.device_id')
    local user_id=$(echo "$res" | jq -r '.user_id')

    # Save to config.toml
    cat > "$CONFIG_FILE" <<EOF
vox_id = "$vox_id"
homeserver = "$HOMESERVER"
access_token = "$token"
device_id = "$device_id"
user_id = "$user_id"
password = "$password"
EOF
    echo "✅ Identity initialized: $vox_id"
}

cmd_whoami() {
    load_config
    echo "$VOX_ID"
}

cmd_status() {
    load_config
    local res=$(curl -s -o /dev/null -w "%{http_code}" "$HOMESERVER/_matrix/client/versions")
    if [ "$res" == "200" ]; then
        local contacts_count=$(cat "$CONTACTS_FILE" 2>/dev/null | grep -c '=' || echo 0)
        echo "Vox ID: $VOX_ID | Homeserver: $HOMESERVER | Contacts: $contacts_count"
    else
        echo "❌ Backend offline."
        exit 1
    fi
}

cmd_contact() {
    local action="$1"
    if [ "$action" == "add" ]; then
        local name="$2"
        local vid="$3"
        if [ -z "$name" ] || [ -z "$vid" ]; then
            echo "Usage: ./vox contact add <name> <vox_id>" >&2
            exit 1
        fi
        set_config_val "$name" "$vid" "$CONTACTS_FILE"
        echo "✅ Contact added: $name -> $vid"
    elif [ "$action" == "list" ]; then
        cat "$CONTACTS_FILE" 2>/dev/null || echo ""
    elif [ "$action" == "remove" ]; then
        local name="$2"
        if grep -q "^$name\s*=" "$CONTACTS_FILE" 2>/dev/null; then
            sed -i.bak "/^$name\s*=/d" "$CONTACTS_FILE" && rm -f "$CONTACTS_FILE.bak"
            echo "✅ Contact removed: $name"
        else
            echo "❌ Contact not found: $name" >&2
            exit 3
        fi
    else
        echo "Usage: ./vox contact <add|list|remove>" >&2
        exit 1
    fi
}

cmd_send() {
    load_config
    local contact="$1"
    local text="$2"
    local conv_id=""
    
    if [ -z "$contact" ] || [ -z "$text" ]; then
        echo "Usage: ./vox send <contact_or_id> <message> [--conv <id>]" >&2
        exit 1
    fi

    shift 2
    while [[ $# -gt 0 ]]; do
        case $1 in
            --conv) conv_id="$2"; shift 2;;
            *) shift;;
        esac
    done

    if [ -z "$conv_id" ]; then
        conv_id="conv_$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
    fi

    # Lookup contact
    local to_vox_id="$contact"
    local found=$(get_config_val "$contact" "$CONTACTS_FILE")
    if [ -n "$found" ]; then
        to_vox_id="$found"
    fi

    # Ensure format for matrix user search
    local invite_id="$to_vox_id"
    if [[ ! "$invite_id" == *@*:* ]]; then
        invite_id="@${invite_id}:${DOMAIN}"
    fi

    # Check for existing room
    local room_id=$(get_config_val "$to_vox_id" "$ROOMS_FILE")

    if [ -z "$room_id" ]; then
        local create_payload='{"preset":"private_chat", "invite":["'"$invite_id"'"]}'
        local create_res=$(api_call POST "/_matrix/client/v3/createRoom" "$create_payload")
        room_id=$(echo "$create_res" | jq -r '.room_id // empty')
        
        if [ -n "$room_id" ]; then
            set_config_val "$to_vox_id" "$room_id" "$ROOMS_FILE"
        else
            echo "❌ Failed to create room: $(echo "$create_res" | jq -r '.error // empty')" >&2
            exit 1
        fi
    fi

    local txn_id="$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 8)"
    local ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Construct Matrix Event
    local safe_text=$(escape_json "$text")
    local payload=$(cat <<EOF
{
    "msgtype": "m.text",
    "body": "$safe_text",
    "vox": {
        "from": "$VOX_ID",
        "to": "$to_vox_id",
        "timestamp": "$ts",
        "conversation_id": "$conv_id"
    }
}
EOF
)

    local escaped_room_id=$(echo "$room_id" | sed 's/!/%21/g' | sed 's/:/%3A/g')
    local send_res=$(api_call PUT "/_matrix/client/v3/rooms/$escaped_room_id/send/m.room.message/$txn_id" "$payload")
    
    local event_id=$(echo "$send_res" | jq -r '.event_id // empty')
    if [ -n "$event_id" ]; then
        echo "✅ Sent to $contact ($conv_id)"
    else
        echo "❌ Failed to send: $(echo "$send_res" | jq -r '.error // empty')" >&2
        exit 1
    fi
}

cmd_inbox() {
    load_config
    local from_contact=""
    while [[ $# -gt 0 ]]; do
        case $1 in
            --from) from_contact="$2"; shift 2;;
            *) shift;;
        esac
    done

    local sync_token=""
    if [ -f "$VOX_HOME/sync_token" ]; then
        sync_token=$(cat "$VOX_HOME/sync_token")
    fi
    
    local endpoint="/_matrix/client/v3/sync?timeout=0"
    if [ -n "$sync_token" ]; then
        endpoint="$endpoint&since=$sync_token"
    fi

    local sync_res=$(api_call GET "$endpoint" "")
    local has_error=$(echo "$sync_res" | jq -r '.error // empty')
    
    if [ -n "$has_error" ]; then
        echo "[]" 
        exit 0
    fi

    # Auto-join invites
    local invites=$(echo "$sync_res" | jq -r '.rooms.invite | keys[]?' 2>/dev/null)
    for invite in $invites; do
        local enc_invite=$(echo "$invite" | sed 's/!/%21/g' | sed 's/:/%3A/g')
        api_call POST "/_matrix/client/v3/rooms/$enc_invite/join" "{}" >/dev/null
    done

    # Save sync token
    local next_batch=$(echo "$sync_res" | jq -r '.next_batch // empty')
    if [ -n "$next_batch" ]; then
        echo "$next_batch" > "$VOX_HOME/sync_token"
    fi

    # JQ transform to match Python JSON output format identically.
    echo "$sync_res" | jq -c '
        try (
            .rooms.join | to_entries | map(
                .key as $roomId |
                # Extract messages
                (.value.timeline.events | map(select(.type == "m.room.message" and .content.msgtype == "m.text"))) as $msgs |
                select($msgs | length > 0) |
                {
                    conversation_id: (
                        ($msgs | map(select(.content.vox.conversation_id != null)) | first | .content.vox.conversation_id) // 
                        ("conv_" + ($roomId | sub("!"; "") | sub(":"; "_") | .[0:12]))
                    ),
                    with: "unknown",
                    messages: $msgs | map({
                        from: (.content.vox.from // .sender),
                        body: .content.body,
                        timestamp: (.content.vox.timestamp // .origin_server_ts | tostring)
                    })
                }
            )
        ) catch []
    ' | jq '.' || echo "[]"
}

if ! command -v curl &> /dev/null || ! command -v jq &> /dev/null; then
    echo "❌ Error: 'curl' and 'jq' are required command line instruments." >&2
    exit 1
fi

case $1 in
    init) cmd_init "${@:2}";;
    whoami) cmd_whoami;;
    status) cmd_status;;
    contact) cmd_contact "${@:2}";;
    send) cmd_send "${@:2}";;
    inbox) cmd_inbox "${@:2}";;
    *)
        echo "Vox CLI (Bash Version)"
        echo "Usage: ./vox <command>"
        echo "Commands:"
        echo "  init [--username <name>]   Create identity"
        echo "  whoami                     Get current Vox ID"
        echo "  status                     Check connection"
        echo "  contact <add|list|remove>  Manage contacts"
        echo "  send <contact> <msg>       Send a message"
        echo "  inbox [--from <contact>]   Check messages"
        exit 1
        ;;
esac
