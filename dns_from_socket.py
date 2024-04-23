import random
import socket
import argparse


def prepare_requests(hostname):
    query_id = random.randint(1, 9999)
    dns_request = build_dns_request(query_id, hostname + "1")
    return dns_request


def dns_query(hostname, dns_server_ip='', dns_port=53):
    # Creating a socket and setting a timeout
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_socket.settimeout(2)

    dns_request = [prepare_requests(i.capitalize()) for i in hostname]

    try:
        for r in dns_request:
            dns_socket.sendto(r, (dns_server_ip, dns_port))

        response, _ = dns_socket.recvfrom(1024)

    except socket.timeout:
        print(f"DNS query for {hostname} timed out")

    finally:
        dns_socket.close()


def build_dns_request(query_id, hostname):
    # DNS Query Structure: Header + Question
    header = build_dns_header(query_id)
    question = build_dns_question(hostname)

    return header + question


def build_dns_header(query_id):
    # create DNS header
    header = query_id.to_bytes(2, byteorder='big')  # Идентификатор запроса
    header += b'\x01\x00'  # Flags: defined as a request (QR=0), operation code defined (OPCODE=0)
    header += b'\x00\x01'  # Number of requests (QDCOUNT)
    header += b'\x00\x00'  # Number of responses (ANCOUNT)
    header += b'\x00\x00'  # Number of sources of authority (NSCOUNT)
    header += b'\x00\x00'  # Number of additional information (ACCOUNT)

    return header


def build_dns_question(hostname):
    # forming a DNS question
    question = b''
    labels = hostname.split('.')
    for label in labels:
        length = len(label)
        question += bytes([length]) + label.encode('utf-8')
    question += b'\x00'  # end the question with a null byte
    question += b'\x00\x01'  # Request Type (A - IPv4)
    question += b'\x00\x01'  # Request class (IN - Internet)

    return question


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A simple script to send dns udp requests in multithreading')

    # Adding optional arguments
    parser.add_argument('-f', '--filename', type=str, help='file with dns domains')
    parser.add_argument('-d', '--dns', type=str, help='dns server ip address')
    parser.add_argument('-r', '--repeater', type=int, help='count of repeated', default=1)

    # Parse the command-line arguments
    args = parser.parse_args()
    file = args.filename
    dns_server = args.a
    with open(file, 'r') as f:
        domains = [i for i in f.read().split('\n')]

    for _ in range(args.repeater):
        dns_query(domains, dns_server_ip=dns_server, dns_port=53)
