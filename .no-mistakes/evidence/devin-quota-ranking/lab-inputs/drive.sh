#!/usr/bin/env bash
# drive.sh <title> <rules-json-file> <snapshot-name|-> : run the real resolver in the lab home and append a transcript.
set -u
LAB=$1; WT=$2; TR=$3; title=$4; rules=$5; snap=$6
cp "$rules" "$LAB/config/crew-dispatch.json"
PORT=$(cat "$LAB/port")
{
  printf '\n==================== %s ====================\n' "$title"
  printf '$ cat $FM_HOME/config/crew-dispatch.json\n'; jq -c . "$LAB/config/crew-dispatch.json"
  if [ "$snap" != - ]; then
    printf '$ QUOTA_AXI_SNAPSHOT=%s quota-axi --json   # devin row as the resolver sees it\n' "snap-$snap.json"
    XDG_CACHE_HOME="$LAB/cache" XDG_CONFIG_HOME="$LAB/xdgconfig" QUOTA_AXI_SNAPSHOT="$LAB/snap-$snap.json" quota-axi --json \
      | jq -c '.providers[] | select(.provider=="devin") | {provider, credits, effectiveAvailability: [.quotaSemantics.effectiveAvailability[] | {scope, effectivePercentRemaining, runway: .runway.status, spendPriority: .selection.spendPriority}]}'
  fi
  printf '$ FM_HOME=$LAB FM_DISPATCH_PROVIDER=systemone FM_DISPATCH_BASE_URL=http://127.0.0.1:$PORT bin/fm-dispatch-resolve.sh brief.md\n'
} >> "$TR"
cd "$WT"
out=$(env -u NO_MISTAKES_GATE -u FM_GATE_REFUSE_BYPASS -u FM_ROOT_OVERRIDE -u FM_STATE_OVERRIDE -u FM_DATA_OVERRIDE \
  -u FM_CONFIG_OVERRIDE -u FM_PROJECTS_OVERRIDE -u TYPESAFE_API_KEY -u OPENROUTER_API_KEY -u OPENAI_API_KEY -u FM_DISPATCH_API_KEY \
  -u QUOTA_AXI_MAX_AGE \
  FM_HOME="$LAB" FM_DISPATCH_PROVIDER=systemone FM_DISPATCH_MODEL=jev-lab FM_DISPATCH_BASE_URL="http://127.0.0.1:$PORT" \
  XDG_CACHE_HOME="$LAB/cache" XDG_CONFIG_HOME="$LAB/xdgconfig" \
  ${snap:+QUOTA_AXI_SNAPSHOT="$LAB/snap-$snap.json"} \
  bin/fm-dispatch-resolve.sh "$LAB/brief.md" 2>&1); code=$?
printf '%s\n[exit %s]\n' "$out" "$code" >> "$TR"
printf '%s\n[exit %s]\n' "$out" "$code"
