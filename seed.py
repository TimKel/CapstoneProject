from app import db
from models import db, User, Skatepark

db.drop_all()
db.create_all()

p1 = Skatepark(name="Jaycee" , description="The park features elongated stair sets, handrails, hubbas, bank to ledge, taco quarter pipe with pool coping, floating corner bowl, a variety of ledges, and a split a-frame kicker with a middle rail and hubbas on both sides." , address="2200-2276 E St Louis Ave, Las Vegas, NV 89104" , image_url="https://skatethestates.com/wp-content/uploads/2020/05/Jaycee-Skatepark-in-Las-Vegas.jpg" )
p2 = Skatepark(name="Craig Ranch" , description="Ledges and stair sets are in abundance here as are rails and hubbas too. If you can’t enjoy yourself at this skatepark you should probably stop skateboarding." , address="628 W. Craig Road, North Las Vegas, NV" , image_url="https://skatethestates.com/wp-content/uploads/2021/02/Craig-Ranch-Skatepark-in-Las-Vegas.jpg" )
p3 = Skatepark(name="Hollywood" , description="The park features an 11 foot kidney bowl, 18 foot full pipe, and street plaza with a 10 stair, boxes, ledges, and rails." , address="1650 S Hollywood Blvd, Las Vegas, NV 89142" , image_url="https://skatethestates.com/wp-content/uploads/2021/02/Hollywood-Skatepark-in-Las-Vegas-Nevada-edited.jpg" )
p4 = Skatepark(name="Hidden Falls" , description="The park features ledges, hubbas, rails, stair sets, flat banks, and a manual pad." , address="281 W Horizon Dr, Henderson, NV 89002" , image_url="https://skatethestates.com/wp-content/uploads/2020/05/Hidden-Falls-Skatepark-in-Las-Vegas.jpg" )
p5 = Skatepark(name="Winchester" , description="It features flat banks, rails, hubbas, ledges, and a stair set" , address="3130 McLeod Dr, Las Vegas, NV 89121" , image_url="https://skatethestates.com/wp-content/uploads/2020/05/Winchester-Skatepark-in-Las-Vegas.jpg" )
p6 = Skatepark(name="Metro" , description="The street section consists of a variety of stair sets, rails, hubbas, ledges, bank ramps, and a pyramid." , address="3509 N Sweden St, Las Vegas, NV 89129" , image_url="https://skatethestates.com/wp-content/uploads/2020/05/Police-Memorial-Skatepark-Las-Vegas.jpg" )
p7 = Skatepark(name="Sunny Springs" , description="It has some nice bowls, some big hubbas, a few nice ledges, and also a fun rail." , address="7620 Golden Talon Ave, Las Vegas, NV 89131" , image_url="https://skatethestates.com/wp-content/uploads/2020/05/Sunny-Springs-Skatepark-Las-Vegas.jpg" )
p8 = Skatepark(name="Cambridge" , description="Some of the ledges are super steep but there are more mellow ones at this park too." , address="3930 Cambridge St, Las Vegas, NV 89119" , image_url="https://skatethestates.com/wp-content/uploads/2020/05/Cambridge-Skatepark-Las-Vegas.jpg" )
p9 = Skatepark(name="Kenny Guinn" , description="Small but fun. This park has a couple banks and a few great rails. All you really need." , address="4150 S Torrey Pines Dr, Las Vegas, NV 89103" , image_url="https://i.ytimg.com/vi/tduNrRfdb0E/maxresdefault.jpg" )
p10 = Skatepark(name="Desert Breeze" , description="Half street, half transition. Some smaller and larger bowls as well as rails, ledges and banks to skate." , address="8425 Spring Mountain Rd, Las Vegas, NV 89147" , image_url="https://www.northwestskater.com/lvdb3357b101610.jpg" )
p11 = Skatepark(name="Duck Creek" , description="Designed for beginner to Intermediate to level With some Advanced aspects, concrete park with benches, shade structure, drinking fountains, no phones, lights on timer." , address="8650 Pollack Drive, Las Vegas, Nevada" , image_url="https://www.northwestskater.com/vegasduck4842a21812.jpg" )
p12 = Skatepark(name="Anthem" , description="Not as much street but an incredible array of bowls, spines and transition." , address="McCullough Hills Pkwy, Henderson, NV 89052" , image_url="https://tinyurl.com/3tbvs9vv" )
# p13 = Skatepark(name="" , description="" , address="" , image_url="" )
# p14 = Skatepark(name="" , description="" , address="" , image_url="" )
# p15 = Skatepark(name= , description="" , address="" , image_url="" )
# p16 = Skatepark(name= , description="" , address="" , image_url="" )
# p17 = Skatepark(name="" , description="" , address="" , image_url="" )
# p18 = Skatepark(name="" , description="" , address="" , image_url="" )
# p19 = Skatepark(name="" , description="" , address="" , image_url="" )
# p20 = Skatepark(name="" , description="" , address="" , image_url="" )

db.session.add_all([p1, p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12])
db.session.commit()
