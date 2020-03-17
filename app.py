from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Dungeon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    def __repr__(self):
        return '<Dungeon %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_item = Dungeon(name=name)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return "Error adding new item"
    
    else:
        dungeons = Dungeon.query.order_by(Dungeon.created_at).all()
        return render_template('index.html', dungeons=dungeons)

    return render_template('index.html', title="Top Dungeon")

if __name__ == '__main__':
    app.run(debug=True)