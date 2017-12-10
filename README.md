# INFO-F-405---Project-Cryptocurrencies.-Encore-

Lancer Le projet : 

- Ouvrir terminal dans master :
Il faut préciser l'ip et le port 
ex : python master.py localhost 12800 

- Ouvrir terminal dans relay :
Il faut préciser l'ip et le port du master et un port pour son serveur
ex : python relay.py localhost 12800 8888

- Ouvrir terminal dans miner :
Il faut préciser l'ip et le port du relay
ex : python miner.py localhost 8888 

- Ouvrir terminal dans wallet :
Créer un wallet avec la ligne
python new_key.py username password

- Ouvrir terminal dans wallet :
Il faut préciser l'ip et le port du relay
ex : python wallet.py localhost 8888 username password



On peut faire un fichier de config pour le port etc. mais j'ai eu la flemme

Pour l'instant le programme permet d'ecrire dans wallet
Le message du wallet se déplace comme ça : (+ ou - le chemin final normalement)
wallet -> relay -> miner -> relay -> master -> relay -> wallet
