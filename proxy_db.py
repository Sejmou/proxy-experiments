import sqlite3
import argparse
from pydantic import validate_call
from typing import List

TABLE_FILE = 'proxies.db'


def execute_query(query: str):
    with sqlite3.connect(TABLE_FILE) as conn:
        c = conn.cursor()
        c.execute(query)
        conn.commit()

def create_table():
    execute_query('''
    CREATE TABLE proxies (
        ip_and_port VARCHAR NOT NULL,
        last_used_at DATETIME,
        last_blocked_at DATETIME,
        account_id INT NOT NULL
    );''')

@validate_call
def add_proxies(proxies: List[str], account_id: int):
    for proxy in proxies:
        execute_query(f'INSERT INTO proxies (ip_and_port, account_id) VALUES ("{proxy}", {account_id});')
        print(f'Added proxy {proxy} for account {account_id}')

@validate_call
def add_proxies_from_file(filepath: str, account_id: int):
    with open(filepath) as f:
        proxies = f.readlines()
        add_proxies(proxies, account_id)

def add_proxies_handler(args):
    add_proxies_from_file(args.file, args.account_id)


def remove_proxy(ip_and_port: str):
    execute_query(f'DELETE FROM proxies WHERE ip_and_port="{ip_and_port}";')
    print(f'Removed proxy {ip_and_port}')

def print_proxies(account_id: int):
    with sqlite3.connect(TABLE_FILE) as conn:
        c = conn.cursor()
        c.execute(f'SELECT ip_and_port FROM proxies WHERE account_id={account_id};')
        proxies = c.fetchall()
        print(f'Proxies for account {account_id}:')
        for proxy in proxies:
            print(proxy[0])
    
def delete_proxies_for_account(account_id: int):
    execute_query(f'DELETE FROM proxies WHERE account_id={account_id};')
    print(f'Removed all proxies for account {account_id}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', title='commands')

    parser_create_table = subparsers.add_parser('create_table', help='creates the proxies table')
    parser_create_table.set_defaults(func=create_table)

    parser_add_proxies = subparsers.add_parser('add_proxies', help='add new proxies')
    parser_add_proxies.add_argument('file', type=str, help='path to file with proxies')
    parser_add_proxies.add_argument('account_id', type=int, help='account id to associate the proxies with')
    parser_add_proxies.set_defaults(func=add_proxies_handler)

    parser_delete_account_proxies = subparsers.add_parser('delete_account_proxies', help='delete all proxies for an account')
    parser_delete_account_proxies.add_argument('account_id', type=int, help='account id to delete proxies for')
    parser_delete_account_proxies.set_defaults(func=delete_proxies_for_account)

    args = parser.parse_args()
    if args.command == 'create_table':
        create_table()
    elif args.command == 'add_proxies':
        add_proxies_handler(args)
    elif args.command == 'delete_account_proxies':
        delete_proxies_for_account(args.account_id)
    else:
        parser.print_help()

