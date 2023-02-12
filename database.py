from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

X2Y2_LOANS_SCHEMA = """CREATE TABLE x2y2_loans (
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

X2Y2_LIQUIDATIONS_SCHEMA = """CREATE TABLE x2y2_liquidations (
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

X2Y2_REPAIDS_SCHEMA = """CREATE TABLE x2y2_repaids (
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

X2Y2_CANCELLED_SCHEMA = """CREATE TABLE x2y2_nonce_cancelled (
    nonce text,
    block_time timestamp,
    block_number text,
    lender text,
    txhash text
);"""

ARCADE_LOANS_SCHEMA = """CREATE TABLE arcade_loans (
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
    txhash text,
    state text,
    num_installments int,
    num_installments_paid int,
    balance text,
    balance_paid text,
    late_fees_accrued text,
    interest_rate text
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

def insert_into_arcade_loans(values):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.executemany("INSERT INTO arcade_loans (loan_id, block_time, block_number, borrower, lender, borrow_amount, borrow_asset, loan_duration, loan_start, loan_end, loan_repay_amount, nft_asset, nft_token_id, txhash, state, num_installments, num_installments_paid, balance, balance_paid, late_fees_accrued, interest_rate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE loan_id=VALUES(loan_id), block_time=VALUES(block_time), block_number=VALUES(block_number), borrower=VALUES(borrower), lender=VALUES(lender), borrow_amount=VALUES(borrow_amount), borrow_asset=VALUES(borrow_asset), loan_duration=VALUES(loan_duration), loan_start=VALUES(loan_start), loan_end=VALUES(loan_end), loan_repay_amount=VALUES(loan_repay_amount), nft_asset=VALUES(nft_asset), nft_token_id=VALUES(nft_token_id), txhash=VALUES(txhash), state=VALUES(state), num_installments=VALUES(num_installments), num_installments_paid=VALUES(num_installments_paid), balance=VALUES(balance), balance_paid=VALUES(balance_paid), late_fees_accrued=VALUES(late_fees_accrued), interest_rate=VALUES(interest_rate)", values)
    except Exception as e:
        print("failed to insert", e)
    
    conn.commit()
    print(f"Inserted {len(values)} rows")
    cur.close()
    conn.close()