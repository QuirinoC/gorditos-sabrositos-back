from db_schema import * 

def get_user_by_session(cookie_session):
    '''
        Return an user object 
    '''
    session = Session.objects.get(session_hash=cookie_session)
    user  = User.objects.get(id=session['userID'])
    return user

def get_restaurants(session, distance=3):
    '''
        Returns the closest restaurants to the user 
    '''
    user = get_user_by_session(session)
    location = get_user_location(user)
    lon, lat = location
    print(lon,lat)
    results = Restaurant.objects(location__geo_within_sphere=[[lon, lat], 3/6371.0])
    return results

def get_locations_by_user(userID):
    try:
        results = Location.objects.get(userID=userID)
    except:
        results = []
    return results

def get_user_location(user):
    location = user['current_location']['coordinates']
    return location

if __name__=='__main__':
    from connect_db import * 
    #print(get_user_by_session("20b7d99251fe04dd2ef62728a876da0f"))
    r = Restaurant.objects.get(pk="5b690b4373c32e764246268c")
    print(r['img_url'])