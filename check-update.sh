#!/bin/sh
# Too many projects with different version schemes in the same repo
git ls-remote --tags https://github.com/SELinuxProject/selinux 2>/dev/null|awk '{ print $2; }' |sed -e 's,refs/tags/,,;s,_,.,g' |grep '^libselinux-' |sed -e 's,^libselinux-,,' |grep -v -- '-rc' |sort -V |tail -n1
