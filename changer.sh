#!/bin/bash
cd ~/Images/Wallpapers
echo "Primeira Execução"
`#Baixando`
COUNTER=0 `#Contara ate 60 (60 tentativas)`
while [  $COUNTER -lt 60 ]; do `#Enquanto nao estourou as tentativas`
	`#Baixa o novo papel de parede`
	wget http://www.opentopia.com/images/cams/world_sunlight_map_rectangular.jpg -O world.jpg -nv
	temp=$(stat -c%s world.jpg) `#Verifica o tamanho`
	if [[ $temp > 1000 ]] ; then `#Se o tamanho esta ok, troca o arquivo world_sunlight`
	    echo "Moving world.jpg to Walpapers folder."
	    #mv world.jpg ~/Images/Wallpapers/world.jpg 
	    echo "Running python script:"
		python ~/Images/Wallpapers/pin_locator.py
		echo "Removing unused images (world.jpg, world_pinned.jpg)."
		rm ~/Images/Wallpapers/world.jpg				
		rm ~/Images/Wallpapers/world_pinned.jpg
		echo "Removing old wallpaper."
		rm ~/Images/Wallpapers/world_sunlight_Wallpaper.jpg 
		echo "Setting world_time as new wallpaper"
		mv ~/Images/Wallpapers/world_time.jpg ~/Images/Wallpapers/world_sunlight_Wallpaper.jpg
		break
	fi
	sleep 5
	let COUNTER=COUNTER+1 
done
`#Final da tarefa de baixar`

while [  1 ]; do
	actual_min=$(date +%M)
	echo $(date)
	
	if [[ $actual_min > 5 && $actual_min < 15 ]] ; then
		echo "Sincronizado"
		`#Baixando`
		COUNTER=0 `#Contara ate 60 (60 tentativas)`
		while [  $COUNTER -lt 60 ]; do `#Enquanto nao estourou as tentativas`
			`#Baixa o novo papel de parede`
			wget http://www.opentopia.com/images/cams/world_sunlight_map_rectangular.jpg -O world.jpg 
			temp=$(stat -c%s world.jpg) `#Verifica o tamanho`
			if [[ $temp > 1000 ]] ; then `#Se o tamanho esta ok, troca o arquivo world_sunlight`
			    echo "Moving world.jpg to Walpapers folder."
			    #mv world.jpg ~/Images/Wallpapers/world.jpg 
			    echo "Running python script:"
				python ~/Images/Wallpapers/pin_locator.py
				echo "Removing unused images (world.jpg, world_pinned.jpg)."
				rm ~/Images/Wallpapers/world.jpg				
				rm ~/Images/Wallpapers/world_pinned.jpg
				echo "Removing old wallpaper."
				rm ~/Images/Wallpapers/world_sunlight_Wallpaper.jpg 
				echo "Setting world_time as new wallpaper"
				mv ~/Images/Wallpapers/world_time.jpg ~/Images/Wallpapers/world_sunlight_Wallpaper.jpg
				break
			fi
			sleep 5
			let COUNTER=COUNTER+1 
		done
		`#Final da tarefa de baixar`
		if [[ $actual_min < 10 ]] ; then `#Espera um tempo ate a proxima tarefa`
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

