from django.core.cache import cache
from backendapp.models.likes import Likes
from backendapp.models.post import Post
from backendapp.models.users import Users
from backendapp.models.comments import Comments
from backendapp.models.connections import Connection

model_name_mapping = {
    "post": Post,
    "users": Users,
    "connection": Connection,
    "comments": Comments,
    "likes": Likes,
}

# Function to get objects, considering cached data
def get_model_object(object_id, model_name):
    if model_name not in model_name_mapping:
        print ("Something Went Wrong")
        return {}

    cache_key = f'{model_name}_{object_id}'
    cacheObject = cache.get(cache_key)
    if cacheObject is None:
        try:
            cacheObject = model_name_mapping[model_name].objects.get(id=object_id)
            cache.set(cache_key, cacheObject)
        except model_name_mapping[model_name].DoesNotExist:
            return None
    return cacheObject