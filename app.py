from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key' #dont care about security 

#db helper
def get_db_connection():
    conn = sqlite3.connect('./db/term.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_Check():
    if 'username' not in session:
                return redirect(url_for('login'))

@app.route('/', methods =['GET'])
def home():
    result = login_Check()
    if result:  
        return result
    return redirect(url_for('dashboard'))

@app.route('/categories')
def categories():
    result = login_Check()
    if result:  
        return result

    username = session['username'] 
    conn = get_db_connection()

    query = '''
        SELECT DISTINCT CATEGORIES.catCode, CATEGORIES.catTitle, CATEGORIES.catDesc
        FROM CATEGORIES
        LEFT JOIN GROUPS ON CATEGORIES.catCode = GROUPS.accessLevel
        LEFT JOIN APART_OF ON GROUPS.groupName = APART_OF.groupName
        WHERE APART_OF.username = ?
           OR 'admin' IN (
               SELECT groupName
               FROM APART_OF
               WHERE username = ?
           );
    '''

    categories_data = conn.execute(query, (username, username)).fetchall()
    conn.close()

    return render_template('categories.html',
                           username=username,
                           categories_data=categories_data)

@app.route('/categories/<category_code>', methods=['GET'])  ##TAKE A BIT LOOK INTO THIS 
def catCode(category_code):
    result = login_Check()
    if result:  
        return result

    conn = get_db_connection()
    items = conn.execute('SELECT * FROM ITEMS WHERE catCode = ?;', (category_code,)).fetchall()
    cat = conn.execute('SELECT * FROM CATEGORIES WHERE catCode = ?;', (category_code,)).fetchone()
    conn.close()

    return render_template('category.html',
                            username=session['username'],
                            items=items,
                            category_data=cat)

@app.route('/items', methods=['GET'])
def items_page():
    result = login_Check()
    if result:  
        return result

    username = session['username']  
    conn = get_db_connection()
    
    query = '''
        SELECT DISTINCT ITEMS.SKU, ITEMS.itemTitle, ITEMS.itemDesc, ITEMS.catCode
        FROM ITEMS
        LEFT JOIN CATEGORIES ON ITEMS.catCode = CATEGORIES.catCode
        LEFT JOIN GROUPS ON CATEGORIES.catCode = GROUPS.accessLevel
        LEFT JOIN APART_OF ON GROUPS.groupName = APART_OF.groupName
        WHERE APART_OF.username = ?
           OR 'admin' IN (
               SELECT groupName
               FROM APART_OF
               WHERE username = ?
           );
    '''
    
    items = conn.execute(query, (username, username)).fetchall()
    conn.close()

    return render_template(
        'items.html',
        username=username,
        items=items
    )

@app.route("/items/<int:sku>", methods=["GET", "POST"])
def item(sku):
    result = login_Check()
    if result:  
        return result
    conn = get_db_connection()
    
    if request.method == "POST":
        item = conn.execute('SELECT * FROM ITEMS WHERE SKU = ?', (sku,)).fetchone() # get item
        if item and item['itemQty'] > 0:
            conn.execute("UPDATE ITEMS SET itemQty = itemQty - 1 WHERE SKU = ?", (sku,)) # remove 1 item if not zero
            
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Includes milliseconds
            username = session.get('username')  
            conn.execute(
                "INSERT INTO SIGNED_OUT (username, SKU, date, signOutQty) VALUES (?, ?, ?, ?)",
                (username, sku, date, 1)
            )
            
            conn.commit()        
        conn.close()
        return redirect(url_for('item', sku=sku))
    
    # GET request: Render the item details
    item = conn.execute('SELECT * FROM ITEMS WHERE SKU = ?', (sku,)).fetchone()
    conn.close()
    return render_template('item.html', item=item)

@app.route('/dashboard', methods =['GET','PUT'])
def dashboard():
    result = login_Check()
    if result:  
        return result

    if request.method == 'GET':
        conn = get_db_connection()

        total_items = conn.execute('SELECT COUNT(*) FROM ITEMS').fetchone()[0]
        total_categories = conn.execute('SELECT COUNT(*) FROM CATEGORIES').fetchone()[0]
        total_users = conn.execute('SELECT COUNT(*) FROM USERS').fetchone()[0]

        signed_out_data = conn.execute('''
            SELECT 
                SIGNED_OUT.SKU, 
                ITEMS.itemTitle, 
                SIGNED_OUT.date, 
                SIGNED_OUT.signOutQty
            FROM SIGNED_OUT
            JOIN ITEMS ON SIGNED_OUT.SKU = ITEMS.SKU
            WHERE SIGNED_OUT.username = ?
        ''', (session['username'],)).fetchall()

        conn.close()
        return render_template(
            'dashboard.html',
            username=session['username'],
            total_items=total_items,
            total_categories=total_categories,
            total_users=total_users,
            signed_out_data=signed_out_data
        )
    if request.method == 'PUT':

        data = request.get_json()
        new_quantity = data.get('quantity')
        sku = data.get('SKU')
        date = data.get('date')
        username = session['username'] 

        print(data)

        conn = get_db_connection()

        if new_quantity == 0: 
            conn.execute("DELETE FROM SIGNED_OUT WHERE SKU = ? AND username = ?  AND date = ?", (sku,username,date))
            conn.execute("UPDATE ITEMS SET itemQty = itemQty + 1 WHERE SKU = ?", (sku,)) #dupe this so no change to bug out

        else:
            conn.execute("""UPDATE SIGNED_OUT SET signOutQty = ? WHERE SKU = ?  AND username = ?  AND date = ?""", (new_quantity, sku, username,date))
            #to add the sign out back to the qty
            conn.execute("UPDATE ITEMS SET itemQty = itemQty + 1 WHERE SKU = ?", (sku,))

        conn.commit()
        conn.close()

        return jsonify({"status": "success"}), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM USERS WHERE username = ?', (username,)).fetchone()
        conn.close()

        #if user exists and password matches
        if user and user['password'] == password:
            session['username'] = username  
            return redirect(url_for('home')) #could change to dashboard later
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # removes user from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)