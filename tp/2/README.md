# B1 Réseau 2018 - TP2

# Notions vues avant le TP

* Manipulations IP et masque (avec le [binaire](../../cours/lexique.md#binaire))
* Être capable de répondre à des questions comme :
  * combien d'adresses dispo dans un réseau donné ? 
  * première et dernière adresse d'un réseau donné ?
  * j'ai un `/24`, je peux faire combien de `/26` ?
  * j'ai X PCs, X imprimantes, X serveurs qui ont besoin d'adresses IP, et un `/24` à ma disposition, comment je le coupe ?
  * est-ce que `192.168.1.24/24` et `192.168.1.23/24` sont dans le même réseau ? 
  
* Firewall (bref)

* Ligne de commande (bref, navigation de dossier)

# TP 2 - Exploration du *réseau* d'un point de vue *client*

Le *réseau* désigne ici toutes fonctionnalités d'un PC permettant de se connecter à d'autres machines.  

De façon simplifiée, on appelle *stack TCP/IP* ou *pile TCP/IP* l'ensemble de logiciels qui permettent d'utiliser et configurer des [cartes réseau](../../cours/lexique.md#carte-r%C3%A9seau-ou-interface-r%C3%A9seau) avec des adresses IP. C'est juste gros mot savant pour désigner tout ce qui touche de près ou de loin au réseau dans une machine okay ? :)

Lorsque l'on parle de réseau, on désigne souvent par *client* tout équipement qui porte une adresse IP. 

Donc vos PCs sont des *clients*, et on va explorer leur *réseau*, c'est à dire, leur *pile TCP/IP*.

# Sommaire

* [Déroulement et rendu du TP](#déroulement-et-rendu-du-tp)
* [Hints pour les TPs en réseau avec moi :)](#hints-généréaux)
* [I. Exploration de la pile TCP/IP (individuel)](#i-exploration-locale-en-solo)
  * [Affichage d'infos](#1-affichage-dinformations-sur-la-pile-tcpip-locale)
  * [Modification d'adresse IP](#2-modifications-des-informations)
    * [Partie 1](#modification-dadresse-ip---pt-1)
    * [Scanner des réseaux avec `nmap`](#nmap)
    * [Partie 2](#modification-dadresse-ip---pt-2)
* [II. Exploration de la pile TCP/IP (par deux)](#ii-exploration-locale-en-duo)
  * [Créer un réseau avec un câble ethernet](#3--création-du-réseau)
  * [Donner Internet à travers un câble](#4-utilisation-dun-des-deux-comme-gateway)
  * [Messagerie instantanée simpliste avec `nc`](#5-petit-chat-privé-)
  * [Analyser le réseau avec `wireshark`](#6-wireshark)
  * [Manipulation basique de pare-feu](#7-firewall)
* [III. Autres outils/protocoles élémentaires côté client](#iii-manipulations-dautres-outilsprotocoles-côté-client)
  * [DHCP](#1-DHCP)
  * [DNS](#2-DNS)
  * [Bonus](#3-bonus--aller-plus-loin)
* **[Bilan](#bilan)**

# Déroulement et rendu du TP

* Groupe de 2 jusqu'à 4 personnes. Il faut au moins deux PCs avec une prise RJ45 (Ethernet) par groupe
* Un câble RJ45 (fourni) pour connecter les deux PCs
* Un compte-rendu par personne
  * vu que vous travaillez en groupe, aucun problème pour copier/coller les parties à faire à plusieurs (tout le [`II.`](#ii-exploration-locale-en-duo))
  * une bonne partie est à faire de façon individuelle malgré tout (tout le [`I.`](#i-exploration-locale-en-solo) et le [`III.`](#iii-manipulations-dautres-outilsprotocoles-côté-client))
  * on prendra le temps, mais le travail devra être rendu à travers Github ou tout autre plateforme supportant le `md` (markdown)
* Le rendu doit : 
  * comporter des réponses aux questions explicites
  * comporter la marche à suivre pour réaliser les outils utilisés :
    * en ligne de commande, screenshots ou copier/coller
    * en interface graphique, screenshots ou nom des menus où cliquer (sinon ça peut vite faire 1000 screenshots)
  * par exemple, pour la partie `1.A.` je veux le nom de la commande tapée
  * vous pouvez vous inspirer de [ce rendu](https://gist.github.com/sellan/0c24b10541f034be206f51578bc73eed) effectué par un élève de B2 pour un cours de Linux
  * de façon générale, tout ce que vous faites et qui fait partie du TP, vous me le mettez :)

# Hints généréaux

* **faites vos recherches internet en anglais**, les résultats seront plus nombreux et plus pertinents
* dans le TP, **lisez en entier une partie avant de commencer à la réaliser.** Ca donne du sens et aide à la compréhension
* **allez à votre rythme.** Le but n'est pas de finir le TP, mais plutôt de bien saisir et correctement appréhender les différentes notions
* **n'hésitez pas à me demander de l'aide régulièrement** mais essayez toujours de chercher un peu par vous-mêmes avant :)
* pour moult raisons, il sera préférable pendant les cours de réseau de **désactiver votre firewall**. Vous comprendrez ces raisons au fur et à mesure du déroulement du cours très justement. N'oubliez pas de le réactiver après coup.

# I. Exploration locale en solo

## 1. Affichage d'informations sur la pile TCP/IP locale

### En ligne de commande

En utilisant la ligne de commande (CLI) de votre OS : 

**Affichez les infos des cartes réseau de votre PC**
  * nom, [adresse MAC](../../cours/lexique.md#mac--media-access-control) et adresse IP de l'interface WiFi
  * nom, [adresse MAC](../../cours/lexique.md#mac--media-access-control) et adresse IP de l'interface Ethernet
  * déterminer, pour chacune d'entre elles :
    * [adresse de réseau](../../cours/lexique.md#adresse-de-r%C3%A9seau)
    * [adresse de broadcast](../../cours/lexique.md#adresse-de-diffusion-ou-broadcast-address)
 
**Affichez votre gateway**
  * trouvez sur internet une commande pour connaître l'adresse IP de la [passerelle](../../cours/lexique.md#passerelle-ou-gateway) de votre carte WiFi
  
### En graphique (GUI : Graphical User Interface)

En utilisant l'interface graphique de votre OS :  

**Trouvez comment afficher les informations sur une carte IP (change selon l'OS)**
  * là aussi, cherchez sur internet
  * trouvez l'IP, la MAC et la [gateway](../../cours/lexique.md#passerelle-ou-gateway) pour l'interface WiFi de votre PC

### Questions

* à quoi sert la [gateway](../../cours/lexique.md#passerelle-ou-gateway) dans le réseau d'Ingésup ?

## 2. Modifications des informations

### A. Modification d'adresse IP - pt. 1  

Utilisez l'interface graphique de vorte OS pour **changer d'adresse IP** :
  * [calculez la première et la dernière IP **disponibles** du réseau](../../cours/1.md#3-exemple-de-manipulation-dip-vue-en-cours) (pour rappel, l'*adresse de réseau* et l'*adresse broadcast* ne sont pas "disponibles")
  * changez l'adresse IP de votre carte WiFi pour une autre (mais toujours dans le même réseau)

* **NOTE :** si vous utilisez la même IP que quelqu'un d'autre, il se passerait la même chose qu'en vrai avec des adresses postales :
  * deux personnes habitent au même numéro dans la même rue, mais dans deux maisons différentes
  * quand une des personnes envoie un message, aucun problème, l'adresse du destinataire est unique, la lettre sera reçue
  * par contre, pour envoyer un message à l'une de ces deux personnes, le facteur sera dans l'impossibilité de savoir dans quelle boîte aux lettres il doit poser le message
  * ça marche à l'aller, mais pas au retour
  
* ça serait bien un outil pour scanner le réseau à un instant T afin de choisir une adresse IP libre, non ? 

### B. `nmap`

`nmap` est un outil de scan réseau. On peut faire des tas de choses avec, on va se cantonner à des choses basiques pour le moment.  
Les commandes `nmap` se présentent comme : `nmap OPTIONS CIBLE`
  * `nmap` est le nom de la commande
  * les `OPTIONS` se précisent avec le caractère `-` comme pour beaucoup de commandes
    * exemple : `nmap -sP` (`sP` c'est un Ping Scan, on y reviendra)
  * la cible est soit une adresse de réseau (on cible tous les hôtes du réseau), soit un hôte simple 
    * hôte simple : `nmap -sP 192.168.1.35`
    * [réseau](../../cours/lexique.md#adresse-de-r%C3%A9seau) : `nmap -sP 192.168.1.0/24` (notation *CIDR*)

* utilisation 
  * téléchargez `nmap` en suivant les instructions du [site officiel](https://nmap.org/book/install.html) pour votre OS
  * que vous l'utilisiez en GUI ou en CLI, vous pouvez utiliser des commandes `nmap`
  
**Utilisez `nmap` pour scanner le réseau de votre carte WiFi et trouver une adresse IP libre**

* exemple de commande pour le réseau Ingésup  `nmap -sn -PE <ADRESSE_DU_RESEAU_CIBLE>` pour trouvez les hôtes actuellements sur le réseau

* trouver le "nom" associés aux adresses IP : `nmap -sL <ADRESSE_DU_RESEAU_CIBLE>` (non-fonctionnel à ingésup, c'est juste pour votre culture :) )
    * attention ! Les hôtes retournés par cette commande peuvent être actuellement déconnectés du réseau
    * on reviendra sur le fonctionnement de ça plus tard :)
    
* `nmap` est un outil de scan de réseau très puissant, on en reparlera !

* suivant ce que vous faites avec `nmap` il y a moyen que ce soit bien le foutoir sur le réseau Ingésup, un peu plus tard dans le TP il y aura une partie pour observer un peu tout ce qui passe.

### C. Modification d'adresse IP - pt. 2

* Modifiez de nouveau votre adresse IP vers une adresse IP que vous savez libre grâce à `nmap`
* Modifiez votre adresse de gateway et essayez d'aller sur un site internet

* **NOTE** : si vous aviez déjà une adresse IP, c'est à cause d'un truc qu'on appelle le *DHCP* on y reviendra aussi !

# II. Exploration locale en duo

Owkay. Vous savez à ce stade : 
* afficher les informations IP de votre machine
* modifier les informations IP de votre machine
* c'est un premier pas vers la maîtrise de votre outil de travail ! 

On va maintenant répéter un peu ces opérations, mais en créant un réseau local de toutes pièces : entre deux PCs connectés avec un câble RJ45. 

## 1. Prérequis

* deux PCs avec ports RJ45
* un câble RJ45
* **firewalls désactivés** sur les deux PCs

## 2. Câblage

Ok c'est la partie tendue. Prenez un câble. Branchez-le des deux côtés. Hop.

## 3 ? Création du réseau

Cette étape peut paraître cruciale. En réalité, elle n'existe pas à proprement parlé. On ne peut pas "créer" un réseau. Si une machine possède une carte réseau, et si cette carte réseau porte une adresse IP, alors cette adresse IP se trouve dans un réseau (l'adresse de réseau). Ainsi, le réseau existe. De fait.  

Donc il suffit juste de définir une adresse IP sur une carte réseau pour que le réseau existe ! Hop.

## 3. Modification d'adresse IP

Si vos PCs ont un port RJ45 alors y'a une carte Ethernet associée : 
* modifiez l'IP des deux machines pour qu'elles soient dans le même réseau
* vérifiez à l'aide de commandes que vos changements ont pris effet
* utilisez `ping` pour tester la connectivité entre les deux machines
* testez avec un `/20`, puis un `/24`, puis le plus petit réseau que vous trouvez. 
  * inventez un nouveau réseau ! Comme `172.16.18.0/24` par exemple ! 

## 4. Utilisation d'un des deux comme gateway 

Ca, ça peut toujours dépann. Comme pour donner internet à une tour sans WiFi quand y'a un PC portable à côté, par exemple. 

L'idée est la suivante : 
* vos PCs ont deux cartes avec des adresses IP actuellement
  * la carte WiFi, elle permet notamment d'aller sur internet, grâce au réseau ingésup
  * la carte Ethernet, qui permet actuellement de joindre votre coéquipier, grâce au réseau que vous avez créé :)
* si on fait un tit schéma tout moche, ça donne ça : 
```
  Internet           Internet
     |                   |
    WiFi                WiFi
     |                   |
    PC 1 ---Ethernet--- PC 2
    
- internet joignable en direct par le PC 1
- internet joignable en direct par le PC 2
```
* vous allez désactiver Internet sur une des deux machines, et vous servir de l'autre machine pour accéder à internet. Schéma tout moche again ? 
```
  Internet           Internet
     X                   |
     X                  WiFi
     |                   |
    PC 1 ---Ethernet--- PC 2
    
- internet joignable en direct par le PC 2
- internet joignable par le PC 1, en passant par le PC 2
```
* pour ce faiiiiiire : 
  * désactivez l'interface WiFi sur l'un des deux postes
  * s'assurer de la bonne connectivité entre les deux PCs à travers le câble RJ45
  * **sur le PC qui n'a plus internet**
    * sur la carte Ethernet, définir comme passerelle l'adresse IP de l'autre PC
  * **sur le PC qui a toujours internet**
    * sur Windows, il y a [un menu fait exprès](https://www.dummies.com/computers/operating-systems/windows-7/how-to-share-an-internet-connection-in-windows-7/)
    * sur Linux, faites le en ligne de commande ou utilisez [Network Manager](https://help.ubuntu.com/community/Internet/ConnectionSharing) (présent sur tous les Linux communs)
    * sur MacOS : toute façon vous avez pas de ports RJ, si ? :o

* pour tester la connectivité à internet on utilise souvent un [`ping`](../../cours/lexique.md#ping)
* je veux voir un [`ping 8.8.8.8`](../../cours/lexique.md#ping) qui fonctionne sur un PC sans carte WiFi. Appelez-moi quand vous avez fait ça :)

## 5. Petit chat privé ?

On va créer un chat extrêmement simpliste à l'aide de `netcat` (abrégé `nc`). Il est souvent considéré comme un bon couteau-suisse quand il s'agit de faire des choses avec le réseau.    

Sur Linux et MacOS vous l'avez sûrement déjà, sinon débrouillez-vous pour l'installer :). Les Windowsien, ça se passe [ici](https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip) (from https://eternallybored.org/misc/netcat/).  

Une fois en possession de `netcat`, vous allez pouvoir l'utiliser en ligne de commande. Comme beaucoup de commandes sous Linux, Mac et Windows, on peut utiliser l'option `-h` (`h` pour `help`) pour avoir une aide sur comment utiliser la commande.  

Sur un Windows, ça donne un truc comme ça :
```
C:\Users\It4\Desktop\netcat-win32-1.11>nc.exe -h
[v1.11 NT www.vulnwatch.org/netcat/]
connect to somewhere:   nc [-options] hostname port[s] [ports] ...
listen for inbound:     nc -l -p port [options] [hostname] [port]
options:
        -d              detach from console, background mode

        -e prog         inbound program to exec [dangerous!!]
        -g gateway      source-routing hop point[s], up to 8
        -G num          source-routing pointer: 4, 8, 12, ...
        -h              this cruft
        -i secs         delay interval for lines sent, ports scanned
        -l              listen mode, for inbound connects
        -L              listen harder, re-listen on socket close
        -n              numeric-only IP addresses, no DNS
        -o file         hex dump of traffic
        -p port         local port number
        -r              randomize local and remote ports
        -s addr         local source address
        -t              answer TELNET negotiation
        -u              UDP mode
        -v              verbose [use twice to be more verbose]
        -w secs         timeout for connects and final net reads
        -z              zero-I/O mode [used for scanning]
port numbers can be individual or ranges: m-n [inclusive]
```

L'idée ici est la suivante : 
* l'un de vous jouera le rôle d'un *serveur*
* l'autre sera le *client* qui se connecte au *serveur*

Précisément, on va dire à `netcat` d'*écouter sur un port*. Des ports, y'en a un nombre fixe (65536, on verra ça plus tard), et c'est juste le numéro de la porte à laquelle taper si on veut communiquer avec le serveur.   

Si le serveur écoute à la porte 20000, alors le client doit demander une connexion en tapant à la porte numéro 20000, simple non ?  

Here we go :
* **sur le PC *serveur*** avec par exemple l'IP 192.168.1.1
  * `nc.exe -l -p 8888` => "`netcat`, écoute sur le port numéro 8888 stp"
  * il se passe rien ? Normal, faut attendre qu'un client se connecte
* **sur le PC *client*** avec par exemple l'IP 192.168.1.2
  * `nc.exe 192.168.1.12 8888` => "`netcat`, connecte toi au port 8888 de la machine 192.168.1.12 stp"
  * une fois fait, vous pouvez taper des messages dans les deux sens
* appelez-moi quand ça marche ! :)

* pour aller un peu plus loin
  * le serveur peut préciser sur quelle IP écouter, et ne pas répondre sur les autres
  * par exemple, on écoute sur l'interface Ethernet, mais pas sur la WiFI
  * pour ce faire `nc.exe -l -p PORT_NUMBER IP_ADDRESS`
  * par exemple `nc.exe -l -p 9999 192.168.1.37`
  * on peut aussi accepter uniquement les connexions internes à la machine en écoutant sur `127.0.0.1`
  
## 6. Wireshark

* téléchargez l'outil [Wireshark](https://www.wireshark.org/)
* utilisez le pour observer les trames qui circulent entre vos deux carte Ethernet
  * pendant un `ping`
  * pendant un `netcat`
  * pendant que le PC1 sert du PC2 comme gateway
  * prenez moi des screens des trames en question
  * on décortiquera tout ça au prochain cours ensemble

## 7. Firewall

Toujours par 2 : 
* le but est de configurer votre firewall pour faire fonctionner plusieurs choses
**1.** Activez votre firewall
**2.** Autoriser `ping`
  * configurer le firewall de votre OS pour accepter le `ping`
  * aidez vous d'internet
  * on rentrera dans l'explication dans un prochain cours mais sachez que `ping` envoie un message *ICMP de type 8* (demande d'ECHO) et reçois un message *ICMP de type 0* (réponse d'écho) en retour
**3.** Autoriser `nc` sur un port spécifique
  * choisissez arbitrairement un port entre 1024 et 20000
  * vous utiliserez ce port pour [communiquer avec `netcat`](#5-petit-chat-privé-) par groupe de 2 toujours
  * le firewall du *PC serveur* devra avoir un firewall activé et une `netcat` qui fonctionne
  * appelez-moi quand c'est OK
  
# III. Manipulations d'autres outils/protocoles côté client

## 1. DHCP
Bon ok vous savez définir des IPs à la main. Mais pour être dans le réseau Ingésup, vous l'avez jamais fait.  
C'est le **serveur DHCP** d'Ingésup qui vous a donné une IP.   

* afficher l'adresse IP du serveur DHCP du réseau WiFi
* cette adresse a une durée de vie limitée. C'est le principe du ***bail DHCP*** (ou *DHCP lease*). Trouver la date d'expiration de votre bail DHCP
* renseignez-vous un peu sur le fonctionnement de DHCP dans les grandes lignes. On aura un cours là dessus :)
* demandez une nouvelle adresse IP (en ligne de commande)

## 2. DNS
Le protocole DNS permet la résolution de nom de domaine vers adresse IP. Ce protocole permet d'aller sur `google.com` plutôt que de devoir utiliser l'adresse IP du serveur de Google.  
Un **serveur DNS** est un serveur à qui l'on peut poser des questions sur un nom de domaine comme `google.com`.  
Si votre navigateur fonctionne "normalement" : il vous permet d'aller sur `google.com`, votre ordinateur connaît forcément l'adresse d'un serveur DNS.  

* trouver l'adresse IP du serveur DNS que connaît votre ordinateur
* utiliser, en ligne de commande l'outil `nslookup` pour lui poser des questions (sur Windows). Sur GNU/Linux et MacOS vous devriez avoir `dig`
  * faites un *lookup* (*lookup* = "dis moi à quelle IP se trouve tel nom de domaine)
    * pour `google.com`
    * pour `ynov.com`
    * interpréter les résultats de ces commandes
  * faites un *reverse lookup* (= "dis moi si tu connais un nom de domaine pour telle IP")
    * pour l'adresse `78.78.21.21`
    * pour l'adresse `92.16.54.88`
    * interpréter les résultats
    * *si vous vous demandez, j'ai pris des adresses random :)*

## 3. Bonus : aller plus loin

En combinant des trucs qu'on a vu plus tôt, ça se fait facilement d'aller plus loin :
* ouvrir Wireshark pendant les requêtes DHCP et DNS
* se renseigner sur les différences entre WiFi et câble
* explorer l'interface d'administration de votre box (chez vous) avec tout ça en tête
* sinon, elle sert à quoi la MAC si on a des IP ? => Se renseigner sur ARP
* utiliser un switch (physique) et se connecter non pas à 2, mais à 3 ou 4 ou 5 et faire mumuse avec le réseau ainsi créé

# Bilan
**Vu pendant le TP :** 
* visualisation de vos interfaces réseau (en GUI et en CLI)
* extraction des informations IP
  * adresse IP et masque 
  * calcul autour de IP : adresse de réseau, etc.
* connaissances autour de/aperçu de :
  * un outil de diagnostic simple : `ping`
  * un outil de scan réseau : `nmap`
  * un outil qui permet d'établir des connexions "simples" (on y reviendra) : `netcat`
  * un outil d'analyse de trafic : `wireshark`
  * un outil pour faire des requêtes DNS : `nslookup` ou `dig`
* manipulation simple de vos firewalls

**Résumé :**  
* Pour permettre à un ordinateur d'être connecté en réseau, il lui faut **une liaison physique** (par câble ou par *WiFi*).  
* Pour réceptionner ce lien physique, l'ordinateur a besoin d'**une carte réseau**. La carte réseau porte une [adresse MAC](../../cours/lexique.md#mac--media-access-control).  
* **Pour être membre d'un réseau particulier, une carte réseau peut porter une adresse IP.** 
Si deux ordinateurs reliés physiquement possèdent une adresse IP dans le même réseau, alors ils peuvent communiquer.  
* **Un ordintateur qui possède plusieurs cartes réseau** peut réceptionner du trafic sur l'une d'entre elles, et le balancer sur l'autre, servant ainsi de "pivot". Cet ordinateur **est appelé routeur**.   
* Il existe dans la plupart des réseaux, certains équipements ayant un rôle particulier : 
  * un équipement appelé **[*passerelle*](../../cours/lexique.md#passerelle-ou-gateway)**. C'est un routeur, et il nous permet de sortir du réseau actuel, pour en joindre un autre.  
  * un équipement qui agit comme **serveur DNS** : il nous permet de connaître les IP derrière des noms de domaine
  * un équipement qui agit comme **serveur DHCP** : il donne automatiquement des IP aux clients qui rejoigne le réseau
  * chez vous, c'est votre Box qui fait les trois :)