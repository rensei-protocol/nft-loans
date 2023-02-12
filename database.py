from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

LOANS_SCHEMA = """CREATE TABLE x2y2_loans (
    loan_id int PRIMARY KEY,
    block_time timestamp,
    block_number text,
    borrower text,
    lender text,
    borrow_amount text,
    borrow_asset text,
    loan_duration text,
    loan_start timestamp,
    loan_end timestamp,
    loan_repay_amount text,
    nft_asset text,
    nft_token_id text,
    nft_is_collection boolean,
    txhash text,
    fee text,
    nonce text
);"""

LIQUIDATIONS_SCHEMA = """CREATE TABLE x2y2_liquidations (
    loan_id int PRIMARY KEY,
    block_time timestamp,
    block_number text,
    borrower text,
    lender text,
    borrow_amount text,
    nft_asset text,
    nft_token_id text,
    loan_liquidation_time timestamp,
    loan_maturity_time timestamp,
    txhash text
);"""

REPAIDS_SCHEMA = """CREATE TABLE x2y2_repaids (
    loan_id int PRIMARY KEY,
    block_time timestamp,
    block_number text,
    borrower text,
    lender text,
    borrow_amount text,
    borrow_asset text,
    loan_repay_amount text,
    nft_asset text,
    nft_token_id text,
    txhash text,
    fee text
);"""

CANCELLED_SCHEMA = """CREATE TABLE x2y2_nonce_cancelled (
    nonce text,
    block_time timestamp,
    block_number text,
    lender text,
    txhash text
);"""

def connect():
    return MySQLdb.connect(
        host= os.getenv("HOST"),
        user=os.getenv("USERNAME"),
        passwd= os.getenv("PASSWORD"),
        db= os.getenv("DATABASE"),
        ssl_mode = "VERIFY_IDENTITY",
        ssl      = {
            "ca": "/etc/ssl/cert.pem"
        }
    )

def create_table(schema):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(schema)
    except Exception as e:
        print("failed to create table", e)
    
    conn.commit()
    print("Created table")
    cur.close()
    conn.close()


def insert_into_loans(values):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.executemany("INSERT IGNORE INTO x2y2_loans VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s);", values)
    except Exception as e:
        print("failed to insert", e)
    
    conn.commit()
    print(f"Inserted {len(values)} rows")
    cur.close()
    conn.close()

def insert_into_repaids(values):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.executemany("INSERT IGNORE INTO x2y2_repaids VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
    except Exception as e:
        print("failed to insert", e)
    
    conn.commit()
    print(f"Inserted {len(values)} rows")
    cur.close()
    conn.close()


def insert_into_liquidations(values):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.executemany("INSERT IGNORE INTO x2y2_liquidations VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", values)
    except Exception as e:
        print("failed to insert", e)
    
    conn.commit()
    print(f"Inserted {len(values)} rows")
    cur.close()
    conn.close()

def insert_into_nonce_cancelled(values):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.executemany("INSERT INTO x2y2_nonce_cancelled VALUES(%s,%s,%s,%s,%s)", values)
    except Exception as e:
        print("failed to insert", e)
    
    conn.commit()
    print(f"Inserted {len(values)} rows")
    cur.close()
    conn.close()
