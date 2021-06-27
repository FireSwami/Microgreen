#!/bin/bash

eval $(docker-machine env core)

docker build -t hub.ferumflex.com/ferumflex/microgreen:prod . && docker push hub.ferumflex.com/ferumflex/microgreen:prod

now=$(date +"%Y/%m/%d")
base="Prod/$now"
tag="$base"
count=1

while true
do
  if git show-ref -q --verify "refs/tags/$tag" 2>/dev/null; then
    count=$((count+1))
    tag="${base}_${count}"
  else
    break
  fi
done

git tag -a "$tag" -m "Prod $now"

git push origin main
git push origin "$tag"

docker stack deploy -c docker-swarm.yml microgreen --with-registry-auth --prune
