from pymysql import connect


def create_sync_con():
    con = connect(host='localhost', user='root', db='reshalaa_bot',
                  password='Andrei123009')
    cur = con.cursor()
    return con, cur


def sync_get_context():
    con, cur = create_sync_con()
    cur.execute('select username from user where tel_id = {0}'.format('420404892'))
    context = cur.fetchone()
    con.close()
    print(context)

    if context is None:
        return None

    return context[0]


def send_price_c(ord_id, auth):
    con, cur = create_sync_con()

    cur.execute('select * from reshalaa_bot.db_manager_ord_auth_price where ord_id = %s and tel_id = %s',
                (ord_id, auth))
    info = cur.fetchone()
    info = info

    new_price = 0
    price = info[2]

    if int(price) <= 50:
        new_price = int(price) + 50
    elif int(price) > 50 and int(price) < 99:
        new_price = int(price) + 70
    elif int(price) > 99 and int(price) <= 500:
        new_price = int(price) + 100
    elif int(price) > 500:
        new_price = int(price) + (int(price) * (20 / 100))
    new_price = round(int(new_price))

    cur.execute('select username from reshalaa_bot.db_manager_order where ord_id = %s', (ord_id))
    username = cur.fetchone()

    try:
        cur.execute('insert into reshalaa_bot.db_manager_cust_pri values (%s, %s, %s, %s, %s, %s, %s)',
                    (info[0], info[1], info[2], info[3], info[4], new_price, username))
        con.commit()
    except:
        cur.execute('delete from reshalaa_bot.db_manager_cust_pri where ord_id = %s', info[0])
        con.commit()
        cur.execute('insert into reshalaa_bot.db_manager_cust_pri values (%s, %s, %s, %s, %s, %s, %s)',
                    (info[0], info[1], info[2], info[3], info[4], new_price, username))
        con.commit()

    cur.execute('select * from reshalaa_bot.db_manager_order where ord_id = %s', ord_id)
    order = cur.fetchone()
    order = order
    try:
        cur.execute(
            'insert into reshalaa_bot.db_manager_priceo values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (order[0], order[1], order[2], order[3], order[4], order[5], order[6],
             order[7], order[8], order[9], order[10], order[11], order[12], '0'))
        con.commit()
    except:
        pass

    '''cur.execute('delete from reshalaa_bot.db_manager_ord_auth_price where ord_id = %s', ord_id)
    con.commit()'''

    '''cur.execute('delete from reshalaa_bot.db_manager_order where ord_id = %s', ord_id)
    con.commit()'''

    cur.execute('select tel_id from reshalaa_bot.user where username = %s', (username))
    tel_id = cur.fetchone()

    con.close()

    return tel_id


def send_price_c_2(ord_id, auth, price):
    con, cur = create_sync_con()

    cur.execute('select * from reshalaa_bot.db_manager_ord_auth_price where ord_id = %s and tel_id = %s',
                (ord_id, auth))
    info = cur.fetchone()
    info = info

    new_price = price

    cur.execute('select username from reshalaa_bot.db_manager_order where ord_id = %s', (ord_id))
    username = cur.fetchone()

    cur.execute('insert into reshalaa_bot.db_manager_cust_pri values (%s, %s, %s, %s, %s, %s, %s)',
                (info[0], info[1], info[2], info[3], info[4], new_price, username))
    con.commit()

    cur.execute('select * from reshalaa_bot.db_manager_order where ord_id = %s', ord_id)
    order = cur.fetchone()
    order = order

    cur.execute(
        'insert into reshalaa_bot.db_manager_priceo values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (order[0], order[1], order[2], order[3], order[4], order[5], order[6],
         order[7], order[8], order[9], order[10], order[11], order[12], '0'))
    con.commit()

    '''cur.execute('delete from reshalaa_bot.db_manager_ord_auth_price where ord_id = %s', ord_id)
    con.commit()'''

    cur.execute('delete from reshalaa_bot.db_manager_order where ord_id = %s', ord_id)
    con.commit()

    cur.execute('select tel_id from reshalaa_bot.user where username = %s', (username))
    tel_id = cur.fetchone()

    con.close()

    return tel_id


def get_new_cost(tel_id, ord_id):
    con, cur = create_sync_con()

    cur.execute('SELECT customer_pr FROM reshalaa_bot.db_manager_cust_pri where ord_id = %s', ord_id)
    orders = cur.fetchone()

    cur.execute('SELECT count_b FROM reshalaa_bot.bonuses where tel_id = %s', tel_id)
    bonuses = cur.fetchone()

    con.close()
    return orders[0], bonuses[0]


def check_and_send_order(ord_id):
    con, cur = create_sync_con()

    cur.execute('SELECT payment FROM reshalaa_bot.db_manager_waito where ord_id = %s', ord_id)
    payment = cur.fetchone()
    payment = int(payment[0])

    cur.execute('SELECT customer_pr FROM reshalaa_bot.db_manager_customer_price where ord_id = %s', ord_id)
    customer_price = cur.fetchone()
    customer_price = int(customer_price[0])

    cur.execute('SELECT customer_username FROM reshalaa_bot.db_manager_customer_price where ord_id = %s', ord_id)
    username = cur.fetchone()

    cur.execute('SELECT tel_id FROM reshalaa_bot.user where username = %s', username)
    tel_id = cur.fetchone()

    cur.execute('SELECT author_links FROM reshalaa_bot.db_manager_waito where ord_id = %s', ord_id)
    files = cur.fetchone()

    cur.execute('SELECT author FROM reshalaa_bot.db_manager_waito where ord_id = %s', ord_id)
    author = cur.fetchone()

    cur.execute('SELECT * FROM reshalaa_bot.authors where username = %s', author[0])
    author_info = cur.fetchone()

    cur.execute('SELECT price FROM reshalaa_bot.db_manager_customer_price where ord_id = %s', ord_id)
    cost = cur.fetchone()

    cur.execute(f'update reshalaa_bot.authors set balance = {int(author_info[12]) + int(cost[0])} where tel_id = {author_info[0]}')
    con.commit()

    con.close()

    if payment >= customer_price:
        return 1, tel_id[0], files[0]
    else:
        return customer_price - payment, tel_id[0], files[0]


def payok_db(ord_id):
    con, cur = create_sync_con()

    cur.execute('delete from reshalaa_bot.db_manager_dpo where ord_id = %s', ord_id)
    con.commit()

    con.close()


def add_dpo(ord_id):
    con, cur = create_sync_con()

    cur.execute('SELECT author FROM reshalaa_bot.db_manager_waito where ord_id = %s', ord_id)
    author = cur.fetchone()

    cur.execute('SELECT * FROM reshalaa_bot.authors where username = %s', author[0])
    author_info = cur.fetchone()

    cur.execute('SELECT price FROM reshalaa_bot.db_manager_customer_price where ord_id = %s', ord_id)
    cost = cur.fetchone()

    cur.execute(
        'insert into reshalaa_bot.db_manager_dpo values (%s, %s, %s, %s, %s)',
        (ord_id, author_info[9], cost, author_info[6], author_info[2]))
    con.commit()

    con.close()


def get_links(ord_id, table):
    con, cur = create_sync_con()
    int(ord_id)

    cur.execute(f'SELECT links FROM reshalaa_bot.{table} where ord_id = {ord_id}')
    links = cur.fetchone()
    con.close()
    return links[0]


def get_links_plus_author(ord_id, table):
    con, cur = create_sync_con()
    int(ord_id)

    cur.execute(f'SELECT links FROM reshalaa_bot.{table} where ord_id = {ord_id}')
    links = cur.fetchone()
    cur.execute(f'SELECT author_links FROM reshalaa_bot.{table} where ord_id = {ord_id}')
    author_links = cur.fetchone()
    con.close()
    return links[0], author_links[0]


def for_start():
    con, cur = create_sync_con()

    cur.execute(f'SELECT count(ord_id) FROM reshalaa_bot.db_manager_order')
    wait = cur.fetchone()

    cur.execute(f'SELECT count(ord_id) FROM reshalaa_bot.db_manager_priceo')
    price = cur.fetchone()

    cur.execute(f'SELECT count(ord_id) FROM reshalaa_bot.db_manager_activeo')
    active = cur.fetchone()

    cur.execute(f'SELECT count(ord_id) FROM reshalaa_bot.db_manager_waito')
    prov = cur.fetchone()

    con.close()
    return wait[0], price[0], active[0], prov[0]


def for_authors():
    con, cur = create_sync_con()

    cur.execute(f'SELECT * FROM reshalaa_bot.authors')
    authors = cur.fetchall()
    con.close()
    return authors


def for_users():
    con, cur = create_sync_con()

    cur.execute(f'SELECT * FROM reshalaa_bot.user')
    users = cur.fetchall()
    con.close()
    return users


def get_authors_count(ord_id):
    con, cur = create_sync_con()
    cur.execute(f'SELECT count(ord_id) FROM reshalaa_bot.db_manager_ord_auth_price where ord_id = {ord_id}')
    count = cur.fetchone()
    con.close()
    return count[0]


def get_customer_and_delete_order(ord_id):
    con, cur = create_sync_con()
    cur.execute(f'SELECT tel_id FROM reshalaa_bot.db_manager_order where ord_id = {ord_id}')
    count = cur.fetchone()
    cur.execute('delete from reshalaa_bot.db_manager_order where ord_id = %s', ord_id)
    con.commit()
    cur.execute('delete from reshalaa_bot.db_manager_ord_auth_price where ord_id = %s', ord_id)
    con.commit()
    con.close()
    return count[0]


def get_new_order(ord_id):
    con, cur = create_sync_con()
    cur.execute('select * from reshalaa_bot.db_manager_order where ord_id = {0}'.format(ord_id))
    order = cur.fetchone()
    con.close()
    return order


def get_user_t(tel_id):
    con, cur = create_sync_con()
    cur.execute('select * from user where tel_id = %s', (tel_id))
    user = cur.fetchone()
    con.close()

    if user is None:
        return None
    return user


def get_authors(ord_id):
    con, cur = create_sync_con()
    cur.execute('select predm from reshalaa_bot.db_manager_order where ord_id = {0}'.format(ord_id))
    predm = cur.fetchone()
    predm = '%' + predm[0] + '%'
    c = 'wait_confirm'
    cur.execute(f'SELECT tel_id FROM reshalaa_bot.authors where predm like "{predm}" and context != {c}')
    authors = cur.fetchall()
    if predm == 'Другое':
        cur.execute(f'SELECT tel_id FROM reshalaa_bot.authors')
        authors = cur.fetchall()
    con.close()
    return authors


def get_docs(ord_id):
    con, cur = create_sync_con()
    cur.execute('select * from reshalaa_bot.files where ord_id = {0}'.format(ord_id))
    context = cur.fetchall()
    con.close()
    if len(context) < 1:
        return False
    return context


def set_b_count_tel_id(tel_id):
    con, cur = create_sync_con()
    st = ""
    cur.execute(f'insert into reshalaa_bot.site_context values ({tel_id}, {0})')
    con.commit()
    con.close()
    return


def get_b_count_tel_id():
    con, cur = create_sync_con()
    cur.execute(f'select * from reshalaa_bot.site_context')
    context = cur.fetchone()
    con.close()
    return context


def get_customer_info(ord_id):
    con, cur = create_sync_con()
    cur.execute(f'select tel_id from reshalaa_bot.db_manager_order where ord_id={ord_id}')
    tel_id = cur.fetchone()
    cur.execute(f'select phone_number from reshalaa_bot.user where tel_id={tel_id[0]}')
    phone_number = cur.fetchone()
    con.close()
    return phone_number


def get_authors_balance():
    con, cur = create_sync_con()
    cur.execute(f'select * from authors')
    info = cur.fetchall()
    con.close()
    return info


def get_ord_auth_price(ord_id):
    con, cur = create_sync_con()
    cur.execute(f'select * from reshalaa_bot.db_manager_ord_auth_price where ord_id = {ord_id}')
    info = cur.fetchall()
    con.close()
    return info

def get_author(username):
    con, cur = create_sync_con()
    print(username)
    cur.execute('select tel_id from reshalaa_bot.user where username = %s', (username))
    tel_id = cur.fetchone()
    return tel_id[0]
