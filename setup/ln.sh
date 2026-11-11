#!/usr/bin/env bash
set -euo pipefail

basedir="${1:?Usage: $0 <basedir>}"

mkdir -p "$HOME/.local"

bin_links=(
    "bin_py:bin_py"
    "bin:bin_share"
)

for bin_link in "${bin_links[@]}"; do
    source_name="${bin_link%%:*}"
    destination_name="${bin_link#*:}"
    source_dir="$basedir/personal/lile-riraku.share/$source_name"
    destination="$HOME/.local/$destination_name"

    if [[ ! -d "$source_dir" ]]; then
        echo "Source directory does not exist: $source_dir" >&2
        exit 1
    fi
    if [[ -e "$destination" && ! -L "$destination" ]]; then
        echo "Destination exists and is not a symbolic link: $destination" >&2
        exit 1
    fi

    ln -sfn "$source_dir" "$destination"
    "../bin/make-all-files-executable" "$source_dir"
done
