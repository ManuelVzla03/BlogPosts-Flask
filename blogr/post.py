from flask import Blueprint, request, flash, redirect, url_for, g, render_template
from .auth import login_required
from .models import Post
from blogr import db

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/posts')
@login_required
def posts ():
    posts = Post.query.all()
    return render_template('admin/posts.html', posts = posts)

@bp.route('/create', methods = ['POST', 'GET'])
@login_required
def create_post ():
    if request.method == 'POST':
        url = request.form.get('url')
        url = url.replace(' ', '-')
        title = request.form.get('title')
        info = request.form.get('info')
        content = request.form.get('ckeditor')

        post = Post(g.user.id, url, title, info, content)

        post_url = Post.query.filter_by(url = url).first()

        if post_url is None:
            db.session.add(post)
            db.session.commit()
            flash(f'El blog {post.title} se guaradó correctamente')
            return redirect(url_for('post.posts'))
        else:
            flash(f'El blog {post.title} ya está registrado')
    return render_template('admin/create.html')

@bp.route('/update/<int:id>', methods = ['POST', 'GET'])
@login_required
def update_post (id):
    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.info = request.form.get('info')
        post.content = request.form.get('ckeditor')

        db.session.commit()
        flash(f'El blog {post.title} se actualizó correctamente')
        return redirect(url_for('post.posts'))
    
    return render_template('admin/update.html', post = post)

@bp.route('/delete/<int:id>', methods = ['POST', 'GET'])
@login_required
def delete_post (id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash(f'El blog {post.title} se eliminó correctamente')
    return redirect(url_for('post.posts'))
