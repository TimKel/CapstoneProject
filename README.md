# **Spot It**: Skatepark Locator

SpotIt enables the skateboard community to showcase skateparks and skate-spots they enjoy with their local community, as well as find spots quickly when they're in unfamiliar areas.

Users who have signed up will be able to upload a picture of the spot and mark it's location/address so others can check it out.

## **Deployment**
You can view the deployed app at [Spot It](https://spot-it-project.herokuapp.com)

## **User Flow**

General user flow would entail a user simply searching areas they're interested in for skate spots as well as getting directions to said location. 

In addition, if a user creates a profile they will also have the ability to add spots to the database for others to see and access on top of standard non-member features mentioned above. 

### **Search**

The homepage provides a search bar. Currently the best version of search will include the city or state you're interested in. This will pull up any submitted skate parks/spots which showcases a visual of the area, a description, address and a location map with a "Get Directions" button.

### **Directions**

For directions to a location you will need to enter where you're coming from. This will take you to a singular page with the skatespot info and directions via Google Maps.

### **Sign Up** if you prefer

Creating a profile is not mandatory however, it does enable the user to upload their own skate parks/spots to continue to build the app and create a greater experience for all users. To create a profile, simply hit sign up and fill out the required fields. Then submit. 

### **Add Skateparks or Skatespots**

Once signed up, the navigation bar shows additional features including "Add Park or Spot". Submit an image address, location address and description to submit your own spots. All users will now have access to finding and skating the spot you've submitted. 

## **API Use**

Spot It utilizes Google Maps API's for functionality. Search pages will use the Google Map Static Map API, while directions will make use of Google Maps Directions API.

## **Tech Stack**:
- Python
- Flask 
- PostgreSQL
- Bootstrap
