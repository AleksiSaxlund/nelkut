from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(db, username, password):
	sql = text("SELECT id, password FROM users WHERE username=:username")
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()

	if not user:
		return False

	if check_password_hash(user.password, password):
		session["user_id"] = user.id
		return True

	return False

def user_id():
	return session.get("user_id", 0)

def logout():
	del session["user_id"]

def register(db, username, password):
	hash_value = generate_password_hash(password)
	try:
		sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
		db.session.execute(sql, {"username":username, "password":hash_value})
		db.session.commit()
	except:
		return False

	return login(db, username, password)
