# Procédures

Vous trouverez ici quelques mini-procédures pour réaliser une opération précise, sur une machine précise. Ce sera évidemment principalement utilise pour notre cours de réseau, mais peut-être serez-vous amenés à le réutiliser plus tard.  

**Elles sont écrites pour un système CentOS7**. Vous en apprendrez (au moins un peu) plus sur le monde GNU/Linux en temps et en heure. Sachez que :
* tout ça est faisable (pour la plupart) sur Windows et Mac. Vous demanderez à google des équivalents
* pour ce qui est du réseau, la plupart des Linux sont très similaires
* ces instructions sont valables pour d'autres systèmes basés sur RedHat, comme Fedora
* pour certaines choses, ça peut changer si vous avez une base Debian (comme Ubuntu)

## Sommaire

* [Changer son nom de domaine](#changer-son-nom-de-domaine)
* [Editer le fichier hosts](#editer-le-fichier-hosts)

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
