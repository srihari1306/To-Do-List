from flask import Flask, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task,User

def init_routes(app):
    
    #home route
    @app.route('/',methods=['GET','POST'])
    def index():
        
        if 'user_id' not in session:
            return redirect('/login')
        
        if request.method == 'POST': #adding new task
            task_content = request.form['content']
            new_task = Task(content=task_content, user_id=session['user_id'])
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        tasks = Task.query.filter_by(user_id=session['user_id']).order_by(Task.date_created).all() #displaying the task
        return render_template('index.html',tasks=tasks)
    
    
    #register route
    @app.route('/register',methods=['GET','POST'])
    def register():
        if request.method=='POST':
            username = request.form['username']
            password = request.form['password']
            
            if User.query.filter_by(username=username).first():
                flash("Username already exists")
                return redirect(url_for('login'))
            
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. Please log in.")
            return redirect(url_for('login'))
        return render_template('register.html')
    
    #login route
    @app.route('/login',methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                session['user_id'] = user.user_id
                session['usernmae'] = user.username
                return redirect('/')
            flash('Invalid Credentials!')
            return redirect('/login')
        
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/login')
    
    #delete route
    @app.route('/delete/<int:task_id>')
    def delete(task_id):
        task_to_del = Task.query.filter_by(task_id=task_id, user_id=session['user_id']).first_or_404()
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    
    #update route
    @app.route('/update/<int:task_id>',methods=['GET','POST'])
    def update(task_id):
        task_to_update = Task.query.filter_by(task_id=task_id, user_id=session['user_id']).first_or_404()
        if request.method == 'POST':
            task_to_update.content = request.form['content']
            db.session.commit()
            return redirect('/')
        return render_template('update.html',task=task_to_update)
    
    #toggle completion
    @app.route('/toggle/<int:task_id>',methods=['POST'])
    def toggle_complete(task_id):
        task = Task.query.filter_by(task_id=task_id, user_id=session['user_id']).first_or_404()
        task.completed = not task.completed
        db.session.commit()
        return redirect('/')