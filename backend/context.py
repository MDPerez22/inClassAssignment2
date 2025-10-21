from models import User
from session import Session

class UserCtx:
	def __init__(self, user: User, session: Session):
		self.user = user
		self.session = session
		
class AdminCtx:
	def __init__(self, user: User, session: Session):
		self.user = user
		self.session = session