from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_ejemplo'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


users = {
    '1': User('1', 'admin', 'admin123'),
    '2': User('2', 'usuario', 'password123')
}



@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)



@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = None
        for u in users.values():
            if u.username == username:
                user = u
                break

        if user and user.check_password(password):
            login_user(user)
            flash('¡Inicio de sesión exitoso!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')

    return render_template('login.html')



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('login'))



@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
