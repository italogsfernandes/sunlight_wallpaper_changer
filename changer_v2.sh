#!/bin/bash
cd ~/Pictures/sunlight_wallpaper_changer
echo "Primeira Execução"
`#Baixando`
COUNTER=0 `#Contara ate 60 (60 tentativas)`
while [  $COUNTER -lt 60 ]; do `#Enquanto nao estourou as tentativas`
    echo "Running script:"
	/home/italo/Pictures/sunlight_wallpaper_changer/venv/bin/python3 /home/italo/Pictures/sunlight_wallpaper_changer/py_wallpaper_changer.py
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
			curl --location --request GET 'https://static.die.net/earth/mercator/1600.jpg' \
				--header 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0' \
				--header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
				--header 'Accept-Language: en-US,en;q=0.5' \
				--header 'Accept-Encoding: gzip, deflate, br' \
				--header 'DNT: 1' \
				--header 'Connection: keep-alive' \
				--header 'Cookie: cf_chl_2=202ac6426f94865; cf_clearance=mSDBuI9T.nqjUYVzQecmokzGmTqv.6_PXMsutzds6rQ-1671093277-0-150; u=0ZfsEmOa3B40aw19Axu5Ag==' \
				--header 'Upgrade-Insecure-Requests: 1' \
				--header 'Sec-Fetch-Dest: document' \
				--header 'Sec-Fetch-Mode: navigate' \
				--header 'Sec-Fetch-Site: cross-site' \
				--header 'Sec-GPC: 1' \
				--header 'Pragma: no-cache' \
				--header 'Cache-Control: no-cache' > /home/italo/Pictures/sunlight_wallpaper_changer/world.jpg
			temp=$(stat -c%s world.jpg) `#Verifica o tamanho`
			if [[ $temp > 1000 ]] ; then `#Se o tamanho esta ok, troca o arquivo world_sunlight`
			    echo "Moving world.jpg to Walpapers folder."
			    #mv world.jpg ~/Pictures/sunlight_wallpaper_changer/world.jpg 
			    echo "Running /home/italo/Pictures/sunlight_wallpaper_changer/venv/bin/python3 script:"
				/home/italo/Pictures/sunlight_wallpaper_changer/venv/bin/python3 ~/Pictures/sunlight_wallpaper_changer/pin_locator.py
				echo "Removing unused images (world.jpg, world_pinned.jpg)."
				#rm ~/Pictures/sunlight_wallpaper_changer/world.jpg				
				#rm ~/Pictures/sunlight_wallpaper_changer/world_pinned.jpg
				echo "Removing old wallpaper."
				#rm ~/Pictures/sunlight_wallpaper_changer/world_sunlight_Wallpaper.jpg 
				echo "Setting world_time as new wallpaper"
				#mv ~/Pictures/sunlight_wallpaper_changer/world_time.jpg ~/Pictures/sunlight_wallpaper_changer/world_sunlight_Wallpaper.jpg
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

