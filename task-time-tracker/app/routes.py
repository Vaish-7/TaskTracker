from flask import Blueprint, jsonify, request, flash, render_template, redirect, url_for, session
from .models import Task, TaskStatus, User
from .db import db
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint("routes-bp", __name__)

@bp.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful, Please Login")
        return redirect(url_for("routes-bp.login"))
    return render_template("register.html")

@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(usernaname=username).first()
        if user and user.check_password(password):
            token = create_access_token(identity = user.id)
            session["jwt"] = token
            return redirect(url_for("routes-bp.dashboard"))
        flash("Invalid Credentials")
    return render_template("login.html")


@bp.route("/dashboard")
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user).all()
    return render_template("dashboard.html", tasks=tasks)

@bp.route("/profile")
@jwt_required()
def profile():
    current_user= get_jwt_identity()
    user = User.query.get_or_404(current_user)
    tasks = Task.query.filtet_by(user_id=current_user).all()

    stats = {
        "total": len(tasks),
        "Completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
        "started": sum(1 for t in tasks if t.status == TaskStatus.STARTED),
        "In-progress": sum(1 for t in tasks if t.status == TaskStatus.PROGRESS),  
    }

    return render_template("profile.html", user=user, tasks=tasks, stats=stats)

@bp.route("/create-task", methods=["POST"])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    name = request.form.get("name")
    notes = request.form.get("notes")
    if not name:
        flash("Task name is required", "danger")
        return redirect(url_for("routes-bp.dashboard"))
    
    task = Task(name=name, notes=notes, user_id=current_user)
    db.session.add(task)
    db.session.commit()
    flash("Task created successfully", "success")
    return redirect(url_for("routes-bp.dashboard"))

@bp.route("/tasks/<int:task_id>/start", methods=["PUT"])
def start_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.start_time = datetime.utcnow()
    task.status = TaskStatus.STARTED
    flash("Task started", "info")
    return redirect(url_for("routes-bp.dashboard"))

@bp.route("/tasks/<int:task_id>/stop", methods=["PUT"])
def stop_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.end_time = datetime.utcnow()
    if task.start_time:
        task.duration = int((task.end_time - task.start_time).total_seconds())
    task.status = TaskStatus.COMPLETED
    db.session.commit()
    flash("Task stopped", "warning")
    return redirect(url_for("routes-bp.dashboard"))

@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def stop_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted", "danger")
    return redirect(url_for("routes-bp.dashboard"))

@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")

    return redirect(url_for("routes-bp.login"))
