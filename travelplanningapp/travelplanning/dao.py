from travelplanning.models import User, Trip


def get_user_by_id(**kwargs):
    user = User.objects

    id = kwargs.get('id')
    if id:
        return user.get(pk=id)

    return user

def get_trip_by_tripplan(**kwargs):
    trip = Trip.objects

    q = kwargs.get('q')
    tripplan_id = kwargs.get('tripplan_id')

    return trip.filter(destination__icontains=q, tripplan_id=tripplan_id)