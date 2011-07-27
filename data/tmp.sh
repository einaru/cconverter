#!/bin/bash

actions=('exec' 'run' 'exit' 'clear_left' 'help_contents' 'help_about')
apps=('kcalc')

source=/mnt/nervanna/pictures/icons/oxygen
target=/mnt/debris/devel/repo/git/cconverter/data/icons/hicolor

for size in 16 22 24 32 48
do
	echo 'png actions'
	for icon in "${actions[@]}"
	do
		mkdir -p ${target}/${size}x${size}/actions
		cp ${source}/${size}x${size}/actions/${icon}.png \
		   ${target}/${size}x${size}/actions/${icon}.png
	done

	echo 'png apps'
	for icon in "${apps[@]}"
	do
		mkdir -p ${target}/${size}x${size}/apps
		cp ${source}/${size}x${size}/apps/${icon}.png \
		   ${target}/${size}x${size}/apps/${icon}.png
	done
done

echo 'scalable actions'
for icon in "${actions[@]}";
do
	mkdir -p ${target}/scalable/actions
	cp ${source}/scalable/actions/${icon}.svg \
	   ${target}/scalable/actions/${icon}.svg
done

echo 'scalable apps'
for icon in "${apps[@]}";
do
	mkdir -p ${target}/scalable/apps
	cp ${source}/scalable/apps/${icon}.svg \
	   ${target}/scalable/apps/${icon}.svg
done
