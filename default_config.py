import os


DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Suxat098!@localhost/terraM'
SQLACHLEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
UPLOADED_DATA_DEST = os.path.join("static", "data")
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]