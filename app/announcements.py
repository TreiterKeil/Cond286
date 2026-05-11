from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.utils.decorators import admin_required
from app.models import Anuncio
from app import db

announcements_bp = Blueprint('announcements', __name__)


@announcements_bp.route('/announcements')
@login_required
def index():
    anuncios = Anuncio.query.order_by(Anuncio.criado_em.desc()).all()
    return render_template('announcements/index.html', anuncios=anuncios)


@announcements_bp.route('/announcements/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        conteudo = request.form.get('conteudo')

        errors = []
        if not titulo:
            errors.append('Introduza um título.')
        if not conteudo:
            errors.append('Introduza o conteúdo do comunicado.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('announcements/new.html')

        anuncio = Anuncio(
            titulo=titulo,
            conteudo=conteudo
        )
        db.session.add(anuncio)
        db.session.commit()

        flash('Comunicado publicado com sucesso!', 'success')
        return redirect(url_for('announcements.index'))

    return render_template('announcements/new.html')


@announcements_bp.route('/announcements/<int:id>')
@login_required
def detail(id):
    anuncio = Anuncio.query.get_or_404(id)
    return render_template('announcements/detail.html', anuncio=anuncio)


@announcements_bp.route('/announcements/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(id):
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()
    flash('Comunicado eliminado.', 'info')
    return redirect(url_for('announcements.index'))