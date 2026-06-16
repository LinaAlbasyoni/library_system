from flask import Flask, render_template, request, redirect
from database import (
    get_all_books, add_book, delete_book, update_book, deactivate_book, search_books,
    get_all_members, add_member, update_member, delete_member, deactivate_member, search_members,
    get_all_borrowed_books, add_borrowed, update_borrowed_status, search_borrowed, delete_borrowed
)

app = Flask(__name__)

# --- Main Dashboard ---
@app.route('/')
def index():
    return render_template('index.html', 
                           books=get_all_books(), 
                           members=get_all_members(), 
                           borrowed=get_all_borrowed_books())

# --- Book Routes ---
@app.route('/add_book', methods=['POST'])
def add_b():
    title, author = request.form.get('title'), request.form.get('author')
    if title and author: add_book(title, author)
    return redirect('/')

@app.route('/delete_book', methods=['POST'])
def delete_book_route(): 
    b_id = request.form.get('book_id')
    if b_id: delete_book(b_id)
    return redirect('/')

@app.route('/update_book', methods=['POST'])
def update_book_route():
    b_id, title, author = request.form.get('book_id'), request.form.get('title'), request.form.get('author')
    if b_id and title and author: update_book(b_id, title, author)
    return redirect('/')

@app.route('/deactivate_book', methods=['POST'])
def deactivate_book_route():
    if request.form.get('book_id'): deactivate_book(request.form.get('book_id'))
    return redirect('/')

@app.route('/search', methods=['GET'])
def search_route():
    query = request.args.get('query', '')
    books = search_books(query) if query else get_all_books()
    return render_template('index.html', books=books, members=get_all_members(), borrowed=get_all_borrowed_books())

# --- Member Routes ---
@app.route('/add_member', methods=['POST'])
def add_m():
    name, email = request.form.get('name'), request.form.get('email')
    if name and email: add_member(name, email)
    return redirect('/')

@app.route('/update_member', methods=['POST'])
def update_member_route():
    m_id, name, email = request.form.get('member_id'), request.form.get('name'), request.form.get('email')
    if m_id and name and email: update_member(m_id, name, email)
    return redirect('/')

@app.route('/deactivate_member', methods=['POST'])
def deactivate_member_route():
    if request.form.get('member_id'): deactivate_member(request.form.get('member_id'))
    return redirect('/')

@app.route('/delete_member', methods=['POST'])
def delete_member_route():
    m_id = request.form.get('member_id')
    if m_id: delete_member(m_id)
    return redirect('/')

@app.route('/search_members', methods=['GET'])
def search_members_route():
    query = request.args.get('query', '')
    members = search_members(query) if query else get_all_members()
    return render_template('index.html', books=get_all_books(), members=members, borrowed=get_all_borrowed_books())

# --- Borrowing Routes ---
@app.route('/add_borrowed', methods=['POST'])
def add_borrowed_route():
    b_id, m_id = request.form.get('book_id'), request.form.get('member_id')
    if b_id and m_id: add_borrowed(b_id, m_id)
    return redirect('/')

@app.route('/delete_borrowed', methods=['POST'])
def delete_borrowed_route():
    b_id = request.form.get('borrowed_id')
    if b_id: delete_borrowed(b_id)
    return redirect('/')

@app.route('/search_borrowed', methods=['GET'])
def search_borrowed_route():
    query = request.args.get('query', '')
    borrowed = search_borrowed(query) if query else get_all_borrowed_books()
    return render_template('index.html', books=get_all_books(), members=get_all_members(), borrowed=borrowed)

@app.route('/update_status', methods=['POST'])
def update_status_route():
    b_id, status = request.form.get('borrowed_id'), request.form.get('status')
    if b_id and status: update_borrowed_status(b_id, status)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)