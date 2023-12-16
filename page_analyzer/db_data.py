from datetime import datetime


def add_new_url(conn, url):
    """Create new name in database from url and return """
    with conn.cursor() as cur:
        cur.execute('''INSERT INTO urls (name, created_at) VALUES (%s, %s) ;''', (url, datetime.now()))


def is_url_exist(conn, url):
    """Check exist url in database and return ID or False"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM urls WHERE name=%s ;""", (url, ))
        response = cur.fetchone()
    if response:
        return response[0]
    return False


def get_data_by_id(conn, id):
    """Return all column for selected ID"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM urls WHERE id=%s ;""", (id, ))
        result = cur.fetchone()
    return result


def get_all_urls(conn):
    """Return id, name, last check data and status code for selected id"""
    with conn.cursor() as cur:
        cur.execute("""SELECT urls.id, urls.name, url_checks.created_at, url_checks.status_code
                            FROM urls LEFT JOIN (
                                SELECT DISTINCT ON (url_id) url_id, created_at, status_code
                                FROM url_checks
                                ORDER BY url_id, created_at DESC) AS url_checks ON urls.id = url_checks.url_id
                            ORDER BY urls.id DESC ;""")
        result = cur.fetchall()
    return result


def is_checks_exist(conn, id):
    """Check if exist and return bool"""
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM url_checks WHERE url_id=%s ;""", (id, ))
        response = cur.fetchone()
    if response:
        return True
    return False


def get_checks_by_id(conn, id):
    """Return all checks for selected id"""
    with conn.cursor() as cur:
        cur.execute("""SELECT id, status_code, h1, title, description, created_at FROM url_checks WHERE url_id=%s ORDER BY id DESC ;""", (id, ))
        result = cur.fetchall()
    return result


def add_new_check(conn, data):
    """Add check data to db"""
    # print(*data, sep="\n")
    time_ = datetime.now()
    # url_id, status_code, h1, title, description = data
    with conn.cursor() as cur:
        cur.execute('''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s) ;''', (*data, time_))
