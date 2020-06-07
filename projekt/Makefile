all: main

main: main.py
	echo "#!/bin/bash" > ./main
	echo "python3 main.py" > ./main
	chmod +x ./main

clean:
	rm main