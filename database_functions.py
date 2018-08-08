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
    location = get_locations_by_user(user['id'])
    print(location)
    results = Restaurant.objects(location__geo_within_sphere=[[-103.391922, 20.673566], 3/6371.0])
    return results

def get_locations_by_user(userID):
    try:
        results = Location.objects.get(userID=userID)
    except:
        results = []
    return results


if __name__=='__main__':
    from connect_db import * 
    print(get_user_by_session("20b7d99251fe04dd2ef62728a876da0f"))