# Procédures

Vous trouverez ici quelques mini-procédures pour réaliser certaines opérations récurrentes. Ce sera évidemment principalement utilisé pour notre cours de réseau, mais peut-être serez-vous amenés à le réutiliser plus tard.  

**Elles sont écrites pour un système CentOS7**. Vous en apprendrez (au moins un peu) plus sur le monde GNU/Linux en temps et en heure. Sachez que :
* tout ça est faisable (pour la plupart) sur Windows et Mac. Vous demanderez à google des équivalents
* pour ce qui est du réseau, la plupart des Linux sont très similaires
* ces instructions sont valables pour d'autres systèmes basés sur RedHat, comme Fedora
* pour certaines choses, ça peut changer si vous avez une base Debian (comme Ubuntu)

## Sommaire

* [Définir une IP statique](#définir-une-ip-statique)
* [Ajouter une route statique](#ajouter-une-route-statique)
* [Changer son nom de domaine](#changer-son-nom-de-domaine)
* [Editer le fichier hosts](#editer-le-fichier-hosts)
* [Interagir avec le firewall](#interagir-avec-le-firewall)


---

### Définir une IP statique
**1. Repérer le nom de l'interface dont on veut changer l'IP**
```
ip a
```
**2. Modifier le fichier correspondant à l'interface**
* il se trouve dans `/etc/sysconfig/network-scripts`
* il porte le nom `ifcfg-<NOM_DE_L'INTERFACE>`
* on peut le créer s'il n'existe pas
* exemple de fichier minimaliste qui assigne `192.168.1.19/24` à l'interface `enp0s8`
```
NAME=enp0s8
DEVICE=enp0s8

BOOTPROTO=static
ONBOOT=yes

IPADDR=192.168.1.19
NETMASK=255.255.255.0
```
**3. Redémarrer l'interface**
```
sudo ifdown <INTERFACE_NAME>
sudo ifup <INTERFACE_NAME>
```

---

### Ajouter une route statique

* **temporairement**
  * `ip route add <NETWORK_ADDRESS> via <LOCAL_IP> dev <LOCAL_INTERFACE_NAME>
  * par exemple `ip route add 192.168.102.0/24 via 192.168.112.2 dev eth0`
  * ce changement sera effacé après `reboot` ou `systemctl restart network`

* **définitivement**
  * comme toujours, afin de rendre le changement permanent, on va l'écrire dans un fichier
  * il peut exister un fichier de route par interface
  * les fichiers de routes :
    * sont dans `/etc/sysconfig/network-scripts/`
    * sont nommés `route-<INTERFACE_NAME>`
    * par exemple `/etc/sysconfig/network-scripts/route-enp0s8`
    * contiennent la même ligne que `ip route add` : 
```
192.168.102.0/24 via 192.168.112.2 dev eth0
192.168.112.0/24 via 192.168.112.2 dev eth0
```

* **pour vérifier**
  * `ip route show`
  
---

### Changer son nom de domaine

**1. Changer le FQDN immédiatement** (temporaire)
```
# commande hostname
sudo hostname <NEW_HOSTNAME>
# par exemple
sudo hostname vm1.tp3.b1
```
**2. Définir un FQDN quand la machine s'allume** (permanent)
* écriture du FQDN dans le fichier `/etc/hostname`
* en une seule commande `echo 'vm1.tp1.b3' > /etc/hostname`

**3. Pour consulter votre FQDN actuel**
```
hostname --fqdn
```

---

### Editer le fichier hosts

Le fichier `hosts` se trouve au chemin `/etc/hosts`. Sa structure est la suivante :
* une seule IP par ligne
* une ligne est une correspondance entre une IP et un (ou plusieurs) noms (FQDN ou nom d'hôte)
* on peut définir des commentaires avec `#`
Par exemple, pour faire correspondre l'IP `192.168.1.19` aux noms `monpc` et `monpc.chezmoi` :
```
192.168.1.19  monpc monpc.chezmoi
```
* on peut tester le fonctionnement avec un `ping`
```
ping monpc.chezmoi
```

### Interagir avec le firewall

CentOS 7 est aussi équipé d'un pare-feu. Par défaut, il bloque tout, à part quelques services comme `ssh` justement.  
Pour manipuler le firewall de CentOS 7, on utilise la commande `firewall-cmd` :
* `firewall-cmd --list-all` pour lister toutes les règles
* `firewall-cmd --add-port=80/tcp --permanent` pour autoriser les connexions sur le port TCP 80 
* `firewall-cmd --remove-port=80/tcp --permanent` pour supprimer une règle qui autorisait les connexions sur le port TCP 80 
* `firewall-cmd --reload` permet aux modifications effectuées de prendre effet

