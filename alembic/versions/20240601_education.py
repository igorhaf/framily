"""cria tabelas de educação

Revision ID: 20240601_education
Revises: 
Create Date: 2024-06-01

"""
from alembic import op
import sqlalchemy as sa

revision = '20240601_education'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'education_institutions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('tipo', sa.Enum('Faculdade', 'Escola', 'Curso Online', 'Workshop', 'Outro', name='tipoinstituicaoenum'), nullable=False, server_default='Outro'),
        sa.Column('descricao', sa.Text(), nullable=True),
    )
    op.create_table(
        'education_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('titulo', sa.String(length=120), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('data_hora', sa.DateTime(), nullable=False),
        sa.Column('tipo', sa.Enum('Aula', 'Prova', 'Palestra', 'Outro', name='tipoeventoenum'), nullable=False, server_default='Outro'),
        sa.Column('instituicao_id', sa.Integer(), sa.ForeignKey('education_institutions.id'), nullable=True),
    )
    op.create_table(
        'certifications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=120), nullable=False),
        sa.Column('instituicao_id', sa.Integer(), sa.ForeignKey('education_institutions.id'), nullable=True),
        sa.Column('data_obtencao', sa.Date(), nullable=False),
        sa.Column('arquivo', sa.String(length=255), nullable=True),
    )
    op.create_table(
        'learning_resources',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('titulo', sa.String(length=120), nullable=False),
        sa.Column('tipo', sa.String(length=60), nullable=False),
        sa.Column('status', sa.Enum('A Fazer', 'Em Andamento', 'Concluído', name='statusrecursoenum'), nullable=False, server_default='A Fazer'),
        sa.Column('observacoes', sa.Text(), nullable=True),
    )
    op.create_table(
        'learning_goals',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('descricao', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('Não Iniciada', 'Em Andamento', 'Concluída', name='statusmetaenum'), nullable=False, server_default='Não Iniciada'),
        sa.Column('progresso', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('prazo', sa.Date(), nullable=True),
    )
    op.create_table(
        'education_expenses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('descricao', sa.String(length=120), nullable=False),
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('categoria', sa.Enum('Mensalidade', 'Material', 'Livro', 'Outro', name='categoriadespesaenum'), nullable=False, server_default='Outro'),
        sa.Column('observacoes', sa.Text(), nullable=True),
    )

def downgrade():
    op.drop_table('education_expenses')
    op.drop_table('learning_goals')
    op.drop_table('learning_resources')
    op.drop_table('certifications')
    op.drop_table('education_events')
    op.drop_table('education_institutions')
    op.execute('DROP TYPE IF EXISTS tipoinstituicaoenum')
    op.execute('DROP TYPE IF EXISTS tipoeventoenum')
    op.execute('DROP TYPE IF EXISTS statusrecursoenum')
    op.execute('DROP TYPE IF EXISTS statusmetaenum')
    op.execute('DROP TYPE IF EXISTS categoriadespesaenum') 