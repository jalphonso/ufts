# INSTALLATION

## Prerequisites

- Python 3.6 https://www.python.org/downloads/
- Docker 19.03 https://docs.docker.com/get-docker/
- Python libraries installed via pip (instructions later on)

## Clone Repository
```
git clone git@github.com:jalphonso/ufts.git
```

## Setup user
For installation and mgmt of the app **do not run as root**.

Ensure user is in the docker group.
```
groupadd docker
usermod -a -G docker <username>
```
Optionally, if more users will need access to manage this project change group ownership of the project dir and files to a common group. We use docker as the group in this example since they must belong to that anyway.
```
chgrp -R docker <project dir>
```

Also as some of the containers are built to run with the UID and GID of the user building them, it is important that in the situation where they are being built and saved on a development machine and then loaded and deployed on a production machine, that the ID's of the users on the two machines match. Changing user and group IDs is only possible as root, so if the change below is done on the development machine, it must be done prior to running make develop. If it is done on the production machine, it needs to be done before make start.

- To retrieve UID(run on both machines to verify)
 ```
 id -u
 ```
- To retrieve GID(run on both machines to verify)
 ```
 id -g
 ```
- To change the IDs(run on one machine or the other)
 ```
 sudo groupmod -g NEWGID(GID from other machine) GROUPNAME(existing groupname)
 sudo usermod -u NEWUID(UID from other machine) USERNAME(existing username)
 ```
## Host Firewall

On CentOS to allow Docker to modify firewalld so containers exposed ports can be accessed,
run these commands after installing Docker.

```
firewall-cmd --permanent --zone=trusted --change-interface=docker0
firewall-cmd --permanent --zone=trusted --add-port=4243/tcp
firewall-cmd --reload
systemctl restart docker
```

## Services used
- Python Django Web Framework
- Nginx
- Consul
- Registrator
- Consul Template
- Celery
- Celery Beat
- HAProxy
- Redis
- Postgres

## Data Storage
- Uploaded software will be stored in software/
- Uploaded books, docs, and other media will be stored in media/
- Application logs stored in logs/ but also sent out through Docker's logging mechanism
- Supporting container logs are visible through Docker's logging mechanism
- Reports are located in reports/
- Emails if email server is not configured will be stored in sent_emails/
- Certs are stored in config/certs/
- Consul, Web, DB, and LB configs are stored in config/
- Static web files like html/css/js and third-party web libraries are stored in /static
- Templated web files are stored in templates/
- DB is stored in a docker named volume typically named ufts_db_volume
- Docker data is stored in /var/lib/docker/ by default

## Certificates
You will need an openssl.cnf preferably in the default location

Mac/Ubuntu:
- /etc/ssl/openssl.cnf

CentOS 7:
- /etc/pki/tls/openssl.cnf

If you have it elsewhere you'll need to supply it with the -config openssl.cnf in most of the commands.

#### openssl.cnf:
```
#
# OpenSSL example configuration file.
# This is mostly being used for generation of certificate requests.
#

# Note that you can include other files from the main configuration
# file using the .include directive.
#.include filename

# This definition stops the following lines choking if HOME isn't
# defined.
HOME                    = .

# Extra OBJECT IDENTIFIER info:
#oid_file               = $ENV::HOME/.oid
oid_section             = new_oids

# To use this configuration file with the "-extfile" option of the
# "openssl x509" utility, name here the section containing the
# X.509v3 extensions to use:
# extensions            =
# (Alternatively, use a configuration file that has only
# X.509v3 extensions in its main [= default] section.)

[ new_oids ]

# We can add new OIDs in here for use by 'ca', 'req' and 'ts'.
# Add a simple OID like this:
# testoid1=1.2.3.4
# Or use config file substitution like this:
# testoid2=${testoid1}.5.6

userName = 1.2.3.4.5.6.7.8

# Policies used by the TSA examples.
tsa_policy1 = 1.2.3.4.1
tsa_policy2 = 1.2.3.4.5.6
tsa_policy3 = 1.2.3.4.5.7

####################################################################
[ ca ]
default_ca      = CA_default            # The default ca section

####################################################################
[ CA_default ]

dir             = .                     # Where everything is kept
certs           = $dir/certs            # Where the issued certs are kept
crl_dir         = $dir/crl              # Where the issued crl are kept
database        = $dir/index.txt        # database index file.
#unique_subject = no                    # Set to 'no' to allow creation of
                                        # several certs with same subject.
new_certs_dir   = $dir/newcerts         # default place for new certs.

certificate     = $dir/ca.crt           # The CA certificate
serial          = $dir/serial           # The current serial number
crlnumber       = $dir/crlnumber        # the current crl number
                                        # must be commented out to leave a V1 CRL
crl             = $dir/crl.pem          # The current CRL
private_key     = $dir/private/ca.key   # The private key

x509_extensions = usr_cert              # The extensions to add to the cert

# Comment out the following two lines for the "traditional"
# (and highly broken) format.
name_opt        = ca_default            # Subject Name options
cert_opt        = ca_default            # Certificate field options

# Extension copying option: use with caution.
# copy_extensions = copy

# Extensions to add to a CRL. Note: Netscape communicator chokes on V2 CRLs
# so this is commented out by default to leave a V1 CRL.
# crlnumber must also be commented out to leave a V1 CRL.
# crl_extensions        = crl_ext

default_days    = 365                   # how long to certify for
default_crl_days= 30                    # how long before next CRL
default_md      = sha256                # use public key default MD
preserve        = no                    # keep passed DN ordering

# A few difference way of specifying how similar the request should look
# For type CA, the listed attributes must be the same, and the optional
# and supplied fields are just that :-)
policy          = policy_match

# For the CA policy
[ policy_match ]
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = supplied
userName                = supplied

# For the 'anything' policy
# At this point in time, you must list all acceptable 'object'
# types.
[ policy_anything ]
countryName             = optional
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional
userName                = optional

####################################################################
[ req ]
default_bits            = 2048
default_keyfile         = privkey.pem
distinguished_name      = req_distinguished_name
attributes              = req_attributes
x509_extensions = v3_ca # The extensions to add to the self signed cert

# Passwords for private keys if not present they will be prompted for
# input_password = secret
# output_password = secret

# This sets a mask for permitted string types. There are several options.
# default: PrintableString, T61String, BMPString.
# pkix   : PrintableString, BMPString (PKIX recommendation before 2004)
# utf8only: only UTF8Strings (PKIX recommendation after 2004).
# nombstr : PrintableString, T61String (no BMPStrings or UTF8Strings).
# MASK:XXXX a literal mask value.
# WARNING: ancient versions of Netscape crash on BMPStrings or UTF8Strings.
string_mask = utf8only

# req_extensions = v3_req # The extensions to add to a certificate request

[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
countryName_default             = US
countryName_min                 = 2
countryName_max                 = 2

stateOrProvinceName             = State or Province Name (full name)
stateOrProvinceName_default     = Maryland

localityName                    = Locality Name (eg, city)
localityName_default            = Columbia

0.organizationName              = Organization Name (eg, company)
0.organizationName_default      = ufts

# we can do this but it is not needed normally :-)
#1.organizationName             = Second Organization Name (eg, company)
#1.organizationName_default     =

organizationalUnitName          = Organizational Unit Name (eg, section)
organizationalUnitName_default  = ufts

commonName                      = Common Name (e.g. server FQDN or YOUR name)
commonName_max                  = 64

emailAddress                    = Email Address
emailAddress_max                = 64

userName                        = User Name
userName_max                    = 64

# SET-ex3                       = SET extension number 3

[ req_attributes ]
challengePassword               = A challenge password
challengePassword_min           = 4
challengePassword_max           = 20

unstructuredName                = An optional company name

[ usr_cert ]

# These extensions are added when 'ca' signs a request.

# This goes against PKIX guidelines but some CAs do it and some software
# requires this to avoid interpreting an end user certificate as a CA.

basicConstraints=CA:FALSE

# Here are some examples of the usage of nsCertType. If it is omitted
# the certificate can be used for anything *except* object signing.

# This is OK for an SSL server.
# nsCertType                    = server

# For an object signing certificate this would be used.
# nsCertType = objsign

# For normal client use this is typical
# nsCertType = client, email

# and for everything including object signing:
# nsCertType = client, email, objsign

# This is typical in keyUsage for a client certificate.
# keyUsage = nonRepudiation, digitalSignature, keyEncipherment

# This will be displayed in Netscape's comment listbox.
nsComment                       = "OpenSSL Generated Certificate"

# PKIX recommendations harmless if included in all certificates.
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer

# This stuff is for subjectAltName and issuerAltname.
# Import the email address.
# subjectAltName=email:copy
# An alternative to produce certificates that aren't
# deprecated according to PKIX.
# subjectAltName=email:move

# Copy subject details
# issuerAltName=issuer:copy

#nsCaRevocationUrl              = http://www.domain.dom/ca-crl.pem
#nsBaseUrl
#nsRevocationUrl
#nsRenewalUrl
#nsCaPolicyUrl
#nsSslServerName

# This is required for TSA certificates.
# extendedKeyUsage = critical,timeStamping

[ v3_req ]

# Extensions to add to a certificate request

basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment

[ v3_ca ]


# Extensions for a typical CA


# PKIX recommendation.

subjectKeyIdentifier=hash

authorityKeyIdentifier=keyid:always,issuer

basicConstraints = critical,CA:true

# Key usage: this is typical for a CA certificate. However since it will
# prevent it being used as an test self-signed certificate it is best
# left out by default.
# keyUsage = cRLSign, keyCertSign

# Some might want this also
# nsCertType = sslCA, emailCA

# Include email address in subject alt name: another PKIX recommendation
# subjectAltName=email:copy
# Copy issuer details
# issuerAltName=issuer:copy

# DER hex encoding of an extension: beware experts only!
# obj=DER:02:03
# Where 'obj' is a standard or added object
# You can even override a supported extension:
# basicConstraints= critical, DER:30:03:01:01:FF

[ crl_ext ]

# CRL extensions.
# Only issuerAltName and authorityKeyIdentifier make any sense in a CRL.

# issuerAltName=issuer:copy
authorityKeyIdentifier=keyid:always

[ proxy_cert_ext ]
# These extensions should be added when creating a proxy certificate

# This goes against PKIX guidelines but some CAs do it and some software
# requires this to avoid interpreting an end user certificate as a CA.

basicConstraints=CA:FALSE

# Here are some examples of the usage of nsCertType. If it is omitted
# the certificate can be used for anything *except* object signing.

# This is OK for an SSL server.
# nsCertType                    = server

# For an object signing certificate this would be used.
# nsCertType = objsign

# For normal client use this is typical
# nsCertType = client, email

# and for everything including object signing:
# nsCertType = client, email, objsign

# This is typical in keyUsage for a client certificate.
# keyUsage = nonRepudiation, digitalSignature, keyEncipherment

# This will be displayed in Netscape's comment listbox.
nsComment                       = "OpenSSL Generated Certificate"

# PKIX recommendations harmless if included in all certificates.
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer

# This stuff is for subjectAltName and issuerAltname.
# Import the email address.
# subjectAltName=email:copy
# An alternative to produce certificates that aren't
# deprecated according to PKIX.
# subjectAltName=email:move

# Copy subject details
# issuerAltName=issuer:copy

#nsCaRevocationUrl              = http://www.domain.dom/ca-crl.pem
#nsBaseUrl
#nsRevocationUrl
#nsRenewalUrl
#nsCaPolicyUrl
#nsSslServerName

# This really needs to be in place for it to be a proxy certificate.
proxyCertInfo=critical,language:id-ppl-anyLanguage,pathlen:3,policy:foo

####################################################################
[ tsa ]

default_tsa = tsa_config1       # the default TSA section

[ tsa_config1 ]

# These are used by the TSA reply generation only.
dir             = .                     # TSA root directory
serial          = $dir/tsaserial        # The current serial number (mandatory)
crypto_device   = builtin               # OpenSSL engine to use for signing
signer_cert     = $dir/tsacert.pem      # The TSA signing certificate
                                        # (optional)
certs           = $dir/cacert.pem       # Certificate chain to include in reply
                                        # (optional)
signer_key      = $dir/private/tsakey.pem # The TSA private key (optional)
signer_digest  = sha256                 # Signing digest to use. (Optional)
default_policy  = tsa_policy1           # Policy if request did not specify it
                                        # (optional)
other_policies  = tsa_policy2, tsa_policy3      # acceptable policies (optional)
digests     = sha1, sha256, sha384, sha512  # Acceptable message digests (mandatory)
accuracy        = secs:1, millisecs:500, microsecs:100  # (optional)
clock_precision_digits  = 0     # number of digits after dot. (optional)
ordering                = yes   # Is ordering defined for timestamps?
                                # (optional, default: no)
tsa_name                = yes   # Must the TSA name be included in the reply?
                                # (optional, default: no)
ess_cert_id_chain       = no    # Must the ESS cert id chain be included?
                                # (optional, default: no)
ess_cert_id_alg         = sha1  # algorithm to compute certificate
                                # identifier (optional, default: sha1)
```

#### CA File Layout
```
$ tree config/certs/
config/certs/
├── ca.crt
├── client1.crt
├── client1.csr
├── client1.key
├── client1.p12
├── crlnumber
├── crlnumber.old
├── index.txt
├── index.txt.attr
├── index.txt.attr.old
├── index.txt.old
├── newcerts
│   ├── 01.pem
│   └── 02.pem
├── newfile.crt.pem
├── private
│   └── ca.key
├── root_crl.pem
├── serial
├── serial.old
├── ufts.crt
├── ufts.csr
├── ufts.key
└── ufts.pem

2 directories, 22 files
```

#### Build CA Infrastructure if you do not have an Enterprise one
```
cd config/certs
mkdir private/ newcerts/
echo 1000 > crlnumber
touch index.txt
echo 01 > serial
openssl genrsa -out private/ca.key 4096
openssl req -new -x509 -days 1826 -key private/ca.key -out ca.crt
```

#### Create Haproxy LB Cert
```
openssl genrsa -out ufts.key 2048
openssl req -new -key ufts.key -out ufts.csr -subj '/userName=ufts/CN=ufts/O=ufts/C=US/ST=Maryland/L=Columbia/emailAddress=no-reply@ufts.lab'
openssl ca -batch -notext -in ufts.csr -out ufts.crt
cat ufts.crt ufts.key > ufts.pem
```

#### Create Client Cert
```
openssl genrsa -out client1.key 2048
openssl req -new -key client1.key -out client1.csr -subj '/userName=client1/CN=firstname lastname/O=ufts/C=US/ST=Maryland/L=Columbia/emailAddress=client1@ufts.lab'
openssl ca -batch -notext -in client1.csr -out client1.crt
openssl pkcs12 -export -clcerts -in client1.crt -inkey client1.key -out client1.p12
```
**Note: CN format should be "firstname lastname"**

Take the p12 cert and import it into your browser and/or system keychain. Safari will use the system keychain, but Firefox manages its own certificate store. On Mac, I also manually trusted the certificate in the system keychain which may or may not be necessary but it seemed like a logical thing to do.


Here is a client cert request with custom OID (userName).
```
openssl req -new -key joe.key -out joe.csr -subj '/userName=joe/CN=Joe Alphonso/O=ufts/C=US/ST=Maryland/L=Columbia/emailAddress=jalphons@home-lab.local'
```
If you have other Custom OIDs in the DN subject line, then you'll want to either create a custom function for processing your cert in django_ssl_auth/cert.py and change the value of USER_DATA_FN in the Django settings file located in ufts/settings.py or modify the existing one referenced.

#### Validate Certs
This is optional but good to know if you've done everything correctly so far. If the cert isn't valid, the load balancer won't start up.
```
$ openssl verify -CAfile ca.crt ufts.pem
ufts.pem: OK
```
Repeat as desired for client certs.

#### Generate CRL
```
openssl ca -gencrl -out root_crl.pem
```

#### To Revoke a Client
```
openssl ca -revoke client1.crt
openssl ca  -gencrl -out root_crl.pem
```


## Configs
#### Update Django settings file
Go through the file carefully and change the following:
1. SECRET_KEY
2. Change DEBUG=False
3. DATABASES db name, user and password
4. Classification settings as appropriate
5. LICENSE_KEY and ACCESS_CODE
6. Comment out EMAIL_BACKEND and EMAIL_FILE_PATH
7. Uncomment EMAIL_HOST and EMAIL_PORT and update values
8. Uncomment EMAIL_HOST_USER and EMAIL_HOST_PASSWORD if not using anonymous smtp
9. Set EMAIL_USE_TLS=True if needed
10. Notice CELERY_BEAT_SCHEDULE at the bottom. You probably do not need to change these settings
    but this is where you would if needed.
11. Change reporting format(pdf,xlsx,docx) with REPORT_FORMAT near the bottom.

```
vim ufts/settings.py
```
#### IP address logging
Because we are using a proxy, in order for correct logging of IP addresses for uploads and downloads, we use a configurable library that attempts to choose the correct IP. By default, we configure it under the assumption that the deployed network is using a private IP space. If this is deployed in a public IP space, replace the IPWARE_META_PRECEDENCE_ORDER settings variable with the following:
```
IPWARE_META_PRECEDENCE_ORDER = (
     'HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR',  # <client>, <proxy1>, <proxy2>
     'HTTP_CLIENT_IP',
     'HTTP_X_REAL_IP',
     'HTTP_X_FORWARDED',
     'HTTP_X_CLUSTER_CLIENT_IP',
     'HTTP_FORWARDED_FOR',
     'HTTP_FORWARDED',
     'HTTP_VIA',
     'REMOTE_ADDR',
 )
```
#### Update domain in nginx config
```
vim config/nginx/conf.d/local.conf
```

#### Update domain and certs in haproxy config
```
vim config/consul/web-haproxy.ctmpl
```

#### Update IP Networks in Docker Compose Template
```
vim docker-compose.j2
```
Edit the networks at the bottom of the file if you need to. Make sure you also update the network
under the app service in this same file.

## Microservices management

### Install Docker and Docker Compose
Follow instructions for your OS on the official Docker website
https://docs.docker.com/get-docker/

Version used during development was 19.03

The Docker compose version used is 1.25.5

Instructions here:
https://docs.docker.com/compose/install/

### Install Python dependency
The only external dependencies required are ruamel.yaml and jinja2

Install directly if Internet access is available with
```
$ pip3 install ruamel.yaml jinja2
```

Otherwise, download the package (dependencies will automatically be downloaded), transfer to target system, and install
```
$ pip3 download ruamel.yaml jinja2
$ ls -l *.whl
-rw-r--r--  1 jalphonso  staff  125774 May 11 13:56 Jinja2-2.11.2-py2.py3-none-any.whl
-rw-r--r--  1 jalphonso  staff   18847 May 11 13:56 MarkupSafe-1.1.1-cp36-cp36m-macosx_10_6_intel.whl
-rw-r--r--  1 jalphonso  staff  111176 May 11 13:56 ruamel.yaml-0.16.10-py2.py3-none-any.whl
-rw-r--r--  1 jalphonso  staff  147211 May 11 13:56 ruamel.yaml.clib-0.2.0-cp36-cp36m-macosx_10_9_x86_64.whl
$ pip3 install *.whl
```

### Build Services
Only necessary if you do not have the docker images or want to do development
```
make develop
```

### Save Docker Images
Save your images after building if transferring to an offline network
```
make save
```
Or use the following shortcut to build and save in one step
```
make build_save_images
```

### Load Docker Images
If installing on system without Internet access take your saved docker images, place them in the docker-images folder in the root of the project. Then load them.

NOTE: The User ID(UID) and Group ID(GID) of the user that the application containers are running as are copied from the user running "make develop". These should match the user running the remaining commands below(ie. UID/GID need to match on development machine and production machine). It is not necessary that the user and group names match, just the IDs.
```
make load
```

Or use the following shortcut to load, install, start the project
```
make offline_install
```

### Prepare Services
```
make prepare
```

### Start Services
```
make start
```

### Setup DB for the first time
```
make migrate
```

### Monitor Services
```
make monitor
```
If you scale the app while tailing the logs you will need to reissue this command to get logs for the new services

If using the syslog driver for your Docker daemon, you'll have to monitor logs on your syslog server instead

### Stop Services
```
make stop
```

### Restart Services
```
make restart
```

### Scale Services
Scale App and Web Tiers to 3 containers each
```
make scale APP=3 WEB=3
```
Scale App and Web Tiers back down to 1 each
```
make scale
```

### Signal HAProxy or Nginx to reload config
```
docker kill -s HUP <container name>
```
There is a docker-compose equivalent command but you probably want to do one container at a time instead of the entire tier

### Restart App Tier
```
docker restart <container name>
```
Likewise, there is a docker-compose equivalent command but you probably want to do one container at a time instead of the entire tier unless there are disruptive code changes. In which case you should do this in a maintenance window.

**Do not issue a SIGHUP signal as this may cause problems. It is better to just restart this container.**

### Remove Services
```
make clean
```

### Cleanly restart app
```
make clean_start
```

### View running services
```
$ make status
docker ps -a
CONTAINER ID        IMAGE                           COMMAND                  CREATED             STATUS              PORTS                                                                      NAMES
cf67833f8531        consul-template:custom          "/bin/docker-entrypo…"   2 minutes ago       Up 2 minutes                                                                                   consul-tpl
77fb53b8af5a        ufts-app                        "gunicorn -w 3 --chd…"   2 minutes ago       Up 2 minutes        8000/tcp                                                                   app0
d638cd1986df        celery:custom                   "celery -A ufts beat…"   2 minutes ago       Up 2 minutes                                                                                   celery-beat
6b22988a6b0d        celery:custom                   "celery -A ufts work…"   2 minutes ago       Up 2 minutes                                                                                   celery
29821ba1bb28        postgres:10                     "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes        5432/tcp                                                                   db
37f7cc13f723        haproxy:custom                  "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes        0.0.0.0:443->443/tcp                                                       web-lb
a0a11219c8e8        redis:alpine                    "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes        6379/tcp                                                                   redis
364410c82a40        nginx:latest                    "nginx -g 'daemon of…"   2 minutes ago       Up 2 minutes        80/tcp                                                                     web0
38c84eb221bd        haproxy:custom                  "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes        8000/tcp                                                                   app-lb
e47a75761c78        gliderlabs/registrator:master   "/bin/registrator -i…"   3 minutes ago       Up 3 minutes                                                                                   registrator
4e5c68bdc96c        consul                          "docker-entrypoint.s…"   3 minutes ago       Up 3 minutes        8300-8302/tcp, 8301-8302/udp, 8600/tcp, 8600/udp, 0.0.0.0:8500->8500/tcp   consul
docker images
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
consul-template             custom              e399a9ad03c0        3 hours ago         333MB
celery                      custom              0ab36fdac6ac        3 hours ago         1.27GB
ufts-app                    latest              076e7c8dbd49        3 hours ago         1.27GB
haproxy                     custom              41733cdac60f        3 hours ago         92.4MB
redis                       alpine              7277f03c430e        26 hours ago        31.6MB
python                      3.6                 8802e0ebf8c7        2 days ago          914MB
hashicorp/consul-template   alpine              a09aa47bf9f9        4 days ago          17.2MB
consul                      latest              197999eb696c        7 days ago          116MB
postgres                    10                  b500168be260        8 days ago          200MB
nginx                       latest              602e111c06b6        8 days ago          127MB
haproxy                     latest              c033852569f1        8 days ago          92.4MB
gliderlabs/registrator      master              70855268d755        3 months ago        14.3MB
docker network ls
NETWORK ID          NAME                    DRIVER              SCOPE
3abc338a83b4        bridge                  bridge              local
80a147c6cebe        host                    host                local
ec2123227ffb        none                    null                local
f7e0f108cbd0        ufts_backend_network    bridge              local
c1ea5fbd637e        ufts_frontend_network   bridge              local
4f584f586b0a        ufts_redis_network      bridge              local
```

### Completely wipe docker environment and all application data
```
make wipe
```

### Wipe and reinstall
```
make fresh_install
```

### Load test data (Not for Production)
```
make testdata
```

### Change or Add multiple hostnames for the application to accept and respond

#### Python Django application
Config File: ufts/settings.py
```
ALLOWED_HOSTS = ['ufts.local', 'myweb.local']
```

#### Nginx web server
Config File: config/nginx/conf.d/local.conf
```
server_name ufts.local myweb.local;
```

#### Web HAProxy LB
Config File: config/consul/web-haproxy.ctmpl

frontend setting
```
acl host_ufts hdr(host) -i ufts.local myweb.local
```

backend setting (only need primary hostname as its used internally for a health check)
```
option httpchk HEAD /static/img/Juniper-Logo.svg HTTP/1.1\r\nHost:\ ufts.local
```

#### App HAProxy LB
Config File: config/consul/app-haproxy.ctmp

backend setting (only need primary hostname as its used internally for a health check)
```
tcp-check send HEAD /about HTTP/1.1\r\nHost:\ ufts.local
```

Afterwards issue a `make restart` for changes to take effect.
