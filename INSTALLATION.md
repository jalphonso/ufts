# INSTALLATION

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
openssl req -new -key client1.key -out client1.csr -subj '/userName=client1/CN=client1/O=ufts/C=US/ST=Maryland/L=Columbia/emailAddress=client1@ufts.lab'
openssl ca -batch -notext -in client1.csr -out client1.crt
openssl pkcs12 -export -clcerts -in client1.crt -inkey client1.key -out client1.p12
```
Take the p12 cert and import it into your browser and/or system keychain. Safari will use the system keychain, but Firefox manages its own certificate store. On Mac, I also manually trusted the certificate in the system keychain which may or may not be necessary but it seemed like a logical thing to do.


Here is a client cert request with custom OID (userName).
```
openssl req -new -key joe.key -out joe.csr -subj '/userName=joe/CN=Joe Alphonso/O=ufts/C=US/ST=Maryland/L=Columbia/emailAddress=jalphons@home-lab.local'
```
If you have other Custom OIDs in the DN subject line, then you'll want to either create a custom function for processing your cert in django_ssl_auth/cert.py and change the value of USER_DATA_FN in the Django settings file located in ufts/settings.py or modify the existing one referenced.

#### Generate CRL
```
openssl ca -gencrl -out root_crl.pem
```

#### To Revoke a Client
```
openssl ca -revoke client1.crt
openssl ca  -gencrl -out root_crl.pem
```

## Create Application Log directory
```
mkdir logs
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

```
vim ufts/settings.py
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

The Docker compose version used is 1.25.5 which we install using pip. To install system wide you will need superuser privileges; otherwise, you can use a virtualenv.

To create and use the virtualenv:
```
make venv
. .venv/bin/activate
```
If using a virtualenv, you'll need to ensure it is activated in all terminals where you run docker-compose commands. The helper shell scripts will do this automatically when needed.

### Build Services
```
make install
```

### Start Services
```
./start_app.sh
```

### Setup DB for the first time
```
docker-compose exec app0 bash
python manage.py migrate
```

### Monitor Services
```
./monitor_app.sh
```
If you scale the app while tailing the logs you will need to reissue this command to get logs for the new services

If using the syslog driver for your Docker daemon, you'll have to monitor logs on your syslog server instead

### Stop Services
```
./stop_app.sh
```

### Restart Services
```
./restart_app.sh
```

### Scale Services
Scale App and Web Tiers to 3 containers each
```
./scale_app.sh 3 3
```
Scale App and Web Tiers back down to 1 each
```
./scale_app.sh
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
make clean && make install && make start
```

### View running services
```
$ docker ps
CONTAINER ID        IMAGE                           COMMAND                  CREATED             STATUS              PORTS                                                                      NAMES
960b93537e5d        nginx:latest                    "nginx -g 'daemon of…"   17 minutes ago      Up 17 minutes       80/tcp                                                                     web1
71a0bc44210d        ufts-app                        "gunicorn -w 3 --chd…"   17 minutes ago      Up 17 minutes       8000/tcp                                                                   app1
cd3886cf6bde        consul-template:custom          "/bin/docker-entrypo…"   17 minutes ago      Up 17 minutes                                                                                  consul-tpl
2d4b12bbf9e7        ufts-app                        "gunicorn -w 3 --chd…"   51 minutes ago      Up 51 minutes       8000/tcp                                                                   app0
0c7d8583c264        celery                          "celery -A ufts beat…"   51 minutes ago      Up 51 minutes                                                                                  celery-beat
ed35fd259916        celery                          "celery -A ufts work…"   51 minutes ago      Up 51 minutes                                                                                  celery
3866422bbf60        nginx:latest                    "nginx -g 'daemon of…"   51 minutes ago      Up 51 minutes       80/tcp                                                                     web0
6debc8fc23c4        haproxy:custom                  "/docker-entrypoint.…"   51 minutes ago      Up 51 minutes       8000/tcp                                                                   app-lb
bed8414fadec        postgres:10                     "docker-entrypoint.s…"   51 minutes ago      Up 51 minutes       5432/tcp                                                                   db
d82c91bb8013        redis:alpine                    "docker-entrypoint.s…"   51 minutes ago      Up 51 minutes       6379/tcp                                                                   redis
03c6aaeaf3e1        haproxy:custom                  "/docker-entrypoint.…"   51 minutes ago      Up 51 minutes       0.0.0.0:443->443/tcp                                                       web-lb
016a61671fbe        gliderlabs/registrator:master   "/bin/registrator -i…"   51 minutes ago      Up 51 minutes                                                                                  registrator
83d4b4e90166        consul                          "docker-entrypoint.s…"   51 minutes ago      Up 51 minutes       8300-8302/tcp, 8301-8302/udp, 8600/tcp, 8600/udp, 0.0.0.0:8500->8500/tcp   consul
```

### Completely wipe docker env: images/datastores
```
make wipe
```

