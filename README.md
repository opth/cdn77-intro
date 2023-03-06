# Intro project pro CDN77.com

### Docker
Celá infrastruktura je postavená na Docker kontejnerech.
Pro kontejnery jsem použil vlastní image, postavený na debianu (dle zadání).
Vlastní image používám kvůli množství vlastních požadavků, třeba předinstalované ssh, nebo python pro Ansible.
Nenašel jsem vyhovující hotový kontejner na [docker hubu](https://hub.docker.com/).
Při tvorbě vlasniho Dockerfile jsem se ale jinými inspiroval.

Docker jsem zvolil hlavně z toho důvodu, že s ním již mám zkušenost.
Ještě jsem přemýšlel nad Proxem, jelikož jej taky už znám (provozuji svůj vlastní server), ale nepřišel mi na tento úkol jako ideální řešení.

### Ansible
Jak jsem dříve napsal, pro konfiguraci jsem zvolil Ansible. Nikdy před tímto úkolem jsem se s Ansible nesetkal. Po přečtení [Getting started with Ansible](https://docs.ansible.com/ansible/latest/getting_started/index.html) jsem usoudil, že Ansible chci vyzkoušet. Tohle rozhodnutí mě párkrát potrápilo, ale jsem rád, že jsem do toho šel. Model Code as a Infrastructure jsem rád zkusil.

### Monitoring
Dle zadání jsem použil Prometheus s Grafanou.
Konfiguraci Promethea jsem nikdy dříve nedělal, Grafanu jsem již párkrát konfiguroval.
Pro instalaci a nastavení celého monitoring kontejneru stačí jediný playbook [monitoring_playbook.yaml](./monitoring_playbook.yaml).
V něm používám dvě role pro instalaci a konfiguraci Promethea.
Tento playbook zároveň provádí kopírování konfigurace dashboardů v Grafaně, kopírování a následné spuštění vlastního scriptu KOPR (KOntrolní PRogram, poslední bod seznamu v zadání).
Tento script je spouštěn pomocí `daemontools`, dle zadání posledního bodu. Loguje stavy do textového souboru.
Zároveň používám docker kontejner jako exporter pro stub_status z Nginxu pro Prometheus.

### Web
Druhý playbook [web_playbook.yaml](./web_playbook.yaml) slouží k instalaci Nginx a jeho konfiguraci na příslušném kontejneru.
Nginx jsem dříve konfiguroval (třeba pro svůj projekt [cobyloveskole.cz](https://cobyloveskole.cz)).
Splnil jsem všechny body zadání Nginxu. Celá konfigurace je v jediném souboru [nginx_static.conf](./web/nginx_static.conf).
V tom samém adresáři jsou i vlastně vygenerované certifikáty a výchozí stránka.

### Etcd
Jako distribuovaný systém jsem si vybral etcd.
Zkušenost s ním nemám, ale dle dokumentace vypadá docela pochopitelně a jednoduše.
Na každém ze tří kontejnerů se spouští jeho instance. Viz folder [etcd](./etcd).
Zde je jedno z míst, kde by šla konfigurace řešit lépe pomocí templatů.
Playbook na instalaci, konfiguraci s spuštění se jmenuje [etcd_playbook.yaml](./etcd_playbook.yaml)

## Návod na zprovoznění
Na systému, kde budete tuto virtuální infrastrukturu rozjíždět je potřeba nainstalovaný a běžící **docker**, dále **docker-compose** a **python3**.

Zjednodušení zajisí setup script [setup.sh](./setup.sh).
```
chmod +x ./setup.sh
./setup.sh
```

Poté už stačí spouštět jednotlivé playbooky.
```
ansible-playbook -i inventory web_playbook.yaml
ansible-playbook -i inventory monitoring_playbook.yaml
ansible-playbook -i inventory web_playbook.yaml