#!/bin/bash

# Function to read excluded branches from the user
read_excluded_branches() {
  echo "Enter branches to exclude (space-separated), then press Enter:"
  read -a EXCLUDED_BRANCHES
}

# Read excluded branches interactively
read_excluded_branches

# Fetch all branches from the origin
git fetch origin

# List all branches and loop through them
for branch in $(git branch -r | grep -v '\->' | grep 'origin/' | sed 's/origin\///'); do
  # Check if the branch is in the excluded list
  if [[ ! " ${EXCLUDED_BRANCHES[@]} " =~ " ${branch} " ]]; then
    # Push the branch to the new remote
    echo "Pushing branch: $branch"
    git push new-origin origin/$branch:refs/heads/$branch
  else
    echo "Excluding branch: $branch"
  fi
done