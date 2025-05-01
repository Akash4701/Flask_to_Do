from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Routes

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get('query')
    if query:
        results = Todo.query.filter(Todo.title.ilike(f"%{query}%")).all()
        return render_template('index.html', allTodo=results, search_term=query)
    return redirect("/")

@app.route("/",methods=['GET','POST'])     
def hello_world(): 
    if request.method=='POST':
        print("post")
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
     if request.method=='POST':
        print("post")
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
     todo=Todo.query.filter_by(sno=sno).first()
     return render_template('update.html',todo=todo)
     
    
@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')    
    
@app.route("/products")

def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'This is the products page'

# Run the app
if __name__ == "__main__":
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()
    
    app.run(host="0.0.0.0",  debug=True)