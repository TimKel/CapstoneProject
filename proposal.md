## Capstone 1 Project Proposal
---
#  **SpotIt**
The skateboarding community brings people together from all walks of life. This community creates some of the strongest friendships you can imagine, where indifferences in viewpoints on the world get pushed aside to enjoy time together. As these mini-communities move away from a park and explore urban landscapes, they search streets for a new spot to skate. It can be anything. A curb, ledge or handrail, or perfectly angeled slabs of concrete to air out off of. Whatever it may be, it takes hours of searching to find and can only be accessed via word of mouth if you know the right person. 

## Project Goals:
SpotIt enables the skateboard community to showcase skate spots they've found with their local community, as well as find spots quickly when they're in unfamiliar territory. 

Users who have signed up will be able to upload a picture of the spot, mark it's location/address so others can get to it, and leave comments if they'd prefer so others know what to expect.

## User Demographic:
SpotIt is able to be used by anyone in the skateboard community looking for fun spots to skate with their friends. 

## Data:
Priority data is address/longitude&latitude/directions 
### API Options: 
- [Googlemaps](https://developers.google.com/maps)- Concern is free vs having to pay
- [TomTom](https://developer.tomtom.com) - Free for 2,500 transactions per day or 75,000 per month
- [Mapbox](https://docs.mapbox.com/api/overview/) - In between TomTom and Googlemaps; Free for 500,00 daily, 250,000 monthly
- Other options like [OpenLayers](https://openlayers.org)- Completely free but user would need to copy+paste location in another app for directions

--- Minimal Private Info: Username/First and Last name/Email/Password ---

## DB Schema: Baseline
![Schema Rough Draft](https://app.quickdatabasediagrams.com/#/d/57rjFg)
1. User
    - User can have multiple locations. 
    - Each location can have 1 comment which can be edited.
2. Locations
    - Locations will have numerous users 
    - users can leave multiple comments on one location
3. Comments
    - Each comment will only have 1 user
    - A user can comment multiple times on one location

--- Each model will have m-2-m relationships with one another ---

### Possible Future Additions:
- Followers
- Ratings/Likes
- Tags to filter types of spots

## Potential Issues
1. **API related issues**- Likely not an issue but accrued API use could lead to overage charges. Also, if the API goes down the app will be down for the time being
2. Potentially having to ban someone or remove locations/comments that are inappropriate. 
3. Maintaining and respecting access to certain locations. Some skate spots may not be "legal entry". Meaning a kid is jumping a fence to get to a set of stairs at a school. 
4. Locations- Address or Long/Lat coordinates. I need to dive into the best way to manage this. What can be null or can't? Address is preferred but what if the user can't access an address?
5. The skate community can be a bit raw and my concern would be how to govern appropriate language. 

## Security and Sensitive Information
- Username will be stored in a database
- Passwords will be protected using Bcrypt
- City and State but no address
- No additional personal information will be used

## Functionality and UserFlow
Users will be able to do the following:
- Create a Username/userID. This is not mandatory but will be the user would like to add skate spot locations and comments
- Look up surrounding skatespots via their personal locations. Can also look up other locations via map scroll or address
- Add skatespots by uploading a picture, location and comments for other users to see
- Users can edit/delete personal info including locations and comments only they have added

### **Stretch Goals:**
- Allow users to follow other users
- Add star ratings or likes to showcase favorites
- Add tags to filter different types of skatespots or quality of spots via stars/likes

## **Challenge:**
**I need to consider how I will ensure the app automatically loads not only skatespots but also skateparks.**

