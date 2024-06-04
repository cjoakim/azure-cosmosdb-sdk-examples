"""
Usage:
  python main.py <func>
  -
  python main.py check_environment_variables
  -
  python main.py load_baseball_players <envname> <dbname>
  python main.py load_baseball_players local postgres
  python main.py load_baseball_players flex postgres
  python main.py load_baseball_players cosmos citus
  -
  python main.py load_baseball_batters local postgres
  python main.py load_baseball_batters flex postgres
  python main.py load_baseball_batters cosmos citus
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import base64
import json
import os
import sys
import time
import traceback

from docopt import docopt

from pysrc.util.counter import Counter
from pysrc.util.fs import FS 
from pysrc.util.pgclient import PGClient

BASEBALL_DOCUMENTS_FILE = '../../data/seanhahman-baseballdatabank/documents.json'

def print_options(msg=None):
    if msg:
        print(msg)
    arguments = docopt(__doc__, version='1.0.0')
    print(arguments)

def check_environment_variables():
    env_vars = [
        'USERNAME',
        'LOCAL_PG_USER',
        'LOCAL_PG_PASS',
        'AZURE_FLEX_PG_SERVER',
        'AZURE_FLEX_PG_USER',
        'AZURE_FLEX_PG_PASS',
        'AZURE_COSMOSDB_PG_USER',
        'AZURE_COSMOSDB_PG_PASS'
    ]
    for env_var in env_vars:
        print('check_env, {}: {}'.format(env_var, os.environ[env_var]))

def load_baseball_players(envname, dbname):
    try:
        opts = {
            'envname': envname,
            'dbname': dbname,
            'autocommit': True
        }
        if envname == 'cosmos':
            opts['port'] = '6432'  # pgbouncer
        print(f'opts: {opts}')

        client = PGClient(opts)
        cursor = client.get_cursor()
        columns_list = [
            'id',
            'player_id',
            'birth_year',
            'birth_country',
            'first_name',
            'last_name',
            'bats',
            'throws',
            'category',
            'primary_position',
            'primary_team',
            'debut_year',
            'final_year',
            'total_games',
            'teams_data',
            'pitching_data',
            'batting_data'
        ]
        columns_tup = str(tuple(columns_list)).replace("'",'')

        print('reading the baseball documents file ...')
        documents = FS.read_json(BASEBALL_DOCUMENTS_FILE)
        player_ids = sorted(documents.keys())

        for idx, pid in enumerate(player_ids):
            try:
                doc = documents[pid]
                if idx < 100_000:
                    id = idx + 1
                    pid = doc['playerID']
                    print(f'loading {id} {pid}')
                    column_values = []
                    column_values.append(id)
                    column_values.append(doc['playerID'])
                    column_values.append(doc['birthYear'])
                    column_values.append(doc['birthCountry'])
                    column_values.append(str(doc['nameFirst']).replace("'",''))
                    column_values.append(str(doc['nameLast']).replace("'",''))
                    column_values.append(doc['bats'])
                    column_values.append(doc['throws'])
                    column_values.append(doc['category'])
                    column_values.append(doc['primary_position'])
                    column_values.append(doc['teams']['primary_team'])
                    column_values.append(doc['debut_year'])
                    column_values.append(doc['final_year'])
                    column_values.append(doc['teams']['total_games'])
                    teams_data    = json.dumps(get_jsonb_value(doc, 'teams'))
                    pitching_data = json.dumps(get_jsonb_value(doc, 'pitching'))
                    batting_data  = json.dumps(get_jsonb_value(doc, 'batting'))
                    column_values.append(teams_data)
                    column_values.append(pitching_data)
                    column_values.append(batting_data)
                    values_tup = tuple(column_values)
                    sql_stmt = f'insert into players {columns_tup} values {values_tup};'
                    print(sql_stmt)
                    cursor.execute(sql_stmt)
            except Exception as e:
                print(f"Exception on doc: {idx} {values_tup}")
                print(str(e))
                print(traceback.format_exc())
    except Exception as excp:
        print(str(excp))
        print(traceback.format_exc())

    client.close()

def load_baseball_batters(envname, dbname):
    try:
        opts = {
            'envname': envname,
            'dbname': dbname,
            'autocommit': True
        }
        if envname == 'cosmos':
            opts['port'] = '6432'  # pgbouncer
        print(f'opts: {opts}')
        
        client = PGClient(opts)
        cursor = client.get_cursor()
        columns_list = [
            'id',
            'player_id',
            'birth_year',
            'birth_country',
            'first_name',
            'last_name',
            'bats',
            'throws',
            'primary_position',
            'primary_team',
            'debut_year',
            'final_year',
            'total_games',
            'atbats',
            'runs',
            'hits',
            'doubles',
            'triples',
            'homeruns',
            'rbi',
            'stolen_bases',
            'caught_stealing',
            'bb',
            'so',
            'ibb',
            'hbp',
            'sacfly',
            'runs_per_ab',
            'batting_avg',
            'double_avg',
            'triple_avg',
            'hr_avg',
            'rbi_avg',
            'bb_avg',
            'so_avg',
            'ibb_avg',
            'hbp_avg',
            'sb_pct'
        ]
        columns_tup = str(tuple(columns_list)).replace("'",'')

        print('reading the baseball documents file ...')
        documents = FS.read_json(BASEBALL_DOCUMENTS_FILE)
        player_ids = sorted(documents.keys())

        for idx, pid in enumerate(player_ids):
            try:
                doc = documents[pid]
                if doc['category'] == 'fielder':
                    if idx < 100_000:
                        id = idx + 1
                        pid = doc['playerID']
                        pp = doc['primary_position']
                        if pp == '?':
                            pass
                        else:
                            print(f'loading {id} {pid} {pp}')
                            column_values = []
                            column_values.append(id)
                            column_values.append(doc['playerID'])
                            column_values.append(doc['birthYear'])
                            column_values.append(doc['birthCountry'])
                            column_values.append(str(doc['nameFirst']).replace("'",''))
                            column_values.append(str(doc['nameLast']).replace("'",''))
                            column_values.append(doc['bats'])
                            column_values.append(doc['throws'])
                            column_values.append(doc['primary_position'])
                            column_values.append(doc['teams']['primary_team'])
                            column_values.append(doc['debut_year'])
                            column_values.append(doc['final_year'])
                            column_values.append(doc['teams']['total_games'])

                            batting = doc['batting']
                            column_values.append(batting['AB'])
                            column_values.append(batting['R'])
                            column_values.append(batting['H'])
                            column_values.append(batting['2B'])
                            column_values.append(batting['3B'])
                            column_values.append(batting['HR'])
                            column_values.append(batting['RBI'])
                            column_values.append(batting['SB'])
                            column_values.append(batting['CS'])
                            column_values.append(batting['BB'])
                            column_values.append(batting['SO'])
                            column_values.append(batting['IBB'])
                            column_values.append(batting['HBP'])
                            column_values.append(batting['SF'])

                            calculated = batting['calculated']
                            column_values.append(calculated['runs_per_ab'])
                            column_values.append(calculated['batting_avg'])
                            column_values.append(calculated['2b_avg'])
                            column_values.append(calculated['3b_avg'])
                            column_values.append(calculated['hr_avg'])
                            column_values.append(calculated['rbi_avg'])
                            column_values.append(calculated['bb_avg'])
                            column_values.append(calculated['so_avg'])
                            column_values.append(calculated['ibb_avg'])
                            column_values.append(calculated['hbp_avg'])
                            column_values.append(calculated['sb_pct'])
                            values_tup = tuple(column_values)
                            sql_stmt = f'insert into batters {columns_tup} values {values_tup};'
                            print(sql_stmt)
                            cursor.execute(sql_stmt)
            except Exception as e:
                print(f"Exception on doc: {idx} {values_tup}")
                print(str(e))
                print(str(sql_stmt))
                print(traceback.format_exc())
    except Exception as excp:
        print(str(excp))
        print(traceback.format_exc())

    client.close()

def get_jsonb_value(doc, key):
    if key in doc.keys():
        return doc[key]
    else:
        return {}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_options(None)
    else:
        func = sys.argv[1].lower()
        if func == 'check_environment_variables':
            check_environment_variables()
        elif func == 'load_baseball_players':
            envname, dbname = sys.argv[2], sys.argv[3]
            load_baseball_players(envname, dbname)
        elif func == 'load_baseball_batters':
            envname, dbname = sys.argv[2], sys.argv[3]
            load_baseball_batters(envname, dbname)
        else:
            print_options('Error: invalid function: {}'.format(func))
