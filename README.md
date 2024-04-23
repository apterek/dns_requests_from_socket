# dns_requests_from_socket

### Run the script as root because you need to access system sockets

```commandline
  python3 dns_from_socket.py -f ./filename -d IP_OF_DNS_SERVER -r 10
```

```commandline
The -f flag is used to set the name of the file that stores
the domain names for verification
```
```commandline
The -d flag is used to set the ip address of the DNS server
to which requests will be made
```
```commandline
The -r flag is used to set the number of repetitions
of domain name requests from a file
```
    
### test_domains.txt example of a file with domain names

### P.S. 
#### For better performance use python 3.11 or higher