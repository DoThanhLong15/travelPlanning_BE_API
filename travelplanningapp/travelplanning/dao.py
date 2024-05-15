from travelplanning.models import User, Trip


def get_user_by_id(**kwargs):
    user = User.objects

    id = kwargs.get('id')
    if id:
        return user.get(pk=id)

    return user

def get_trip(**kwargs):
    trip = Trip.objects

    q = kwargs.get('q')
    if q:
        trip = trip.filter(destination__icontains=q)

    return trip.all()