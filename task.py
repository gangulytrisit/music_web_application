from workers import celery
from jinja2 import Template
from weasyprint import HTML
from mail import send_email
import csv
from model import db, User as user_m, Song as song_m, Playlist as playlist_m, Album as album_m, Rating as rating_m, Role


#pdf format

def format_rep(template1,data,user="user"):
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(data=data,user=user)


def pdf_rep(data,user):
    msg = format_rep("./templates/month_rep.html",data=data,user=user)
    # print(msg)
    html = HTML(string=msg)
    # print(html)
    file_name = str(user)+"_created_song_report"+".pdf"
    print(file_name)
    html.write_pdf(target=file_name)   



## daily remainder

@celery.task()
def daily_rem():
    users = user_m.query.filter(user_m.roles.any(Role.name == 'user')).all()
    print (users)
    for user in users:   
        print(user.email)
        email = user.email
        # filtered_user = user_m.query.filter_by(email = user.email).first()
        username = user.username
        # print(email, user.username)
        with open('./templates/daily_rem.html','r') as f:
            template = Template(f.read())
        send_email(email,'Daily Reminder',template.render(user=username),content="html")
    return "Daily reminder sent"


#monthly report


from sqlalchemy import func

@celery.task()
def month_rep():
    creator = user_m.query.filter(user_m.roles.any(Role.name == 'creator')).all()
    data=[]
    for user in creator:
        username = user.username
        user_song_data = song_m.query.filter_by(user_id=user.id).all()
        # print(user_song_data)
        count = 0  
        track = []
        for songall in user_song_data:
            count+=1
            song_rating = db.session.query(func.avg(rating_m.rating)).filter_by(song_id=songall.id).scalar()
            track_dict = {  
                "id": count,
                "title": songall.title,
                "genre": songall.genre,
                "singer": songall.singer,
                "lyrics": songall.lyrics, 
                "rating": song_rating, 
            }
 
            track.append(track_dict)
        pdf_rep(track,username)

        with open('./templates/month_rep.html','r') as f:
            template = Template(f.read())
        send_email(user.email,'Monthly Pdf Report for creator',template.render(User=username,data=track),content="html",attachment="./"+str(username)+"_created_song_report.pdf")    
    data.append(track)
    return data,user.email  



#csv_report for admin exporting

@celery.task()
def csv_rep(data, email, user):
    with open('./static/csv_rep.csv', 'w', encoding='utf8', newline='') as f:
        file = csv.DictWriter(f,fieldnames=data[0].keys(),restval='')
        file.writeheader()
        file.writerows(data)
    with open('./templates/csv_rep.html','r') as f:
        template = Template(f.read())
    send_email(email,'App Summary',template.render(user=user,data=data),content="html",attachment="./static/csv_rep.csv")    
    return "Csv created." 