# Lexique

* [Sigles et Acronymes](#siglesacronymes)
* [Notions](#notions)
* [Commandes](#commandes)

## Sigles/Acronymes

### *CIDR* : Classless Inter-Domain Routing
* de façon simple, c'est le `/24` dans `192.168.1.1/24` par exemple
* un `/24` veut dire "24 bits à 1" et correspond donc au masque `11111111.11111111.11111111.00000000` soit `255.255.255.0`

### *HTTP* : HyperText Transfer Protocol
* protocole utilisé pour discuter avec des serveurs web

### *IP* : Internet Protocol
* protocole utilisé pour discuter à travers des réseaux
* une *adresse IP* peut être "portée" par une *carte réseau*

### *LAN* : Local Area Network
* réseau local

### *MAC* : Media Access Control
* on parle l'ici de *l'adresse MAC* ou *adresse physique*
* elle est *obligatoirement* portée par une *carte réseau*
* sur une carte physique, elle est gravée sur la carte (on ne peut pas la changer)
* l'*adresse MAC* est composée de 12 caractères hexadécimaux (par exemple `D4-6D-7D-00-15-3F`)

### *RFC* : Request For Comments
* document texte qui définit une notion, un concept, un protocole (principalement utilisés en informatique)
* les RFCs peuvent écrit par n'importe qui et sont des documents publics
* comme sont l'indique, une RFC a pour but d'être lue et commentée
* si les gens la lisent, la commentent, la complètent, une RFC finit par contenir des choses intéressantes
* les protocoles que vous connaissez ont tous été définis dans des RFCs :
  * IP [RFC 791](https://tools.ietf.org/html/rfc791)
  * Allocation d'adresses privées [RFC 1918](https://tools.ietf.org/html/rfc1918)
  * HTTP [RFC 2616](https://tools.ietf.org/html/rfc2616)
  * TCP [RFC 793](https://tools.ietf.org/html/rfc793)
  * etc.
  
### *TCP* : Transmission Control Protocol

* permet d'établir un tunnel entre deux personnes, généralement un client et un serveur
* une fois le tunnel établi, le client et le serveur peuvent échanger des données
* voyez TCP comme un échange de messages (comme des textos) **avec accusé de réception**
* **on utilise TCP lorsqu'on veut une connexion stable, même si elle est un peu plus lente**
* une connexion HTTP utilise un tunnel TCP par exemple

### *UDP* : User Datagram Protocol

* permet d'échanger des données, générélament entre un client et un serveur
* aucun tunnel n'est établi, les données sont envoyées **sans accusé de réception**
* **on utilise UDP lorsqu'on s'en fiche de perdre certains messages sur la route, afin d'optimiser la vitesse de transport**
* UDP est par exemple très utilisé dans les jeux en ligne (typiquement pour des FPS en ligne)

### *WAN* : Wide Area Network
* réseau étendu
* celui que vous utilisez le plus est Internet

## Notions

### Adresse de réseau
* adresse qui définit un réseau
* elle ne peut pas être utilisée comme adresse d'un hôte
* elle correspond à la première adresse disponible d'un réseau
* exemple :
  * pour l'adresse IP `192.168.1.37/24`, l'adresse de réseau est `192.168.1.0/24`

### Adresse de diffusion ou *broadcast address*
* dernière adresse d'un réseau
* est utilisée pour envoyer un message à tous les hôtes d'un réseau
* elle ne peut pas être utilisée comme adresse d'un hôte
* **l'adresse de broadcast n'est portée par aucune machine**, c'est une adresse réservée dans tous les LANs du monde :)
* exemple :
  * pour l'adresse IP `192.168.1.37/24`, l'adresse de broadcast est `192.168.1.255/24`

### Binaire
* c'est la base 2 des mathématiques
* nous sommes habitués à compter en base 10
* n'importe quelle base est possible, certaines sont beaucoup utilisées en informatique
  * binaire (base 2)
  * décimal (base 10)
  * octal (base 8)
  * héxadécimal (base 16)
  * base 64 (oui oui, base 64)
  * pour les curieux : en fait l'ASCII normal (pas la table étendue), c'est juste une base 128 hein :)
* le cours 1 contient [un passage avec des calculs binaires](./1.md#3-exemple-de-manipulation-dip-vue-en-cours)
 
### Carte réseau (ou interface réseau)
* carte physique dans une machine (ou virtuelle, on verra ça plus tard)
* porte forcément une adresse MAC
* peut porter une adresse IP et ainsi "être dans un réseau"
* dans nos PCs du quotidien, on en a au moins une : la carte WiFi

### Loopback
* quand on parle de Loopback on parle d'une interface réseau
* il existe au moins une Loopback sur tous les équipements
  * sur vos PCs elle porte l'IP `127.0.0.1`
  * parfois elle est gérée différemment par rapport aux autres interfaces (vous ne la voyez pas sur Windows avec un `ipconfig`)
* **une interface de loopback permet uniquement de se joindre soi-même**
  * en fait c'est juste qu'elle porte une IP dans un `/32`, un masque un peu particulier, utilisé à cet effet :)
* go test un `ping 127.0.0.1` vous aurez jamais vu un `ping` si rapide. Normal : vous pingez votre propre machine, sans passer par le réseau

### Masque de sous-réseau
* permet d'extraire l'[adresse de réseau](#adresse-de-réseau) d'une adresse IP
* se présente sous sa forme classique `255.255.255.0` ou en notation [CIDR](#cidr--classless-inter-domain-routing) `/24`
* **les trois affirmations suivantes sont parfaitement équivalentes :**
  * "j'ai un réseau en `255.255.255.0`"
  * "j'ai un `/24`"
  * "j'ai un réseau avec 256 adresses possibles"

### Passerelle ou *Gateway*
* la *passerelle* est un noeud agissant comme pivot, et elle permet de sortir du réseau (de chez vous vers Internet par exemple)
* il existe des réseaux sans passerelle
* la passerelle possède souvent l'IP juste avant la *broadcast*, mais pas toujours (ce n'est pas le cas à Ingésup par exemple)
* **la passerelle est une machine. L'adresse IP de gateway est donc l'adresse IP d'une machine présente sur le même réseau que nous,  contrairement à l'adresse de broadcast** c'est une adresse IP réelle, et elle est portée par un équipement.
* **un réseau qui ne souhaite pas être connecté à d'autres réseaux ne possède pas de passerelle**

### Ports
* [le cours est plus complet à ce sujet](./2.md#notion-de-ports)
* un serveur est une machine qui "écoute" sur un port
  * un client est une machine qui se connecte à un port où un serveur écoute
* un port est un point d'entrée unique **sur une interface réseau**
  * donc si on a deux interfaces réseau, on a deux ports 443 (entre autres) : un sur chaque interface
* on peut demander à des applications "d'écouter" sur un ou plusieurs ports
* par exemple, pour un site web, on demande souvent au serveur Web d'écouter sur le port 443 pour HTTPS

### Subnetting
* c'est le fait de découper un réseau en plusieurs sous-réseaux
* par exemple, un `/24` contient deux `/25`
  * `192.168.1.0/24` est la réunion de `192.168.1.0/25` et `192.168.1.128/25`
* il existe des tonnes d'outils permettant d'assister le subnetting en évitant de devenir fou avec le binaire, comme [celui-ci](http://www.davidc.net/sites/default/subnets/subnets.html)

## Commandes

### `ipconfig` ou `ifconfig` ou `ip a`
* affiche des informations sur les carte réseau
```
# Windows
ipconfig 
ipconfig /all

# GNU/Linux ou MacOS
ifconfig
ip a
```

### `ping`
* message très simple qui fait un aller-retour sur le réseau
* on l'utilise souvent pour tester la présence de quelqu'un sur le réseau
* la valeur en millisecondes est le temps de l'aller-retour
* utilisation : `ping IP` où `IP` est l'adresse IP d'un hôte sur le réseau
* test d'accès internet
  * souvent, pour tester l'accès d'une machine à internet on fait `ping 8.8.8.8`
  * `8.8.8.8` est une adresse simple  mémoriser et correspond en réalité à un serveur de Google
  * `1.1.1.1` peut aussi être utilisé de la même façon, c'est un serveur de CloudFlare
  
### `nmap`
* outil de scan réseau
* permet de récupérer des informations sur un réseau et les machines qui y sont connectées
* beaucoup de scans sont possibles
  * le plus simple, le scan de ping envoie simplement un `ping` à toutes les IPs d'un réseau
  * exemple de scan de ping : `nmap -sP 192.168.1.0/24`

### `nc` ou `netcat`
* outil permettant de simples connexions [TCP](#TCP) ou [UDP](#UDP)
* on a effectué des simples connexions entre vos PCs en cours
* mais on peut aussi s'en servir pour se connecter à un serveur web, aucun problème
  * faut savoir parler l'HTTP par contre ehe

### `netstat` ou `ss`
* outils permettant de lister les connexions actives d'une machine
  * entre autres, une par site web que l'on visite par exemple
* options communes de `ss`
  * `-l` pour les ports en écoute (`-l` comme *listen*)
  * `-t` pour les ports TCP
  * `-u` pour les ports UDP
  * `-4` pour les connexions IPv4
  * `-n` pour ne pas transformer le numéro de ports en nom de service
  * `-p` pour voir l'application (le processus) qui est attaché à un port

### `nslookup` ou `dig`
* outils permettant d'effectuer des opérations liées au protocole DNS
* un "lookup DNS" consiste à demander quelle est l'IP d'un nom donné
  * "à quelle IP se trouve le serveur www.google.com ?" par exemple
* un "reverse lookup DNS" c'est l'inverse : on cherche à connaître à quel nom est associée une IP
  * "y'a-t-il des noms associés à 76.32.43.32 ?" par exemple

### `curl` et `wget`
* permettent de faire des requêtes HTTP
* tout ce que fait `wget`, `curl` sait le faire. La réciproque n'est pas vraie.
* `wget` c'est l'outil simple mais peu puissant et très peu flexible
* `curl`, c'est l'inverse
* souvent, pour imiter un simple `wget`, vous pouvez faire `curl -SLO`
* exemple : 
  * `curl -L www.google.com` permet de récupérer le contenu du serveur web de  `www.google.com`
