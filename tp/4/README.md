# B1 Réseau 2018 - TP4

# Notions vues avant le TP

* Manipulations IP et masque (avec le [binaire](../../cours/lexique.md#binaire))
* Adressage d'IP statique et dynamique sur vos OS
* Firewall (bref)
* Ligne de commande
  * navigation de dossier
  * `ipconfig` ou `ifconfig` suivant l'OS
  * `nmap` (un peu)
  * `netcat` ou `nc` suivant l'OS
* Utilisation de CentOS
  * installation simple
  * configuration réseau (voir la fiche de [procédures](../../cours/procedures.md))
    * configuration d'interface
    * configuration firewall
    * configuration routage statique

# TP 4 - Spéléologie réseau : descente dans les couches
Gné ? "Spéléologie" ? Oui, on va descendre dans les couches du *modèles OSI* (on y reviendraaaaaa), explorer le principe d'encapsulation, et regarder un peu comment ça fonctionne **vraiment** tout ça.  

**En vrai c'est le TP qui fait un peu mal aux dents, alors gardez le sourire, soyez motivées et tout ira bien.** :)  

Ha et **c'est un TP solo** ! Vous pouvez vous aider (aidez-vous, vous êtes beaux et forts), mais un rendu/personne exigé ! 

# Déroulement et rendu du TP 
* vous utiliserez un l'hyperviseur de votre choix parmi : 
  * [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
  * VMWare Workstation
  * j'utiliserai VirtualBox pour ma part, c'est avec lui que les exemples seront donnés

* les machines virtuelles : 
  * l'OS **devra être** [CentOS 7 (en version minimale)](http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso)
  * pas d'interface graphique (que de la ligne de commande)
  
* il y a beaucoup de ligne de commande dans ce TP, préférez les copier/coller aux screens

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

  
---
# 0. Préparation d'une VM "patron"
Bon c'est rigolo d'installer CentOS, mais c'est vite chiant. Nos hyperviseurs permettent de cloner des machines. Sauf que vos machines précédentes, vous les avez bien pourries !  

Vous allez réaliser **une nouvelle installation de CentOS**, configurer le minimum, et l'éteindre. **Vous ne rallumerez plus jamais cette VM**, elle ne servira qu'à être clonée. Cela accélerera grandement la mise en place de nos TPs !

Installation et configuration de la VM "patron" : 
* créer une VM
  * 512 Mo RAM
  * 1 CPU
  * Réseau
    * une carte NAT
  * Stockage
    * disque de 8Go
    * `.iso` de CentOS 7
* installation
  * config avant install 
    * langue : anglais
    * clavier : français
    * timezone > Paris, France
    * réseau > activer la carte réseau
    * stockage > cliquer > laisser tout par défaut (ne rien faire) > valider
  * **Commencer l'installation**
    * **utilisez des mots de passe simples**, ce n'est qu'un petit lab avec des VMs en local
    * utilisateur > définir nom et mot de passe > cocher "Faire de cet utilisateur un administrateur"
    * root > définir un mot de passe root
* wait for installation process to finish
* redémarrer la VM
  * vous pouvez enlever le `.iso` du lecteur CD si ce n'est pas fait automatiquement :)
* configuration VM
  * se logger avec votre utilisateur
  * exécutez :
```bash
# Désactivation de SELinux
sudo setenforce # temporaire
sudo sed -i 's/enforcing/permissive/g' /etc/selinux/config # permanent

# Mise à jour des dépôts
sudo yum update -y

# Installation de plusieurs paquets réseau dont on se sert souvent
sudo yum install -y traceroute bind-utils tcpdump nc

# Eteindre la machine
sudo shutdown now
```



# I. Mise en place du lab

Le "lab", c'est juste l'environnement nécessaire à notre TP. Vous allez créer des VMs quoi !

## 1. Création des réseaux

On va créer de nouveaux réseaux host-only. Pour rappel, la création d'un réseau host-only **ajoute une carte réseau sur votre PC**. Vous pouvez la voir avec un `ipconfig` bien sûr ! 

Créez les réseaux suivants :
* le "réseau 1" ou `net1` : `10.1.0.0/24`
  * la carte réseau de l'hôte doit porter l'IP `10.1.0.1`
  * **PAS** de DHCP
* le "réseau 2" ou `net2` : `10.2.0.0/24`
  * la carte réseau de l'hôte doit porter l'IP `10.2.0.1`
  * **PAS** de DHCP

## 2. Création des VMs


Créez les VMs suivantes (= clonez votre VM patron !) :
* VM cliente ou `client1.tp4`
  * elle a une carte réseau dans `net1` qui porte l'IP `10.1.0.10`
  * elle nous servira... de client !
* VM serveur ou `server1.tp4`
  * elle a une carte réseau dans `net2` qui porte l'IP `10.2.0.10`
  * elle nous servira de serveur :|
* VM routeur ou `router1.tp4`
  * elle a une carte réseau dans `net1` qui porte l'IP `10.1.0.254`
  * et une carte réseau dans `net2` qui porte l'IP `10.2.0.254`
  * cette machine sera notre routeur. Ce sera la passerelle de `client1` et `server1`

Je pense que vous avez compris le principe. Au cas où, je vous fais un schéma moche !
```
client  <--net1--> router <--net2--> server
```

Checklist (à faire sur toutes les machines) :
* [ ] [Définition des IPs statiques](../../cours/procedures.md#définir-une-ip-statique)
* [ ] [Définition du nom de domaine](../../cours/procedures.md##changer-son-nom-de-domaine)
* [ ] [Remplissage du fichier `/etc/hosts`](../../cours/procedures.md#editer-le-fichier-hosts)
* `client1` ping `router1.tp4` sur l'IP `10.1.0.254`
* `client2` ping `router1.tp4` sur l'IP `10.2.0.254`

Petit tableau récapitulatif :
Machine | `net1` | `net2`
--- | --- | ---
`client1.tp4` | `10.1.0.10` | X
`router1.tp4` | `10.1.0.254` | `10.2.0.254`
`server1.tp4` | X | `10.2.0.10` 

**IMPORTANT** : habituez-vous à faire ce genre de tableau, c'est une méthode qui vous fera gagner énormément de temps. Pensez à quand vous aurez ~10 machines avec des IPs différentes. Je les ferai pas toujours à votre place ;)