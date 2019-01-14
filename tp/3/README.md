# B1 Réseau 2018 - TP3

# Notions vues avant le TP

* Manipulations IP et masque (avec le [binaire](../../cours/lexique.md#binaire))
* Adressage d'IP statique et dynamique sur vos OS
* Firewall (bref)
* Ligne de commande
  * navigation de dossier
  * `ipconfig` ou `ifconfig` suivant l'OS
  * `nmap` (un peu)
  * `netcat` ou `nc` suivant l'OS

# TP 3 - Plusieurs réseaux : routage statique
Pour ce TP (et probablement pour beaucoup de TPs à l'avenir), on va se servir de machines virtuelles.  
Le but sera de simuler un petit réseau dans chacun de vos machines, afin de les faire communiquer.  

# Déroulement et rendu du TP 
* vous utiliserez un l'hyperviseur de votre choix parmi : 
  * [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
  * VMWare Workstation
  * j'utiliserai VirtualBox pour ma part, c'est avec lui que les exemples seront donnés
* les machines virtuelles : 
  * l'OS **devra être** [CentOS 7 (en version minimale)](http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso)
  * pas d'interface graphique (que de la ligne de commande)
  
* il y a beaucoup de ligne de commande dans ce TP, préférez les copier/coller aux screens
  * vous pourrez copiez/coller simplement à partir du [II.2.](#2-ssh)
  * soit vous screenez ce qu'il y a avant, soit vous prenez des notes et vous refaites une fois que vous pouvez copier/coller (c'est très vite fait à refaire)
* le rendu doit toujours se faire [au même format](../README.md)

# Hints généraux
* **pour vos recherches Google** (ou autres) : 
  * **en anglais**
  * **précisez l'OS et la version** dans vos recherches ("centos 7" ici)
* dans le TP, **lisez en entier une partie avant de commencer à la réaliser.** Ca donne du sens et aide à la compréhension
* **allez à votre rythme.** Le but n'est pas de finir le TP, mais plutôt de bien saisir et correctement appréhender les différentes notions
* **n'hésitez pas à me demander de l'aide régulièrement** mais essayez toujours de chercher un peu par vous-mêmes avant :)
* pour moult raisons, il sera préférable pendant les cours de réseau de **désactiver votre firewall**. Vous comprendrez ces raisons au fur et à mesure du déroulement du cours très justement. N'oubliez pas de le réactiver après coup.

# Sommaire

* [I. Création et utilisation simples d'un VM CentOS](#i-création-et-utilisation-simples-dune-vm-centos)
  * [Premiers Pas](#1-création)
  * [Configuration réseau](#4-configuration-réseau-dune-machine-centos)
  * [Quelques commandes liées au réseau](#5-faire-joujou-avec-quelques-commandes)
* [II. Notion de ports et SSH](#ii-notion-de-ports-et-ssh)
  * [Exploration des ports locaux](#1-exploration-des-ports-locaux)
  * [Serveur SSH](#2-ssh)
  * [Firewall](#3-firewall)
* [III. Routage statique](#iii-routage-statique)
  * [Rappels et Objectifs](#0-rappels-et-objectifs)
  * [Préparation des hôtes](#1-préparation-des-hôtes-vos-pcs)
  * [Configuration du routage](#2-configuration-du-routage)
  * [Configuration des noms de domaine](#3-configuration-des-noms-de-domaine)
* **[Bilan](#bilan)**
  
---
# I. Création et utilisation simples d'une VM CentOS

Dans cette partie, on va créer, installer et configurer une amchine virtuelle. L'étape de configuration se centrera évidemment sur l'aspect réseau de la machine.

## 1. Création
**(déjà fait ensemble en cours)**  

Créez une machine virtuelle en utilisant un [`iso` de CentOS 7 (version minimale)](http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso).  
Avant la création, la seule chose qu'on va toucher, c'est le réseau. Assurez-vous que : 
* votre VM possède une interface de type NAT
* votre VM possède une interface de type *réseau privé hôte* ou *host-only network*
  * ce réseau *host-only* **ne doit pas** avoir de serveur DHCP activé

## 2. Installation de l'OS
**(déjà fait ensemble en cours)**  

CentOS 7 est fourni avec un installateur graphique (on peut cliquer et faire des bails et tout), afin de faciliter l'installation de l'OS.  
On laisse la plupart des éléments par défaut excepté : 
* activation de la carte réseau NAT
* définition d'un utilisateur administrateur ainsi que de son mot de passe
* définition du mot de passe de l'utilisateur `root`
* timezone correcte (fuseau horaire)
* disposition du clavier en *fr*

## 3. Premier boot
**(déjà fait ensemble en cours)**  

Que de la ligne de commande, alors petit rappel :
* `cd` change de dossier
* `ls` liste les fichiers/dossiers du dossier actuel
* `pwd` affiche le répertoire où on est actuellement
Avec ces 3 là vous pouvez vous baladez un peu partout. Sachez juste que la *racine* du disque dur n'est pas à `C:` mais simplement à `/`. Donc `cd /` vous amène dans un dossier qui contient tous les autres.   

En plus on va avoir besoin de : 
* `man` : affiche le manuel d'une commande. Avec celle-ci vous pouvez conquérir toutes les autres :)
* `ifconfig` (obsolète) ou `ip a` (à jour) pour avoir des infos sur vos cartes réseau
* `cat` qui permet de lire le contenu d'un fichier (un fichier texte par exemple)
  * par exemple `cat /etc/os-release` permet d'ouvrir et afficher le contenu du fichier texte `os-release`, se trouvant dans le dossier `/etc`
* `nano` (simple, mais nul) ou `vi`/`vim` (complexe, mais puissant) pour éditer des fichiers
* rien de particulier à faire ici, juste se familiariser un peu avec les commandes peut être intéressant avant de passer à la suite ;)

**Avant tout le reste, [désactivez SELinux](#annexe-1--désactiver-selinux).**  

## 4. Configuration réseau d'une machine CentOS
**(déjà fait ensemble en cours)**  

Ca se présentera à peu près pareil pour beaucoup d'OS Linux, les fichiers sont simplement différents parfois.   
Cherchez sur internet afin que votre VM :
* possède une connectivité à Internet
  * c'est l'interface *NAT* qui fait ça
  * aucune configuration nécessaire normalement
* possède une IP privée permettant de joindre l'hôte
  * c'est l'interface *host-only* qui s'en occupe
  * vous devrez modifier **un seul** fichier dans `/etc/sysconfig/network-scripts` pour ce faire
  * vous pouvez ensuite faire `ifdown` puis `ifup` sur l'interface pour l'éteinder puis la rallumer
  * un petit `ip a` pour vérifier que le changement a pris effet

* **A FAIRE :**
  * *a.* utilisez une commande pour prouver que vous avez internet depuis la VM
  * *b.* prouvez que votre PC hôte et la VM peuvent communiquer
  * *c.* affichez votre table de routage **sur la VM** et expliquez chacune des lignes

## 5. Faire joujou avec quelques commandes

Rien à faire pour le moment, juste quelques commandes utiles liées au réseau avec lesquelles vous pouvez faire joujou, afin de vous familiariser avec la ligne de commande : 
* [`ping`](../../cours/lexique.md#ping)
* [`curl`](../../cours/lexique.md#curl-et-wget) : permet de faire des requêtes HTTP (comme un navigateur)
  * `curl -SL www.google.com` par exemple
* [`dig`](../../cours/lexique.md#nslookup-ou-dig) : requêtes DNS
* `tcpdump` : Wireshark. Mais en ligne de commande. :)
* [`nmap`](../../cours/lexique.md#nmap)
* [`nc`](../../cours/lexique.md#nc-ou-netcat) : c'est `netcat`
* [`ss`](../../cours/lexique.md#netstat-ou-ss) : permet de lister les ports utilisés sur la machine

**A faire :** 
* `ping`
  * `ping` hôte -> VM
  * `ping` VM -> hôte
* afficher la table de routage
  * de l'hôte
  * de la VM
  * mettre en évidence la ligne qui leur permet de discuter *via* le réseau host-only (dans chacune des tables)
* depuis la VM utilisez `curl` (ou `wget`) pour télécharger un fichier sur internet
* depuis la VM utilisez `dig` pour connaître l'IP de :
  * `ynov.com`
  * `google.com`

# II. Notion de ports et SSH

[La notion de port a déjà été expliquée en cours ici.](../../cours/lexique.md#ports)

## 1. Exploration des ports locaux
* **utilisez la commande [`ss`](../../cours/lexique.md#netstat-ou-ss) pour lister les ports TCP sur lesquels la machine virtuelle écoute**
  * pour ce faire, il faudra ajouter des options à la commande [`ss`](../../cours/lexique.md#netstat-ou-ss)
  * par exemple, pour avoir uniquement les connexions en IPv4, on peut utiliser `ss -4`
  * il vous faut une option pour (utilisez le `man`) : 
    * TCP
    * *listening* : les ports en écoute (là où votre VM attend la connexion d'un client)
* utilisez les options
  * `-n` pour avoir le numéro du port, plutôt qu'un nom
  * `-p` pour connaître l'application qui écoute sur ce port
* vous devriez voir une application qui écoute sur le port 22

## 2. SSH

**Pour rappel, il faut [désactiver SELinux](#annexe-1--désactiver-selinux).**  

SSH est un protocole pour se connecter sur un serveur à distance :
* on installe un serveur SSH sur un serveur
* on configure le serveur SSH pour écouteur sur une adresse IP et un port spécifiques
  * par convention, on met souvent le serveur SSH sur le port 22
* on lance le serveur SSH
* quelqu'un qui est peut joindre le serveur peut alors utiliser un client SSH pour se connecter au serveur

A quoi ça sert ? Bah c'est pratique quand le serveur est à 500km de chez vous par exemple.  

Mais on va aussi s'en servir pour se connecter à la VM, entre autres parce que : 
* permet de gérer toutes les VMs directement depuis votre hôte
* permet de faire des copier/coller izi, plutôt que de galérer avec la console

Pour notre TP : 
* CentOS 7 intègre déjà un serveur SSH installé, configuré, et lancé
* si vous êtes sur Windows
  * téléchargez [putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
  * **c'est votre client SSH**
* si vous êtes sur GNU/Linux ou MacOS
  * ouvrez un terminal, vous avez la commande `ssh`
  * **c'est votre client SSH**
* connectez-vous en SSH à la machine virtuelle

## 3. Firewall

CentOS 7 est aussi équipé d'un pare-feu. Par défaut, il bloque tout, à part quelques services comme `ssh` justement.  

Rdv dans la section procédure pour savoir comment [interagir avec le firewall de CentOS](../../cours/procedures.md#interagir-avec-le-firewall).  

* **A. SSH** : 
  * modifier le fichier `/etc/ssh/sshd_config`
    * changer le numéro du port sur lequel votre serveur SSH écoute
    * **utilisez un port strictement supérieur à 1024** (`2222` par exemple)
  * redémarrez le serveur SSH pour que le changement prenne effet
    * `systemctl restart sshd`
  * vérifiez que votre serveur SSH écoute sur un port différent de `22` (le vôtre)
    * utilisez [la commande `ss`](../../cours/lexique.md#netstat-ou-ss)
  * connectez-vous au serveur en utilisant ce port
    * utilisez votre client SSH
  * sans autre modification, la connexion devrait échouer
    * expliquez pourquoi
    * trouvez une solution
    
* **B. `netcat`** 
  * dans un premier terminal 
    * lancer un serveur `netcat` dans un terminal (commande `nc -l`)
    * le serveur doit écouter sur le port `5454` en TCP
    * il faudra autoriser ce port dans le firewall
  * dans un deuxième terminal
    * se connecter au serveur `netcat` (commande `nc`)
  * dans un troisième terminal
    * utiliser `ss` pour visualiser la connexion `netcat` en cours

# III. Routage statique

**Pour rappel, il faut [désactiver SELinux](#annexe-1--désactiver-selinux).**  

Le routage, c'est le fait d'utiliser une machine comme pivot (le routeur), entre deux réseau, afin qu'il fasse passer le trafic d'un réseau à un autre.  
Le routage statique consiste à définir de façon simple les routes utilisables par le routeur et les machines. C'est l'administrateur qui les définit à la main.  

## 0. Rappels et objectifs
La dernière fois, dans le TP 2, on a fait ça :
* deux PCs reliés avec un câble
* les interfaces Ethernet des deux PCs étaient dans le même réseau pour pouvoir communiquer
* "être dans le même réseau" c'est avoir une adresse IP dans le même réseau IP
```
  Internet           Internet
     |                   |
    WiFi                WiFi
     |                   |
    PC 1 ---Ethernet--- PC 2
```
Et dans ce TP 3 on a fait ça : 
* deux PCs reliés avec un câble
  * l'un est physique, c'est votre hôte
  * l'autre est virtuel, c'est la VM
  * le câble, c'est le réseau host-only
* les interfaces host-only des deux PCs sont dans le même réseau pour pouvoir communiquer
* en fait c'est la même chose, clairement.
```
   PC 1
    |
Host-only 1
    |
   VM 1
```

Objectif, encore un schéma moche :
```
 Internet            Internet
    |                    |
  WiFi                  WiFi
    |                    |
   PC 1  ---Ethernet--- PC 2
    |                    |
Host-only 1          Host-only 2
    |                    |
   VM 1                 VM 2
```
* vos PCs vont devenir de vrais routeurs
  * on pourrait les appeler R1 et R2, plutôt que PC1 et PC2 ;)

* dans la suite on appelle
  * réseau `1` le réseau host-only 1
  * réseau `2` le réseau host-only 2
  * réseau `12` le réseau formé par le câble Ethernet (parce qu'il lie le `1` et le `2`)

* **mettez-vous par deux, comme au TP2**

## 1. Préparation des hôtes (vos PCs)

### Préparation avec câble
Faites en sorte que :
* vos deux PCs puissent se ping à travers le câble
* vos carte Ethernet doivent être dans le réseau `12` : `192.168.112.0/30`

### Préparation VirtualBox
Modifier vos réseaux host-only pour qu'ils soient :
* PC1 : réseau `1` : `192.168.101.0/24`
* PC2 : réseau `2` : `192.168.102.0/24`

Créez (ou réutilisez) une VM, et modifiez son adresse :
* VM1 (sur PC1) : `192.168.101.10`
* VM2 (sur PC2) : `192.168.102.10`

### Check
Assurez vous que :
* PC1 et PC2 se ping en utilisant le réseau `12`
* VM1 et PC1 se ping en utilisant le réseau `1`
* VM2 et PC2 se ping en utilisant le réseau `2`

Observez vos tables de routage sur tous les hôtes, pour comprendre : 
* `ip route` sur les Linux ou MacOS
* `route print -4` sur Windows

### Activation du routage sur les PCs

Pour que vos hôtes (vos PCs) puissent agir comme des routeurs, il va falloir faire un peu de configuration, qui va dépendre de votre OS.  

#### Windows
* modifier la clé registre `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\ Services\Tcpip\Parameters\IPEnableRouter` en passant sa valeur de `0` à `1`
* vous pouvez reboot là (ça évite des pbs)
* activer le service de routage ("lancer l'application de routage")
  * `Win + R`
  * `services.msc` > `Entrée`
  * Naviguer à "Routage et accès distant"
    * Clic-droit > Propriétés
    * Pour le démarrage, sélectionner "Automatique"
    * `Appliquer`
    * `Démarrer`

#### MacOS ou GNU/Linux
* `sysctl -w net.ipv4.conf.all.forwarding=1`

## 2. Configuration du routage
Vous avez 3 réseaux : 
* **réseau `1`**, un /24 entre PC1 et VM1 (host-only 1)
* **réseau `2`**, un /24 entre PC2 et VM2 (host-only 2)
* **réseau `12`**, un /30 entre PC1 et PC2 (câble)

Faites un bilan des adresses IP portés par chacune des interfaces utilisées dans le TP, pour les 4 machines (PC1, PC2, VM1, VM2)
* carte Ethernet et Host-only pour les hôtes
* carte host-only pour les VMs

Le but va être de faire en sorte que VM1 puisse ping VM2 et réciproquement. Pour ce faire, avec du routage statique simple, on va devoir faire en sorte que tout le monde connaisse un chemin pour aller dans chacun des réseaux !  

### PC1
PC1 accède déjà aux réseaux `1` et `12`, il faut juste lui dire comment accéder au réseau `2`
* Windows
  * `route add <IP_2> mask 255.255.255.0 <IP_12_PC2>`
  * soit `route add 192.168.102.0/24 mask 255.255.255.0 192.168.112.2`
* GNU/Linux
  * `ip route add <IP_2> via <IP_12_PC2> dev <INTERFACE_12_NAME>`
  * par exemple `ip route add 192.168.102.0/24 via 192.168.112.2 dev eth0`
* MacOS
  * `route -n add -net <IP_2> <IP_12_PC2>`
  * `route -n add -net 192.168.102.0/24 192.168.112.2`
* **quoiqu'il en soit", la règle peut se traduire par :**
  * *"si tu veux aller dans le réseau 192.168.102.0/24, passe par la machine 192.168.112.2"
  * cela nécessite de déjà connaître la machine 192.168.112.2, ici, c'est PC2 :)

* PC1 devrait pouvoir ping `192.168.102.1` (l'adresse de PC2 dans `2`)

### PC2
Faire l'opération inverse.
* PC2 devrait pouvoir ping `192.168.101.1` (l'adresse de PC1 dans `1`)

---
**Appelez-moi pour que je vérifie tout ça !**  

---

### VM1
VM1 n'a accès qu'au réseau `1`. Tristesse. Il faut dire à VM1 qu'elle peut joindre les réseaux `12` et `2` en utilisant le lien qui l'unit avec `PC1`. Pour lui dire d'accéder au réseau `12` en passant par `1` : 
* `ip route add <IP_12> via <IP_1_PC1> dev <INTERFACE_1_NAME>`
* `ip route add 192.168.112.0/24 via 192.168.101.1 dev enp0s8`
* taper une deuxième commande pour lui dire d'accéder au réseau `2`

* VM1 devrait pouvoir ping `192.168.112.2`, l'adresse de PC2 dans le réseau `12`
* VM1 devrait pouvoir ping `192.168.102.1`, l'adresse de PC2 dans le réseau `2`

### VM2
Faire comme sur VM1

* VM2 devrait pouvoir ping `192.168.112.1`, l'adresse de PC1 dans le réseau `12`
* VM2 devrait pouvoir ping `192.168.101.1`, l'adresse de PC1 dans le réseau `1`

## 3. Configuration des noms de domaine

La configuration du [nom de domaine](../../cours/4.md#noms-de-domaine) d'une machine se fait en deux étapes : 

**1. Donner un nom à la machine**
  * ceci permet à la machine elle-même de connaître un nom
  * c'est effectué **sur la machine elle-même**
  
**2. Configurer un outil pour que les autres machines connaissent son nom**
  * c'est effectué **à l'extérieur de la machine**
  * soit on configure un serveur [DNS](../../cours/lexique.md#dns--domain-name-system) (c'est le plus courant mais un peu hardu pour le moment)
  * sont on remplit le fichiers `hosts` de toutes les autres machines

**NOTE** : *une machine peut être jointe par son nom, même si elle ne le connaît pas elle-même. Autrement dit, dans les deux étapes citées ci-dessus, seule la deuxième est strictement obligatoire*  
* ne me faites pas dire ce que je n'ai pas dit, le 1 reste important dans beaucoup de cas

Pour notre TP : 
* donner un nom de domaine aux machines virtuelles 
  * PAS aux hôtes physiques, pour éviter de pourrir votre vraie configuration
* remplir le fichier `hosts` des machines virtuelles **ET** des PCs physiques
  * Linux et MacOS : `/etc/hosts`
  * Windows : `C:\Windows\System32\drivers\etc\hosts`

Un tableau récapitulatif, qui distingue les notions de [noms de domaine, nom d'hôtes et FQDN](../../cours/4.md#noms-de-domaine) :  

Host | Hostname |  Domain  |     FQDN
---- | -------- | -------- | ------------
PC1  |   `pc1`  | `tp3.b1` | `pc1.tp3.b1`
PC2  |   `pc2`  | `tp3.b1` | `pc2.tp3.b1`
VM1  |   `vm1`  | `tp3.b1` | `vm1.tp3.b1`
VM2  |   `vm2`  | `tp3.b1` | `vm2.tp3.b1`

**But à atteindre** :
* la VM1 doit pouvoir ping tous les FQDN y compris `vm2.tp3.b1`
* la VM2 doit pouvoir ping tous les FQDN y compris `vm2.tp3.b1`
* un ultime `netcat` entre `vm1.tp3.b1` et `vm2.tp3.b1`

---

# Bilan
* création de machine virtuelle simple
* configuration des cartes réseau de la VM
* configuration d'IP statique sous vos OS natifs et CentOS7
* gestion de réseau élémentaire sous Linux 
  * `ping`, `netcat`, `ip a`, `ss`
* création d'un routage statique simple avec des VMs Linux comme clients et les PCs hôtes comme routeurs
  * tout le monde doit connaître toutes les routes
  * `PC1`, `PC2`, `VM1` et `VM2` ont tous une route vers les réseaux `1`, `2` et `12` dans leur table de routage
* aperçu de la gestion de nom de domaines
---

### Annexe 1 : Désactiver SELinux
SELinux (*Security Enhanced Linux*) est un outil présent sur les distributions GNU/Linux dérivés de RHEL (comme CentOS).  
**Pour nos TPs, la seule chose à savoir, c'est qu'on va le désactiver :**
* `sudo setenforce 0`
* modifier le fichier `/etc/selinux/config`
  * modifier la valeur de `SELINUX` à `permissive`
  * `SELINUX=permissive`
* pour vérifier : `sestatus` doit afficher `Current mode:   permissive`

### Annexe 2 : Routing si vos PCs sont sous Linux
Un peu plus restrictif (et donc sécurisé) que sur un Winwin. Il va falloir autoriser explicitement le traffic à circuler entre l'interface host-only et votre carte ethernet : 
* `iptables -A FORWARD -o <ETHERNET_CARD_NAME> -i <HOST-ONLY_CARD_NAME> -j ACCEPT`
* `iptables -A FORWARD -o <HOST-ONLY_CARD_NAME> -i <ETHERNET_CARD_NAME> -j ACCEPT`
* `iptables -t nat -A POSTROUTING -s <DESTINATION_NETWORK_CIDR> -j MASQUERADE`  
  * on reviendra sur le NAT plus tard en cours :)
  * c'pas du vrai vrai routing ça ehe

Appelez-moi si vous galérez.
