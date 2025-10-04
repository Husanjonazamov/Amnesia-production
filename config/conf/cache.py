from config.env import env

CACHES = {
    "default": {
        "BACKEND": env.str("CACHE_BACKEND"),
        "LOCATION": env.str("REDIS_URL"),
        "TIMEOUT": env.str("CACHE_TIMEOUT"),
    },
}

CACHE_MIDDLEWARE_SECONDS = env("CACHE_TIMEOUT")


CACHEOPS_REDIS = env.str("REDIS_URL")
CACHEOPS_DEFAULTS = {
    "timeout": env.str("CACHE_TIMEOUT"),
}

CACHEOPS = {
    "havasbook.BookModel": {
        "ops": ("fetch", "get", "count"),   
        "timeout": 60 * 5, 
    },

    "havasbook.BookimageModel": {
        "ops": ("fetch", "get"),
        "timeout": 60 * 10,  
    },

    "havasbook.BannerModel": {
        "ops": "all",
        "timeout": 60 * 10, 
    },

    "havasbook.CategoryModel": {
        "ops": ("fetch", "get"),
        "timeout": 60 * 60, 
    },
    "havasbook.SubCategoryModel": {
        "ops": ("fetch", "get"),
        "timeout": 60 * 60, 
    },
    "havasbook.ChildCategoryModel": {
        "ops": ("fetch", "get"),
        "timeout": 60 * 60, 
    },
}




CACHEOPS_DEGRADE_ON_FAILURE = True
CACHEOPS_ENABLED = env.bool("CACHE_ENABLED", False)
