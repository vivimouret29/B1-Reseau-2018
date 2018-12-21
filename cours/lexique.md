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

### *MAC* : Media Access Control
* on parle l'ici de *l'adresse MAC* ou *adresse physique*
* elle est *obligatoirement* portée par une *carte réseau*
* sur une carte physique, elle est gravée sur la carte (on ne peut pas la changer)
* l'*adresse MAC* est composée de 12 caractères hexadécimaux (par exemple `D4-6D-7D-00-15-3F`)

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
* [le cours est plus complete à ce sujet](./2.md#notion-de-ports)
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

### `nc` ou `netcat`

### `netstat` ou `ss`

### `nslookup` ou `dig`
