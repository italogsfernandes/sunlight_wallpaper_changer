#!/bin/bash
cd ~/Pictures/Wallpapers
echo "Primeira Execucao"
`#Baixando`
COUNTER=0 `#Contara ate 60 (60 tentativas)`
while [  $COUNTER -lt 60 ]; do `#Enquanto nao estourou as tentativas`
	`#Baixa o novo papel de parede`
	wget http://www.opentopia.com/images/cams/world_sunlight_map_rectangular.jpg -O world.jpg 
	temp=$(stat -c%s world.jpg) `#Verifica o tamanho`
	if [[ $temp > 1000 ]] ; then `#Se o tamanho esta ok, troca o arquivo world_sunlight`
		rm /home/mario/Images/Wallpapers/world_sunlight_Wallpaper.jpg 
		mv world.jpg /home/mario/Images/Wallpapers/world_sunlight_Wallpaper.jpg
		break
	fi
	sleep 5
	let COUNTER=COUNTER+1 
done
`#Final da tarefa de baixar`

while [  1 ]; do
	actual_min=$(date +%M)
	echo $(date)
	
	if [[ $actual_min > 10 && $actual_min < 21 ]] ; then
		echo "Sincronizado"
		`#Baixando`
		COUNTER=0 `#Contara ate 60 (60 tentativas)`
		while [  $COUNTER -lt 60 ]; do `#Enquanto nao estourou as tentativas`
			`#Baixa o novo papel de parede`
			wget http://www.opentopia.com/images/cams/world_sunlight_map_rectangular.jpg -O world.jpg 
			temp=$(stat -c%s world.jpg) `#Verifica o tamanho`
			if [[ $temp > 1000 ]] ; then `#Se o tamanho esta ok, troca o arquivo world_sunlight`
				rm /home/mario/Images/Wallpapers/world_sunlight_Wallpaper.jpg 
				mv world.jpg /home/mario/Images/Wallpapers/world_sunlight_Wallpaper.jpg
				break
			fi
			sleep 5
			let COUNTER=COUNTER+1 
		done
		`#Final da tarefa de baixar`
		if [[ $actual_min < 15 ]] ; then `#Espera um tempo ate a proxima tarefa`
			echo "Waiting 61:40 Minutes..."
			sleep 3700
		else
			echo "Waiting 58:40 Minutes..."
			sleep 3500
		fi
	else
		echo "Ainda nao sincronizado..."
		sleep 600
	fi
done

