from flask import Flask, render_template,request,redirect,url_for,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import geopandas as gpd
import os
import pandas
import io
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import geoplot
import random
import copy
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///yogesh.db'

db=SQLAlchemy(app)
a=os.getcwd()
class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<task %r>' %self.id

@app.route('/', methods=['POST','GET'])
def hello():
    if request.method=='POST':
        email =request.form['email']
        password=request.form['psw']
        new_task=Todo(email=email,password=password)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/home/')
        except:
            return 'Error While Imprting Data'
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error While Deleting Data'

@app.route('/home/')
def carousel():
    return render_template('carousel.html')
@app.route('/home/displayvector',methods=('POST','GET'))
def addvector():
    if request.method=='POST':
        f=request.form['file']
        return render_template('carousel.html',f=f)
@app.route('/home/displayvector/<name>/<file>',methods=('POST','GET'))
def displayvector(name,file):
    f=file
    b=r'E:\Gis_Data\GCS_WGS_19 - Copy\GCS_WGS_19 - Copy'
    df1=gpd.read_file(os.path.join(b,f))
    df=df1[df1.columns.difference(['geometry'])]
    os.chdir(os.path.join(a,'static','lmg'))
    if name=='map':
        ax=df1.plot()
        files_in_directory=os.listdir(os.getcwd())
        filtred_files=[file for file in files_in_directory if file.endswith(".png")]
        for file in filtred_files:
            path_to_file=os.path.join(os.getcwd(),file)
            os.remove(path_to_file)
        k=random.random()
        plt.savefig('Outputmap'+str(k)+'.png')
        path='lmg/Outputmap'+str(k)+'.png'
        projection=df1.crs
        return render_template('map.html',k=path,projection=projection,columns=df.columns)
    elif name=='attribute':
        return render_template('attribute.html',tables=[df.to_html(classes='data')],titles=df.columns.values)


if __name__=='__main__':
    app.run(debug=True)