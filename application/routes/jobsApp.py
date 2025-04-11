
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, get_flashed_messages

from application.helpers.gestor_restaurant import ManagerData
from application.controllers.restaurant.JobsController import JobsController
from ..controllers.restaurant.userController import UsersAdmin

managerData = ManagerData()
userController = UsersAdmin()
jobsController = JobsController()
jobs = Blueprint("jobs", __name__)
# ONLY USERS W
@jobs.route("/home")
def home():
    data_filter = {
        "keyword" : request.args.get("keyword", ""),
        "location" : request.args.get("location", ""),
        "job_type" : request.args.get("job_type", ""),
        "job_salary_time" : request.args.get("job_salary_time", ""),
    }
    
    list_jobs =  jobsController.get_filter(data=data_filter)
    for index, job in enumerate(list_jobs):
        id_admin = job["id_admin"]
        user_admin = userController.show_id(id_=id_admin)
        list_jobs[index]["admin_image"] = user_admin["user_image"]

    data_render = {
        "image_profile" : managerData.image_name_saved_cookie_or_session(),
        "level_user_context" : managerData.level_saved_cookie_or_session(),
        "list_jobs" : list_jobs,
        "data_filter" : data_filter,
    }
    return render_template("home/jobs/users/index.html", **data_render)

@jobs.route("/create_job", methods=["GET", "POST"])
def create_job():
    # ONLY ADMIN
    if request.method == "GET":
        list_jobs =  jobsController.get_all()
        
        data_render = {
            "image_profile" : managerData.image_name_saved_cookie_or_session(),
            "level_user_context" : managerData.level_saved_cookie_or_session(),
            "list_jobs" : list_jobs,
        }
        return render_template("home/jobs/admin/create_job.html", **data_render)
    
    elif request.method == "POST":
        data_update = {"id_admin":managerData.email_to_id_admin()}

        data_update["job_title"] = request.form.get("job_title")
        data_update["job_details"] = request.form.get("job_details")
        data_update["job_location"] = request.form.get("job_location")
        data_update["job_salary_time"] = request.form.get("job_salary_time")
        data_update["job_type"] = request.form.get("job_type")
        data_update["job_minimum_salary"] = request.form.get("job_minimum_salary")
        data_update["job_maximum_salary"] = request.form.get("job_maximum_salary")

        res = jobsController.create_job(data_update)
        
        return redirect(url_for("jobs.create_job"))