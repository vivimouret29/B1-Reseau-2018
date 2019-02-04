# Procédures

Vous trouverez ici quelques mini-procédures pour réaliser certaines opérations récurrentes. Ce sera évidemment principalement utilisé pour notre cours de réseau, mais peut-être serez-vous amenés à le réutiliser plus tard.  

**Elles sont écrites pour un système Cisco**.

## Sommaire

* [Les modes du terminal]()
* [Définir une IP statique](#définir-une-ip-statique)
* [Ajouter une route statique](#ajouter-une-route-statique)
* [Changer son nom de domaine](#changer-son-nom-de-domaine)
* [Editer le fichier hosts](#editer-le-fichier-hosts)
* [Interagir avec le firewall](#interagir-avec-le-firewall)
* [Gérer sa table ARP](#gérer-sa-table-arp)


---

### Les modes du terminal
Le terminal Cisco possède plusieurs modes

Mode | Commande | What ? | Why ?
--- | --- | --- | ---
`user EXEC` | X | C'est le mode par défaut : il permet essentiellement de visualiser des choses, mais peu d'actions à réaliser | Pour visualiser les routes ou les IPs par ex
`privileged EXEC` | enable | Mode privilégié : permet de réalisé des actions privilégiées sur la machine | Peu utilisé dans notre cours au début
`global conf` | conf t | Configuration de la machine | Permet de configurer les interface et le routage 

L'idée globale c'est que pour **faire des choses** on passera en `global conf` pour **faire** des choses, et on restera en **user EXEC** pour **voir** des choses.

### Définir une IP statique
**1. Repérer le nom de l'interface dont on veut changer l'IP**
```
# show ip interface brief
OU
# show ip int br
```
**2. Passer en mode configuration d'interface**
```
# conf t
(config)# interface ethernet <NUMERO>
```
**3. Définir une IP**
```
(config-if)# ip address <IP> <MASK>
Exemple :
(config-if)# ip address 10.5.1.254 255.255.255.0
```
**4. Allumer l'interface**
```
(config-if)# no shut
```
**5. Vérifier l'IP**
```
(config-if)# exit
(config)# exit
# show ip int br
```
---

### Ajouter une route statique

**1. Passer en mode configuration d'interface**
```
# conf t
```

**2. Ajouter la route**
```
(config)# ip route <NETWORK_ADDRESS> <MASK> <GATEWAY_IP> 
Exemple : 
(config)# ip route 10.1.0.0 255.255.255.0 10.2.0.254 
```

**3. Vérifier la route**
```
(config)# exit
# show ip route
```

### Changer son nom de domaine
**1. Passer en mode configuration d'interface**
```
# conf t
```

**2. Changer le hostname**
```
(config)# hostname <HOSTNAME>
```

### Gérer sa table ARP

* voir sa table ARP
```
# show arp
```
